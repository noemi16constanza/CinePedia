from base import create_app
from flask_bcrypt import Bcrypt
import os

app = create_app()
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5036))
    app.run(host='127.0.0.1', port=port, debug=True)