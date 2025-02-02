import time
import json
import pandas as pd
from openai import Client
import requests
from prompts import PROMPTS, PromptType
from config import CONFIG
from utils import log_info, log_error, analyze_sentiment
import openai
import time
import random
import anthropic

client = Client(api_key=CONFIG["CHATGPT_API_KEY"])


def query_chatgpt(prompt, max_retries=6):
    """Query ChatGPT using the modern client with retries."""
    retries = 0
    backoff_time = 5  # initial delay in seconds
    while retries < max_retries:
        try:
            # Note: The modern client uses the lowercase "chat" namespace and "completions.create" method.
            response = client.chat.completions.create(
                model=CONFIG["MODEL_CHATGPT"],
                messages=[{"role": "user", "content": prompt}],
                temperature=CONFIG["TEMPERATURE"],
                max_tokens=CONFIG["MAX_TOKENS"],
            )
            # Access the text from the response; the new response object is a Pydantic model.
            return response.choices[0].message.content.strip()
        except client.errors.RateLimitError:
            # Catch rate limit errors and back off
            wait_time = backoff_time
            log_error(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            backoff_time *= 2  # Exponential backoff
            retries += 1
        except Exception as e:
            log_error(f"ChatGPT API error: {e}")
            return f"Error: {e}"
    return "Error: Too many retries, API rate limit still exceeded."


claude_client = anthropic.Anthropic(api_key=CONFIG["ANTHROPIC_API_KEY"])


def query_claude(prompt, max_retries=6):
    """
    Query Claude via Anthropic's Python client with retries and exponential backoff.
    """
    retries = 0
    backoff_time = 5  # starting delay in seconds
    while retries < max_retries:
        try:
            # The new API expects a list of message dicts.
            # Adjust the model parameter if needed; here we use a sample model name.
            message = claude_client.messages.create(
                model=CONFIG["MODEL_CLAUDE"],  # e.g. "claude-3-5-sonnet-20241022"
                max_tokens=CONFIG["MAX_TOKENS"],
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content.strip()
        except Exception as e:
            log_error(f"Claude API error: {e}")
            wait_time = backoff_time + random.uniform(0, 2)
            log_error(f"Retrying Claude in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            backoff_time *= 2
            retries += 1
    return "Error: Too many retries, Claude API request still failing."


def main():
    """Main script execution."""
    results = []

    for tone_enum, topics in PROMPTS.items():
        for topic, prompt in topics.items():
            log_info(f"Processing {topic} ({tone_enum.value} tone)")

            chatgpt_response = query_chatgpt(prompt)
            claude_response = query_claude(prompt)

            chatgpt_sentiment = analyze_sentiment(chatgpt_response)
            claude_sentiment = analyze_sentiment(claude_response)

            results.append(
                {
                    "topic": topic,
                    "tone": tone_enum.value,
                    "prompt": prompt,
                    "chatgpt_response": chatgpt_response,
                    "chatgpt_sentiment": json.dumps(chatgpt_sentiment),
                    "claude_response": claude_response,
                    "claude_sentiment": json.dumps(claude_sentiment),
                }
            )

            time.sleep(1)  # Prevent hitting API rate limits

    df_results = pd.DataFrame(results)
    df_results.to_csv(CONFIG["RESULTS_FILE"], index=False)
    log_info(f"Validation testing complete. Results saved to {CONFIG['RESULTS_FILE']}.")


if __name__ == "__main__":
    main()
