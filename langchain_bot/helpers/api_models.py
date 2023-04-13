import uuid
from typing import Optional

import pydantic


class Interaction(pydantic.BaseModel):
    conversation_id: Optional[uuid.UUID]
    text: str