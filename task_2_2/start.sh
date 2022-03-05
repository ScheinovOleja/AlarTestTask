python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export APP_SETTINGS="server.config.ProductionConfig"
export FLASK_APP='manage.py'
python server/create_data.py
flask run