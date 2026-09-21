require('dotenv').config();
const { WebSocketServer } = require('ws');
const jwt = require('jsonwebtoken');
const { createClient } = require('redis');
const celery = require('celery-node');
const url = require('url');

const PORT = 8081;
const JWT_SECRET = process.env.JWT_SECRET_KEY || 'your_secret_key'; // Убедись, что переменная совпадает с бекендом

// Инициализация Celery клиента (RabbitMQ)
// Инициализация Celery клиента (RabbitMQ)
const celeryClient = celery.createClient(
    process.env.CELERY_BROKER_URL || 'amqp://guest:guest@rabbitmq:5672//',
    process.env.CELERY_BROKER_URL || 'amqp://guest:guest@rabbitmq:5672//' 
);

const wss = new WebSocketServer({ port: PORT });

// Redis клиенты (один для подписки, другой для публикации)
const pubClient = createClient({ url: process.env.REDIS_URL || 'redis://redis:6379' });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
    console.log('Connected to Redis');
});

// Храним подключения: board_id -> Set(ws)
const boards = new Map();

wss.on('connection', async (ws, req) => {
    const parameters = url.parse(req.url, true).query;
    const token = parameters.token;
    const boardId = parameters.board_id;

    if (!token || !boardId) {
        ws.close(4000, 'Token and board_id are required');
        return;
    }

    try {
        // Валидация JWT токена
        const decoded = jwt.verify(token, JWT_SECRET);
        ws.userId = decoded.sub;
        ws.boardId = boardId;

        // Добавляем клиента в комнату доски
        if (!boards.has(boardId)) {
            boards.set(boardId, new Set());
            // Подписываемся на канал Redis для этой доски
            await subClient.subscribe(`board:${boardId}`, (message) => {
                // Рассылаем всем клиентам на этой доске (кроме отправителя, если нужно)
                const parsedMessage = JSON.parse(message);
                boards.get(boardId).forEach(client => {
                    if (client !== ws && client.readyState === ws.OPEN) {
                        client.send(message);
                    }
                });
            });
        }
        boards.get(boardId).add(ws);

        ws.on('message', (data) => {
            try {
                const msg = JSON.parse(data);

                // 1. Событие перемещения (микрособытие) - только через Redis Pub/Sub
                if (msg.type === 'ELEMENT_MOVE') {
                    pubClient.publish(`board:${boardId}`, JSON.stringify({
                        type: 'ELEMENT_MOVED',
                        userId: ws.userId,
                        elementId: msg.payload.element_id,
                        x: msg.payload.x,
                        y: msg.payload.y,
                        rotation: msg.payload.rotation
                    }));
                } 
                // 2. Событие отпускания (фиксация) - отправляем в брокер для БД
                else if (msg.type === 'ELEMENT_DROP') {
                    // Создаем задачу для Celery
                    const task = celeryClient.createTask('src.elements.tasks.update_element');
                    task.delay(
                        msg.payload.element_id, 
                        ws.boardId,
                        ws.userId,
                        {
                            x: msg.payload.x,
                            y: msg.payload.y,
                            width: msg.payload.width,
                            height: msg.payload.height,
                            rotation: msg.payload.rotation
                        }
                    );
                    
                    // Опционально: оповестить других, что элемент зафиксирован
                    pubClient.publish(`board:${boardId}`, JSON.stringify({
                        type: 'ELEMENT_SAVED',
                        elementId: msg.payload.element_id
                    }));
                }
            } catch (err) {
                console.error('Message processing error:', err);
            }
        });

        ws.on('close', () => {
            const boardClients = boards.get(boardId);
            if (boardClients) {
                boardClients.delete(ws);
                if (boardClients.size === 0) {
                    boards.delete(boardId);
                    subClient.unsubscribe(`board:${boardId}`);
                }
            }
        });

    } catch (err) {
        ws.close(4001, 'Invalid token');
    }
});

console.log(`WebSocket server started on port ${PORT}`);