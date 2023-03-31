import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Make a request to the ChatCompletion API
openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

# Initialize a list to store the conversation history
previous_messages = []


def chatbot(question):
    # define the conversation context based on the input question and the previous messages
    if "world series" in question:
        messages = [
            {"role": "system", "content": "You are a helpful assistant created by Barry."},
            {"role": "user", "content": question},
            {"role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    else:
        # default conversation context if question doesn't match any specific case
        messages = [
            {"role": "system", "content": "You are a helpful assistant created by Barry."},
            {"role": "user", "content": question}
        ]
    # append the previous messages to the conversation context
    messages.extend(previous_messages)

    # generating the response based on the conversation context
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.6,
        stop=[" Human:", "AI:"]
    )

    # return the generated response
    return response["choices"][0]["message"]["content"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["message"]
    response = chatbot(user_message)
    return jsonify(response=response)


if __name__ == "__main__":
    app.run(debug=True)
