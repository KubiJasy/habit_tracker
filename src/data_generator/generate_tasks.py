import datetime
from datetime import timedelta
import random


def random_time_between(start_time, end_time):
    """Generate a random time between the given start_time and end_time."""
    start_seconds = start_time.hour * 3600 + \
        start_time.minute * 60 + start_time.second
    end_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
    random_seconds = random.randint(start_seconds, end_seconds)
    return datetime.time(
        hour=random_seconds // 3600,
        minute=(random_seconds % 3600) // 60,
        second=random_seconds % 60
    )


def generate_task_data(habit_data):
    tasks = []
    for habit in habit_data:
        habit_id = habit[0]
        periodicity = habit[2]
        current_streak = int(habit[3])  # Convert to integer
        longest_streak = int(habit[4])  # Convert to integer
        next_completion_date = datetime.datetime.strptime(
            habit[5], "%Y-%m-%d %H:%M:%S")
        created_at = datetime.datetime.strptime(habit[6], "%Y-%m-%d %H:%M:%S")

        # Ensure periodicity is valid (excluding monthly)
        if periodicity not in ["daily", "weekly"]:
            continue  # Skip invalid periodicity

        # Set the reference date to be the current datetime set a day back
        reference_date = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)

        # Generate potential completion dates based on periodicity and created_at
        # ! Adjust current time conf when necessary
        # potential_completions = []
        # if periodicity == "daily":
        #     for i in range(((datetime.datetime.now() - timedelta(days=1)) - created_at).days + 1):
        #         potential_completions.append(created_at + timedelta(days=i))
        # elif periodicity == "weekly":
        #     for i in range(((datetime.datetime.now() - timedelta(days=1)) - created_at).days // 7 + 1):
        #         potential_completions.append(
        #             created_at + timedelta(days=i * 7))

        potential_completions = []
        if periodicity == "daily":
            for i in range((reference_date - created_at).days + 1):
                potential_completions.append(created_at + timedelta(days=i))
        elif periodicity == "weekly":
            for i in range((reference_date - created_at).days // 7 + 1):
                potential_completions.append(created_at + timedelta(days=i * 7))

        # Mark the most recent consecutive completions based on current streak
        completed_tasks = []
        for completion_date in reversed(potential_completions):
            if len(completed_tasks) >= current_streak:
                break
            completed_tasks.append(completion_date)

        # Simulate the longest streak by choosing a block of consecutive completions
        def simulate_longest_streak(potential_completions, longest_streak, completed_tasks, current_streak):
            # Ensure there are enough dates to choose a longest streak
            if len(potential_completions) < longest_streak:
                return []  # If not enough dates, return an empty list

            # Exclude the most recent `current_streak` dates if current_streak is 0
            if current_streak == 0:
                # Exclude only the last `current_streak` number of dates from the pool for longest streak
                available_completions = potential_completions[:-(
                    current_streak or 1)]
            else:
                available_completions = potential_completions

            # If longest_streak == current_streak, allow overlap with completed tasks
            if longest_streak == current_streak:
                return completed_tasks

            # Find a valid block of consecutive dates that do not overlap with completed_tasks
            max_start_index = len(available_completions) - longest_streak
            possible_streaks = []

            for start_index in range(max_start_index + 1):
                # Get a block of consecutive dates
                streak = available_completions[start_index:start_index + longest_streak]

                # Check if any of these dates overlap with completed_tasks
                if not any(date in completed_tasks for date in streak):
                    possible_streaks.append(streak)

            # If there are valid non-overlapping streaks, randomly select one
            if possible_streaks:
                return random.choice(possible_streaks)
            else:
                # As fallback, allow the first valid streak in history
                return available_completions[:longest_streak]

        # Simulate the longest streak tasks
        longest_streak_tasks = simulate_longest_streak(
            potential_completions, longest_streak, completed_tasks, current_streak)

        # Create task entries for both current and longest streak
        for i, completion_date in enumerate(potential_completions):
            expected_completion_by = completion_date.replace(
                hour=23, minute=59, second=59)
            completed = completion_date in completed_tasks or completion_date in longest_streak_tasks

            # Generate the 'completed_on' time based on the conditions
            if completed:
                if i == 0:  # If it's the first potential completion date
                    # Random time between created_at time and 23:59:59
                    completed_time = random_time_between(
                        created_at.time(), datetime.time(23, 59, 59))
                else:
                    # Random time between 01:00:00 and 23:59:59
                    completed_time = random_time_between(
                        datetime.time(1, 0, 0), datetime.time(23, 59, 59))

                completed_on = completion_date.replace(
                    hour=completed_time.hour, minute=completed_time.minute, second=completed_time.second)
            else:
                completed_on = None

            # Calculate created_at based on periodicity and task index
            if completion_date == potential_completions[0]:
                task_created_at = created_at
            elif periodicity == "daily":
                task_created_at = completion_date - timedelta(days=1)
            elif periodicity == "weekly":
                task_created_at = completion_date - timedelta(days=7)

            if completed:
                # Set updated_at to the same as completed_on
                task_updated_at = completed_on
            else:
                # Keep updated_at the same as the created_at (or leave it unchanged)
                task_updated_at = task_created_at

            tasks.append({
                "habit_id": habit_id,
                "completed": completed,
                "completed_on": completed_on,
                "expected_completion_by": expected_completion_by,
                "created_at": task_created_at,
                "updated_at": task_updated_at  # Use task_updated_at
            })

        # Add a task for the next completion date (marked as incomplete)
        tasks.append({
            "habit_id": habit_id,
            "completed": False,
            "completed_on": None,
            "expected_completion_by": next_completion_date,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return tasks
