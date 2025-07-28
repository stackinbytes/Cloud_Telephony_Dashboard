from sqlalchemy import Column, String, Integer, DateTime, Enum
from uuid import uuid4
from datetime import datetime
from enum import Enum as PyEnum

from database import Base

# Enum definitions
class CallStatus(str, PyEnum):
    ringing = "ringing"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    missed = "missed"
    queued = "queued"

class CallDirection(str, PyEnum):
    inbound = "inbound"
    outbound = "outbound"

# Call model
class Call(Base):
    __tablename__ = "calls"

    call_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    from_number = Column(String, nullable=False)
    to_number = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer, nullable=True)
    status = Column(Enum(CallStatus), nullable=False)
    direction = Column(Enum(CallDirection), nullable=False)
    recording_url = Column(String, nullable=True)
    notes = Column(String, nullable=True)
