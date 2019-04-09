import argparse

def _define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", help="specify the database name", type=str, required=True)
    parser.add_argument("--username", help="specify the username of the db", type=str, required=True)
    parser.add_argument("--port", help="specify the port to run server", type=int, required=True)
    args = parser.parse_args()
    return args
