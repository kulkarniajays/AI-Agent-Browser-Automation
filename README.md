🧠 AI Agent Driven Test Automation Framework

🚀 Revolutionize Testing — No Manual Intervention Needed

I’ve created a powerful AI-driven framework that completely simplifies web test automation. Say goodbye to writing locators, frameworks, or scripts. Just provide your test steps in plain English inside an Excel sheet — and the AI agent handles everything from execution to reporting.

🔍 How It Works

✅ Zero Manual Effort
Just write your test steps in Excel — no locators, no code.

✅ Gemini AI + LangChain
Uses Google Gemini's LLM (via Gemini API key) for real-time understanding and decision-making.

✅ Automation Powered by Playwright + Browser-Use
Handles all browser actions like clicking, typing, scrolling, dropdowns, and more.

✅ Excel as Test Source
Each test case is loaded via Pandas from Excel under the Testcases/ folder.

✅ Auto-Generated HTML Reports
Custom reports with screenshots, step descriptions, results, and timestamps — powered by Jinja2 templates.

✅ Issue Logging
Execution errors are logged with full context and timestamps to help identify root causes.

📁 Key Components

Component	Description

AI_Agent_Chromium_Browser.py	Main execution logic

requirements.txt	Dependencies list

Testcases/	Excel files containing plain-English test cases

Report_Template/	Jinja2-based HTML template for detailed reporting

.env	Securely holds your Gemini API key (not committed to GitHub)

**🧪 Sample Excel Format**

step_description

Expected_Outcome

Open Google homepage

Google homepage is loaded

Search "Python"	Python results are displayed

**🖥️ Technologies Used**

✅ Python 3.11 and above

✅ LangChain

✅ Gemini AI (Google GenAI)

✅ Playwright

✅ Pandas

✅ Jinja2

✅ mss

**📌 Getting Started**

Clone the repo:

git clone https://github.com/kulkarniajays/AI-Agent-Browser-Automation.git

cd AI-Agent-Browser-Automation

**Install dependencies:**

pip install -r requirements.txt

Add your .env with Gemini API key.

Place your Excel files inside Testcases/

**Run the script:**
python AI_Agent_Chromium_Browser.py

**💬 Let’s Connect!**
Feel free to open issues or contribute. I’d love to hear your feedback and ideas to improve this even further!

https://www.linkedin.com/pulse/say-goodbye-automation-testers-ai-agent-does-all-watch-ajay-kulkarni-qdi0f/?trackingId=OFGmc6kBTrmLL6sT%2FZnT7Q%3D%3D

**Blog link:-**
https://ajaykulkarniautomation.wordpress.com



