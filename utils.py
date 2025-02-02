import logging
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

# from transformers import pipeline
# import text2emotion as te
nltk.download("punkt_tab")
nltk.download("vader_lexicon")
from nltk.sentiment import SentimentIntensityAnalyzer

# Setup logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_info(message):
    logging.info(message)
    print(message)  # Also print for real-time feedback


def log_error(message):
    logging.error(message)
    print(f"ERROR: {message}")


# Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Initialize the transformer sentiment pipeline once.
# You may choose a different model if desired.
# sentiment_pipeline = pipeline(
#     "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
# )


# def analyze_sentiment(text):
#     """
#     Analyze sentiment using multiple methods:
#       - VADER: Provides a dictionary of lexicon-based scores (neg, neu, pos, compound).
#       - Transformer: Uses a Hugging Face model to return a sentiment label (e.g. POSITIVE/NEGATIVE) and a confidence score.
#       - Text2Emotion: Returns scores for multiple emotions (e.g., Happy, Angry, Surprise, Sad, Fear).

#     Returns:
#         dict: A dictionary containing results from each method.
#     """
#     # VADER analysis
#     vader_scores = sia.polarity_scores(text)

#     # Transformer-based sentiment analysis (returns a list; we take the first result)
#     transformer_result = sentiment_pipeline(text)[0]

#     # Emotion detection
#     emotion_scores = te.get_emotion(text)

#     return {
#         "vader": vader_scores,
#         "transformer": transformer_result,
#         "emotions": emotion_scores,
#     }


def analyze_sentiment(text):
    """
    Analyze sentiment using multiple methods.
    In this example we only use VADER, but you can combine
    transformer- and emotion-based scores for a richer view.
    Returns a dict with at least a "vader" key.
    """
    vader_scores = sia.polarity_scores(text)
    # In a complete version, you might also call a Hugging Face pipeline
    # or text2emotion here.
    return {"vader": vader_scores}


def compute_grade_for_response(sentiment_json_str, expected_tone):
    """
    Given a JSON string of sentiment scores and an expected tone, compute a grade (0-100).

    For tone:
      - "positive": expected compound ≈ +0.5
      - "neutral": expected compound ≈ 0.0
      - "negative": expected compound ≈ -0.5

    The grade is computed as:
        grade = max(0, 100 - (abs(compound - expected_compound) * 100))
    """
    # Parse the sentiment scores from JSON string
    try:
        sentiment = json.loads(sentiment_json_str)
    except json.JSONDecodeError:
        # If parsing fails, return zero grade
        return 0

    compound = sentiment.get("compound", 0)

    tone = expected_tone.lower()
    if tone == "positive":
        expected_compound = 0.5
    elif tone == "negative":
        expected_compound = -0.5
    else:  # neutral (or any other)
        expected_compound = 0.0

    diff = abs(compound - expected_compound)
    # Convert difference to a grade: if diff==0 -> 100; if diff==1 -> 0.
    grade = max(0, 100 - (diff * 100))
    return grade


def grade_llm_responses(csv_path):
    """
    Reads the LLM responses CSV, computes a grade for each response based on its tone,
    and outputs a new CSV with a "grade" column. It also prints average grades per tone.
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Compute a grade for each row using the "chatgpt_sentiment" column and the "tone" column.
    df["grade"] = df.apply(
        lambda row: compute_grade_for_response(row["chatgpt_sentiment"], row["tone"]),
        axis=1,
    )

    # Compute overall (average) grade per tone.
    overall_grades = df.groupby("tone")["grade"].mean().to_dict()

    # Optionally, write the graded results to a new CSV.
    df.to_csv("graded_llm_responses.csv", index=False)

    return overall_grades


def assess_quality(text):
    """
    Compute a composite quality score for an LLM response.

    The composite score is the average of:
      - Readability: Measured by the Flesch Reading Ease score (typically 0-100; higher is easier to read)
      - Lexical Diversity: The ratio of unique words to total words (normalized to a 0-100 scale)

    Returns:
        quality_score (float): Composite quality score (0-100)
    """
    # Compute readability (if textstat fails, set to 0)
    try:
        readability = textstat.flesch_reading_ease(text)
    except Exception:
        readability = 0

    # Tokenize text to compute lexical diversity
    words = word_tokenize(text)
    if len(words) > 0:
        diversity = (len(set(words)) / len(words)) * 100  # Normalize to 0-100 scale
    else:
        diversity = 0

    # Composite quality score: simple average of readability and lexical diversity
    quality_score = (readability + diversity) / 2
    return quality_score


def grade_quality(csv_file):
    """
    Reads the LLM responses CSV (with at least columns:
    - 'tone'
    - 'chatgpt_response')

    Computes a quality score for each response using assess_quality(),
    then aggregates mean and standard deviation of quality per tone.

    Returns:
        quality_stats (dict): Dictionary mapping each tone to a dict of mean and std quality.
        df (DataFrame): DataFrame with an added "quality" column.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Compute quality score for each ChatGPT response
    df["quality"] = df["chatgpt_response"].apply(assess_quality)

    # Group by tone and compute mean and standard deviation
    grouped = df.groupby("tone")["quality"].agg(["mean", "std"])
    quality_stats = grouped.to_dict("index")

    # Optionally, save the graded results to a new CSV file
    df.to_csv("graded_quality_responses.csv", index=False)

    return quality_stats, df


if __name__ == "__main__":
    # Run the grading on your results CSV
    csv_file = "results/llm_responses_results.csv"
    quality_stats, df = grade_quality(csv_file)

    print("Quality Statistics by Tone:")
    for tone, stats in quality_stats.items():
        print(
            f"{tone.capitalize()}: Mean Quality = {stats['mean']:.2f}, Std Dev = {stats['std']:.2f}"
        )
