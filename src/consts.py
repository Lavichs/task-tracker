# цвета
RED = (255, 21, 21)
GREEN = (0, 180, 0)
YELLOW = (220, 220, 21)
BLUE = (51, 51, 255)
VIOLET = (200, 0, 200)
WHITE = (255, 255, 255)


# команды действия
class ActionsList:
    add = "add"
    update = "update"
    delete = "delete"
    list = "list"


# дополнительные атрибуты команд
class AdditionalFields:
    description = 'description'  # second field of command "add"
    id_upd = 'id_upd'  # second field of command "update"
    new_description = 'new_description'  # third field of command "update"
    id_del = 'id_del'  # second field of command "delete"
    filter = 'filter'  # second field of command "list"


# статусы задач
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


actions = ActionsList()
fields = AdditionalFields()
statuses = Statuses()
