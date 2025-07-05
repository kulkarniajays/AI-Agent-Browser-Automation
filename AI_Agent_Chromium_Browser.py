import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime, time
import sys
from jinja2 import Template
import mss

load_dotenv()

# Initialize the report list to store the data for each step
report_data = []

# Function to generate the HTML report using the external template
def generate_html_report(report_data, template_file, output_file):
    try:
        # Verify that the template file exists
        if not os.path.exists(template_file):
            print(f"Error: Template file '{template_file}' not found.")
            return

        # Verify that report data is not empty
        if not report_data:
            print("Warning: No data to write in HTML report.")
            return

        # Load the HTML template from the external file
        with open(template_file, 'r', encoding='utf-8') as f:
            html_template = f.read()

        # Create a template from the loaded string
        template = Template(html_template)

        # Generate the HTML content using the provided data
        html_content = template.render(test_results=report_data)

        # Save the generated HTML report to the specified file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ HTML report successfully generated: {output_file}")

    except Exception as e:
        print(f"❌ Error generating HTML report: {str(e)}")

# Before calling `generate_html_report`, ensure that `report_data` is being populated correctly.

# Function to log the console output to a text file
class LogToFile:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def write(self, message):
        with open(self.log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(message)

    def flush(self):
        pass  # No need to flush, as we are appending messages

# Function to replace sys.stdout with the LogToFile class
def setup_logging():
    # Create the 'log' folder if it doesn't exist
    log_folder = 'log'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Generate log file name based on current date and time
    log_file_name = f"log/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    # Redirects print statements to the log file
    sys.stdout = LogToFile(log_file_name)  # Log to file

    # Optional: Also print logs to console
    sys.stderr = sys.stdout  # To capture error logs as well

    print(f"Logging started. Output will be saved to {log_file_name}.")

# Function to take a screenshot and save it with a specific name
def take_screenshot(step_number, scroll_count, excel_name):
    screenshot_folder = 'screenshots'

    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

    # Create a formatted screenshot file name
    replace_dot_with_underscore = os.path.splitext(excel_name)[0].replace('.', '_')  # Replace dot with underscore
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{screenshot_folder}/{replace_dot_with_underscore}_Step_{step_number}_{scroll_count}_{current_datetime}.PNG"

    # Capture screenshot using mss
    with mss.mss() as mss_instance:
         mss_instance.shot(output=file_name)

    print(f"Screenshot saved as {file_name}")
    return file_name

# Function to execute tasks from the Excel sheet
async def execute_tasks_from_excel(task_steps, task_numbers, excel_name, df):
    global report_data
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key is None:
        print("API key is missing. Please check your .env file.")
        return

    # Initialize the LLM model for Google Generative AI
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=api_key)

    # Initialize the agent with the tasks and the use of vision (if required)
    agent = Agent(task_steps, llm, use_vision=True)

    try:
        history = await agent.run()
    except Exception as e:
        print(f"Error during agent run: {str(e)}")
        return

    print(f"Processing {len(task_steps)} steps...")

    # Process the results for each step
    for step_number, task in zip(task_numbers, task_steps):
        # Capture expected outcome from the Excel file (Expected_Outcome column)
        expected_outcome = df.loc[step_number, 'Expected_Outcome'] if 'Expected_Outcome' in df.columns else "Not Applicable"

        print(f"Expected outcome for step {step_number + 1}: {expected_outcome}")

        eval_output = history.final_result() or "No output"

        # Check if eval_output is a list. If it is, join the list into a single string.
        if isinstance(eval_output, list):
            eval_output = ' '.join(eval_output)  # Join list into a single string

        print(f"Eval output for step {step_number + 1}: {eval_output}")

        # Determine result based on eval_output
        result = "Failed" if "Success" in eval_output or "completed successfully" in eval_output else "Passed"

        # Capture the screenshot for this step
        screenshot_path = take_screenshot(step_number + 1, 1, excel_name)

        # Add this information to the report_data
        report_data.append({
            'step_no': step_number + 1,  # Adjusting to start step number from 1
            'description': task,
            'expected_result': expected_outcome,
            'screenshot': screenshot_path,
            'result': result
        })

    # After processing all steps, check if any step was marked as "Failed"
    print("Finalizing results...")
    for report in report_data:
        if report['result'] != "Passed":
            report['result'] = "Failed"
        else:
            report['result'] = "Passed"

# Validation function to process all Excel files and generate reports
async def validation():
    folder_path = 'E:\\Users\\kulka\\PycharmProjects\\AI_Agent_Browser_Use\\Testcases\\'  # Change this to the actual folder path

    # List all Excel files in the folder
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

    if not excel_files:
        print("No Excel files found in the folder.")
        return

    # Create the 'report' folder if it doesn't exist
    report_folder = 'report'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # Process each Excel file one by one
    for excel_file in excel_files:
        file_path = os.path.join(folder_path, excel_file)
        print(f"Processing file: {file_path}")

        # Reset report_data for each new file
        report_data.clear()

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Assuming the task descriptions are in a column named 'step_description'
        if 'step_description' not in df.columns:
            print(f"step_description column not found in {file_path}. Skipping file.")
            continue

        # Extract all task steps from the Excel file into a list and capture step numbers
        task_steps = df['step_description'].tolist()
        task_numbers = df.index.tolist()  # Use index as step numbers
        print(f"Loaded {len(task_steps)} steps from {file_path}.")

        # Execute all steps for the current Excel file
        print(f"Executing tasks from file: {file_path}")
        await execute_tasks_from_excel(task_steps, task_numbers, excel_file, df)

        # Generate the unique HTML report file name using the Excel file name and current date and time
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file_name = os.path.join(report_folder,
                                        f"{os.path.splitext(excel_file)[0]}_Automation_Report_{current_datetime}.html")

        # Path to the HTML template file
        template_file = 'E:\\Users\\kulka\\PycharmProjects\\AI_Agent_Browser_Use\\Report_Template\\report_template.html'  # Path to the template file

        # After processing the current Excel file, generate the HTML report
        generate_html_report(report_data, template_file, report_file_name)

# Run the validation asynchronously using asyncio
setup_logging()  # Set up logging before running the validation
asyncio.run(validation())
