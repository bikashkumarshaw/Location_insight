# Location Insight

#### This service helps in analyzing travel data of cabs booked. 

#### Note you would need postgresql installed in your system for this.

## Clone:
```
git clone https://github.com/bikashkumarshaw/Location_insight.git
```

## Install Virtual Environment:
```
pip install virtualenv

cd Location_insight

virtualenv -p python2 [environment name eg. env]

source env/bin/activate (env is the name of the environment here. please set according to your environment name)

Now install all the dependencies as listed below
```

## Dependencies:
- pip install -r requirements.txt

## Run command:
```
python routes.py --dbname `provide your postgresql db name` --username `provide your postgresql username` --port `provide the port to run service` --password `specify the password of postgresql user` --ip `specify the ip of the machine where this service will be hosted`
```

## API'S supported:

```
area_data (returns data of specified area having highest demand)
get_demand (returns data of areas having highest demand)
load_data (loads data to postgresql)
```

## get_demand

### Positional params:

**date:**

* ##### The api supports date param, eg. date=10/3/2013, this would return top 20 area code and related data that were booked on 10/3/2013. The output is sorted in descending order based on bookings made, Default value of date = all which means the results will have the top 20 areas info throughout the data.

* Ref 1: http://127.0.0.1:3344/api/get_demand?date=10/3/2013
* Ref 2: http://127.0.0.1:3344/api/get_demand

```jsond
{
  "result": [
    {
      "area_code": "836",
      "bookings_made": 17,
      "rides_cancelled": 0,
      "mobile_site_booking": 0,
      "cancel_percentage": 0
    },
    {
      "area_code": "393",
      "bookings_made": 15,
      "rides_cancelled": 0,
      "mobile_site_booking": 1,
      "cancel_percentage": 0
    },
    {
      "area_code": "1010",
      "bookings_made": 5,
      "rides_cancelled": 1,
      "mobile_site_booking": 0,
      "cancel_percentage": 20
    },
    {
      "area_code": "571",
      "bookings_made": 5,
      "rides_cancelled": 0,
      "mobile_site_booking": 0,
      "cancel_percentage": 0
    },
    {
      "area_code": "1070",
      "bookings_made": 4,
      "rides_cancelled": 0,
      "mobile_site_booking": 0,
      "cancel_percentage": 0
    }
  ]
}

```

**fromdate:**

* #### This argument is used to specify the starting range of date between which we need bookings info, it can be used with todate param.

**todate:**

* #### This argument is used to specify the ending range of date between which we need bookings info, it can be used with fromdate param.

* Ref : http://127.0.0.1:3344/api/get_demand?fromdate=10/3/2013&todate=11/3/2013

```jsond
{
  "result": [
    {
      "area_code": "393",
      "bookings_made": 546,
      "rides_cancelled": 26,
      "mobile_site_booking": 44,
      "cancel_percentage": 5
    },
    {
      "area_code": "293",
      "bookings_made": 152,
      "rides_cancelled": 34,
      "mobile_site_booking": 7,
      "cancel_percentage": 22
    },
    {
      "area_code": "571",
      "bookings_made": 145,
      "rides_cancelled": 27,
      "mobile_site_booking": 6,
      "cancel_percentage": 19
    },
    {
      "area_code": "83",
      "bookings_made": 101,
      "rides_cancelled": 25,
      "mobile_site_booking": 5,
      "cancel_percentage": 25
    },
    {
      "area_code": "142",
      "bookings_made": 90,
      "rides_cancelled": 9,
      "mobile_site_booking": 5,
      "cancel_percentage": 10
    }
  ]
}
```

**num:**

* #### num specifies the number of results to be shown, eg num=2. the default value of num=20.

* Ref: http://127.0.0.1:3344/api/get_demand?fromdate=10/3/2013&todate=11/3/2013&num=2

```jsond
{
  "result": [
    {
      "area_code": "393",
      "bookings_made": 546,
      "rides_cancelled": 26,
      "mobile_site_booking": 44,
      "cancel_percentage": 5
    },
    {
      "area_code": "293",
      "bookings_made": 152,
      "rides_cancelled": 34,
      "mobile_site_booking": 7,
      "cancel_percentage": 22
    }
  ]
}
```

**sort:**

* #### By default sorting is done on number of bookings made in an area, sort can be set to sort=cancel_rate this sorts the top 20 areas data having highest bookings with respect to cancel percentage, where cancel_percentage = (rides_cancelled/bookings_made)*100, this will help us understand which area out of top 20 highest bookings have more cancellation rates.

Ref: http://127.0.0.1:3344/api/get_demand?fromdate=10/3/2013&todate=11/3/2013&sort=cancel_rate

```jsond
{
  "result": [
    {
      "area_code": "1026",
      "bookings_made": 50,
      "rides_cancelled": 18,
      "mobile_site_booking": 0,
      "cancel_percentage": 36
    },
    {
      "area_code": "61",
      "bookings_made": 50,
      "rides_cancelled": 15,
      "mobile_site_booking": 1,
      "cancel_percentage": 30
    },
    {
      "area_code": "330",
      "bookings_made": 58,
      "rides_cancelled": 17,
      "mobile_site_booking": 2,
      "cancel_percentage": 29
    },
    {
      "area_code": "396",
      "bookings_made": 43,
      "rides_cancelled": 11,
      "mobile_site_booking": 1,
      "cancel_percentage": 26
    }
  ]
}
```

## area_data

### Positional params:

**area_code:**

* This is a required argument for area_data API, This api is used to analyze bookings made by users in a given area. This returns top users data based on thier no of bookings in a given area. 

Ref: http://127.0.0.1:3344/api/area_data?area_code=393

```
{
  "result": [
    {
      "user_id": "45500",
      "no_of_times_booked": 27,
      "to_area_code": [
        "NULL",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "NULL",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "1175",
        "NULL",
        "846",
        "846",
        "846",
        "NULL",
        "1175"
      ],
      "travel_type": [
        "hourly rental",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "hourly rental",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "point to point",
        "hourly rental",
        "point to point",
        "point to point",
        "point to point",
        "hourly rental",
        "point to point"
      ]
    }
  ]
}
```

**date:**
* Same as that of get_demand api.

Ref: http://127.0.0.1:3344/api/area_data?area_code=393&date=10/03/2013

```jsond
{
  "result": [
    {
      "user_id": "41621",
      "no_of_times_booked": 1,
      "to_area_code": [
        "1010"
      ],
      "travel_type": [
        "point to point"
      ]
    },
    {
      "user_id": "41626",
      "no_of_times_booked": 1,
      "to_area_code": [
        "516"
      ],
      "travel_type": [
        "point to point"
      ]
    }
  ]
}
```

**fromdate:**

* Same as that of get_demand api

Ref: http://127.0.0.1:3344/api/area_data?area_code=393&fromdate=10/3/2013&todate=11/3/2013

**todate:**

* Same as that of get_demand api

Ref: http://127.0.0.1:3344/api/area_data?area_code=393&fromdate=10/3/2013&todate=11/3/2013

