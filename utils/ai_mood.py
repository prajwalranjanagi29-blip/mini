import openai
import os

# Set your OpenAI API key as environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_mood_analysis(user_text):
    """
    Generate AI explanation / solution for user's mood paragraph.
    """
    try:
        prompt = f"User wrote about their mood: '{user_text}'. Analyze and provide a short, helpful, empathetic insight."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"AI analysis not available: {e}"
