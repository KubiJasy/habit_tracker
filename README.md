# Habit Tracker App

This is a cross-platform habit tracker and task manager application written in Python. It allows users to manage their daily habits and tasks, track progress, and analyze performance using a command-line interface (CLI). The application is built using Python's Object-Oriented and Functional Programming paradigms and leverages SQLAlchemy for database management.

## Features
- Track habits and tasks
- Analyze habit and task performance with built-in analytics
- Cross-platform support (Windows, macOS, Linux)
- Command-line interface (CLI) for user interaction

## Project Structure
- **Questionary CLI**: Command-line interface for user input and interaction
- **HabitManager & TaskManager**: Manage habit and task entities
- **SQLAlchemy**: ORM for database management
- **pytest**: Unit testing framework

---

## Setup Instructions

### 1. Clone the repository

Start by cloning the repository from GitHub (replace with the actual link):
```bash
git clone https://github.com/yourusername/habit_tracker.git
cd habit_tracker
```

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

#### On Windows:
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   .\venv\Scripts\activate
   ```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Run the Application

After setting up the virtual environment and installing dependencies, you can start the application:

```bash
python habit_tracker/cli.py
```

### 5. Deactivate the Virtual Environment (optional)

When you're done working in the virtual environment, deactivate it:
```bash
deactivate
```

---

## Running Tests

This project uses `pytest` for testing. To run the tests, use the following command:

```bash
pytest
```

---

## Contributing

Feel free to fork this repository and make contributions. When contributing, ensure that:
1. Code is tested thoroughly.
2. New features include documentation and tests.
3. You follow Python best practices (e.g., PEP 8).

---

## License

This project is licensed under the MIT License.

---

## Troubleshooting

If you encounter any issues during setup or installation, ensure:
- You are using the correct Python version (preferably Python 3.10 or later).
- The virtual environment is activated properly.
- All dependencies in `requirements.txt` are installed without errors.

For further help, raise an issue in the repository.

---

This README gives a good starting point for setting up and running your application across different operating systems. You can expand on the documentation as your project evolves.