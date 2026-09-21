from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime

class BoardOutputSchema(BaseModel):
    model_config=ConfigDict(
        from_attributes=True
    )
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_public: bool
