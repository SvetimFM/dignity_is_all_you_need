import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "CHATGPT_API_KEY": os.getenv("CHATGPT_API_KEY"),
    "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY"),
    "MODEL_CHATGPT": "gpt-4o-mini",
    "MODEL_CLAUDE": "claude-v3.5",
    "TEMPERATURE": 0.7,
    "MAX_TOKENS": 500,
    "RESULTS_FILE": "results/llm_responses_results.csv",
    "LOG_FILE": "logs/app.log",
}
