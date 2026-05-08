#print("RUNNING FILE: main.py ACTIVE VERSION")
import os
from dotenv import load_dotenv

# Load .env properly
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("OPENAI_API_KEY")

print("DEBUG KEY:", api_key)  # should show sk-...


import openai

openai.api_key = api_key


from prompts import (
    STORY_PLANNER_PROMPT,
    STORY_WRITER_PROMPT,
    JUDGE_PROMPT,
    REFINER_PROMPT
)

"""
If I had 2 more hours, I would add:
- interactive user feedback loops
- story personalization by age group
- memory across multiple stories
- visual story generation support
- automated evaluation metrics for story quality
"""


def call_model(prompt: str, max_tokens=1000, temperature=0.7):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message["content"]


def generate_story_plan(user_input):
    prompt = f"""
    {STORY_PLANNER_PROMPT}

    USER REQUEST:
    {user_input}
    """
    return call_model(prompt)


def generate_story(story_plan):
    prompt = f"""
    {STORY_WRITER_PROMPT}

    STORY PLAN:
    {story_plan}
    """
    return call_model(prompt)


def judge_story(story):
    prompt = f"""
    {JUDGE_PROMPT}

    STORY:
    {story}
    """
    return call_model(prompt)


def refine_story(story, feedback):
    prompt = f"""
    {REFINER_PROMPT}

    ORIGINAL STORY:
    {story}

    JUDGE FEEDBACK:
    {feedback}
    """
    return call_model(prompt)


def main():
    user_input = input("What kind of bedtime story you want to hear? ")

    print("\nCreating story plan...\n")
    story_plan = generate_story_plan(user_input)
    print(story_plan)

    print("\nWriting story...\n")
    first_story = generate_story(story_plan)
    print(first_story)

    print("\nEvaluating story quality...\n")
    feedback = judge_story(first_story)
    print(feedback)

    print("\nImproving story...\n")
    final_story = refine_story(first_story, feedback)

    print("\nFINAL STORY:\n")
    print(final_story)


if __name__ == "__main__":
    main()