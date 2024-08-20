WITH j AS (
    select
        job_id,
        skill_abr
    from
    {{ ref('src_job_skills') }}
),

    s AS (
    select  
        skill_name,
        skill_abr
    from 
    {{ ref('src_skills')}}
),

    b AS (
    select  
        job_id,
        inferred,
        type
    from 
    {{ ref('src_benefits')}}
)

Select 
    j.job_id,
    j.skill_abr,
    s.skill_name,
    b.inferred,
    b.type 

FROM 
    j 
LEFT JOIN b ON j.job_id = b.job_id 
LEFT JOIN s on j.skill_abr = s.skill_abr

