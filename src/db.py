from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, Habit, Task


DATABASE_URL = "sqlite:///habit_tracker.sqlite3"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def initialize_db():
    """
    Initialize the database schema.
    This method should handle creating all necessary tables and setting up the schema.
    """
    Base.metadata.create_all(engine)


class StorageComponent:
    """
    Storage component responsible for managing database interactions.
    """

    def __init__(self):
        self.engine = engine
        self.session = session

    def load_habits(self, name=None, periodicity=None, current_streak=None, longest_streak=None):
        """
        Load habits from the database with optional filters.
        
        :param name: Optional filter by habit name (partial or full match).
        :param periodicity: Optional filter by periodicity (e.g., 'daily', 'weekly').
        :param current_streak: Optional filter by current streak value.
        :param longest_streak: Optional filter by longest streak value.
        :return: A list of filtered habits.
        """
        query = self.session.query(Habit)

        # Apply filters based on provided arguments
        if name:
            query = query.filter(Habit.name.like(f'%{name}%'))  # Partial match for name
        if periodicity:
            query = query.filter(Habit.periodicity == periodicity)
        if current_streak is not None:
            query = query.filter(Habit.current_streak == current_streak)
        if longest_streak is not None:
            query = query.filter(Habit.longest_streak == longest_streak)

        return query.all()

    def load_tasks(self):
        """
        Load tasks from the database.
        This method will query the database and return all task records.
        """
        return self.session.query(Task).all()

    def load_tasks_for_habit(self, habit_id):
        habit = self.session.query(Habit).filter_by(id=habit_id).first()
        return habit.tasks if habit else None

    def save_habit(self, habit):
        """
        Save or update a habit to the database.
        :param habit: The habit object to be saved or updated.
        """
        existing_habit = self.session.query(Habit).filter_by(
            id=habit.id).first() if hasattr(habit, 'id') else None
        if existing_habit:
            # Update existing habit
            # print("in here updated")
            existing_habit.name = habit.name
            existing_habit.periodicity = habit.periodicity
            existing_habit.current_streak = habit.current_streak
            existing_habit.longest_streak = habit.longest_streak
            existing_habit.next_completion_date = habit.next_completion_date
            existing_habit.updated_at = datetime.now()
            self.session.commit()
            return existing_habit
        else:
            # Create new habit
            # print("in here created")
            new_habit = Habit(
                name=habit.name,
                periodicity=habit.periodicity,
                current_streak=habit.current_streak,
                longest_streak=habit.longest_streak,
                next_completion_date=habit.next_completion_date,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.session.add(new_habit)
            self.session.commit()
            return new_habit

    def save_task(self, task):
        """
        Save or update a task to the database.
        :param task: The task object to be saved or updated.
        """
        existing_task = self.session.query(Task).filter_by(
            id=task.id).first() if hasattr(task, 'id') else None
        if existing_task:
            # Update existing task
            existing_task.habit_id = task.habit_id
            existing_task.completed = task.completed
            existing_task.completed_on = task.completed_on
            existing_task.expected_completion_by = task.expected_completion_by
            existing_task.updated_at = datetime.now()
            self.session.commit()
            return existing_task
        else:
            # Create new task
            new_task = Task(
                habit_id=task.habit_id,
                completed=task.completed,
                completed_on=task.completed_on,
                expected_completion_by=task.expected_completion_by,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.session.add(new_task)
            self.session.commit()
            return new_task

    def close(self):
        """
        Close the database session.
        """
        self.session.close()
