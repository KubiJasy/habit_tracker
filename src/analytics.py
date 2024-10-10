from .db import StorageComponent
from .habits import HabitManager


def list_habits():
    """
    List all habits.
    """
    habit_manager = HabitManager(StorageComponent())
    return habit_manager.habits


def list_habits_periodicity(periodicity):
    """
    List habits filtered by a given periodicity.

    Arguments:
    periodicity -- the periodicity to filter habits by (e.g., 'daily', 'weekly').
    """
    habit_manager = HabitManager(StorageComponent())
    habits = habit_manager.storage.load_habits(periodicity=periodicity)  # Filter by periodicity
    return habits if habits else f"No habits found with periodicity '{periodicity}'."


def longest_streak_from_habits():
    """
    Find the habit with the longest streak across all habits.
    """
    habit_manager = HabitManager(StorageComponent())
    habits = habit_manager.storage.load_habits()  # Load all habits
    
    if not habits:
        return "No habits found."
    
    # Find the habit with the longest streak
    longest_habit = max(habits, key=lambda habit: habit.longest_streak)
    
    return f"The habit with the longest streak is '{longest_habit.name}' with a streak of {longest_habit.longest_streak}."



def longest_streak_for_given_habit(habit_name):
    """
    Find the longest streak for a given habit.

    Arguments:
    habit_name -- the name of the habit to find the longest streak for.
    """
    habit_manager = HabitManager(StorageComponent())
    habits = habit_manager.storage.load_habits(name=habit_name)  # Filter by habit name
    
    if not habits:
        return f"No habit found with the name '{habit_name}'."
    
    # Assuming there could be more than one habit with the same name, find the max streak among them
    longest_streak_habit = max(habits, key=lambda habit: habit.longest_streak)
    
    return f"The longest streak for habit '{habit_name}' is {longest_streak_habit.longest_streak}."

