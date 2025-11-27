import speech_recognition as sr
import tempfile

def transcribe_audio_file(audio_file):
    """Convert uploaded audio file to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()

    # Save uploaded audio temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    # Convert to text
    with sr.AudioFile(temp_path) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Audio could not be understood."
    except sr.RequestError:
        return "Speech recognition service unavailable."
