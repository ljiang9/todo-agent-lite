"""命令行：python -m todo_agent_lite "明天下午三点开会" 或交互式。"""
from __future__ import annotations
import argparse
from .parser import parse_intent
from .store import TodoStore


def _format(t):
    flag = "✓" if t.done else " "
    due = ""
    if t.due_date:
        due = f"  📅{t.due_date}"
        if t.due_time: due += f" {t.due_time}"
    return f"  [{flag}] #{t.id} {t.text}{due}"


def run(utterance, store):
    intent = parse_intent(utterance)
    a = intent.action
    if a == "list":
        todos = store.list()
        if not todos: return "（暂无待办）"
        return "待办列表：\n" + "\n".join(_format(t) for t in todos)
    if a == "add":
        t = store.add(intent.text, intent.due_date, intent.due_time)
        return f"已添加：#{t.id} {t.text}" + (f"（截止 {t.due_date} {t.due_time}）" if t.due_date else "")
    if a == "done":
        return f"已完成 #{intent.target_id}" if store.mark_done(intent.target_id) else f"未找到 #{intent.target_id}"
    if a == "remove":
        return f"已删除 #{intent.target_id}" if store.remove(intent.target_id) else f"未找到 #{intent.target_id}"
    if a == "edit":
        return f"已修改 #{intent.target_id} → {intent.text}" if store.edit(intent.target_id, intent.text) else f"未找到 #{intent.target_id}"
    return "（无法理解，请换个说法，例如：明天下午三点开会）"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="todo-agent", description="自然语言待办管理")
    ap.add_argument("utterance", nargs="?")
    ap.add_argument("--store", default="todos.json")
    args = ap.parse_args(argv)
    store = TodoStore(args.store)
    if args.utterance:
        print(run(args.utterance, store)); return 0
    print("待办助手（输入 exit 退出）。试试：明天下午三点开会 / 列出待办 / 完成 1")
    while True:
        try: line = input("> ").strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not line: continue
        if line in ("exit", "quit", "退出"): break
        print(run(line, store))
    return 0


if __name__ == "__main__": raise SystemExit(main())
