set FLASK_APP=webapp && flask db migrate -m "+ OrderContent ondelete CASCADE"
flask db upgrade
