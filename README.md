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

Start by cloning the repository from GitHub:
```bash
git clone https://github.com/KubiJasy/habit_tracker.git
cd habit_tracker
```

### 2. Environment Variable Configuration

1. Create a `.env` file in the root directory of the project
2. Use the provided `.env-sample` file as a reference
3. Set the `LOAD_DATA` variable:
   - `LOAD_DATA=True` - Generates sample data for the application
   - `LOAD_DATA=False` - Starts the application with existing data
4. This environment variable needs to be set to ensure that predefined data is loaded for a new instance of the app or any existing data is used

### 3. Create and Activate a Virtual Environment

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
   
   Command Prompt:
   ```bash
   .\venv\Scripts\activate
   ```
   
   PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

### 4. Install Dependencies

Once the virtual environment is activated, install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### 5. Run the Application

After setting up the virtual environment and installing dependencies, you can start the application:

```bash
python main.py
```

### 6. Deactivate the Virtual Environment (optional)

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

## Troubleshooting

If you encounter any issues during setup or installation, ensure:
- You are using the correct Python version (preferably Python 3.10 or later).
- The virtual environment is activated properly.
- All dependencies in `requirements.txt` are installed without errors.
- The `.env` file is properly configured with the correct `LOAD_DATA` value.
- If using PowerShell and encountering execution policy errors, you may need to run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

For further help, raise an issue in the repository.

---