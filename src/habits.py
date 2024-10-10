from datetime import datetime, timedelta
from .tasks import TaskManager


class Habit:

    def __init__(self, name, periodicity, current_streak=0, longest_streak=0, next_completion_date=None):
        """
        Initialize a new Habit instance.

        :param name: The name of the habit.
        :param periodicity: The periodicity of the habit (e.g., daily, weekly).
        :param current_streak: The current streak of the habit.
        :param longest_streak: The longest streak achieved for the habit.
        :param next_completion_date: The date when the habit should next be completed.
        """
        self.name = name
        self.periodicity = periodicity
        self.current_streak = current_streak
        self.longest_streak = longest_streak
        self.next_completion_date = next_completion_date

    def get_streak(self):
        """
        Get the current streak of the habit.

        :return: The current streak.
        """
        return self.current_streak

    def calculate_next_completion(self):
        """
        Calculate the next completion date based on the periodicity.

        :return: The next completion date.
        """
        now = datetime.now()
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)

        if self.periodicity == 'daily':
            return end_of_day + timedelta(days=1) if self.next_completion_date else end_of_day
        elif self.periodicity == 'weekly':
            if self.next_completion_date:
                next_completion_weekday = self.next_completion_date.weekday()
                end_of_day_weekday = end_of_day.weekday()

                # If the end_of_day weekday matches the next completion date weekday
                if next_completion_weekday == end_of_day_weekday:
                    return end_of_day + timedelta(weeks=1)
                else:
                    # Calculate the difference in days to get the next closest matching weekday
                    days_difference = (
                        next_completion_weekday - end_of_day_weekday + 7) % 7
                    next_closest_date = end_of_day + \
                        timedelta(days=days_difference)

                    # Check if the next closest date falls in the same week as the end_of_day
                    if next_closest_date <= end_of_day + timedelta(days=6):
                        return next_closest_date + timedelta(weeks=1)
                    else:
                        return next_closest_date
            else:
                return end_of_day
        else:
            raise ValueError(
                "Unsupported periodicity. Use 'daily' or 'weekly'.")

    def complete_habit(self, latest_task, storage_component):
        """
        Mark the habit as completed, update the streak and calculate the next completion date.

        :param latest_task: The latest task record for the given habit.
        :param storage_component: Storage component instance to handle database interactions.
        :return: A message indicating the result of the completion attempt.
        """
        now = datetime.now()
        # print(vars(latest_task))
        # print(latest_task.expected_completion_by.date())

        if latest_task.expected_completion_by.date() > now.date():
            return "This habit is not due for completion yet😌."

        # Proceed with updating the habit
        if now <= latest_task.expected_completion_by:
            # Person is on track with their habit
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Person missed the expected completion date
            self.current_streak = 0

        latest_task.completed = True
        latest_task.completed_on = now
        storage_component.save_task(latest_task)

        # Create a new task record for the next expected completion
        TaskManager(storage_component).create_task(
            latest_task.habit_id, self.periodicity)

        # Update the next completion date of the habit
        self.next_completion_date = self.calculate_next_completion()
        self.updated_at = now
        self.id = latest_task.habit_id

        storage_component.save_habit(self)

        return "Habit marked as completed😊!"

    def reset_streak(self):
        """
        Reset the current streak of the habit.
        """
        self.current_streak = 0
        self.next_completion_date = self.calculate_next_completion()
        self.updated_at = datetime.now()

    def is_due(self):
        """
        Check if the habit is due for completion.

        :return: True if the habit is due, False otherwise.
        """
        return datetime.now() >= self.next_completion_date


class HabitManager:
    """
    Manages a collection of habits.
    needs the storage component on initialization
    """

    def __init__(self, storage_component):
        self.storage = storage_component
        self.habits = self.storage.load_habits()

    def create_habit(self, name, periodicity):
        """
        Creates a new habit and adds it to the habit list.
        :param name: The name of the habit.
        :param periodicity: The periodicity of the habit (e.g., daily, weekly).
        """
        new_habit = Habit(name=name, periodicity=periodicity)
        new_habit.next_completion_date = new_habit.calculate_next_completion()
        # print("Habits", self.habits)
        # print("New Habit", new_habit)
        created_habit = self.storage.save_habit(new_habit)
        self.habits.append(created_habit)
        return created_habit

    def update_habit(self, habit_id, **kwargs):
        """
        Updates an existing habit.
        :param habit_id: The ID of the habit to be updated.
        :param kwargs: Key-value pairs of attributes to update.
        """
        habit = next((h for h in self.habits if h.id == habit_id), None)
        if habit:
            for key, value in kwargs.items():
                if hasattr(habit, key):
                    setattr(habit, key, value)
            self.storage.save_habit(habit)

    def delete_habit(self, habit_id):
        """
        Deletes a habit from the habit list.
        :param habit_id: The ID of the habit to be deleted.
        """
        habit = next((h for h in self.habits if h.id == habit_id), None)
        if habit:
            self.habits.remove(habit)
            self.storage.session.delete(habit)
            self.storage.session.commit()

    # def delete_habit(self, habit_id):
    #     """
    #     Deletes a habit from the habit list.
    #     :param habit_id: The ID of the habit to be deleted.
    #     """
    #     habit = next((h for h in self.habits if h.id == habit_id), None)
    #     if habit:
    #         self.habits.remove(habit)
    #         self.storage.delete_habit(habit_id)

    def mark_habit_completed(self, habit_id):
        """
        Marks a habit as completed by calling the complete_habit method of the Habit class.

        :param habit_id: The ID of the habit to be marked as completed.
        :return: A message indicating the result of the completion attempt.
        """
        habit = next((h for h in self.habits if h.id == habit_id), None)
        habit_attrs = {k: v for k, v in vars(habit).items() if not k.startswith(
            '__') and not callable(v) and not k.startswith('_')}

        # removing uneccessary attrs
        del habit_attrs["created_at"]
        del habit_attrs["updated_at"]
        del habit_attrs["id"]

        if habit:
            habit_obj = Habit(**habit_attrs)
            latest_task = self.storage.load_tasks_for_habit(habit_id)[-1]
            return habit_obj.complete_habit(latest_task, self.storage)
        return "Habit not found."

    def clear_habits(self):
        """
        Clears all habits from the habit list.
        """
        self.habits.clear()
        self.storage.session.query(Habit).delete()
        self.storage.session.commit()
