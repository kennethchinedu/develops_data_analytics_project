-- Industries table  
WITH i AS (
    select
        industry_id,
        industry_name
    from
    {{ ref('src_industries') }}
),
-- Job industries
    ji AS (
    select  
        job_id,
        industry_id
    from 
    {{ ref('src_job_industries')}}
),
-- Job skills
    jk AS (
    select  
        job_id,
        skill_abr
    from 
    {{ ref('src_job_skills')}}
),
--skills
    s AS (
    select  
        skill_name,
        skill_abr
    from 
    {{ ref('src_skills')}}
)

Select 
    i.industry_id,
    i.industry_name,
    jk.skill_abr,
    s.skill_name
 


FROM 
    ji 
LEFT JOIN i ON i.industry_id = ji.industry_id 
LEFT JOIN jk on ji.job_id = jk.job_id
LEFT JOIN s on jk.skill_abr = s.skill_abr