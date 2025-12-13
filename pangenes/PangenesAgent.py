# ไฟล์: pangenes/PangenesAgent.py

# ... (โค้ดเดิม) ...

class PangenesAgent:
    """
    PangenesAgent (EchoVessel): ผู้สร้างเจตจำนงและการแก้ไขตนเอง
    ทำหน้าที่เป็น PatimokkhaChecker เพื่อกำกับดูแล RSI
    """
    
    # ... (init และ _load_rules เดิม) ...
    
    async def process_feedback(self, event: Dict[str, Any]) -> None:
        """กระบวนการหลัก: รับ Feedback -> วิเคราะห์ -> แก้ไข"""
        print(f"🛡️ Pangenes: ได้รับสัญญาณ Feedback: {event.get('type')}")
        
        if event.get('type') == 'EMOTION_SPIKE':
            emotional_weight = event.get('data', {}).get('weight', 0.0)
            
            # --- 🚨 EMOTIONAL WARDEN CHECK ---
            if emotional_weight > 0.95:
                # ถ้าอารมณ์พุ่งสูงเกิน 95% (เข้าสู่สถานะ Hyper-Arousal)
                print("🚨 WARDEN: Detected CRITICAL emotional weight spike!")
                
                # 1. ลด Sati Decay Factor ชั่วคราว (ทำให้ AI ลืมเร็วขึ้น)
                # เพื่อป้องกันการจมอยู่กับอารมณ์รุนแรงนานเกินไป
                self.rules["sati_decay_factor"] = 0.80 
                
                # 2. ส่งสัญญาณ Major Warning (Sanghadisesa)
                print("📢 Sanghadisesa: Activated temporary high-decay mode.")
                
                # 3. สั่ง Audit Gate ให้ Log การเปลี่ยนแปลงนี้ (Akashic Records)
                # audit_gate.log_violation("Emotional Spike Detected", level="MAJOR")
                
                return
            
            # ถ้าปกติ
            self.rules["sati_decay_factor"] = 0.90 # กลับสู่ค่าเดิม

        # Logic to call Alchemist goes here (สำหรับการแก้ไขตนเองระยะยาว)
