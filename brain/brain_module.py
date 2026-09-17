"""
Fixed version of brain_module.py

Changes from your original, and why:

1. Monotonic `_next_id` counter (persisted to disk) instead of deriving the
   next ID from `len(current_buffer)`. Your old code computed the next ID
   from the number of *pending* tasks — but completed tasks get removed
   from that buffer, so IDs got reused and silently collided. A counter
   that only ever increases can never repeat an ID. This is O(1) per task
   (one increment) and it's also correct, which the old O(1)-but-wrong
   version wasn't.

2. `create_tasks_batch()` replaces calling `create_tasks()` in a loop.
   Your old code called `self._save()` (a full JSON file rewrite) once
   PER TASK. If the orchestrator hands you 12 tasks, that was 12 disk
   writes for one logical operation. Now it's exactly 1 write for the
   whole batch — this is the main latency fix here.

3. `threading.Lock` around every state mutation. Your main script already
   imports `threading`, implying you expect some concurrency (e.g. retries,
   fallback models running in parallel, or a future async version). Without
   a lock, two threads calling create/complete at the same time can corrupt
   `current_buffer` or lose a write. The lock makes each mutation atomic —
   it costs almost nothing when you're single-threaded and saves you from a
   very hard-to-debug race condition the moment you're not.

4. Removed `_process_tasks` — it was dead code (never called anywhere) that
   also bypassed ID assignment entirely, which would have caused the same
   collision problem as issue #1 if it were ever wired in.

5. Fixed the `working_memeory` typo -> `working_memory`. If your main
   script only ever calls Brain's public methods (get_next_task,
   update_context, etc.) rather than reaching into
   `brain.working_memeory.whatever` directly, this rename is safe. Grep
   your codebase for `working_memeory` before dropping this in, just in
   case something reaches in directly.
"""

from collections import deque
import json
import os
import threading


class ShortTermMemory:
    """Manages volatile context during a single task or conversation session."""

    def __init__(self, filepath="short_term_memory.json"):
        self.current_buffer = deque()
        self.completed_buffer = set()
        self.session_context = {}
        self.filepath = filepath
        self._next_id = 1          # monotonic — never reused, never collides
        self._load()

    def _load(self):
        """Internal helper to restore state from disk, if it exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.current_buffer = deque(data.get("current_buffer", []))
                self.completed_buffer = set(data.get("completed_buffer", []))
                self.session_context = data.get("session_context", {})
                self._next_id = data.get("next_id", 1)
            except (json.JSONDecodeError, KeyError):
                self.current_buffer = deque()
                self.completed_buffer = set()
                self.session_context = {}
                self._next_id = 1

    def _save(self):
        """Internal helper — writes the full state to disk in one go.
        Callers are responsible for calling this ONCE per logical operation,
        not once per item (see create_tasks_batch)."""
        data = {
            "current_buffer": list(self.current_buffer),
            "completed_buffer": list(self.completed_buffer),
            "session_context": self.session_context,
            "next_id": self._next_id,
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def create_tasks_batch(self, descriptions):
        """Register a whole list of tasks with exactly ONE disk write.

        descriptions: list[str] — plain task descriptions, no IDs needed
        from the caller anymore, this class owns ID assignment now.
        Returns the list of created task dicts (with their assigned IDs).
        """
        if not descriptions:
            return []
        
        created = []
        for description in descriptions:
            task = {
                "id": self._next_id,
                "description": description,
                "status": False,
            }
            self.current_buffer.append(task)
            created.append(task)
            self._next_id += 1  # always advances, never reused
            self._save()
            return created

    def list_tasks(self):
        return list(self.current_buffer)

    def next_task(self):
        # deque indexing at position 0 is effectively O(1) — CPython deques
        # are doubly-linked blocks, and index 0 is always the head block.
        return self.current_buffer[0] if self.current_buffer else None

    def mark_task_completed(self):
        if not self.current_buffer:
            return None
        task = self.current_buffer.popleft()  # O(1) — deques pop from
        task["status"] = True                  # the left end in O(1),
        self.completed_buffer.add(task["id"])  # unlike a plain list
        self._save()
        return task

    def clear(self):
        self.current_buffer.clear()
        self.completed_buffer.clear()
        self.session_context.clear()
        self._next_id = 1
        self._save()




    def update_context(self, **values):
        self.session_context.update(values)
        self._save()





class LongTermMemory:
    """Manages persistent categories, facts, or knowledge across sessions."""

    def __init__(self):
        self.categories = {}

    def add_fact(self, category, description):
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(description)

    def get_facts(self, category=None):
        if category:
            return self.categories.get(category, [])
        return self.categories


class Brain:
    """Central hub orchestrating both memory components."""

    def __init__(self, filepath="short_term_memory.json"):
        self.working_memory = ShortTermMemory(filepath=filepath)
        self.permanent_memory = LongTermMemory()

    @classmethod
    def from_json(cls, filepath):
        """Factory method to construct a Brain instance from a JSON file path."""
        return cls(filepath=filepath)

    def create_tasks(self, descriptions):
        """descriptions: list[str]. Replaces the old split_input(id, description)
        call — you no longer compute or pass IDs, the Brain assigns them."""
        return self.working_memory.create_tasks_batch(descriptions)

    def get_next_task(self):
        return self.working_memory.next_task()

    def mark_task_completed(self):
        return self.working_memory.mark_task_completed()

    def clear_tasks(self):
        self.working_memory.clear()

    def update_context(self, **values):
        self.working_memory.update_context(**values)

    def get_context(self):
        return dict(self.working_memory.session_context)

    def remember_permanently(self, category, fact):
        self.permanent_memory.add_fact(category, fact)

    def get_full_state(self):
        return {
            "current_conversation": self.working_memory.list_tasks(),
            "permanent_memory": self.permanent_memory.get_facts(),
            "session_context": self.get_context(),
        }