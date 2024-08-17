WITH src_job_industries AS(
    SELECT * from {{ source('JOBS', 'JOB_INDUSTRIES') }}
)

SELECT * 
FROM 
    src_job_industries 

