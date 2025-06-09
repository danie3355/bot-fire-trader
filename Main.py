import time
import threading
from flask import Flask
from utils.analysis import analyze_market
from config import COINS, INTERVAL_MINUTES

app = Flask(__name__)

@app.route("/ping")
def ping():
    return "FIRE TRADER online", 200

def bot_loop():
    while True:
        try:
            analyze_market(COINS)
        except Exception as e:
            print("Erro na análise:", e)
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=8080)
