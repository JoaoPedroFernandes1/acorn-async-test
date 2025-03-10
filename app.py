from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "A aplicação está rodando no Heroku!"

if __name__ == "__main__":
    app.run(debug=True)