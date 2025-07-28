# from fastapi import FastAPI, HTTPException, Path
# from pydantic import BaseModel, Field, HttpUrl
# from typing import Optional, List
# from uuid import uuid4, UUID
# from enum import Enum
# from datetime import datetime

# from sqlalchemy import create_engine, Column, String, DateTime, Integer, Enum as SqlEnum
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Initialize FastAPI app
# app = FastAPI(title="Cloud Telephony Dashboard API")

# # SQLite DB setup
# DATABASE_URL = "sqlite:///./calls.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

# # Enums for status and direction
# class CallStatus(str, Enum):
#     ringing = "ringing"
#     in_progress = "in_progress"
#     completed = "completed"
#     failed = "failed"
#     missed = "missed"
#     queued = "queued"

# class CallDirection(str, Enum):
#     inbound = "inbound"
#     outbound = "outbound"

# # SQLAlchemy model
# class Call(Base):
#     __tablename__ = "calls"

#     call_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
#     from_number = Column(String, nullable=False)
#     to_number = Column(String, nullable=False)
#     start_time = Column(DateTime, nullable=False)
#     duration = Column(Integer, nullable=True)
#     status = Column(SqlEnum(CallStatus), nullable=False)
#     direction = Column(SqlEnum(CallDirection), nullable=False)
#     recording_url = Column(String, nullable=True)
#     notes = Column(String, nullable=True)

# # Create DB tables
# Base.metadata.create_all(bind=engine)

# # Pydantic schema
# class CallSchema(BaseModel):
#     call_id: UUID
#     from_number: str
#     to_number: str
#     start_time: datetime
#     duration: Optional[int]
#     status: CallStatus
#     direction: CallDirection
#     recording_url: Optional[HttpUrl]
#     notes: Optional[str]

#     class Config:
#         orm_mode = True

# class CallCreateSchema(BaseModel):
#     from_number: str
#     to_number: str
#     status: CallStatus
#     direction: CallDirection
#     recording_url: Optional[HttpUrl]
#     notes: Optional[str]

# class CallUpdateSchema(BaseModel):
#     from_number: Optional[str]
#     to_number: Optional[str]
#     duration: Optional[int]
#     status: Optional[CallStatus]
#     direction: Optional[CallDirection]
#     recording_url: Optional[HttpUrl]
#     notes: Optional[str]

# class AudioPlayRequest(BaseModel):
#     audio_url: HttpUrl

# class CallTransferRequest(BaseModel):
#     target_number: str

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Route: Get all calls
# @app.get("/calls", response_model=List[CallSchema])
# def get_all_calls():
#     db = SessionLocal()
#     calls = db.query(Call).all()
#     return calls

# @app.post("/calls", response_model=CallSchema)
# def initiate_call(call: CallCreateSchema):
#     db = SessionLocal()
#     new_call = Call(
#         call_id=str(uuid4()),
#         from_number=call.from_number,
#         to_number=call.to_number,
#         start_time=datetime.utcnow(),
#         status=call.status,
#         direction=call.direction,
#         recording_url=call.recording_url,
#         notes=call.notes,
#     )
#     db.add(new_call)
#     db.commit()
#     db.refresh(new_call)
#     return new_call

# @app.get("/calls/{call_id}", response_model=CallSchema)
# def get_call_by_id(call_id: UUID):
#     db = SessionLocal()
#     call = db.query(Call).filter(Call.call_id == str(call_id)).first()
#     if not call:
#         raise HTTPException(status_code=404, detail="Call not found")
#     return call

# @app.patch("/calls/{call_id}", response_model=CallSchema)
# def update_call(call_id: UUID, updates: CallUpdateSchema):
#     db = SessionLocal()
#     call = db.query(Call).filter(Call.call_id == str(call_id)).first()
#     if not call:
#         raise HTTPException(status_code=404, detail="Call not found")
    
#     update_data = updates.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(call, key, value)

#     db.commit()
#     db.refresh(call)
#     return call

# @app.post("/actions/call/{call_id}/play_audio")
# def play_audio(call_id: UUID, payload: AudioPlayRequest):
#     db = SessionLocal()
#     call = db.query(Call).filter(Call.call_id == str(call_id)).first()
#     if not call:
#         raise HTTPException(status_code=404, detail="Call not found")
#     # Simulate audio playback (in a real system, you’d stream or log this)
#     return {"message": f"Simulated playing audio from {payload.audio_url} for call {call_id}"}

# # Simulate call transfer
# @app.post("/actions/call/{call_id}/transfer", response_model=CallSchema)
# def transfer_call(call_id: UUID, payload: CallTransferRequest):
#     db = SessionLocal()
#     call = db.query(Call).filter(Call.call_id == str(call_id)).first()
#     if not call:
#         raise HTTPException(status_code=404, detail="Call not found")
#     call.to_number = payload.target_number
#     call.status = CallStatus.queued  # or "transferred" if you add that status
#     db.commit()
#     db.refresh(call)
#     return call

# # Simulate hangup
# @app.post("/actions/call/{call_id}/hangup", response_model=CallSchema)
# def hangup_call(call_id: UUID):
#     db = SessionLocal()
#     call = db.query(Call).filter(Call.call_id == str(call_id)).first()
#     if not call:
#         raise HTTPException(status_code=404, detail="Call not found")
#     call.status = CallStatus.completed
#     call.duration = int((datetime.utcnow() - call.start_time).total_seconds())
#     db.commit()
#     db.refresh(call)
#     return call


from fastapi import FastAPI
from database import engine, Base
from routers import call_routes
from fastapi.middleware.cors import CORSMiddleware
# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Cloud Telephony API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with ["http://localhost:5173"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all call-related routes
app.include_router(call_routes.router)
