# ไฟล์: AG API/GENESIS API/server.py (อัปเดต)
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
# --- NEW: Import ChelvasCore and its components ---
# (สมมติว่า ChelvasCore ถูกนำมาวางในโครงสร้างโปรเจกต์แล้ว)
from chevas_core import ChelvasCore, SystemStatus, protocol_safety_net, protocol_reinforcement

app = FastAPI()
manager = object() # ConnectionManager for WebSocket (ใช้จากโค้ดเดิม)

# --- Initialize Chelvas Core ---
core = ChelvasCore()
core.transformer.register_rule("anger", "seek_safety")
core.transformer.register_rule("joy", "confirm_path")
core.map_detection_logic("anger", ["hate", "mad", "error", "fail"])
core.map_cone_handler("seek_safety", protocol_safety_net)

@app.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    print(f"Chat Client {client_id} connected.")
    
    # ส่งข้อความต้อนรับ
    await websocket.send_json({"sender": "AI", "message": "Aetherium Genesis: Online. How may I process your intent?", "status": core.status.name})
    
    try:
        while True:
            # 1. รับข้อความจากผู้ใช้ (Input Text)
            data = await websocket.receive_text()
            user_input = json.loads(data).get("message", "")
            
            # 2. Process Intent ผ่าน Chelvas Core
            # เราใช้ AsyncTask เพื่อให้ Core ทำงานได้โดยไม่ Block Web Socket
            
            # (Note: ในการใช้งานจริง ควรส่ง IntentRequest ไปที่ ChelvasCore)
            
            # Mock Processing (จำลองการทำงานของ ChelvasCore)
            raw_vec = core._rod_detection(user_input)
            inspira_vec = core.transformer.apply_lorentz_boost(raw_vec)
            outcome = core._cone_execution(inspira_vec)
            
            # 3. ส่งคำตอบกลับ (Response)
            response_message = f"[{inspira_vec.derived_intent.upper()}]: {outcome}"
            
            await websocket.send_json({
                "sender": "AI",
                "message": response_message,
                "emotion_detected": raw_vec.detected_emotion.upper(),
                "intent": inspira_vec.derived_intent.upper()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
        manager.disconnect(websocket)
