# task-tracker

Трекер задач — это учебный проект для отслеживания задач и управления ими. В данном проекте был создан простой интерфейс командной строки (CLI) для отслеживания актуальных, выполненных и запланированных задач. Выполнение данного проекта позволило попрактиковаться в... 

## Содержание
- [Навигация по документации](#Навигация-по-документации)
- [Установка](#Установка)
- [Использование](#Использование)

## Навигация по документации

В данном документе приведено общее описание проекта, процесс установки и использования. Более подробная информация представлена в соответствующих документах:
* [Техническое задание](technical_specification.md)

## Установка

Для установки приложения выполните следующую команду:

```bash
git clone https://github.com/Lavichs/task-tracker.git
```

## Использование

Базовый пример использования:


![Базовый пример использования](example.svg)

Полный список команд и их использование:
```bash
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task as in progress or done
task-cli mark-in-progress 1
task-cli mark-done 1

# Listing all tasks
task-cli list

# Listing tasks by status
task-cli list done
task-cli list todo
task-cli list in-progress
```
