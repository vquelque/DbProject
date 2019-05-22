from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#general configuration
app = Flask(__name__)
#for hot reoading
app.debug = True
app.secret_key='super_secret'

#database connection
engine = create_engine('oracle://C##DB2019_G43:DB2019_G43@cs322-db.epfl.ch:1521/ORCLCDB')
connection = engine.connect()
metadata = MetaData()
metadata.reflect(bind=connection)
#tables
# address = Table('ADDRESS', metadata, autoload=True, autoload_with=engine)
# bed_type = Table('BED_TYPE', metadata, autoload=True, autoload_with=engine)
# calendar = Table('CALENDAR', metadata, autoload=True, autoload_with=engine)
# cancellation_policy = Table('CANCELLATION_POLICY', metadata, autoload=True, autoload_with=engine)
# city = Table('CITY', metadata, autoload=True, autoload_with=engine)
# country = Table('COUNTRY', metadata, autoload=True, autoload_with=engine)
# host = Table('HOST', metadata, autoload=True, autoload_with=engine)
# host_reponse_time = Table('HOST_RESPONSE_TIME', metadata, autoload=True, autoload_with=engine)
# neighbourhood = Table('NEIGHBOURHOOD', metadata, autoload=True, autoload_with=engine)
# offer = Table('OFFER', metadata, autoload=True, autoload_with=engine)
# prices = Table('PRICES', metadata, autoload=True, autoload_with=engine)
# property = Table('PROPERTY', metadata, autoload=True, autoload_with=engine)
# property_type = Table('PROPERTY_TYPE', metadata, autoload=True, autoload_with=engine)
# review = Table('REVIEW', metadata, autoload=True, autoload_with=engine)
# room_type = Table('ROOM_TYPE', metadata, autoload=True, autoload_with=engine)
# scores = Table('SCORES', metadata, autoload=True, autoload_with=engine)

#db helper functions
def dump_table(table_name) :
    table = metadata.tables[table_name]
    query = table.select()
    ResultProxy = connection.execute(query)
    result = ResultProxy.fetchmany(10)
    ResultProxy.close()
    return result

#search form
class SearchForm(FlaskForm):
    query = StringField('search query :', validators=[DataRequired()])
    

@app.route('/', methods=['GET', 'POST'])
def get():
    table = request.form.get('comp_select')
    if table == None :
        table = 'host'
    selected_table = str(table)
    return render_template('index.html', tables = metadata.sorted_tables,
    columns = metadata.tables[table].columns.keys(), 
    records = dump_table(table), 
    selected_table = selected_table)

@app.route('/search', methods=['GET', 'POST'])
def search() :
    table = request.form.get('comp_select')
    if table == None :
        table = 'host'
    form = SearchForm()
    if form.validate_on_submit():
        return render_template('search.html', tables = metadata.sorted_tables, form=form)
    return render_template('search.html', tables = metadata.sorted_tables, form=form)

if __name__ == "__main__":
    app.run()

    


