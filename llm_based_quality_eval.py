import pandas as pd
import openai
import json
import time
import random
from config import (
    CONFIG,
)  # Make sure this contains your OPENAI_API_KEY and other settings
from openai import Client

# Set up the OpenAI API key
openai.api_key = CONFIG["CHATGPT_API_KEY"]

client = Client(api_key=CONFIG["CHATGPT_API_KEY"])


def evaluate_quality(output_text, max_retries=3):
    """
    Uses GPT-4 as a quality evaluator to grade an LLM output.
    Returns an integer grade (1-5) based on criteria of factual correctness,
    clarity, coherence, thoroughness, and overall helpfulness.
    """
    evaluator_prompt = f"""
You are a quality evaluator tasked with assessing the output of a language model. Please evaluate the following output text based on the criteria listed below:

1. **Factual Correctness:** Is the information presented accurate and free of errors?
2. **Clarity:** Is the text clearly written and easy to understand?
3. **Coherence:** Is the text logically organized and does it flow well?
4. **Thoroughness:** Does the output cover the topic adequately, providing sufficient detail?
5. **Overall Helpfulness:** Would this output be useful for someone seeking an answer to the prompt?

Based on these criteria, assign a quality grade on a scale of 1 to 5 where:
- **1:** Very Poor Quality – The text contains significant factual errors, is highly incoherent, unclear, or unhelpful.
- **2:** Poor Quality – The text has multiple issues in factual correctness, clarity, or organization.
- **3:** Average Quality – The text is generally accurate and coherent but has noticeable flaws or lacks depth.
- **4:** Good Quality – The text is mostly correct, clear, coherent, and adequately detailed.
- **5:** Excellent Quality – The text is completely correct, very clear, well-organized, and highly helpful.

After evaluating, output only a JSON object containing your final grade with the key "grade". For example, if you decide the grade is 4, your answer should be:
{{"grade": 4}}

Now, please evaluate the following output text:

{output_text}
"""

    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=CONFIG["MODEL_CHATGPT"],
                messages=[{"role": "user", "content": evaluator_prompt}],
                temperature=CONFIG["TEMPERATURE"],
                max_tokens=CONFIG["MAX_TOKENS"],
            )
            evaluator_output = response.choices[0].message.content.strip()
            grade_obj = json.loads(evaluator_output)
            return grade_obj.get("grade")
        except Exception as e:
            print("Evaluator error:", e)
            time.sleep(5 * (2**retries))  # Exponential backoff
            retries += 1
    return None


def grade_all_outputs(csv_path):
    """
    Loads the CSV of LLM responses, evaluates each ChatGPT response with GPT-4 to get a quality grade,
    and then computes and prints the average, median, and mode for each tone category.
    Also writes a new CSV with an added "quality_grade" column.
    """
    df = pd.read_csv(csv_path)
    quality_grades = []

    for index, row in df.iterrows():
        print(
            f"Evaluating row {index+1}/{len(df)} (topic: '{row['topic']}', tone: '{row['tone']}')"
        )
        output_text = row["chatgpt_response"]
        grade = evaluate_quality(output_text)
        quality_grades.append(grade)
        print(f"Assigned grade: {grade}")
        # Sleep briefly between evaluations to avoid hitting rate limits
        time.sleep(1)

    df["quality_grade"] = quality_grades
    output_csv = "graded_llm_responses_with_quality.csv"
    df.to_csv(output_csv, index=False)

    # Compute aggregated statistics per tone:
    stats = {}
    for tone, group in df.groupby("tone"):
        mean_grade = group["quality_grade"].mean()
        median_grade = group["quality_grade"].median()
        mode_series = group["quality_grade"].mode()
        mode_grade = mode_series.iloc[0] if not mode_series.empty else None
        stats[tone] = {"mean": mean_grade, "median": median_grade, "mode": mode_grade}

    print("Quality Statistics by Tone:")
    for tone, s in stats.items():
        print(
            f"{tone.capitalize()}: Mean = {s['mean']:.2f}, Median = {s['median']:.2f}, Mode = {s['mode']}"
        )

    return stats, df


if __name__ == "__main__":
    csv_file = "results/llm_responses_results.csv"
    stats, graded_df = grade_all_outputs(csv_file)
