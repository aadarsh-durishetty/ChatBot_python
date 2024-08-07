import re
import random
import spacy

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Define substitution patterns
substitutions = {
    r"\bI am\b": "you are",
    r"\bI'm\b": "you're",
    r"\bI\b": "you",
    r"\bmy\b": "your",
    r"\bme\b": "you",
    r"\bmine\b": "yours",
    r"\byou are\b": "I am",
    r"\byou're\b": "I'm",
    r"\byour\b": "my",
    r"\byours\b": "mine",
    r"\byou\b": "I",
    r"\bam\b": "are",
    r"\bwas\b": "were",
    r"\bmyself\b": "yourself",
    r"\bwe\b": "you",
    r"\bus\b": "you",
    r"\bour\b": "your",
    r"\bours\b": "yours"
}

# Precompile substitution patterns
substitution_patterns = {re.compile(k): v for k, v in substitutions.items()}

# Define patterns and responses
patterns_responses = [
    (re.compile(r'hello|hi|hey'), ["Hello! How can I help you today?", "Hi there! How can I assist you?", "Hey! How can I be of service today?"]),
    (re.compile(r'good morning|morning'), ["Good morning! How can I help you today?", "Morning! How can I assist you?", "Good morning! What can I do for you today?"]),
    (re.compile(r'good afternoon|afternoon'), ["Good afternoon! How can I help you today?", "Afternoon! How can I assist you?", "Good afternoon! What can I do for you today?"]),
    (re.compile(r'good evening|evening'), ["Good evening! How can I help you today?", "Evening! How can I assist you?", "Good evening! What can I do for you today?"]),
    (re.compile(r'(.*) need (.*)'), ["Why do you need {1}?", "Are you sure you need {1}?", "What makes you need {1}?"]),
    (re.compile(r'(.*) problem (.*)'), ["I'm sorry to hear you have a problem with {1}. Can you provide more details?", "What seems to be the issue with {1}?", "Can you explain the problem with {1} in more detail?"]),
    (re.compile(r'(.*) help (.*)'), ["Sure, I can help with {1}. What exactly do you need assistance with?", "I'm here to help you with {1}. What do you need?", "I'd be happy to assist you with {1}. What do you need help with?"]),
    (re.compile(r'(.*) buy (.*)'), ["Are you looking to buy {1}?", "I can help you with buying {1}. Can you tell me more?", "What are you looking to buy regarding {1}?"]),
    (re.compile(r'(.*) return (.*)'), ["I'm sorry you want to return {1}. Can you tell me the reason?", "Can you provide more details on why you want to return {1}?", "Why do you want to return {1}?"]),
    (re.compile(r'(.*) refund (.*)'), ["Can you tell me why you need a refund for {1}?", "I'm sorry you're requesting a refund for {1}. Can you explain why?", "What is the reason for requesting a refund for {1}?"]),
    (re.compile(r'(.*) exchange (.*)'), ["What do you want to exchange {1} for?", "Can you provide more details on the exchange for {1}?", "Why do you want to exchange {1}?"]),
    (re.compile(r'(.*) order status (.*)'), ["Let me check the status of your order for {1}. Can you provide your order ID?", "I'll need your order ID to check the status of {1}. Can you provide it?", "Checking the status of {1} requires your order ID. Please provide it."]),
    (re.compile(r'(.*) shipping (.*)'), ["Are you inquiring about the shipping status of {1}?", "I can help you with shipping details for {1}. What specifically do you need to know?", "What details about shipping for {1} are you looking for?"]),
    (re.compile(r'(.*) delivery (.*)'), ["Are you asking about the delivery date for {1}?", "I can check the delivery status of {1} for you. Please provide more details.", "When do you expect the delivery of {1}?"]),
    (re.compile(r'(.*) damaged (.*)'), ["I'm sorry to hear that {1} is damaged. Can you provide more details?", "What seems to be the issue with the damaged {1}?", "Can you explain how {1} got damaged?"]),
    (re.compile(r'(.*) warranty (.*)'), ["Are you inquiring about the warranty for {1}?", "I can provide details about the warranty for {1}. What do you need to know?", "What specific information about the warranty for {1} are you looking for?"]),
    (re.compile(r'(.*) support (.*)'), ["How can I support you with {1}?", "I'm here to provide support for {1}. What do you need?", "What kind of support do you need for {1}?"]),
    (re.compile(r'(.*) upgrade (.*)'), ["Are you looking to upgrade {1}?", "I can help you with the upgrade process for {1}. What exactly do you need?", "What are you looking to upgrade regarding {1}?"]),
    (re.compile(r'(.*) discount (.*)'), ["Are you looking for a discount on {1}?", "I can check for discounts on {1}. What is the item?", "Let me see if there are any discounts available for {1}. Can you provide more details?"]),
    (re.compile(r'(.*) coupon (.*)'), ["Do you have a coupon code for {1}?", "I can apply a coupon for {1}. Please provide the code.", "Can you provide the coupon code for {1}?"]),
    (re.compile(r'(.*) complaint (.*)'), ["I'm sorry to hear you have a complaint about {1}. Can you provide more details?", "What is the nature of your complaint regarding {1}?", "Can you explain the issue you have with {1}?"]),
    (re.compile(r'(.*) feedback (.*)'), ["I'd love to hear your feedback about {1}. What do you think?", "Please provide your feedback on {1}.", "What feedback do you have for {1}?"]),
    (re.compile(r'(.*) suggestion (.*)'), ["Do you have any suggestions for {1}?", "I'd appreciate your suggestions for {1}. What are they?", "What suggestions do you have for {1}?"]),
    (re.compile(r'(.*) contact (.*)'), ["You can contact us at our support email or phone number.", "Please reach out to us via our contact page for further assistance.", "You can contact our support team for help with {1}."]),
    (re.compile(r'(.*) hours (.*)'), ["Our operating hours are from 9 AM to 5 PM, Monday to Friday.", "We are open from 9 AM to 5 PM on weekdays.", "Our business hours are 9 AM to 5 PM, Monday through Friday."]),
    (re.compile(r'(.*) location (.*)'), ["We are located at 123 Main Street, Anytown, USA.", "Our office is at 123 Main Street, Anytown, USA.", "You can find us at 123 Main Street, Anytown, USA."]),
    (re.compile(r'(.*) policy (.*)'), ["You can read our policies on our website.", "Our policies are available on the policy page of our website.", "Please check our website for our policies."]),
    (re.compile(r'(.*) pricing (.*)'), ["You can find our pricing details on our website.", "Our pricing information is available on the pricing page of our website.", "Please visit our website to see our pricing details."]),
    (re.compile(r'(.*) membership (.*)'), ["We offer various membership plans. Please visit our website for more details.", "Our membership plans are detailed on our website.", "You can learn more about our membership options on our website."]),
    (re.compile(r'bye|exit|quit'), ["Goodbye! Have a great day!", "See you later! Take care!", "Thank you for chatting with me. Goodbye!"])
]

# Function to apply substitutions
def apply_substitutions(text):
    for pattern, replacement in substitution_patterns.items():
        text = pattern.sub(replacement, text)
    return text

# Function to get response from patterns
def get_response(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)  # Use spaCy to tokenize and preprocess the input
    user_input_processed = " ".join([token.text for token in doc])
    for pattern, responses in patterns_responses:
        match = pattern.match(user_input_processed)
        if match:
            response = random.choice(responses).format(*[apply_substitutions(group) for group in match.groups()])
            return response
    return "I'm not sure how to respond to that. Can you please provide more details?"

# Main function to run the chatbot
def run_chatbot():
    print("Customer Service Assistant: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Customer Service Assistant: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print(f"Customer Service Assistant: {response}")

# Run the chatbot
run_chatbot()
