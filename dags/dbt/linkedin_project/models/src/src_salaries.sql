WITH src_salaries AS(
    SELECT * from {{ source('JOBS', 'SALARIES') }}
)

SELECT * 
FROM 
    src_salaries 

