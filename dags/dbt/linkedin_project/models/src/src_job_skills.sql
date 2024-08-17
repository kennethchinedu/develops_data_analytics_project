WITH src_job_skills AS(
    SELECT * from {{ source('JOBS', 'JOB_SKILLS') }}
)

SELECT * 
FROM 
    src_job_skills 

