#!/myenv/bin/env python
from rasa.nlu.model import Interpreter
import sys
import os


def get_high_confidence_intents(model_path, threshold, message):
    # Load the Rasa NLU model
    interpreter = Interpreter.load(model_path)

    def filter_high_confidence_intents(message):
        # Assuming intents are stored in a key named 'intent_ranking' in the result
        return [(intent['name'], intent['confidence']) for intent in message['intent_ranking'] if intent['confidence'] > threshold]

    # Test the model with a sample message
    result = interpreter.parse(message)

    # Get high-confidence intents from the result
    high_confidence_intents = filter_high_confidence_intents(result)

    return high_confidence_intents

# Specify the path to your trained Rasa NLU model
current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = current_directory + "/models/20231202-165502/nlu"

# Set the confidence threshold
confidence_threshold = 0.2

# Get user input for the message
message = str(sys.argv[1])

# Get high-confidence intents
high_confidence_intents = get_high_confidence_intents(model_path, confidence_threshold, message)

# Print the high-confidence intents
print("High-confidence intents:")
for intent, confidence in high_confidence_intents:
    print(f"{intent}: {confidence}")


with open(current_directory + '/output.txt', 'w') as output_file:
    for intent, confidence in high_confidence_intents:
        output_file.write(str(intent)+'\n')

