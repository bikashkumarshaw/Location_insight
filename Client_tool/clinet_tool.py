import csv
import json
import argparse
import requests
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

class ClientTool(object):

    def run(self):
        self.define_args()
        if self.args.prepare_graph!="false":
            self.prepare_graph()
        else:
            self.load_data()

    def load_data(self):
        csvfile = open(self.args.file, 'r')
        headers = csvfile.readline().strip().split(",")

        fieldnames = headers
        reader = csv.DictReader( csvfile, fieldnames)
        out = []
        for row in reader:
            if len(out)==self.args.threshold:
                r = requests.post("http://{0}:{1}/api/load_data".format(self.args.ip, self.args.port), \
                data=json.dumps(dict(value=out)), headers={'Content-Type': 'application/json'})
                out = []
                print r.json()

            out.append(row)

        if len(out)>0:
            r = requests.post("http://{0}:{1}/api/load_data".format(self.args.ip, self.args.port), \
            data=json.dumps(dict(value=out)), headers={'Content-Type': 'application/json'})

            print r.json()

    def prepare_graph(self):
        if self.args.prepare_graph=="for_all":
            r = requests.get("http://{0}:{1}/api/get_demand?num={2}"\
            .format(self.args.ip, self.args.port, self.args.num))
        elif self.args.prepare_graph=="for_range":
            r = requests.get("http://{0}:{1}/api/get_demand?fromdate={2}&todate={3}&num={4}"\
            .format(self.args.ip, self.args.port, self.args.from_date, self.args.to_date, self.args.num))

        resp = r.json()["result"]
        area = []
        bookings = []
        canceled = []
        for val in resp:
            area.append(val.get("area_code", ""))
            bookings.append(val.get("bookings_made", 0))
            canceled.append(val.get("rides_cancelled", 0))

        trace1 = go.Bar(x=area, y=bookings, name='bookings')
        trace2 = go.Bar(x=area, y=canceled, name='canceled')
        data = [trace1, trace2]

        plotly.offline.plot({"data": data, \
        "layout": go.Layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='area code')), \
        yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='no of bookings')), title='{0} - {1}'\
        .format(self.args.from_date, self.args.to_date))})

    def define_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", help="Specify the csv file path location", type=str)
        parser.add_argument("--prepare-graph", \
        help="for_all -> graph of top 10 area, for_range -> graph of top 10 area in a range of date specified", \
        type=str, default="false")
        parser.add_argument("--ip", help="specify location_ai service ip", type=str, required=True)
        parser.add_argument("--port", help="specify location ai service port", type=str, required=True)
        parser.add_argument("--from-date", help="specify the start date to prepare graph for", \
        type=str, required=False, default='all')
        parser.add_argument("--to-date", help="specify the end date to prepare graph for", \
        type=str, required=False, default='all')
        parser.add_argument("--threshold", help="specify number of data to be loaded at a time while loading", \
        type=int, default=5000)
        parser.add_argument("--num", help="specify top n number of records to build graph for", \
        type=int, default=10)
        self.args = parser.parse_args()

if __name__== "__main__":
    ClientTool().run()
