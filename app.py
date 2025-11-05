from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

API_KEY = os.getenv("SCREENSHOTBASE_API_KEY")
API_URL = "https://api.screenshotbase.com/v1/take"

# Ensure the screenshots directory exists
os.makedirs(os.path.join("static", "screenshots"), exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    screenshot_path = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            error = "⚠️ Please enter a valid website URL."
            return render_template("index.html", screenshot=None, error=error)

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
            file_name = f"screenshot_{timestamp}.png"
            file_path = os.path.join("static", "screenshots", file_name)

            # Save screenshot
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


# --- Production entry point ---
if __name__ == "__main__":
    # Use port provided by Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
