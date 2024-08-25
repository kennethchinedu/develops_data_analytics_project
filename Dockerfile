FROM quay.io/astronomer/astro-runtime:11.8.0



RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install  dbt-snowflake && deactivate \
    pip install -U duckdb  \
    pip install  dbt-duckdb 

