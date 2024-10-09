import questionary
from datetime import datetime, time
from habits import HabitManager
from tasks import TaskManager
from db import StorageComponent


class HabitTrackerCLI:
    def __init__(self):
        self.storage_component = StorageComponent()
        self.habit_manager = HabitManager(self.storage_component)
        self.task_manager = TaskManager(self.storage_component)

    def create_habit(self):
        name = questionary.text("Enter the name of the habit:").ask()
        periodicity = questionary.select(
            "Select the periodicity of the habit:", choices=["daily", "weekly"]).ask()

        # Create habit and corresponding task
        created_habit = self.habit_manager.create_habit(name, periodicity)
        end_of_day = datetime.combine(datetime.now().date(), time.max)
        new_task = self.task_manager.create_task(created_habit.id)
        new_task.expected_completion_by = end_of_day
        self.storage_component.save_task(new_task)

    def update_habit(self):
        habits = self.habit_manager.habits
        if not habits:
            print("No habits available to update.")
            return

        habit_choices = [
            f"ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}" for habit in habits]
        selected_habit = questionary.select(
            "Select the habit to update:", choices=habit_choices, use_arrow_keys=True).ask()
        selected_index = habit_choices.index(selected_habit)
        habit_id = habits[selected_index].id

        attribute = questionary.select("Select the attribute to update:", choices=[
                                       "name"]).ask()
        value = questionary.text(f"Enter the new value for {attribute}:").ask()

        self.habit_manager.update_habit(habit_id, **{attribute: value})

    def delete_habit(self):
        habits = self.habit_manager.habits
        if not habits:
            print("No habits available to delete.")
            return

        habit_choices = [
            f"ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}" for habit in habits]
        selected_habit = questionary.select(
            "Select the habit to delete:", choices=habit_choices, use_arrow_keys=True).ask()
        selected_index = habit_choices.index(selected_habit)
        habit_id = habits[selected_index].id

        self.habit_manager.delete_habit(habit_id)

    def load_habits(self):
        habits = self.habit_manager.habits
        if habits:
            for habit in habits:
                print(f"ID: {habit.id}, Name: {habit.name}, Periodicity: {habit.periodicity}, Current Streak: {habit.current_streak}, Longest Streak: {habit.longest_streak}, Next Completion Date: {habit.next_completion_date}")
        else:
            print("No habits found.")

    def run(self):
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Create a new habit",
                    "Update an existing habit",
                    "Delete a habit",
                    "Load all habits",
                    "Exit"
                ]
            ).ask()

            if action == "Create a new habit":
                self.create_habit()
                print("Habit successfully created😊!")
            elif action == "Update an existing habit":
                self.update_habit()
                print("Habit successfully updated😊!")
            elif action == "Delete a habit":
                self.delete_habit()
            elif action == "Load all habits":
                self.load_habits()
            elif action == "Exit":
                self.storage_component.close()
                exit()


if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()
