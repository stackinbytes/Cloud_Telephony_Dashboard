from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


# Enums
class CallStatus(str, Enum):
    ringing = "ringing"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    missed = "missed"
    queued = "queued"


class CallDirection(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


# Main response model
class CallSchema(BaseModel):
    call_id: UUID
    from_number: str
    to_number: str
    start_time: datetime
    duration: Optional[int]
    status: CallStatus
    direction: CallDirection
    recording_url: Optional[HttpUrl]
    notes: Optional[str]

    class Config:
        orm_mode = True


# Model for creating a call
class CallCreateSchema(BaseModel):
    from_number: str
    to_number: str
    status: CallStatus
    direction: CallDirection
    recording_url: Optional[HttpUrl]
    notes: Optional[str]


# Model for patch updates
class CallUpdateSchema(BaseModel):
    from_number: Optional[str]
    to_number: Optional[str]
    duration: Optional[int]
    status: Optional[CallStatus]
    direction: Optional[CallDirection]
    recording_url: Optional[HttpUrl]
    notes: Optional[str]


# Call Actions
class AudioPlayRequest(BaseModel):
    audio_url: HttpUrl


class CallTransferRequest(BaseModel):
    target_number: str
