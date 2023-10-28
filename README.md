```markdown
# Candle Processing Project

This Django-based project allows you to upload a CSV file containing financial data and process it into candlestick charts.

## Getting Started

Follow these steps to set up and run the project.

### Prerequisites

- Python 3.11.1
- Django
- Visual Studio Code (optional)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ANGADJIT/Trading-Project.git
   cd Trading-Project
   ```

2. Install project dependencies:

   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

3. Run the migrations to create the database:

   ```bash
   python manage.py migrate
   ```

### Usage

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Access the application in your web browser at `http://localhost:8000/mainapp`.

3. Upload a CSV file with financial data, specify the timeframe, and process the data into candlestick charts.

### Configuration for Visual Studio Code

The project is pre-configured for running in Visual Studio Code. To start the project using the F5 key:

1. Open the project in Visual Studio Code.

2. Install the Python extension if not already installed.

3. Create a `launch.json` file in the `.vscode` folder. Add the following configuration:

   ```json
   {
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}\\TradingProject\\manage.py",
            "args": [
                "runserver"
            ],
            "django": true,
            "console": "internalConsole",
            "justMyCode": true
        }
    ]
    }
   ```

4. Save the `launch.json` file.

5. Now, you can start the project with F5.
