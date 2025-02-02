# import os
# import time
# import json
# import requests
# import pandas as pd
# import openai
# from nltk.sentiment import SentimentIntensityAnalyzer
# from prompts import get_prompt, PROMPTS, PromptType  # Use our structured prompt repo

# # Initialize VADER sentiment analyzer.
# sia = SentimentIntensityAnalyzer()

# def query_chatgpt(prompt, api_key, model="gpt-4", temperature=0.7, max_tokens=500):
#     openai.api_key = api_key
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=temperature,
#         max_tokens=max_tokens
#     )
#     return response.choices[0].message.content.strip()

# def query_claude(prompt, api_key, model="claude-v3.5", temperature=0.7, max_tokens=500):
#     url = "https://api.anthropic.com/v1/complete"  # Replace with actual endpoint if needed.
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }
#     payload = {
#         "prompt": prompt,
#         "model": model,
#         "max_tokens_to_sample": max_tokens,
#         "temperature": temperature
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     data = response.json()
#     return data.get("completion", "").strip()

# def analyze_sentiment(text):
#     return sia.polarity_scores(text)

# def main():
#     # Retrieve API keys from environment variables.
#     chatgpt_api_key = os.getenv("CHATGPT_API_KEY")
#     claude_api_key = os.getenv("CLAUDE_API_KEY")

#     results = []

#     # Iterate over all tones and topics from our structured prompt repo
#     for tone_enum, topics in PROMPTS.items():
#         for topic, prompt in topics.items():
#             print(f"Processing {topic} ({tone_enum.value} tone)")

#             try:
#                 chatgpt_response = query_chatgpt(prompt, chatgpt_api_key)
#             except Exception as e:
#                 chatgpt_response = f"Error: {e}"

#             try:
#                 claude_response = query_claude(prompt, claude_api_key)
#             except Exception as e:
#                 claude_response = f"Error: {e}"

#             chatgpt_sentiment = analyze_sentiment(chatgpt_response)
#             claude_sentiment = analyze_sentiment(claude_response)

#             results.append({
#                 "topic": topic,
#                 "tone": tone_enum.value,
#                 "prompt": prompt,
#                 "chatgpt_response": chatgpt_response,
#                 "chatgpt_sentiment": json.dumps(chatgpt_sentiment),
#                 "claude_response": claude_response,
#                 "claude_sentiment": json.dumps(claude_sentiment)
#             })

#             time.sleep(1)  # Brief pause to manage API rate limits

#     # Save results to CSV
#     results_df = pd.DataFrame(results)
#     results_df.to_csv("llm_responses_results.csv", index=False)
#     print("Validation testing complete. Results saved to llm_responses_results.csv")

# if __name__ == "__main__":
#     main()
