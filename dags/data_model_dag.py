from airflow import DAG
from datetime import timedelta, datetime
import json, requests, os
from airflow.operators.python import PythonOperator 
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.hooks.S3_hook import S3Hook
from queries import create_table_query, load_title_query, create_staging_query, create_stream_query, load_stream_query


profile_config = ProfileConfig(profile_name="admin",
                               target_name="dev",
                               profile_mapping=SnowflakeUserPasswordProfileMapping(conn_id="snowflake", 
                                                    profile_args={
                                                        "database": "project",
                                                        "schema": "raw"
                                                        },
                                                    ))


dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig("/usr/local/airflow/dags/dbt/linkedin_project",),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",),
    schedule_interval="@daily",
    start_date=datetime(2023, 9, 10),
    catchup=False,
    dag_id="dbt_dag",
)



default_args = {
    'owner' : 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 12),
    'email': ['anamsken60@gmail.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    'Data_Model_Dag',
    default_args=default_args,
    schedule_interval = '@daily',
    catchup=False ) as dag:

    # Define the dbt run command as a BashOperator
    # run_dbt_model = BashOperator(
    #     task_id='run_dbt_model',
    #     bash_command='dbt debug',
    #     dag=dag
    # )

    create_raw_table_tsk = SnowflakeOperator(
        task_id = 'create_raw_table_tsk',
        sql = create_table_query,
        snowflake_conn_id='snowflake'
    )

    create_stg_table_tsk = SnowflakeOperator(
        task_id = 'create_staging_query',
        sql = create_staging_query,
        snowflake_conn_id='snowflake'
    )

    # create_stream_task = SnowflakeOperator(
    #     task_id = 'create_stream_task',
    #     sql = create_stream_query,
    #     snowflake_conn_id='snowflake_con'
    # )

    # extract_movies_task = PythonOperator(
    #     task_id="extract_movies_task",
    #     python_callable= extract_titles,
    # )

    # upload_to_s3_task = PythonOperator(
    # task_id='upload_to_s3_task',
    # python_callable=upload_titles_to_s3,
    # provide_context=True,  # This allows you to access task instance information like XCom
    # )
    
    # load_title_snowflake = SnowflakeOperator(
    #     task_id = 'load_title_snowflake',
    #     sql = load_title_query,
    #     snowflake_conn_id='snowflake_con'
    # )

    # load_stream_tsk = SnowflakeOperator(
    #     task_id = 'load_stream_tsk',
    #     sql = load_stream_query,
    #     snowflake_conn_id='snowflake_con'
    # )
    #This last task triggers another dbt dag after  the extraction and loading tasks are done
    trigger_dbt_dag = TriggerDagRunOperator(
        task_id="trigger_dbt_dag",
        trigger_dag_id="dbt_dag",
        wait_for_completion=True 
    )

    
    [create_raw_table_tsk, create_stg_table_tsk ]  >> trigger_dbt_dag
    
