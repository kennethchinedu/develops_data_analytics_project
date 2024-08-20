WITH src_company_specialities AS(
    SELECT * from {{ source('JOBS', 'COMPANY_SPECIALITIES') }}
)

SELECT * 
FROM 
    src_company_specialities 

