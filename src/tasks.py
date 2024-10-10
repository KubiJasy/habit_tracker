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

    def calculate_expected_completion_by(self, habit_periodicity, last_task_completion_date=None):
        """
        Calculate the expected completion date for a task based on the habit's periodicity.

        :param habit_periodicity: The periodicity of the habit (e.g., daily, weekly).
        :param last_task_completion_date: The completion date of the last task for the habit.
        :return: The expected completion date.
        """
        now = datetime.datetime.now()

        # If there is no last task completion date, the expected completion date is today at the end of the day
        if not last_task_completion_date:
            return now.replace(hour=23, minute=59, second=59, microsecond=0)

        base_date = now

        if habit_periodicity == 'daily':
            return (base_date + datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)

        elif habit_periodicity == 'weekly':
            # Weekday of the last task completion date
            last_task_completion_date_weekday = last_task_completion_date.weekday()
            now_weekday = now.weekday()  # Current weekday (today)

            # If the current weekday matches the base weekday
            if now_weekday == last_task_completion_date_weekday:
                return (now + datetime.timedelta(weeks=1)).replace(hour=23, minute=59, second=59, microsecond=0)
            else:
                # Calculate days difference to the next occurrence of the base weekday
                days_difference = (
                    last_task_completion_date_weekday - now_weekday + 7) % 7
                next_closest_date = now + \
                    datetime.timedelta(days=days_difference)

                # If the closest date is within the same week as today, add 1 week
                if next_closest_date <= now + datetime.timedelta(days=6):
                    return (next_closest_date + datetime.timedelta(weeks=1)).replace(hour=23, minute=59, second=59, microsecond=0)
                else:
                    return next_closest_date.replace(hour=23, minute=59, second=59, microsecond=0)

        else:
            raise ValueError(
                "Unsupported periodicity. Use 'daily' or 'weekly'.")


class TaskManager:
    """
    Manages a collection of tasks, allowing for the creation, updating, and deletion of tasks.
    Must be initialized with a storage component
    """

    def __init__(self, storage_component):
        self.storage = storage_component
        self.tasks = self.storage.load_tasks()

    def create_task(self, habit_id, habit_periodicity):
        """
        Create a new task and add it to the task list.
        :param habit_id: The ID of the habit associated with the task.
        """
        # new_task = Task(habit_id=habit_id,
        #                 expected_completion_by=expected_completion_date)
        # created_task = self.storage.save_task(new_task)
        # self.tasks.append(created_task)
        # return created_task

        """
        Create a new task and add it to the task list.
        :param habit_id: The ID of the habit associated with the task.
        :param habit_periodicity: The periodicity of the habit (e.g., daily, weekly).
        :param is_initial_task: Whether this is the first task for the habit.
        """
        # checking if there is an existing task for the habit already, meaning this is an existing habit
        tasks_for_habit = self.storage.load_tasks_for_habit(habit_id)
        last_task = tasks_for_habit[-1] if tasks_for_habit else None

        # print(last_task.expected_completion_by)
        # checking the expected completion date for the latest task record
        last_task_expected_completion_date = last_task.expected_completion_by if last_task else None
        expected_completion_date = Task(habit_id).calculate_expected_completion_by(
            habit_periodicity, last_task_expected_completion_date)
        new_task = Task(habit_id=habit_id,
                        expected_completion_by=expected_completion_date)
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
