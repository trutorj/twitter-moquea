from src.config import PORT
from src.app import app
import src.controllers.principal


app.run("0.0.0.0", PORT, debug=True)