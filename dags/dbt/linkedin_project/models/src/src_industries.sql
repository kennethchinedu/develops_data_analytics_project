WITH src_industries AS(
    SELECT * from {{ source('JOBS', 'INDUSTRIES') }}
)

SELECT * 
FROM 
    src_industries


