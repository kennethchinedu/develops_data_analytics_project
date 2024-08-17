WITH src_company_industries AS(
    SELECT * from {{ source('JOBS', 'COMPANY_INDUSTRIES') }}
)

SELECT * 
FROM 
    src_company_industries

