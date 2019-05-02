from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
#general configuration
app = Flask(__name__)
#for hot reoading
app.debug = True

#database connection
engine = create_engine('oracle://C##DB2019_G43:DB2019_G43@cs322-db.epfl.ch:1521/ORCLCDB')
result = engine.execute("select bed_type from bed_type")

@app.route('/')
def get():
    return render_template('index.html', result = result)

if __name__ == "__main__":
    app.run()

    