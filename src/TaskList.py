import sys

from src.Task import Task
from src.consts import *
from src.utils import getColoredText


class TaskList:
    max_id: int
    tasks: list[Task]

    def __init__(self, data=None):
        if data is None:
            self.tasks = []
            self.max_id = 0
        else:
            self.max_id = data.get('max_id')
            self.tasks = [Task(task.get('id'),
                               task.get('description'),
                               task.get('status'),
                               task.get('createdAt'),
                               task.get('updatedAt'))
                          for task in data.get('tasks')]

    def getAvailableId(self) -> int:
        return self.max_id

    def addTask(self, task: Task):
        self.tasks.append(task)
        self.max_id += 1

    def __repr__(self):
        return f"""{{
    "max_id": {self.max_id},
    "tasks": {[item.toDict() for item in self.tasks]}
}}"""

    def show(self, status_filter):
        """
        Данная функция выводит на экран список дел отфильтрованных по статусу
        (если фильтр пустой – выводятся все задачи)
        :param status_filter: str
        :return: None
        """
        if len(self.tasks) == 0:
            print(getColoredText("Список задач пуст", GREEN))
            return 0
        print(getColoredText("ID\tстатус\t\tописание", VIOLET))
        count = 0
        for task in self.tasks:
            if status_filter != '' and task.status != status_filter:
                continue
            colored_status = getColoredText(task.status, statuses.getStatusColor(task.status))
            if task.status == statuses.in_progress:
                colored_status += '\t'
            else:
                colored_status += '\t\t'
            print(f"{task.id}\t{colored_status}{task.description}")
            count += 1
        print(f"Total: {count}")

    def update(self, _id, new_description):
        task = next((task for task in self.tasks if task.id == _id), None)
        if task is None:
            print(getColoredText(f"Задача с ID: {_id} не найдена", RED))
            sys.exit()
        task.description = new_description

    def delete(self, _id):
        self.tasks = list(filter(lambda task: task.id != _id, self.tasks))
