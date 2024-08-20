-- Company industry
WITH co AS (
    select
        company_id,
        name,
        description,
        company_size,
        state,
        country,
        city, 
        zipcode,
        address,
        url

    from
    {{ ref('src_companies') }}
),
-- Company speciality
    cs AS (
    select  
        company_id,
        speciality
    from 
    {{ ref('src_company_specialities')}}
)

Select 
    co.company_id,
    co.name,
    cs.speciality,
    co.description,
    co.company_size,
    co.state,
    co.country,
    co.city, 
    co.zipcode,
    co.address,
    co.url


FROM 
    co
LEFT JOIN cs ON co.company_id = cs.company_id 

