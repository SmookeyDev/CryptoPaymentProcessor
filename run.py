from flask import Flask
from nano.main import nanopay
from bitcoin.main import bitcoinpay
from ethereum.main import ethereumpay
import threading
from nano.processor import makedeposits, makewithdraw

global processing

app = Flask(__name__)

app.register_blueprint(nanopay)
app.register_blueprint(bitcoinpay)
app.register_blueprint(ethereumpay)

deposits = threading.Thread(target=makedeposits, args=(), daemon=True)

@app.route('/')
def index():
    return "Default route of this api."


if __name__ == "__main__":
    deposits.start()
    app.run(host='127.0.0.1', port='3000', debug=True)