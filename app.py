from __future__ import print_function  # In python 2.7
import sys
import numpy as np
from flask import Flask, flash, render_template, request, url_for, Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired
from flask import Flask
from queries import queries
from queries import para_queries

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

queries = queries()
para_queries = para_queries()


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
        s = s + "'{0}', ".format(v)
    sql_query = sql_query[:-2] + ") " + s[:-2] + ")"
    print(sql_query, file=sys.stderr)
    connection.execute(sql_query)
    # result ?

def delete_in_table(name, table_name, col_name):

    # Maybe change for int values or others 
    sql_query = "DELETE FROM {0} WHERE UPPER({1}) LIKE UPPER('{2}')".format(
        table_name, col_name, name
    )
    print(sql_query, file=sys.stderr)
    connection.execute(sql_query)
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

 #launch query
def launch_query(query) :
    ResultProxy = connection.execute(query)
    description_tuple = ResultProxy.cursor.description
    columns = [k[0] for k in description_tuple]
    return (columns,ResultProxy.fetchall())

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


# search advanced form
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
    host_name = StringField(
        label = "Host name :",
        validators=[DataRequired()])
    host_about = StringField(
        label = "Host about :",
        validators=[DataRequired()])
    name = StringField(
        label = "Name :",
        validators=[DataRequired()])
    description = StringField(
        label = "Description :",
        validators=[DataRequired()])
    cancellation_policy_id = SelectField(
        label = "Cancellation Policy :",
        choices = [(0, "flexible"),(2, "moderate"),
                (5,"strict"),(1,"strict with grace period"),
                (3,"super strict 30"),(4,"super strict 60")],
        validators=[DataRequired()])
    min_nights = IntegerField(
        label = "Minimum number of nights :",
        validators=[DataRequired(message='Please enter an integer')])
    
    #submit = SubmitField("Insert",render_kw={"class": "btn btn-success"})

class DeleteForm(FlaskForm):
    select_col = SelectField("column :")
    query = StringField("Delete row where :", validators=[DataRequired()])

    def __init__(self, columns, *args, **kwargs):
        super(DeleteForm, self).__init__(*args, **kwargs)
        col_choices = []
        for col in columns:
            col_choices.append((col.name, col.name))
        self.select_col.choices = col_choices

#query form
class QueryForm(FlaskForm) :
    select_query = SelectField("Select query :", choices=[(q['id'],q['name']) for q in queries])
    sumbit = SubmitField("Launch Query !")

class ParaQueryForm1(FlaskForm):
    score = SelectField("Select score: ", choices=[("review_scores_communication","review scores communication"),
                                                    ("review_scores_rating","review scores rating"),
                                                    ("review_scores_cleanliness","review scores cleanliness")])
    amenity = SelectField("Select amenity: ", choices=[("TV","TV"),("WIFI","WIFI")])
    sumbit = SubmitField("Launch Query !")

class ParaQueryForm2(FlaskForm):
    country = SelectField("Select country: ", choices=[("Spain","Spain"),("Germany","Germany")])
    sumbit = SubmitField("Launch Query !")

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

    form = InsertForm()
    if request.method == "POST":
        listing_id = np.random.randint(1000000000, 2000000000)
        host_id = np.random.randint(10000000, 20000000)

        col_value = []
        col_value = col_value + [("host_id",host_id)]
        col_value = col_value + [("host_name", form.host_name.data)]
        col_value = col_value + [("host_about", form.host_about.data)]
        insert_in_table(col_value, "Host")

        col_value = []
        col_value = col_value + [("listing_id",listing_id)]
        col_value = col_value + [("host_id",host_id)]
        col_value = col_value + [("name",form.name.data)]
        col_value = col_value + [("description", form.description.data)]
        col_value = col_value + [("cancellation_policy_id ",form.cancellation_policy_id.data)]
        col_value = col_value + [("minimum_nights",form.min_nights.data)]
        insert_in_table(col_value, "Offer")
        
        render_template("insert.html", form=form)
        
    return render_template("insert.html", form=form)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if "change_table" in request.form:
        selected_table = request.form.get("comp_select")
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

@app.route('/query', methods=["GET","POST"])
def query() :
    form = QueryForm()
    query = queries[0]['query']
    if form.is_submitted() :
        query_index = int(form.select_query.data) - 1
        query = queries[query_index]
        columns, records = launch_query(query['query'])
        return render_template('query.html', form=form, columns=columns,records=records,query=query)
    return render_template('query.html', form=form, query=query)

@app.route('/parameterizedquery', methods=["GET","POST"])
def para_query():
    form1 = ParaQueryForm1()
    form2 = ParaQueryForm2()
    query1 = para_queries[0]
    query2 = para_queries[1]
    if request.method == 'POST':
        if request.form['btn'] == 'launch query 1':
            query1['query'] = query1['query'].replace("TV", form1.amenity.data)
            query1['query'] = query1['query'].replace("WIFI", form1.amenity.data)
            query1['query'] = query1['query'].replace("review_scores_cleanliness", form1.score.data)
            query1['query'] = query1['query'].replace("review_scores_rating", form1.score.data)
            query1['query'] = query1['query'].replace("review_scores_communication", form1.score.data)
            query1['text'] = query1['text'].replace("TV", form1.amenity.data)
            query1['text'] = query1['text'].replace("WIFI", form1.amenity.data)
            query1['text'] = query1['text'].replace("review_scores_cleanliness", form1.score.data)
            query1['text'] = query1['text'].replace("cleaning review score", form1.score.data)
            query1['text'] = query1['text'].replace("review_scores_rating", form1.score.data)
            query1['text'] = query1['text'].replace("review_scores_communication", form1.score.data)
            columns, records = launch_query(query1['query'])
            return render_template('para_query.html', form1=form1, form2=form2, columns=columns,records=records,query1=query1, query2=query2)
        else:
            query2['query'] = query2['query'].replace("Spain", form2.country.data)
            query2['query'] = query2['query'].replace("Germany", form2.country.data)
            query2['text'] = query2['text'].replace("Spain", form2.country.data)
            query2['text'] = query2['text'].replace("Germany", form2.country.data)
            print(query2['query'], file=sys.stderr)
            columns, records = launch_query(query2['query'])
            return render_template('para_query.html', form1=form1, form2=form2, columns=columns,records=records,query1=query1, query2=query2)
        
    return render_template('para_query.html', form1=form1, form2=form2, query1=query1, query2=query2)

if __name__ == "__main__":
    app.run()

