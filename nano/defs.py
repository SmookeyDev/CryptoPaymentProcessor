import threading
from nano.processor import makewithdraw

withdraws = threading.Thread(target=makewithdraw, args=(), daemon=True)