import datetime

from src.consts import statuses


class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str

    def __init__(self, task_id: int, description: str, status: str, createdAt: str, updatedAt: str):
        self.id = task_id
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    @staticmethod
    def createNewTask(task_id: int, description: str):
        return Task(
            task_id,
            description,
            statuses.todo,
            str(datetime.datetime.now()),
            str(datetime.datetime.now())
        )

    def __repr__(self):
        return f"""{{
    "id": {self.id},
    "description": "{self.description}",
    "status": "{self.status}",
    "createdAt": "{self.createdAt}",
    "updatedAt": "{self.updatedAt}"
}}"""

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": str(self.createdAt),
            "updatedAt": str(self.updatedAt)
        }
