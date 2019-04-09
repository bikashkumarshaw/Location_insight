import csv
import json
import argparse
import requests
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

class FileReader(object):

    def run(self):
        self.define_args()
        if self.args.prepare_graph:
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
            if len(out)==1000:
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
        r = requests.get("http://{0}:{1}/api/get_demand?fromdate=10/3/2013&todate=11/3/2013&num=5".format(self.args.ip, self.args.port))
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

        plotly.offline.plot({"data": data, "layout": go.Layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='area code')), yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='no of bookings')))})

        #k = plotly.offline.plot({"data": [go.Bar(x=area, y=bookings)], "layout": go.Layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='area code')), yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='no of bookings')))})

        #m = plotly.offline.plot({"data": [go.Bar(x=area, y=canceled)], "layout": go.Layout(xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='area code')), yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='no of cancelations')))})

    def define_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", help="Specify the csv file path location", type=str)
        parser.add_argument("--prepare-graph", help="set this to true to get graph of demand", type=bool, default=False)
        parser.add_argument("--ip", help="specify location ai service ip", type=str)
        parser.add_argument("--port", help="specify location ai service port", type=str)
        self.args = parser.parse_args()

if __name__== "__main__":
    FileReader().run()
