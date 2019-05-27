from __future__ import print_function  # In python 2.7
import sys
from flask import Flask, render_template, request, url_for, Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired
from flask import Flask

# general configuration
app = Flask(__name__)
# for hot reoading
app.debug = True
app.secret_key = "super_secret"
session = Session()
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "oracle://C##DB2019_G43:DB2019_G43@cs322-db.epfl.ch:1521/ORCLCDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

engine = db.engine
metadata = db.metadata
sq_session = db.session
connection = engine.connect()
metadata.reflect(bind=connection)

Base = automap_base()
Base.prepare(engine, reflect=True)
City = Base.classes.city
Property_type = Base.classes.property_type
Offer = Base.classes.offer
Host = Base.classes.host
Property = Base.classes.property


# db helper functions
def dump_table(table_name):
    table = metadata.tables[table_name]
    query = table.select()
    ResultProxy = connection.execute(query)
    result = ResultProxy.fetchmany(10)
    ResultProxy.close()
    return result


def search_in_table(query, table_name, col_name):
    sql_query = "SELECT * FROM {0} WHERE UPPER({1}) LIKE UPPER('%{2}%')".format(
        table_name, col_name, query
    )
    print(sql_query, file=sys.stderr)
    ResultProxy = connection.execute(sql_query)
    result = ResultProxy.fetchmany(10)
    return result

def insert_in_table(col_value, table_name):
    # query is of the form [(host_id, 2324),(host_name, "Robin"),(col_name, value),...]

    sql_query = "INSERT INTO {0} (".format(table_name)
    s = "VALUES ("
    for (c,v) in col_value:
        sql_query = sql_query + "{0}, ".format(c)
        s = s + "{0}, ".format(v)
    sql_query = sql_query[:-2] + ") " + s[:-2] + ")"
    print(sql_query, file=sys.stderr)
    #ResultProxy = connection.execute(sql_query)
    # result ?

def delete_in_table(name, table_name, col_name):

    # Maybe change for int values or others 
    sql_query = "DELETE FROM {0} WHERE UPPER({1}) LIKE UPPER('{2}')".format(
        table_name, col_name, name
    )
    print(sql_query, file=sys.stderr)
    # ResultProxy = connection.execute(sql_query)
    # result ?

def advance_search(
    city, property_type, number_of_guests, available_from, available_to, price_max
):
    available_from = '2001-01-01' if not available_from else available_from
    available_to = '2020-01-01' if not available_to else available_to
    if number_of_guests :
        guests = 'AND p.ACCOMMODATES = {}'.format(number_of_guests)
    else :
        guests =''
    if price_max :
        price = 'AND p.price <= {}'.format(price_max)
    else :
        price = ''

    query_ = ("SELECT o.name, o.summary, o.description, p.price "
        "FROM Offer o, Prices p "
        "WHERE o.listing_id IN ("
	        "SELECT p.listing_id "
	        "FROM Property p, Property_type pt "
            "WHERE (p.property_type_id = pt.property_type_id) {4} AND (pt.property_type = '{0}') AND p.property_id IN ( "
		        "SELECT a.property_id "
		        "FROM Address a, Neighbourhood n "
		        "WHERE a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID AND n.CITY_ID IN ( "
                    "SELECT c.CITY_ID "
                    "FROM City c "
                    "WHERE c.CITY = '{1}')"
           ")) AND p.LISTING_ID=o.LISTING_ID {5} AND o.LISTING_ID IN ("
           "SELECT c.listing_id "
           "FROM Calendar c "
           "WHERE c.DATE_ BETWEEN TO_DATE('{2}', 'YYYY-MM-DD') AND TO_DATE('{3}', 'YYYY-MM-DD') AND c.AVAILABLE='t')" ).format(property_type,city,available_from,available_to,guests,price)
    print(query_)
    ResultProxy = connection.execute(query_)
    return ResultProxy.fetchmany(50)


# search form
class SearchForm(FlaskForm):
    select_col = SelectField("column to search :")
    query = StringField("search query :", validators=[DataRequired()])

    def __init__(self, columns, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        col_choices = []
        for col in columns:
            col_choices.append((col.name, col.name))
        self.select_col.choices = col_choices


def str_to_tuples(str):
    array = []
    for s in str:
        tu = (s.value, s.value)
        array.append(tu)
    return array


# search form
class SearchAdvancedForm(FlaskForm):
    city = SelectField(
        "City :",
        choices=str_to_tuples(sq_session.query(City.city.label("value")).all()),
    )
    property_type = SelectField(
        "Property type :",
        choices=str_to_tuples(
            sq_session.query(Property_type.property_type.label("value")).all()
        ),
    )
    number_of_guests = IntegerField("Number of guests :")
    available_from = DateField("Available from :", format="%m/%d/%Y")
    available_to = DateField("Available to :", format="%m/%d/%Y")
    price_max = IntegerField("Maximum price :")


# insert form
class InsertForm(FlaskForm):
    value = StringField(validators=[DataRequired()])
    def __init__(self, col_name, *args, **kwargs):
        super(InsertForm, self).__init__(*args, **kwargs)
        self.value.label = col_name      

class DeleteForm(FlaskForm):
    select_col = SelectField("column :")
    query = StringField("Delete row where :", validators=[DataRequired()])

    def __init__(self, columns, *args, **kwargs):
        super(DeleteForm, self).__init__(*args, **kwargs)
        col_choices = []
        for col in columns:
            col_choices.append((col.name, col.name))
        self.select_col.choices = col_choices

@app.route("/", methods=["GET", "POST"])
def get():
    table = request.form.get("comp_select")
    if table == None:
        table = "host"
    selected_table = table
    return render_template(
        "index.html",
        tables=metadata.sorted_tables,
        columns=metadata.tables[table].columns.keys(),
        records=dump_table(table),
        selected_table=selected_table,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    if "change_table" in request.form:
        selected_table = request.form.get("comp_select")
        print(selected_table)
        session["curr_table"] = selected_table
    if "curr_table" in session:
        selected_table = session["curr_table"]
    else:
        selected_table = "host"
    columns = metadata.tables[selected_table].columns
    form = SearchForm(columns)
    if form.validate_on_submit():
        query = form.query.data
        col_name = form.select_col.data
        records = search_in_table(query, selected_table, col_name)
        return render_template(
            "search.html",
            tables=metadata.sorted_tables,
            form=form,
            columns=columns,
            records=records,
            selected_table=selected_table,
        )
    return render_template(
        "search.html",
        tables=metadata.sorted_tables,
        form=form,
        selected_table=selected_table,
        columns=columns,
    )


@app.route("/advancedsearch", methods=["GET", "POST"])
def adv_search():
    form = SearchAdvancedForm()
    city = form.city.data
    property_type = form.property_type.data
    number_of_guests = form.number_of_guests.data
    available_from = form.available_from.data
    available_to = form.available_to.data
    price_max = form.price_max.data
    if request.method == "POST":
        records = advance_search(
            city,
            property_type,
            number_of_guests,
            available_from,
            available_to,
            price_max,
        )
        return render_template(
            "adv_search.html",
            form=form,
            columns=[
                "name",
                "summary",
                "description",
                "price",
            ],
            records=records,
        )
    return render_template(
        "adv_search.html",
        form=form,
        columns=["name", "summary", "description","price"],
    )


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if 'change_table' in request.form :
        selected_table = request.form.get("comp_select")
        print(selected_table)
        session['curr_table'] = selected_table
        session['col_value'] = []
        print(session['curr_table'], file=sys.stderr)
        session['index'] = 0
    if 'curr_table' in session :
        selected_table = session['curr_table']
        print('curr_table', file=sys.stderr)
    else :
        selected_table = "host"
        session['col_value'] = []
        session['index'] = 0
        print("la table normale host", file=sys.stderr)
    columns = metadata.tables[selected_table].columns
    len_columns = len(columns)
    index = session['index']
    print("index = " + str(index), file=sys.stderr)
        
    if(len_columns == index):
        insert_in_table(session['col_value'], selected_table)
        form = InsertForm("fini")
        return render_template("insert.html", tables=metadata.sorted_tables, form=form, selected_table=selected_table)
    # vraiment degueulasse, TODO trouver un meilleur moyen
    i = 0
    for c in columns:
        if (i == index):
            print(c.name, file=sys.stderr)
            col_name = c.name
            form = InsertForm(col_name)
            value = form.value.data
            print("value is " + str(value), file=sys.stderr)
            session['col_value'] = session['col_value'] + [(col_name, value)]
        i += 1   

    if form.validate_on_submit() :
        session['index'] += 1
        print("index2 =" + str(session['index']), file=sys.stderr)
        return render_template(
        "insert.html",
        tables=metadata.sorted_tables,
        form=form,
        selected_table=selected_table
        )

    return render_template("insert.html", tables=metadata.sorted_tables, form=form, selected_table=selected_table)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if "change_table" in request.form:
        selected_table = request.form.get("comp_select")
        print(selected_table)
        session["curr_table"] = selected_table
    if "curr_table" in session:
        selected_table = session["curr_table"]
    else:
        selected_table = "host"
    columns = metadata.tables[selected_table].columns
    form = DeleteForm(columns)
    
    if form.validate_on_submit():
        query = form.query.data
        col_name = form.select_col.data
        delete_in_table(query, selected_table, col_name)
        return render_template(
            "delete.html",
            tables=metadata.sorted_tables,
            form=form,
            columns=columns,
            selected_table=selected_table,
        )
    return render_template(
        "delete.html",
        tables=metadata.sorted_tables,
        form=form,
        selected_table=selected_table,
        columns=columns,
    )

if __name__ == "__main__":
    app.run()

