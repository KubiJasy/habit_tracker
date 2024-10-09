import datetime


class Task:
    def __init__(self, habit_id, completed=False, completed_on=None, expected_completion_by=None):
        """
        Initializes a new instance of the Task class.

        :param habit_id: The ID of the habit associated with this task.
        :param completed: Whether the task is completed or not.
        :param completed_on: The date on which the task was completed.
        """
        self.habit_id = habit_id
        self.completed = completed
        self.completed_on = completed_on
        self.expected_completion_by = expected_completion_by

    def record_habit_completion(self, habit_id, next_completion_date, current_streak, longest_streak):
        """
        Records the completion of a habit.

        :param habit_id: The ID of the habit associated with this task.
        :param next_completion_date: The next date the habit is scheduled to be completed.
        :param current_streak: The current streak of habit completions.
        :param longest_streak: The longest streak of habit completions.
        """
        self.habit_id = habit_id
        self.completed = True
        self.completed_on = datetime.now()

    def set_completed_on(self, date):
        """
        Sets the completion date for the task.

        :param date: The date on which the task was completed.
        :return: The date the task was completed.
        """
        self.completed_on = date
        return self.completed_on


class TaskManager:
    """
    Manages a collection of tasks, allowing for the creation, updating, and deletion of tasks.
    Must be initialized with a storage component
    """

    def __init__(self, storage_component):
        self.storage = storage_component
        self.tasks = self.storage.load_tasks()

    def create_task(self, habit_id):
        """
        Create a new task and add it to the task list.
        :param habit_id: The ID of the habit associated with the task.
        """
        new_task = Task(habit_id=habit_id)
        created_task = self.storage.save_task(new_task)
        self.tasks.append(created_task)
        return created_task

    def update_task(self, task_id, **kwargs):
        """
        Update an existing task in the task list.
        :param task_id: The ID of the task to be updated.
        :param kwargs: Key-value pairs of attributes to update.
        """
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.storage.save_task(task)

    def delete_task(self, task_id):
        """
        Delete a task from the task list.
        :param task_id: The ID of the task to be deleted.
        """
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.storage.session.delete(task)
            self.storage.session.commit()
