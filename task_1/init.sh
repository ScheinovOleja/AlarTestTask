python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=login_app
export APP_SETTINGS="config.ProductionConfig"
export DATABASE_URL='postgresql://oleg:oleg2000@localhost/alar_task'
flask auth init
flask auth createsuperuser