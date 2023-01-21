set FLASK_APP=webapp && flask db migrate -m "+ Order"
flask db upgrade
