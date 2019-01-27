from app import app
from config import BIND_IP, BIND_PORT

app.run(debug=True, host=BIND_IP, port=BIND_PORT)