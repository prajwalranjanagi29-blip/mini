import openai

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
openai.api_key = "YOUR_API_KEY_HERE"

def get_mood_explanation(text):
    """Return AI-based explanation of mood."""
    try:
        prompt = f"Explain the following mood text in 1-2 sentences: '{text}'"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Could not generate explanation: {e}"
