from flask import Flask, request
import json
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

from args import _define_args
from queries import SQL_QUERY

app = Flask(__name__)

ARGS = _define_args()
CONN = psycopg2.connect("dbname = {0} user = {1}".format(ARGS.dbname, ARGS.username))
cur = CONN.cursor()

@app.route("/api/load_data", methods=["POST"])
def load_data():
    sq_query = SQL_QUERY.get("load_to_db", "")
    cur.execute(sq_query)
    if request.method == 'POST':
        data = request.json["value"]
    else:
        data = request.args.get("value")

    sq_query = SQL_QUERY.get("insert_data", "")
    for line in data:
        _id = line.pop("id", None)

        cur.execute(sq_query.format(_id, json.dumps(line)))

    CONN.commit()
    return json.dumps({"message": "inserted {} records".format(len(data))})

def _get_sql_query(req_from, date, fromdate, todate, area_code):
    if fromdate!="" and todate=="" or fromdate=="" and todate!="":
        return json.dumps({"error": "please specify fromdate and todate"})
    if req_from=="demand_data":
        if date.lower()=="all" and fromdate=="" and todate=="":
            sq_query = SQL_QUERY.get("get_all", "")

            return sq_query

        elif date and fromdate=="" and todate=="":
            date_delim = date.split("/")[2][:3]

            sq_query = SQL_QUERY.get("get_date", "")
            sq_query = sq_query%(date_delim, date)

            return sq_query
        else:
            sq_query = SQL_QUERY.get("get_range", "")
            from_date_delim = fromdate.split("/")[2][:3]
            to_date_delim = todate.split("/")[2][:3]
            sq_query = sq_query%(from_date_delim, fromdate, to_date_delim, todate)

            return sq_query

    elif req_from=="user_data":
        if date.lower()=="all" and fromdate=="" and todate=="":
            sq_query = SQL_QUERY.get("user", "")
            sq_query = sq_query%area_code

            return sq_query

        elif date and fromdate=="" and todate=="":
            date_delim = date.split("/")[2][:3]

            sq_query = SQL_QUERY.get("user_date", "")
            sq_query = sq_query%(area_code, date_delim, date)

            return sq_query

        else:
            sq_query = SQL_QUERY.get("user_date_range", "")
            from_date_delim = fromdate.split("/")[2][:3]
            to_date_delim = todate.split("/")[2][:3]
            sq_query = sq_query%(area_code, from_date_delim, fromdate, to_date_delim, todate)

        return sq_query


@app.route("/api/get_demand")
def get_demand():

    date = request.args.get("date", "all")
    fromdate = request.args.get("fromdate", "")
    todate = request.args.get("todate", "")
    sort = request.args.get("sort", "")
    num = request.args.get("num", 20)
    num = int(num)
    sq_query = _get_sql_query("demand_data", date, fromdate, todate, '')

    if "error" in sq_query:
        return sq_query

    cur.execute(sq_query)

    area = cur.fetchall()

    area_map = {}
    for areas in area:
        try:
            area_map[areas[0][0]] = [areas[1], \
            sum(map(int, areas[2])), sum(map(int, areas[3])), \
            round(sum(map(int, areas[2]))/float(areas[1])*100)]
        except ZeroDivisionError:
            area_map[areas[0][0]] = [areas[1], \
            sum(map(int, areas[2])), sum(map(int, areas[3])), 0.0]

    final_area = sorted(area_map.items(), key=lambda x: x[1], reverse=True)

    if sort=="cancel_rate":
        final_area = sorted(final_area[:num], key=lambda x: x[1][3], reverse=True)

    demand = {}
    analyzed_data = []
    for records in final_area[0:num]:
        demand["area_code"] = records[0]
        demand["bookings_made"] = records[1][0]
        demand["rides_cancelled"] = records[1][1]
        demand["mobile_site_booking"] = records[1][2]
        demand["cancel_percentage"] = records[1][3]
        analyzed_data.append(demand)
        demand = {}

    return json.dumps({"result": analyzed_data})

@app.route("/api/area_data")
def get_area_data():
    area_code = request.args.get("area_code", "")
    num = request.args.get("num", 20)
    date = request.args.get("date", "all")
    fromdate = request.args.get("fromdate", "")
    todate = request.args.get("todate", "")

    sq_query = _get_sql_query("user_data", date, fromdate, todate, area_code)
    if "error" in sq_query:
        return sq_query

    cur.execute(sq_query)
    data = cur.fetchall()

    user_data = {}
    analyzed_data = []
    for rec in data:
        user_data["user_id"] = rec[0][0]
        user_data["no_of_times_booked"] = rec[1]
        user_data["to_area_code"] = rec[2]
        analyzed_data.append(user_data)
        user_data = {}

    analyzed_data = sorted(analyzed_data, key=lambda x: x["no_of_times_booked"], reverse=True)

    return json.dumps({"result": analyzed_data[:num]})

if __name__=="__main__":
    app.run(debug=True, port=ARGS.port)
