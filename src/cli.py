import questionary
from datetime import datetime, time
from .habits import HabitManager
from .tasks import TaskManager
from .db import StorageComponent
from .analytics import list_habits, longest_streak_for_given_habit, longest_streak_from_habits, list_habits_periodicity


class HabitTrackerCLI:
    def __init__(self):
        self.storage_component = StorageComponent()
        self.habit_manager = HabitManager(self.storage_component)
        self.task_manager = TaskManager(self.storage_component)

    def create_habit(self):
        action = questionary.select(
            "Do you want to proceed with creating a new habit or go back?",
            choices=["Proceed", "Go back"]
        ).ask()

        if action == "Go back":
            return
        name = questionary.text("Enter the name of the habit:").ask()
        periodicity = questionary.select(
            "Select the periodicity of the habit:", choices=["daily", "weekly"]).ask()

        # Create habit and corresponding task
        created_habit = self.habit_manager.create_habit(name, periodicity)
        self.task_manager.create_task(
            created_habit.id, created_habit.periodicity)
        print("Habit successfully created😊!")

    def update_habit(self):
        habits = self.habit_manager.habits
        if not habits:
            print("No habits available to update.")
            return

        while True:
            habit_choices = [
                "Go back"] + [f"ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}" for habit in habits]
            selected_habit = questionary.select(
                "Select the habit to update:", choices=habit_choices, use_arrow_keys=True).ask()

            if selected_habit == "Go back":
                return

            selected_index = habit_choices.index(selected_habit) - 1
            habit_id = habits[selected_index].id

            attribute = questionary.select("Select the attribute to update:", choices=[
                                           "Go back", "name"]).ask()

            if attribute == "Go back":
                continue

            value = questionary.text(
                f"Enter the new value for {attribute}:").ask()

            self.habit_manager.update_habit(habit_id, **{attribute: value})
            print("Habit successfully updated😊!")
            break

    def delete_habit(self):
        habits = self.habit_manager.habits
        if not habits:
            print("No habits available to delete.")
            return

        while True:
            habit_choices = [
                "Go back"] + [f"ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}" for habit in habits]
            selected_habit = questionary.select(
                "Select the habit to delete:", choices=habit_choices, use_arrow_keys=True).ask()

            if selected_habit == "Go back":
                return

            selected_index = habit_choices.index(selected_habit) - 1
            habit_id = habits[selected_index].id

            self.habit_manager.delete_habit(habit_id)
            print("Habit successfully deleted😊!")
            break

    def list_habits(self):
        habits = list_habits()
        if not habits:
            print("No habits found.")
            return

        # For a numbered list of habits in the database

        habit_names = [f"{index + 1}. {habit.name}" for index,
                       habit in enumerate(habits)]
        habit_names.append("Go back")
        selected_habit_name = questionary.select(
            "Select a habit to view details:", choices=habit_names).ask()
        if selected_habit_name == "Go back":
            return
        selected_index = int(selected_habit_name.split('.')[0]) - 1
        selected_habit = habits[selected_index]
        print(f"\nID: {selected_habit.id}\nName: {selected_habit.name}\nPeriodicity: {selected_habit.periodicity}\nCreated On: {selected_habit.created_at.strftime('%A, %B %d, %Y')}\nNext Completion Date: {selected_habit.next_completion_date.strftime('%A, %B %d, %Y')}\n")

        while True:
            action = questionary.select(
                "What would you like to do with this habit?",
                choices=["Mark as completed", "View streaks", "Go back"]
            ).ask()

            if action == "Mark as completed":
                response = self.habit_manager.mark_habit_completed(
                    selected_habit.id)
                print(response)
                break
            elif action == "View streaks":
                print(
                    f"\nCurrent Streak: {selected_habit.current_streak}\nLongest Streak: {selected_habit.longest_streak}\n")
            elif action == "Go back":
                break

    def view_analytics(self):
        """
        View analytics options and handle user selections.
        """
        while True:
            action = questionary.select(
                "Select an analytics option:",
                choices=[
                    "List habits by periodicity",
                    "Longest streak across all habits",
                    "Longest streak for a given habit",
                    "Go back"
                ]
            ).ask()

            if action == "List habits by periodicity":
                self.list_habits_by_periodicity()
            elif action == "Longest streak across all habits":
                self.display_longest_streak_across_habits()
            elif action == "Longest streak for a given habit":
                self.display_longest_streak_for_given_habit()
            elif action == "Go back":
                break

    def list_habits_by_periodicity(self):
        """
        Display habits filtered by periodicity.
        """
        periodicity = questionary.select(
            "Select the periodicity to filter by:", choices=["daily", "weekly", "Go back"]
        ).ask()

        if periodicity == "Go back":
            return

        habits = list_habits_periodicity(periodicity)
        if not habits:
            print(f"No habits found with periodicity '{periodicity}'.")
        else:
            for index, habit in enumerate(habits):
                print(
                    f"{index + 1}. ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}")

    def display_longest_streak_across_habits(self):
        """
        Display the habit with the longest streak across all habits.
        """
        result = longest_streak_from_habits()
        print(result)

    def display_longest_streak_for_given_habit(self):
        """
        Display the longest streak for a specific habit.
        """
        habits = list_habits()
        if not habits:
            print("No habits found.")
            return

        habit_names = [f"{index + 1}. {habit.name}" for index,
                       habit in enumerate(habits)]
        habit_names.append("Go back")

        selected_habit_name = questionary.select(
            "Select a habit to view its longest streak:", choices=habit_names
        ).ask()
        if selected_habit_name == "Go back":
            return
        selected_index = int(selected_habit_name.split('.')[0]) - 1
        selected_habit = habits[selected_index]

        result = longest_streak_for_given_habit(selected_habit.name)
        print(result)

    def run(self):
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Create a new habit",
                    "Update an existing habit",
                    "Delete a habit",
                    "List all habits",
                    "View Analytics",  # Added option for analytics
                    "Exit"
                ]
            ).ask()

            if action == "Create a new habit":
                self.create_habit()
            elif action == "Update an existing habit":
                self.update_habit()
            elif action == "Delete a habit":
                self.delete_habit()
            elif action == "List all habits":
                self.list_habits()
            elif action == "View Analytics":
                self.view_analytics()
            elif action == "Exit":
                self.storage_component.close()
                exit()


if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()
