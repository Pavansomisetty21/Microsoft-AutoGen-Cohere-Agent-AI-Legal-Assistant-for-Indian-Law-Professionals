import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Retrieve API key securely from environment variables
api_key = "api key"

if not api_key:
    raise ValueError("API key is missing. Set it as an environment variable 'COHERE_API_KEY'.")

MAX_USER_REPLIES = 2
statement=input("enter the statement") # here we enter what is the statement of case in detail
INPUT_START_MESSAGE = """
 You are an AI-powered Legal Assistant specializing in Indian law. Your task is to provide legal insights, case law analysis, predictive case outcomes, and AI-driven legal assistance for lawyers, judges, and citizens in India.
"""

# Define the model configuration
config_list_COHERE = [
    {
        "model": "command-a-03-2025",
        "api_key": api_key,
        "api_type": "cohere"
    }
]

# Initialize the assistant agent with the Gemini model configuration
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,
        "config_list": config_list_COHERE,
        "seed": 42
    },
)

# Initialize the user proxy agent
try:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=MAX_USER_REPLIES,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "JUSTICE",
            "use_docker": False
        },
    )
except Exception as e:
    print(f"Error initializing user proxy agent: {str(e)}")
    exit()

# Start the chat between the user proxy and the assistant agent
try:
    chat_response = user_proxy.initiate_chat(
        assistant,
        message=INPUT_START_MESSAGE,
    )

    chat_id = chat_response.chat_id
    convs = chat_response.chat_history
    

    print(f"CHAT REF: {chat_id}")
    

    for conv in convs:
        content = conv.get('content', '')
        active_role = conv.get('role', '')

        print(f"{active_role}: {content}")

    print("COMPLETE")

except Exception as e:
    print(f"Error during chat execution: {str(e)}")
