from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import hashlib
import json
from typing import Any, Optional


def _normalize_for_signature(value: Any) -> Any:
    """แปลงข้อมูลให้เป็นรูปแบบที่ serialize ได้คงที่สำหรับการสร้างลายเซ็น"""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_for_signature(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return [_normalize_for_signature(item) for item in value]
    return value

class AkashicEnvelope(BaseModel):
    """
    DNA ของระบบ: บันทึกข้อมูลแบบ Immutable (แก้ไขไม่ได้)
    สอดคล้องกับหลักการ 'ความทรงจำบริสุทธิ์' (Frozen=True)
    """
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    intent: str  # เจตนา (Inspira)
    actor: str   # ผู้กระทำ (Agent Name)
    action_type: str # เช่น 'economic_transaction', 'code_generation'
    payload: Any     # ข้อมูลดิบ
    previous_hash: Optional[str] = None # เชื่อมโยงเหมือน Blockchain
    signature: str = "" # ลายเซ็นดิจิทัล (Hash)

    class Config:
        frozen = True # ทำให้ Object นี้แก้ไขไม่ได้หลังจากสร้าง (Immutability)

    @field_validator('signature', mode='before')
    @classmethod
    def generate_signature(cls, v, info):
        # คำนวณ Hash จากข้อมูลทั้งหมดเพื่อยืนยันความถูกต้อง (Integrity Check)
        if v: return v # ถ้ามีลายเซ็นแล้วให้ผ่าน
        
        # ดึงข้อมูลดิบมา Hash
        data = info.data
        signature_payload = {
            "id": data.get("id"),
            "timestamp": _normalize_for_signature(data.get("timestamp")),
            "intent": data.get("intent"),
            "actor": data.get("actor"),
            "action_type": data.get("action_type"),
            "payload": _normalize_for_signature(data.get("payload")),
            "previous_hash": data.get("previous_hash"),
        }
        canonical_json = json.dumps(signature_payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode()).hexdigest()

class AkashicLedger:
    """
    สมุดบัญชีแยกประเภทที่บันทึกทุกการกระทำของ AG (Database Layer)
    """
    def __init__(self):
        self._chain = []

    def record(self, envelope: AkashicEnvelope):
        # ตรวจสอบความถูกต้องก่อนบันทึก
        if len(self._chain) > 0:
            last_record = self._chain[-1]
            expected_previous_hash = last_record.signature

            if envelope.previous_hash != expected_previous_hash:
                raise ValueError(
                    "Invalid previous_hash: expected hash of the latest record"
                )

        elif envelope.previous_hash is not None:
            raise ValueError(
                "Invalid previous_hash: genesis record must not reference a previous hash"
            )
        
        self._chain.append(envelope)
        print(f"📜 [AKASHIC]: Recorded Action '{envelope.action_type}' by {envelope.actor} | Hash: {envelope.signature[:8]}...")
  
