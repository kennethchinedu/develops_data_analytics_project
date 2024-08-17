WITH src_skills AS(
    SELECT * from {{ source('JOBS', 'SKILLS') }}
)

SELECT * 
FROM 
    src_skills 



