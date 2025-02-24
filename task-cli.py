import argparse
import datetime
import json
import os
from colorama import Fore, Style, init

# Инициализация colorama
init()


class ActionsList:
    add = "add"
    update = "update"
    delete = "delete"
    list = "list"


class SecondFields:
    description = 'description'  # second field of command "add"
    id_upd = 'id_upd'  # second field of command "update"
    id_del = 'id_del'  # second field of command "delete"
    filter = 'filter'  # second field of command "list"


class Statuses:
    todo = "todo"
    in_progress = "in-progress"
    done = "done"


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


actions = ActionsList()
fields = SecondFields()
statuses = Statuses()


def main():
    # определение главного парсера
    parser = argparse.ArgumentParser(prog='task-cli',
                                     description='CLI app to track your tasks and manage your to-do list')
    # создание объекта, который будет создавать суб парсеры
    subparsers = parser.add_subparsers(help='List of commands')

    # создание суб парсеров для команд действия для разных сценариев выполнения программы
    # каждый парсер будет иметь свой набор аргументов
    add_parser = subparsers.add_parser("add", help='add task')  # создание
    update_parser = subparsers.add_parser("update", help='update task')  # обновление
    delete_parser = subparsers.add_parser("delete", help='update task')  # удаление
    list_parser = subparsers.add_parser("list", help='update task')  # вывод (чтение)

    # аргументы для создания
    # описание новой задачи
    add_parser.add_argument(fields.description,
                            type=str, help='description of new task')

    # аргументы для обновления
    # ID задачи которую нужно обновить
    update_parser.add_argument(fields.id_upd,
                               type=int, help='ID of task')

    # аргументы для удаления
    # ID задачи которую нужно удалить
    delete_parser.add_argument(fields.id_del,
                               type=int, help='ID of task')

    # аргументы для чтения (вывода)
    # статус по которому нужно отфильтровать задачи при выводе
    list_parser.add_argument(fields.filter,
                             type=str,
                             help='one of the following statuses: done, todo, in-progres',
                             nargs='?',
                             default="")

    # парсинг аргументов вызова программы
    args = parser.parse_args()
    arguments = vars(args)  # конвертация Namespace в Dict для удобства работы

    # выполнение разных сценариев в зависимости от выбранного действия
    # выбранное действие определяется по полученным аргументам полученным из парсера, т.к. у каждого субпарсера они свои
    # если в аргументах есть description, значит выполняется действие add (далее description -> add)
    if fields.description in args:
        # если файл со списком задач существует
        if os.path.isfile('tasks.json'):
            # открываем его на чтение
            with open('tasks.json', 'r') as json_file:
                data = json_file.read()
                try:
                    # если данные корректно загружаются
                    # создавать список дел на основе данных файла
                    json_data = json.loads(data)
                    taskList = TaskList(json_data)
                except Exception as e:
                    # если не удалось корректно загрузить данные
                    # создать пустой список дел
                    taskList = TaskList()
        else:
            # если файла со списком задач не существует – создаем пустой список дел
            taskList = TaskList()

        task = Task.createNewTask(taskList.getAvailableId(), arguments.get(fields.description))
        taskList.addTask(task)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"').replace(" ", ''))

        print(Fore.GREEN + f"Task added successfully (ID: {task.id})" + Style.RESET_ALL)

    if fields.id_upd in args:
        ...
    if fields.id_del in args:
        ...
    if fields.filter in args:
        ...


if __name__ == '__main__':
    main()
