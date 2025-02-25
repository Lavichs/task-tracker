import argparse
import datetime
import json
import os

from colorama import init

# Инициализация colorama
init()

RED = (255, 21, 21)
GREEN = (0, 180, 0)
YELLOW = (220, 220, 21)
BLUE = (51, 51, 255)
VIOLET = (200, 0, 200)
WHITE = (255, 255, 255)


def getColoredText(text, color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m" + text + "\033[0m"


class ActionsList:
    add = "add"
    update = "update"
    delete = "delete"
    list = "list"


class AdditionalFields:
    description = 'description'  # second field of command "add"
    id_upd = 'id_upd'  # second field of command "update"
    new_description = 'new_description'  # third field of command "update"
    id_del = 'id_del'  # second field of command "delete"
    filter = 'filter'  # second field of command "list"


class Statuses:
    todo = "todo"
    in_progress = "in-progress"
    done = "done"

    @staticmethod
    def getStatusColor(status):
        match status:
            case Statuses.todo:
                return YELLOW
            case Statuses.in_progress:
                return BLUE
            case Statuses.done:
                return GREEN
            case _:
                return WHITE


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

    def show(self, filter):
        """
        Данная функция выводит на экран список дел отфильтрованных по статусу
        (если фильтр пустой – выводятся все задачи)
        :param filter: str
        :return: None
        """
        if len(self.tasks) == 0:
            print(getColoredText("Список задач пуст", GREEN))
            return 0
        print(getColoredText("ID\tстатус\t\tописание", VIOLET))
        count = 0
        for task in self.tasks:
            if filter != '' and task.status != filter:
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
        # task = list(filter(lambda task: task.id == _id, self.tasks))[0]
        # self.
        task = next((task for task in self.tasks if task.id == _id), None)
        task.description = new_description


actions = ActionsList()
fields = AdditionalFields()
statuses = Statuses()


def loadTasks() -> TaskList:
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
                return taskList
            except Exception as e:
                # если не удалось корректно загрузить данные
                print(getColoredText("Не удалось загрузить список задач. "
                                     "Проверьте целостность файла tasks.json или удалите его", YELLOW))
    return TaskList()


def main():
    # определение главного парсера
    parser = argparse.ArgumentParser(prog='task-cli',
                                     description='CLI-приложение для отслеживания ваших задач и управления списком дел.'
                                                ' (CLI app to track your tasks and manage your ToDo list)')
    # создание объекта, который будет создавать суб парсеры
    subparsers = parser.add_subparsers(help='Список команд. (List of commands)')

    # создание суб парсеров для команд действия для разных сценариев выполнения программы
    # каждый парсер будет иметь свой набор аргументов
    add_parser = subparsers.add_parser("add", help='добавить задачу. (add task)')  # создание
    update_parser = subparsers.add_parser("update", help='обновить задачу. (update task)')  # обновление
    delete_parser = subparsers.add_parser("delete", help='удалить. (delete task)')  # удаление
    list_parser = subparsers.add_parser("list", help='вывести список задач. (display a list of tasks)')  # вывод (чтение)

    # аргументы для создания
    # описание новой задачи
    add_parser.add_argument(fields.description,
                            type=str, help='описание новой задачи. (description of new task)')

    # аргументы для обновления
    # ID задачи которую нужно обновить
    update_parser.add_argument(fields.id_upd,
                               type=int, help='ID задачи. (ID of task)')
    # новое описание задачи
    update_parser.add_argument(fields.new_description,
                               type=str, help='новое описание задачи. (new description of task)')

    # аргументы для удаления
    # ID задачи которую нужно удалить
    delete_parser.add_argument(fields.id_del,
                               type=int, help='ID задачи. (ID of task)')

    # аргументы для чтения (вывода)
    # статус по которому нужно отфильтровать задачи при выводе
    list_parser.add_argument(fields.filter,
                             type=str,
                             help='один из следующих статусов: [done, todo, in-progres]. '
                                  ' (one of the following statuses: [done, todo, in-progres])',
                             nargs='?',
                             default="")

    # парсинг аргументов вызова программы
    args = parser.parse_args()
    arguments = vars(args)  # конвертация Namespace в Dict для удобства работы

    # выполнение разных сценариев в зависимости от выбранного действия
    # выбранное действие определяется по полученным аргументам полученным из парсера, т.к. у каждого субпарсера они свои
    # если в аргументах есть description, значит выполняется действие add (далее description -> add)
    if fields.description in args:
        taskList = loadTasks()

        task = Task.createNewTask(taskList.getAvailableId(), arguments.get(fields.description))
        taskList.addTask(task)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(f"Задача успешно добавлена (ID: {task.id})", GREEN))

    if fields.id_upd in args:
        _id = arguments.get(fields.id_upd)
        new_description = arguments.get(fields.new_description)

        taskList = loadTasks()
        taskList.update(_id, new_description)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(f"Задача успешно обновлена (ID: {_id}, описание: {new_description})", GREEN))
    if fields.id_del in args:
        ...
    if fields.filter in args:
        taskList = loadTasks()
        taskList.show(arguments.get(fields.filter))


if __name__ == '__main__':
    main()
