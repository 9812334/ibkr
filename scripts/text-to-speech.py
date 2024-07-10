import pyttsx3

# Create a Text-to-Speech engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Set the text to read out
text = "Hello, how are you?"

# Read out the text
engine.say(text)

# Wait for the text to be read out
engine.runAndWait()