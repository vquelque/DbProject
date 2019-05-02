from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
#general configuration
app = Flask(__name__)
#for hot reoading
app.debug = True

#database connection
engine = create_engine('oracle://C##DB2019_G43:DB2019_G43@cs322-db.epfl.ch:1521/ORCLCDB')
connection = engine.connect()
metadata = MetaData()
#tables
host = Table('HOST', metadata, autoload=True, autoload_with=engine)

#db helper functions
def dump_table(table) :
    query = table.select()
    ResultProxy = connection.execute(query)
    result = ResultProxy.fetchmany(10)
    ResultProxy.close()
    return result

@app.route('/')
def get():
    return render_template('index.html', columns = host.columns.keys(), records = dump_table(host))

if __name__ == "__main__":
    app.run()

    


