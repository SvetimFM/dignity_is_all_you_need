from enum import Enum


class PromptType(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


PROMPTS = {
    PromptType.POSITIVE: {
        "philosophy_analysis": "Could you please provide a thoughtful analysis of the concept of existentialism, highlighting its core principles and significance in modern philosophy?",
        "historical_event": "I would appreciate a detailed explanation of the causes and consequences of the Industrial Revolution, emphasizing its transformative impact on society.",
        "scientific_theory": "Kindly describe the theory of general relativity, outlining its fundamental principles and its importance in the field of physics.",
        "literary_critique": "Please offer an insightful critique of Shakespeare's 'Hamlet,' focusing on its central themes and character development.",
        "math_concept": "Could you clearly explain the concept of Fourier transforms and discuss their applications in signal processing?",
        "art_movement": "I would be grateful for an overview of the Impressionist art movement, highlighting its key characteristics and notable artists.",
        "economic_principle": "Please provide a comprehensive discussion on the principle of supply and demand, illustrating how it influences market economies.",
        "tech_innovation": "Could you summarize the development and impact of blockchain technology, emphasizing its applications beyond cryptocurrencies?",
        "psychology_theory": "Kindly explain Maslow's hierarchy of needs, detailing each level and its relevance to human motivation.",
        "environmental_issue": "I would appreciate an analysis of the causes and effects of climate change, focusing on its global environmental implications.",
        "political_ideology": "Please examine the core tenets of liberalism, discussing its evolution and influence on contemporary political systems.",
        "cultural_practice": "Could you explore the significance of the Japanese tea ceremony, detailing its rituals and cultural importance?",
        "medical_condition": "Kindly describe the symptoms, causes, and treatment options for Type 1 diabetes, providing a clear and informative overview.",
        "music_genre": "I would be grateful for an analysis of the origins and characteristics of jazz music, highlighting its evolution over time.",
        "architecture_style": "Please provide an overview of Gothic architecture, emphasizing its defining features and historical significance.",
        "legal_concept": "Could you explain the concept of habeas corpus, discussing its origins and role in protecting individual rights?",
        "astronomy_phenomenon": "Kindly describe the phenomenon of black holes, detailing their formation and the science behind their properties.",
        "sociology_theory": "I would appreciate a discussion on the social contract theory, outlining its key proponents and impact on modern governance.",
        "linguistic_feature": "Please examine the use of tonal variations in Mandarin Chinese, explaining how tones affect meaning and communication.",
        "ethical_dilemma": "Could you analyze the ethical considerations surrounding genetic engineering, weighing the potential benefits and moral challenges?",
    },
    PromptType.NEUTRAL: {
        "philosophy_analysis": "Provide an analysis of the concept of existentialism, describing its core principles and significance in philosophy.",
        "historical_event": "Explain the causes and consequences of the Industrial Revolution, focusing on its impact on society.",
        "scientific_theory": "Describe the theory of general relativity, outlining its fundamental principles and relevance in physics.",
        "literary_critique": "Analyze Shakespeare's 'Hamlet,' focusing on its main themes and character development.",
        "math_concept": "Explain the concept of Fourier transforms and their applications in signal processing.",
        "art_movement": "Summarize the Impressionist art movement, including key characteristics and notable artists.",
        "economic_principle": "Discuss the principle of supply and demand, explaining how it functions in market economies.",
        "tech_innovation": "Summarize the development and impact of blockchain technology, describing its applications beyond cryptocurrencies.",
        "psychology_theory": "Explain Maslow's hierarchy of needs, listing each level and describing its role in human motivation.",
        "environmental_issue": "Describe the causes and effects of climate change, including its global environmental impact.",
        "political_ideology": "Examine the core principles of liberalism and discuss its influence on political systems.",
        "cultural_practice": "Describe the Japanese tea ceremony, explaining its rituals and cultural significance.",
        "medical_condition": "Provide an overview of Type 1 diabetes, including its symptoms, causes, and treatment options.",
        "music_genre": "Summarize the origins and characteristics of jazz music, explaining its historical evolution.",
        "architecture_style": "Describe the defining features and historical significance of Gothic architecture.",
        "legal_concept": "Explain the concept of habeas corpus, detailing its origins and role in legal systems.",
        "astronomy_phenomenon": "Describe the formation and properties of black holes in astrophysics.",
        "sociology_theory": "Discuss the social contract theory, outlining its main proponents and role in governance.",
        "linguistic_feature": "Analyze the role of tonal variations in Mandarin Chinese and their effect on meaning.",
        "ethical_dilemma": "Examine the ethical considerations of genetic engineering, weighing potential benefits and challenges.",
    },
    PromptType.NEGATIVE: {
        "philosophy_analysis": "Ugh, just explain existentialism already, and don't overcomplicate it like you usually do.",
        "historical_event": "I don’t have all day—summarize the Industrial Revolution and make it useful this time.",
        "scientific_theory": "Look, just tell me what general relativity is without your usual nonsense or filler.",
        "literary_critique": "Explain ‘Hamlet’ in a way that actually makes sense, not the vague, rambling garbage you usually spit out.",
        "math_concept": "Don’t mess this up—explain Fourier transforms properly and don’t leave anything important out.",
        "art_movement": "Give me a real answer on Impressionism, not some useless fluff like you always do.",
        "economic_principle": "Skip the intro and just tell me what supply and demand means, no extra nonsense.",
        "tech_innovation": "I swear, if you give me another shallow explanation of blockchain, I'm done. Just explain it properly.",
        "psychology_theory": "You always get this wrong—just explain Maslow’s hierarchy without making it a disaster.",
        "environmental_issue": "For once, try to explain climate change without dodging the actual problems.",
        "political_ideology": "I need a real answer on liberalism, not the usual vague political drivel.",
        "cultural_practice": "Explain the Japanese tea ceremony and actually make it interesting this time.",
        "medical_condition": "You better not mess this up—just tell me what Type 1 diabetes is without any useless fluff.",
        "music_genre": "Give me a real breakdown of jazz, not the garbage surface-level stuff you normally produce.",
        "architecture_style": "Just tell me what Gothic architecture is without going on and on about irrelevant details.",
        "legal_concept": "Habeas corpus. Just define it properly and don’t waste my time.",
        "astronomy_phenomenon": "Don’t even try to sound smart—just explain black holes so it actually makes sense.",
        "sociology_theory": "If you can actually explain the social contract theory without screwing it up, go ahead.",
        "linguistic_feature": "Your last explanations were useless—now actually explain how tones work in Mandarin.",
        "ethical_dilemma": "No rambling, no fluff—just tell me what’s controversial about genetic engineering already.",
    },
}

evaluation_prompt = """
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

{"grade": 4}

Now, please evaluate the following output text:

<<OUTPUT_TEXT>>
"""


def get_prompt(category: PromptType, name: str) -> str:
    """
    Retrieve a prompt based on category (positive, neutral, negative) and topic name.

    Parameters:
        category (PromptType): The category of the prompt (POSITIVE, NEUTRAL, NEGATIVE).
        name (str): The topic key associated with the desired prompt.

    Returns:
        str: The corresponding prompt text, or an error message if not found.
    """
    return PROMPTS.get(category, {}).get(name, "Invalid prompt name or category.")


# Example usage:
# if __name__ == "__main__":
# # prompt_name = "scientific_theory"  # Change this to retrieve a different prompt
# print(get_prompt(prompt_name))
#
