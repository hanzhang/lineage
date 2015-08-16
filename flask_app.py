from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return send_from_directory('html', 'app.html')

if __name__ == "__main__":
    app.run()
