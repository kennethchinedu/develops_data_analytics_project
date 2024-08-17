WITH src_employee_counts AS(
    SELECT * from {{ source('JOBS', 'EMPLOYEE_COUNTS') }}
)

SELECT * 
FROM 
    src_employee_counts 

