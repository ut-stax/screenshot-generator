from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("SCREENSHOTBASE_API_KEY")
API_URL = "https://api.screenshotbase.com/v1/take"

os.makedirs("static/screenshots", exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    screenshot_path = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')

        if not url.startswith("http"):
            url = "https://" + url

        params = {
            "url": url,
            "full_page": 1,
            "format": "png"
        }
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join("static", "screenshots", f"screenshot_{timestamp}.png")

            with open(file_path, "wb") as f:
                f.write(response.content)

            screenshot_path = file_path

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] API Request failed: {e}")
            error = "⚠️ Unable to capture screenshot. Please check the URL or try again later."

        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            error = "⚠️ Something went wrong while processing your request."

    return render_template("index.html", screenshot=screenshot_path, error=error)

if __name__ == '__main__':
    app.run(debug=True)
