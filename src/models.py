from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

# Define the base for declarative models
Base = declarative_base()


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    periodicity = Column(String)
    current_streak = Column(Integer)
    longest_streak = Column(Integer)
    next_completion_date = Column(DateTime)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # One-to-Many relationship with Task
    tasks = relationship('Task', back_populates='habits')

# Task model


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    completed = Column(Boolean)
    completed_on = Column(DateTime)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Many-to-One relationship with Habit
    habit = relationship('Habit', back_populates='tasks')
