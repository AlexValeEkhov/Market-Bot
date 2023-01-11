set FLASK_APP=webapp && flask db migrate -m "+ Artist, Product tables, add nullables"
flask db upgrade
