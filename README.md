# sqlalchemy-challenge
Repo for bootcamp module 10 - SQLAlchemy challenge

Vincent Passanisi

Due Date: December 28, 2022
Submitted January 1, 2023

# **Introduction**

This challenge requires a climate analysis for a Hawaiian vacation, using Python and SQLAlchemy. The analysis is comprised of a precipitation analysis for the most recent 12 months of data in the dataset, and a temperature analysis of the station with the greatest number of observations. The precipitation analysis is plotted visually on a bar graph and the temperature analysis is represented with a histogram.

# **Files**

In the folder *SurfsUp* are the completed challenge files.

* *climate_starter_final.ipynb* - my jupyter notebook with my SQLAlchemy analysis and matplotlib graphs.
* *app_complete.py* - My python script with my Flask API.
* *Resources* folder with the data .csv files and sqlite engine
* *Output* folder with image files

# **Results**

The precipitation analysis shows the rainfall for all stations for the last year of data starting on 8/23/16. First exploratory analysis was conducted to see the available data from the provided .csv files. One file had the infomration for each station. The second file contained all the mearurement data, including rainfall and temperature. A dataframe was created with the data for all stations and the results plotted on a bar graph.

![Precipitation Analysis](SurfsUp/Output/precipitation_12mo.png)

A statistical analysis was also done of the dataframe and yielded the following results.

	prcp
count	2021.000000
mean	0.177279
std	0.461190
min	0.000000
25%	0.000000
50%	0.020000
75%	0.130000
max	6.700000

The temperature analysis was conducted on the most active station in terms of observations. That station was WAIHEE 837.5, HI US which had 2,772 observations in the dataset. 

The average temperature as well as the high and low for the period were examined. For WAIHEE the low was 54.0 F, the high 85.0 F.,and the average temperature was 71.66 F. The frequency of observations was plotted on a histogram, shown below.


![Temperature histogram for Waihee](SurfsUp/Output/temp_frequency.png)

Finally, a python script was written to create an API using the Flask framework. Below is a simple layout of my home page.

    **Welcome to the Climate App API!**

    **Vincent Passanisi**
    **December 2022 - UCI Data Analytics Bootcamp**

    **Here are the Available Routes:**

    For a JSON of the precipitation analysis, use this route:

    */api/v1.0/precipitation*

    For a JSON list of stations in the dataset, use this route:

    */api/v1.0/stations*

    For a JSON list of temperature observations for the previous year for the most active station, use this route:

    */api/v1.0/tobs*

    For a JSON list of the minimum temperature, the average temperature, and the maximum temperature,for a specified start date for each station,
    append a start date to the route in the format yyyy-mm-dd

    */api/v1.0/*

    For a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified date range,
    append a start and end date in the format yyyy-mm-dd/yyyy-mm-dd

    */api/v1.0//*

# **Comments and Thoughts**

This was one of the more difficult modules for me. I felt like I had a good grasp of SQL, but the SQLAlchemy threw me for a loop. Setting up the engine and bases confused me a great deal. Once I started reworking the activities and watching the class recordings, it started to come to me. And I felt much more comfortable by the time I completed my Jupyter notebook. Flask was another challenge. I had a pretty easy time with the class activities, but putting it all together turned into a struggle for me, especially with the start and date range analysis. I tried using the numpy.ravel function, but could not get it to work, so I changed tactics and created a list using a loop instead.

The instructions were a little unclear about whether the json returned for the start date and date range were supposed to be for all stations combined, individually, or just one station. I decided to compute the average, low and high temperatures for each station and list them by name. I was pretty happy with the results. I used the following query.

    temp_start = session.query(func.min(Measure.tobs)\
            , func.max(Measure.tobs)\
            , func.round(func.avg(Measure.tobs),2), Station.name).\
            filter(Measure.station == Station.station).\
            filter(Measure.date >= start).\
            group_by(Measure.station).all()

And I got the following json. This one is for one month from April 23, 2013 to May 23, 2013.

    [
    {
        "name": "HONOLULU OBSERVATORY 702.2, HI US", 
        "tavg": 71.81, 
        "tmax": 78.0, 
        "tmin": 64.0
    }, 
    {
        "name": "KANEOHE 838.1, HI US", 
        "tavg": 71.06, 
        "tmax": 79.0, 
        "tmin": 66.0
    }, 
    {
        "name": "KUALOA RANCH HEADQUARTERS 886.9, HI US", 
        "tavg": 75.28, 
        "tmax": 81.0, 
        "tmin": 69.0
    }, 
    {
        "name": "MANOA LYON ARBO 785.2, HI US", 
        "tavg": 72.03, 
        "tmax": 78.0, 
        "tmin": 69.0
    }, 
    {
        "name": "PEARL CITY, HI US", 
        "tavg": 76.19, 
        "tmax": 80.0, 
        "tmin": 70.0
    }, 
    {
        "name": "WAIHEE 837.5, HI US", 
        "tavg": 72.1, 
        "tmax": 81.0, 
        "tmin": 64.0
    }, 
    {
        "name": "WAIKIKI 717.2, HI US", 
        "tavg": 75.26, 
        "tmax": 84.0, 
        "tmin": 69.0
    }, 
    {
        "name": "WAIMANALO EXPERIMENTAL FARM, HI US", 
        "tavg": 74.47, 
        "tmax": 80.0, 
        "tmin": 69.0
    }
    ]

Overall, I enjoyed this challenge and learned a great deal.