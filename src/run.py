import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src.app import app






if __name__ == "__main__":
    
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
    app.run(debug=app.config['DEBUG'],port=4990)
