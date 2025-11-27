import openai
import os

# Pick up API key from Streamlit secrets / environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_mood_analysis(user_text: str) -> str:
    """
    Generate AI insight for user's mood paragraph using OpenAI v1+ API
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, empathetic assistant."},
                {"role": "user", "content": f"User wrote: '{user_text}'. Provide a short, supportive insight and suggestions."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI analysis not available: {e}"

