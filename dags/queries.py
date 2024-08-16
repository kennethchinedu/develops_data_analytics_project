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


#---------------------------


# CREATE TABLE "Company" (
#     "company_id" Not   NULL,
#     "name" string   NOT NULL,
#     "description" string   NOT NULL,
#     "company_size" int   NOT NULL,
#     "state" string   NOT NULL,
#     "country" string   NOT NULL,
#     "city" string   NOT NULL,
#     "zip_code" int   NOT NULL,
#     "address" string   NOT NULL,
#     "url" string   NOT NULL,
#     CONSTRAINT "pk_Company" PRIMARY KEY (
#         "company_id"
#      )
# );

# CREATE TABLE "Industry" (
#     "company_id" string   NOT NULL,
#     "industry" string   NOT NULL,
#     CONSTRAINT "pk_Industry" PRIMARY KEY (
#         "company_id"
#      )
# );

# CREATE TABLE "Company_speciality" (
#     "company_id" NOT   NULL,
#     "speciality" string   NOT NULL,
#     CONSTRAINT "pk_Company_speciality" PRIMARY KEY (
#         "company_id"
#      )
# );

# CREATE TABLE "Company_employee_count" (
#     "company_id" NOT   NULL,
#     "employee_count" int   NOT NULL,
#     "follower_count" int   NOT NULL,
#     "time_recorded" datetme   NOT NULL,
#     CONSTRAINT "pk_Company_employee_count" PRIMARY KEY (
#         "company_id"
#      )
# );

# CREATE TABLE "Job_benefits" (
#     "job_id" NOT   NULL,
#     "inferred" string   NOT NULL,
#     "type" string   NOT NULL,
#     CONSTRAINT "pk_Job_benefits" PRIMARY KEY (
#         "job_id"
#      )
# );

# CREATE TABLE "job_industries" (
#     "job_id" string   NOT NULL,
#     "industry_id" string   NOT NULL,
#     CONSTRAINT "pk_job_industries" PRIMARY KEY (
#         "job_id"
#      )
# );

# CREATE TABLE "company_industry" (
#     "company_id" NOT   NULL,
#     "industry" string   NOT NULL,
#     CONSTRAINT "pk_company_industry" PRIMARY KEY (
#         "company_id"
#      )
# );

# CREATE TABLE "job_skills" (
#     "job_id" string   NOT NULL,
#     "skill_abr" string   NOT NULL,
#     CONSTRAINT "pk_job_skills" PRIMARY KEY (
#         "job_id"
#      )
# );

# CREATE TABLE "salaries" (
#     "salary_id" string   NOT NULL,
#     "job_id" string   NULL,
#     "max_salary" int   NOT NULL,
#     "med_salary" int   NOT NULL,
#     "min_salary" int   NOT NULL,
#     "pay_period" string   NOT NULL,
#     "currency" string   NOT NULL,
#     "compensation_type" string   NOT NULL,
#     CONSTRAINT "pk_salaries" PRIMARY KEY (
#         "salary_id"
#      )
# );

# CREATE TABLE "Industries" (
#     "industry_id" string   NOT NULL,
#     "industry_name" string   NOT NULL,
#     CONSTRAINT "pk_Industries" PRIMARY KEY (
#         "industry_id"
#      )
# );

# ALTER TABLE "Company" ADD CONSTRAINT "fk_Company_company_id" FOREIGN KEY("company_id")
# REFERENCES "Industry" ("company_id");

# ALTER TABLE "Company_speciality" ADD CONSTRAINT "fk_Company_speciality_company_id" FOREIGN KEY("company_id")
# REFERENCES "Company" ("company_id");

# ALTER TABLE "Company_employee_count" ADD CONSTRAINT "fk_Company_employee_count_company_id" FOREIGN KEY("company_id")
# REFERENCES "Company" ("company_id");

# ALTER TABLE "Job_benefits" ADD CONSTRAINT "fk_Job_benefits_job_id" FOREIGN KEY("job_id")
# REFERENCES "salaries" ("job_id");

# ALTER TABLE "job_industries" ADD CONSTRAINT "fk_job_industries_industry_id" FOREIGN KEY("industry_id")
# REFERENCES "Industries" ("industry_id");

# ALTER TABLE "company_industry" ADD CONSTRAINT "fk_company_industry_company_id" FOREIGN KEY("company_id")
# REFERENCES "Company" ("company_id");

# ALTER TABLE "company_industry" ADD CONSTRAINT "fk_company_industry_industry" FOREIGN KEY("industry")
# REFERENCES "Industries" ("industry_name");

# ALTER TABLE "job_skills" ADD CONSTRAINT "fk_job_skills_job_id" FOREIGN KEY("job_id")
# REFERENCES "job_industries" ("job_id");

# ALTER TABLE "salaries" ADD CONSTRAINT "fk_salaries_job_id" FOREIGN KEY("job_id")
# REFERENCES "job_skills" ("job_id");

