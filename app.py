from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
# Ensure you have set GROQ_API_KEY in your .env file
api_key = os.environ.get("GROQ_API_KEY")
client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
else:
    print("Warning: GROQ_API_KEY not set in environment variables.")

def get_fashion_advice(user_message):
    """
    Get fashion advice. Checks for specific keywords first, otherwise uses Groq's LLM.
    """
    msg = user_message.lower()
    
    # Hardcoded logic for specific keywords
    if "summer" in msg:
        return "For summer, I recommend light fabrics like linen and cotton. Floral prints and pastel colors are trending this season! ☀️👗"
    elif "winter" in msg:
        return "Layering is key for winter! Try a turtleneck under a wool coat, paired with a chunky scarf. Don't forget stylish boots! ❄️🧥"
    elif "party" in msg:
        return "For a party, you can't go wrong with a classic little black dress or a sharp blazer with dark jeans. Add some statement accessories to stand out! 🎉✨"
    elif "casual" in msg:
        return "A nice pair of fitted jeans, a white tee, and a denim jacket is a timeless casual look. Sneakers or loafers complete the vibe. 👖👟"
    
    # Fallback to Groq API for other queries
    # Fallback to Groq API for other queries
    try:
        if not client:
            return "My connection to the fashion world is a bit spotty right now (API Key missing). Please check the server configuration! 🚫👗"

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are FashBot, a high-end, trendy fashion stylist AI. Your goal is to provide personalized, stylish, and practical outfit advice. Use emojis to make the conversation lively. Keep your answers concise (around 2-3 sentences) unless asked for details. Be encouraging and confident in your tone."
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Darling, I'm having a moment... I couldn't reach my fashion sources. Please check your API key connection! 💅✨"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "I didn't catch that. Could you say it again?"})
    
    bot_response = get_fashion_advice(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
