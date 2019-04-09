# Client tool:

## This tool can be used to load csv data to load_data API.

# Install Virtual Environment:
```
pip install virtualenv

virtualenv -p python2 [environment name eg. env]

source env/bin/activate (env is the name of the environment here. please set according to your environment name)

Now install all the dependencies as listed below
```

## Dependencies:
- pip install -r requirements.txt

# Guide to use Client tool

## Arguments supported by tool

```
python clinet_tool.py -h
```

![](https://i.imgur.com/QxgXFmH.png)

## To load data.

Run the command below in Client_tool folder.

```
python clinet_tool.py --file ~/Downloads/data.csv --ip 127.0.0.1 --port 3344
```

In the command above --file takes full path of csv file --ip is the ip of the server where load_data API is hosted --port is the port on which load_data API is running

## To prepare graph for all data(shows top 10 areas booking and cancelation graph)

Run the command below in Client tool Folder

```
python clinet_tool.py --prepare-graph for_all --ip 127.0.0.1 --port 3344
```

graph view:

![](https://i.imgur.com/7uX6Jql.png)

## To prepare graph within a range of date(shows top 10 areas booking and cancelation graph within a given range)

Run the command below in Client tool Folder

```
python clinet_tool.py --prepare-graph for_range --ip 127.0.0.1 --port 3344 --from-date 10/3/2013 --to-date 11/3/2013
```

graph view:

![](https://i.imgur.com/aOPo6u3.png)
