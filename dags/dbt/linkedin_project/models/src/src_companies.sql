WITH src_companies AS(
    SELECT * from {{ source('JOBS', 'COMPANIES') }}
)

SELECT * 
FROM 
    src_companies 

