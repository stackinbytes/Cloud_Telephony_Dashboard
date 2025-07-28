from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from database import SessionLocal
from models.call import Call, CallStatus
from schemas.call import (
    CallSchema,
    CallCreateSchema,
    CallUpdateSchema,
    AudioPlayRequest,
    CallTransferRequest,
)

router = APIRouter()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all calls
@router.get("/calls", response_model=list[CallSchema])
def get_all_calls(db: Session = Depends(get_db)):
    return db.query(Call).all()


# Get a specific call by ID
@router.get("/calls/{call_id}", response_model=CallSchema)
def get_call(call_id: UUID, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == str(call_id)).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


# Initiate a new call
@router.post("/calls", response_model=CallSchema)
def initiate_call(payload: CallCreateSchema, db: Session = Depends(get_db)):
    new_call = Call(
        from_number=payload.from_number,
        to_number=payload.to_number,
        start_time=datetime.utcnow(),
        status=payload.status,
        direction=payload.direction,
        recording_url=payload.recording_url,
        notes=payload.notes,
    )
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    return new_call


# Update call (PATCH)
@router.patch("/calls/{call_id}", response_model=CallSchema)
def update_call(call_id: UUID, payload: CallUpdateSchema, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == str(call_id)).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(call, field, value)

    db.commit()
    db.refresh(call)
    return call


# Simulate playing audio
@router.post("/actions/call/{call_id}/play_audio")
def play_audio(call_id: UUID, payload: AudioPlayRequest, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == str(call_id)).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return {"message": f"Simulated playing audio from {payload.audio_url} for call {call_id}"}


# Transfer call
@router.post("/actions/call/{call_id}/transfer", response_model=CallSchema)
def transfer_call(call_id: UUID, payload: CallTransferRequest, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == str(call_id)).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    call.to_number = payload.target_number
    call.status = CallStatus.queued
    db.commit()
    db.refresh(call)
    return call


# Hang up call
@router.post("/actions/call/{call_id}/hangup", response_model=CallSchema)
def hangup_call(call_id: UUID, db: Session = Depends(get_db)):
    call = db.query(Call).filter(Call.call_id == str(call_id)).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    call.status = CallStatus.completed
    call.duration = int((datetime.utcnow() - call.start_time).total_seconds())
    db.commit()
    db.refresh(call)
    return call
