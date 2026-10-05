import sys, tempfile, unittest
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from todo_agent_lite.parser import parse_intent, _resolve_date, _resolve_time
from todo_agent_lite.store import TodoStore
from todo_agent_lite.cli import run

BASE = datetime(2026, 10, 6, 10, 0)

class TestParser(unittest.TestCase):
    def test_resolve_date_tomorrow(self): self.assertEqual(_resolve_date("明天", BASE), "2026-10-07")
    def test_resolve_date_day_after(self): self.assertEqual(_resolve_date("后天", BASE), "2026-10-08")
    def test_resolve_date_next_wed(self): self.assertEqual(_resolve_date("下周三", BASE), "2026-10-14")
    def test_resolve_date_friday(self): self.assertEqual(_resolve_date("周五", BASE), "2026-10-09")
    def test_resolve_time_afternoon(self): self.assertEqual(_resolve_time("下午三点"), "15:00")
    def test_resolve_time_morning(self): self.assertEqual(_resolve_time("早上九点半"), "09:30")
    def test_resolve_time_24h(self): self.assertEqual(_resolve_time("14:30"), "14:30")
    def test_parse_add(self):
        p = parse_intent("明天下午三点开会", base=BASE)
        self.assertEqual(p.action, "add"); self.assertEqual(p.due_date, "2026-10-07"); self.assertEqual(p.due_time, "15:00")
    def test_parse_list(self): self.assertEqual(parse_intent("列出待办", base=BASE).action, "list")
    def test_parse_done(self):
        p = parse_intent("把 2 标记为完成", base=BASE)
        self.assertEqual(p.action, "done"); self.assertEqual(p.target_id, 2)
    def test_parse_remove(self):
        p = parse_intent("删除 5 号", base=BASE)
        self.assertEqual(p.action, "remove"); self.assertEqual(p.target_id, 5)
    def test_parse_edit(self):
        p = parse_intent("把 2 改成买苹果", base=BASE)
        self.assertEqual(p.action, "edit"); self.assertEqual(p.target_id, 2); self.assertEqual(p.text, "买苹果")

class TestStoreAndRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = TodoStore(Path(self.tmp.name) / "todos.json")
    def tearDown(self): self.tmp.cleanup()
    def test_add_list_done(self):
        run("明天下午三点开会", self.store)
        self.assertIn("开会", run("列出待办", self.store))
        self.assertIn("已完成 #1", run("把 1 标记为完成", self.store))
        self.assertTrue(self.store.list()[0].done)
    def test_remove(self):
        run("买牛奶", self.store); run("买鸡蛋", self.store)
        self.assertIn("已删除 #1", run("删除 1 号", self.store))
        self.assertEqual(len(self.store.list()), 1)
    def test_edit(self):
        run("买牛奶", self.store)
        self.assertIn("买苹果和香蕉", run("把 1 改成买苹果和香蕉", self.store))
        self.assertEqual(self.store.list()[0].text, "买苹果和香蕉")
    def test_persist_roundtrip(self):
        run("明天交报告", self.store)
        store2 = TodoStore(self.store.path)
        self.assertEqual(len(store2.list()), 1)
        self.assertEqual(store2.list()[0].due_date, "2026-10-07")

if __name__ == "__main__": unittest.main()
