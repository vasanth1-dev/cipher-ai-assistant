from services.todo_service import todo_service


INTENT = "todo"


def _normalize(text):

    return " ".join(
        text.lower().strip().split()
    )


def _number(command, prefix):

    try:

        return int(
            command[len(prefix):].strip()
        )

    except (ValueError, TypeError):

        return None


def handle(command: str):

    if not command:
        return None

    command = _normalize(command)

    # -------------------------------------------------
    # Add Task
    # -------------------------------------------------

    prefixes = (
        "add task",
        "create task",
        "add todo",
        "add a todo",
        "create todo",
        "create a todo",
    )

    for prefix in prefixes:

        if command.startswith(prefix):

            task = command[len(prefix):].strip()

            if not task:
                return "What task should I add?"

            return todo_service.add(task)

    # -------------------------------------------------
    # Show Tasks
    # -------------------------------------------------

    if command in (
        "show tasks",
        "list tasks",
        "my tasks",
        "todo",
        "todo list",
        "show todo",
        "show todos",
        "show my todos",
        "list todos",
    ):

        return todo_service.list()

    # -------------------------------------------------
    # Complete Task
    # -------------------------------------------------

    prefix = "complete task"

    if command.startswith(prefix):

        number = _number(command, prefix)

        if number is None:
            return "Please tell me the task number."

        return todo_service.complete(number)

    # -------------------------------------------------
    # Delete Task
    # -------------------------------------------------

    prefix = "delete task"

    if command.startswith(prefix):

        number = _number(command, prefix)

        if number is None:
            return "Please tell me the task number."

        return todo_service.delete(number)

    # -------------------------------------------------
    # Clear Completed
    # -------------------------------------------------

    if command in (
        "clear completed tasks",
        "clear tasks",
    ):

        if hasattr(todo_service, "clear_completed"):
            return todo_service.clear_completed()

        return "This feature is not available."

    return None