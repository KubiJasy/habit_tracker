from datetime import datetime, timedelta


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
        self.next_completion_date = next_completion_date or self.calculate_next_completion()

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
        if self.periodicity == 'daily':
            return datetime.now() + timedelta(days=1)
        elif self.periodicity == 'weekly':
            return datetime.now() + timedelta(weeks=1)
        else:
            raise ValueError(
                "Unsupported periodicity. Use 'daily' or 'weekly'.")

    def complete_habit(self):
        """
        Mark the habit as completed, update the streak and calculate the next completion date.
        """
        self.current_streak += 1
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.next_completion_date = self.calculate_next_completion()
        self.updated_at = datetime.now()

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

    def clear_habits(self):
        """
        Clears all habits from the habit list.
        """
        self.habits.clear()
        self.storage.session.query(Habit).delete()
        self.storage.session.commit()
