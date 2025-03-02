#!/usr/bin/env python3

import argparse
import ctypes
import json
import os
import sys

from src.Task import Task
from src.TaskList import TaskList
from src.consts import *
from src.utils import getColoredText

if os.name == 'nt':
    # Включаем поддержку ANSI-кодов на Windows
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING


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
            except json.decoder.JSONDecodeError as e:
                # если не удалось корректно загрузить данные
                print(getColoredText("Не удалось загрузить список задач. "
                                     "Проверьте целостность файла tasks.json или удалите его", RED))
                sys.exit(0)
            except Exception as error:
                print(getColoredText(f"Произошла непредвиденная ошибка ({error})"))
                sys.exit(0)
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
    list_parser = subparsers.add_parser("list",
                                        help='вывести список задач. (display a list of tasks)')  # вывод (чтение)
    # изменение статуса на in-progress
    mark_in_progress_parser = subparsers.add_parser("mark-in-progress",
                                                    help='установить задаче статус "в процессе (in-progress)" '
                                                         '(set task status in-progress)')
    mark_done_parser = subparsers.add_parser("mark-done",
                                             help='установить задаче статус "выполненная (done)" '
                                                  '(set task status in done)')  # изменение статуса на done

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

    # аргументы для изменения статуса
    # ID задачи которую нужно отметить выполняемой
    mark_in_progress_parser.add_argument(fields.id_tmp,
                                         type=int, help='ID задачи. (ID of task)')
    # ID задачи которую нужно отметить выполненной
    mark_done_parser.add_argument(fields.id_tmd,
                                  type=int, help='ID задачи. (ID of task)')

    # парсинг аргументов вызова программы
    args = parser.parse_args()
    arguments = vars(args)  # конвертация Namespace в Dict для удобства работы

    # Выполнение разных сценариев в зависимости от выбранного действия
    # выбранное действие определяется по полученным аргументам полученным из парсера, т.к. у каждого субпарсера они свои
    # если в аргументах есть description, значит выполняется действие add
    if fields.description in args:
        taskList = loadTasks()

        task = Task.createNewTask(taskList.getAvailableId(), arguments.get(fields.description))
        taskList.addTask(task)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(f"Задача успешно добавлена (ID: {task.id})", GREEN))

    # если в аргументах есть id_upd (id задачи для обновления), значит выполняется действие update
    if fields.id_upd in args:
        _id = arguments.get(fields.id_upd)
        new_description = arguments.get(fields.new_description)

        taskList = loadTasks()
        taskList.update(_id, new_description=new_description)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(f"Задача успешно обновлена (ID: {_id}, описание: {new_description})", GREEN))

    # если в аргументах есть id_del (id задачи для удаления), значит выполняется действие delete
    if fields.id_del in args:
        _id = arguments.get(fields.id_del)
        taskList = loadTasks()
        taskList.delete(_id)
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(f"Задача с ID: {_id} удалена", GREEN))

    # если в аргументах есть filter (статус задачи для выборки), значит выполняется действие List
    if fields.filter in args:
        taskList = loadTasks()
        taskList.show(arguments.get(fields.filter))

    # если в аргументах есть id_tmp (id задачи для изменения статуса на in-progress),
    # значит выполняется действие mark-in-progress
    if fields.id_tmp in args:
        _id = arguments.get(fields.id_tmp)
        taskList = loadTasks()
        taskList.update(_id, new_status=statuses.in_progress)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(
            f"Статус задачи успешно изменен (ID: {_id}, статус: "
            f"{getColoredText(statuses.in_progress, statuses.getStatusColor(statuses.in_progress))})",
            GREEN))

    # если в аргументах есть id_tmd (id задачи для изменения статуса на done),
    # значит выполняется действие mark-in-done
    if fields.id_tmd in args:
        _id = arguments.get(fields.id_tmd)
        taskList = loadTasks()
        taskList.update(_id, new_status=statuses.done)

        # сохранить список в формате json
        with open('tasks.json', 'w') as json_file:
            json_file.write(taskList.__repr__().replace("'", '"'))
        print(getColoredText(
            f"Статус задачи успешно изменен (ID: {_id}, статус: "
            f"{getColoredText(statuses.done, statuses.getStatusColor(statuses.done))})",
            GREEN))


if __name__ == '__main__':
    main()
