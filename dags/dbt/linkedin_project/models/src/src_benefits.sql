WITH src_benefits AS(
    SELECT * from {{ source('JOBS', 'BENEFITS') }}
)

SELECT * 
FROM 
    src_benefits 

