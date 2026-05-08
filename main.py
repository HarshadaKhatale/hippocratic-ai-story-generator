#print("RUNNING FILE: main.py ACTIVE VERSION")
import os
from unicodedata import category
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
    REFINER_PROMPT,
    USER_FEEDBACK_PROMPT
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


def generate_story(story_plan, strategy):
    prompt = f"""
    {STORY_WRITER_PROMPT}

    STORY STRATEGY:
    {strategy}

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

def apply_user_feedback(story, user_feedback):

    prompt = f"""
    {USER_FEEDBACK_PROMPT}

    ORIGINAL STORY:
    {story}

    USER FEEDBACK:
    {user_feedback}
    """

    return call_model(prompt)

def categorize_request(user_input):

    categories = {
        "fantasy": ["dragon", "magic", "wizard", "castle"],
        "animal": ["cat", "dog", "rabbit", "lion"],
        "adventure": ["adventure", "treasure", "explore"],
        "space": ["space", "planet", "rocket", "alien"],
        "educational": ["learn", "school", "science"]
    }

    user_input_lower = user_input.lower()

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in user_input_lower:
                return category

    return "general"

def get_category_strategy(category):

    strategies = {

        "fantasy":
        "Use magical settings, whimsical characters, and imaginative storytelling.",

        "animal":
        "Focus on emotional warmth, friendship, and playful animal behavior.",

        "adventure":
        "Include exploration, teamwork, and exciting but child-safe challenges.",

        "space":
        "Use wonder, curiosity, and fun space exploration themes.",

        "educational":
        "Include gentle educational lessons and curiosity-driven learning.",

        "general":
        "Create a balanced, comforting bedtime story."
    }

    return strategies[category]


def main():
    user_input = input("What kind of bedtime story you want to hear? ")

    category = categorize_request(user_input)
    strategy = get_category_strategy(category)
    print(f"\nDetected category: {category}\n")

    print("\nCreating story plan...\n")
    story_plan = generate_story_plan(user_input)
    print(story_plan)

    print("\nWriting story...\n")
    first_story = generate_story(story_plan, strategy)
    print(first_story)

    print("\nEvaluating story quality...\n")
    feedback = judge_story(first_story)
    print(feedback)

    print("\nImproving story...\n")
    final_story = refine_story(first_story, feedback)

    print("\nFINAL STORY:\n")
    
    print(final_story)
    
    while True:

        user_choice = input("\nDid you enjoy the story? (yes/no): " )

        if user_choice.lower() == "yes":

            print(
                "\nI'm so happy you enjoyed the story! "
                "Sweet dreams! 🌙✨" )

            break

        elif user_choice.lower() == "no":

            feedback = input(
                "\nWhat would you like to change in the story? "
                "\nYou can ask for:\n"
                "- more adventure\n"
                "- funnier characters\n"
                "- more magic\n"
                "- shorter story\n"
                "- new animals\n"
                "\nTell me your idea: "
            )

            print("\nUpdating your story...\n")

            final_story = apply_user_feedback(
                final_story,
                feedback
            )

            print("\nUPDATED STORY:\n")

            print(final_story)

        else:

            print(
                "\nPlease type 'yes' or 'no'."
            )


if __name__ == "__main__":
    main()