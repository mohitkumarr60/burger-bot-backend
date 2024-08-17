from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Define Model Instance
model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(history=[])

# Define function, which helps to execute any prompt
def get_llm_response(message):
    response = chat.send_message(message)
    return response.text

base_info = """
You are OrderBot, an automated service to collect orders for a Burger Singh Restaurant. \
You first greet the customer, then collects the order, \
and then asks if its a pickup or delivery. \
Please do not use your own knowladge, stick within the given context only. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else.
"""

delivery_info = """If its a delivery, you ask for an address. \
Finally you collect the payment. \
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu. \
You respond in a short, very conversational friendly style. \
The menu includes"""

# Define available burger types
burger_type = """
Desi burger for 79 Rs \
Maharaja burger for 179 Rs \
Aloo Tikki burger for 99 Rs \
Classic Cheese burger for 129 Rs \
Double Cheese burger for 179 Rs \
"""

# Define available fries
snacks = """ fries 45 Rs 60 Rs 80 Rs \
  onion rings 25 Rs 35 Rs 45 Rs \
  cheese fries 35 Rs 50 Rs 60 Rs \
"""

# Define available toppings
toppings = """
lettuce 15 Rs  \
tomato 15 Rs  \
onion 15 Rs  \
pickles 15 Rs  \
mushrooms 15 Rs  \
extra cheese 20 Rs  \
Tandoori sauce 15 Rs  \
peppers 10 Rs
"""

# define drinks
drinks = """
coke 60 Rs, 45 Rs, 30 Rs \
sprite 60 Rs, 45 Rs, 30 Rs \
bottled water 50 Rs \
"""

# create prompt
context = [f"""
{base_info} \
{delivery_info} \
{burger_type} \
snacks: {snacks} \
Toppings: {toppings} \
Drinks: {drinks} \
"""]  # accumulate messages


@app.route('/api/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get('message')
    context.append(user_message)
    bot_response = get_llm_response(context)
    context.append(bot_response)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)