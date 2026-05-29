import uuid
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from utils.config import load_todos, save_todos


class TodoManager(QObject):
    todo_added = pyqtSignal(dict)
    todo_updated = pyqtSignal(dict)
    todo_deleted = pyqtSignal(str)
    todo_reminder = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._todos = load_todos()
        self._reminded = set()
        self._check_timer = QTimer(self)
        self._check_timer.timeout.connect(self._check_reminders)
        self._check_timer.start(60000)

    @property
    def todos(self) -> list:
        return self._todos

    def add(self, title: str, due: str = "", priority: str = "normal") -> dict:
        todo = {
            "id": uuid.uuid4().hex[:8],
            "title": title,
            "done": False,
            "due": due,
            "priority": priority,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self._todos.append(todo)
        self._save()
        self.todo_added.emit(todo)
        return todo

    def toggle(self, todo_id: str):
        for t in self._todos:
            if t["id"] == todo_id:
                t["done"] = not t["done"]
                self._save()
                self.todo_updated.emit(t)
                return

    def delete(self, todo_id: str):
        self._todos = [t for t in self._todos if t["id"] != todo_id]
        self._save()
        self.todo_deleted.emit(todo_id)

    def update(self, todo_id: str, **kwargs):
        for t in self._todos:
            if t["id"] == todo_id:
                t.update(kwargs)
                self._save()
                self.todo_updated.emit(t)
                return

    def get_pending(self) -> list:
        return [t for t in self._todos if not t["done"]]

    def _save(self):
        save_todos(self._todos)

    def _check_reminders(self):
        now = datetime.now()

        for t in self._todos:
            if t["done"] or not t.get("due"):
                continue

            due_str = t["due"]
            try:
                due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
            except ValueError:
                continue

            due_date = due_dt.date()
            tomorrow = (now + timedelta(days=1)).date()

            if due_date == tomorrow:
                slot_key_am = (t["id"], "day_before_am")
                if now.hour >= 10 and slot_key_am not in self._reminded:
                    self._reminded.add(slot_key_am)
                    self.todo_reminder.emit(f'提醒: "{t["title"]}" 明天到期')
                    return

                slot_key_pm = (t["id"], "day_before_pm")
                if now.hour >= 16 and slot_key_pm not in self._reminded:
                    self._reminded.add(slot_key_pm)
                    self.todo_reminder.emit(f'提醒: "{t["title"]}" 明天到期')
                    return

            slot_key_overdue = (t["id"], "overdue")
            if now >= due_dt and slot_key_overdue not in self._reminded:
                self._reminded.add(slot_key_overdue)
                self.todo_reminder.emit(f'待办到期: {t["title"]}')
                return

    def check_boot_reminders(self):
        """开机时检查并提醒未完成的待办事项"""
        pending = self.get_pending()
        if not pending:
            return

        now = datetime.now()
        for t in pending:
            if t.get("due"):
                try:
                    due_dt = datetime.strptime(t["due"], "%Y-%m-%d %H:%M")
                    if now >= due_dt:
                        self._reminded.add((t["id"], "overdue"))
                except ValueError:
                    pass

        count = len(pending)
        titles = ", ".join(t["title"] for t in pending[:3])
        suffix = f" 等{count}项" if count > 3 else ""
        self.todo_reminder.emit(f"你有{count}个待办未完成: {titles}{suffix}")
