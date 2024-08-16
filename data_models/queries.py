# To successfully run the codes here using snowflake python operators, I have created snowflake aws connection 
# See aws_con_and_DDL file in snowflake folder to see these connections


#This query creates a partitioned table in snowflake to store our raw data directly from the source
create_table_query = """ 
    CREATE TABLE IF NOT EXISTS movie_raw(
        imdb VARCHAR,
        title VARCHAR,
        rating INT,
        year VARCHAR,
        runtime INT,
        top250 INT,
        top250tv INT, 
        title_date DATE
    )
    cluster by (title_date);
"""

## the data from this api call changes over time, we are creating this table to capture slowly dimension
## as we load our data, this staging table will connect directly to DBT
create_staging_query = """ 
    CREATE TABLE IF NOT EXISTS movie_stg(
        imdb VARCHAR,
        title VARCHAR,
        rating INT,
        year VARCHAR,
        runtime INT,
        top250 INT,
        top250tv INT, 
        title_date DATE, 
        insert_date date,
        last_updated_date date
    )
    cluster by (title_date);
"""

# This query loads data from the snowflake stage into the partitioned table
#The distinct is a way to handle the data load so that we don't have duplicate data in the table
load_title_query = """ 
    COPY INTO movie_raw
    FROM (
          select distinct * from @movie_title_stage  
         )
    FILE_FORMAT = csv_format
    pattern = '.*[.]csv'
    on_error = continue ;
"""


# Snowflake streams looks at our data and identify slowly changind dimenstion columns
# in sour data, based on this query:
# It creates a stream against our raw table 

create_stream_query = """ 
    create stream IF NOT EXISTS movie_stream on table PROJECT.NETFLIX_RAW.MOVIE_STG ;
"""


# # 

load_stream_query = """ 
    merge into PROJECT.NETFLIX_RAW.MOVIE_STG n 
    using PROJECT.NETFLIX_RAW.MOVIE_STREAM s 
        on n.imdb = s.imdb 
    when matched 
        and s.METADATA$ACTION = 'DELETE'
        and s.METADATA$ISUPDATE = 'FALSE'
    then delete 
    when matched 
        and s.METADATA$ACTION = 'INSERT'
        and s.METADATA$ISUPDATE = 'TRUE'
        then update 
        set n.imdb = s.imdb,
            n.title = s.title,
            n.rating = s.rating,
            n.year = s.year,
            n.runtime = s.runtime,
            n.top250 = s.top250,
            n.top250tv = s.top250tv,
            n.title_date = s.title_date,
            n.last_updated_date = current_date
    when not matched 
        and s.METADATA$ACTION = 'INSERT'
        and s.METADATA$ISUPDATE = 'FALSE'
        then insert(imdb,title,rating,year,runtime,top250,top250tv,title_date,last_updated_date)
    values(s.imdb,s.title,s.rating,s.year,s.runtime,s.top250,s.top250tv,s.title_date,current_date);

"""