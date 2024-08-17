WITH src_postings AS(
    SELECT * from {{ source('JOBS', 'POSTINGS') }}
)

SELECT * 
FROM 
    src_postings 

