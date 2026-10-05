"""待办存储：JSON 持久化，增删改查。"""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Todo:
    id: int
    text: str
    done: bool = False
    due_date: str | None = None
    due_time: str | None = None

class TodoStore:
    def __init__(self, path="todos.json"):
        self.path = Path(path); self.todos = []; self._next_id = 1
        if self.path.exists(): self.load()
    def load(self):
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.todos = [Todo(**t) for t in data.get("todos", [])]
        self._next_id = data.get("next_id", 1)
    def save(self):
        self.path.write_text(json.dumps({"todos": [asdict(t) for t in self.todos], "next_id": self._next_id}, ensure_ascii=False, indent=2), encoding="utf-8")
    def add(self, text, due_date=None, due_time=None):
        t = Todo(id=self._next_id, text=text, due_date=due_date, due_time=due_time)
        self._next_id += 1; self.todos.append(t); self.save(); return t
    def mark_done(self, tid):
        for t in self.todos:
            if t.id == tid: t.done = True; self.save(); return True
        return False
    def remove(self, tid):
        before = len(self.todos)
        self.todos = [t for t in self.todos if t.id != tid]
        if len(self.todos) != before: self.save(); return True
        return False
    def edit(self, tid, new_text):
        for t in self.todos:
            if t.id == tid: t.text = new_text; self.save(); return True
        return False
    def list(self, include_done=True):
        return list(self.todos) if include_done else [t for t in self.todos if not t.done]
