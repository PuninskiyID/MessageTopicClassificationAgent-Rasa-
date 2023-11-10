from rasa.nlu.model import Interpreter
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Set TensorFlow logging to only display errors

# Load the trained model
interpreter = Interpreter.load("F:/Ai/rasa1_8/models/nlu-20231110-211338/nlu")

# Get intent from text
text = "What's the weather like today?"
result = interpreter.parse("What movie can you advice?")

# Print the predicted intent
print("Predicted Intent:", result['intent']['name'])