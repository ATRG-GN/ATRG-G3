import asyncio
import uuid
import time
from collections import defaultdict
from typing import Callable, Dict, Any, Optional, List
from .envelope import Envelope
from .signature import OriginMetadata, AISource

class AetherConductor:
    """
    AetherBus: The Central Nervous System (Async & Thread-Safe Concept)
    Acts as Message Broker and Job Registry.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AetherConductor, cls).__new__(cls)
            cls._instance.channels = defaultdict(list)
            cls._instance.trust_scores = {
                AISource.HUMAN_ARCHITECT: 100,
                AISource.GEMINI_CORE: 95,
                AISource.UNKNOWN_ECHO: 10
            }
            # --- Job Registry ---
            cls._instance._job_registry = {}
            cls._instance._lock = None
            cls._instance._background_tasks = set()

        return cls._instance

    async def subscribe(self, topic: str, handler: Callable):
        self.channels[topic].append(handler)
        print(f"👀 AetherBus: Agent subscribed to topic -> {topic}")

    async def publish(self, topic: str, envelope: Envelope):
        # 1. Signature Check (Listen)
        content_sample = str(envelope.payload)
        sig = OriginMetadata.analyze_code_style(content_sample)
        trust = self.trust_scores.get(sig.source, 0)

        print(f"[Conductor] 🎻 Wave on '{topic}' | Origin: {sig.source.value} | Trust: {trust}")

        # 2. Structural Adjustment (Guide)
        if trust < 50:
            print("   -> 🛡️ Low Trust: Quarantine Mode Activated")
            envelope.payload["_quarantine"] = True

        # 3. Dispatch (Async)
        if topic in self.channels:
            # Fire-and-forget dispatch:
            # keep references to prevent tasks from being garbage-collected
            # before completion, then log handler errors asynchronously.
            for handler in self.channels[topic]:
                task = asyncio.create_task(handler(envelope))
                self._background_tasks.add(task)

                def _on_done(completed_task: asyncio.Task):
                    self._background_tasks.discard(completed_task)
                    if completed_task.cancelled():
                        return
                    exc = completed_task.exception()
                    if exc:
                        print(f"[Conductor] ❌ Handler error on '{topic}': {exc}")

                task.add_done_callback(_on_done)

    # --- Job Registry Methods (The Governance Layer) ---

    async def _get_lock(self) -> asyncio.Lock:
        """Lazily initialize lock when running inside an async context."""
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    async def register_job(self, intent_data: Dict[str, Any], initial_status: str = "INTENT_GENERATED") -> str:
        """
        Registers a new Intent as a Job.
        """
        job_id = intent_data.get('id', str(uuid.uuid4()))
        lock = await self._get_lock()

        async with lock:
            if job_id not in self._job_registry:
                self._job_registry[job_id] = {
                    "intent": intent_data,
                    "status": initial_status,
                    "history": [{
                        "timestamp": time.time(),
                        "status": initial_status,
                        "note": "Job registered"
                    }]
                }
        return job_id

    async def update_job_status(self, job_id: str, new_status: str, note: str = "") -> bool:
        """ Updates the status of a tracked Job. """
        lock = await self._get_lock()
        async with lock:
            if job_id in self._job_registry:
                self._job_registry[job_id]["status"] = new_status
                self._job_registry[job_id]["history"].append({
                    "timestamp": time.time(),
                    "status": new_status,
                    "note": note
                })
                print(f"🔄 AetherBus: Job ID {job_id[:8]}... Status updated to: {new_status}")
                return True
            return False

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """ Retrieves job details. """
        lock = await self._get_lock()
        async with lock:
            # Return a copy to prevent mutation outside lock
            data = self._job_registry.get(job_id)
            if data:
                return data.copy()
            return None

conductor = AetherConductor()
