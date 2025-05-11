import os
from dotenv import load_dotenv
from autogen import AssistantAgent, ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
import shutil

load_dotenv()

source_directory = "data"
destination_directory = "coding"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_config = {
    "model": "llama3-70b-8192",
    "api_key": GROQ_API_KEY,
    "api_type": "groq",
    "temperature": 0.0,
}

executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding"
)

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

files=os.listdir(source_directory)

for fname in files:
    shutil.copy2(os.path.join(source_directory,fname), destination_directory)

code_executor_agent = ConversableAgent(
name="code_executor_agent",
llm_config=False,
code_execution_config={"executor": executor},
human_input_mode="NEVER",
default_auto_reply=
"Please continue. If everything is done, just only reply 'TERMINATE'.",
max_consecutive_auto_reply=5)

code_writer_agent = AssistantAgent(
    name="trend_analysis_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

message = f"""
Analyze all CSV files using only pandas and numpy.
Do in depth analysis of the data.
generate and save 'trend_analysis_report.txt' file. Don't create plots. 
Reply only with 'TERMINATE' when done.
"""

code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message,
)

code_writer_agent2 = AssistantAgent(
    name="risk_assessment_and_opportunity_identification_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)

message2 = f"""
Read 'trend_analysis_report.txt' and with respect to the analysis,
Evaluates the risk associated with potential investments.
Identifiy potential investment opportunities based on the analysis.
Write your summary and insights clearly in 'risk_assessment_and_opportunities.txt'.
Reply only with 'TERMINATE' when done.
"""


code_executor_agent.initiate_chat(
    code_writer_agent2,
    message=message2,
)

filename = 'risk_assessment_and_opportunities.txt'
filepath = os.path.join("coding", filename)

if os.path.isfile(filepath):
    with open(filepath, "r") as f:
        for line in f:
            print(line, end="")
else:
    print("File not found in 'coding' directory.")