from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.utils.dates import days_ago
from airflow.providers.airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess


CONN_ID = ''

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


dag = DAG(
    dag_id='elt_dag',
    start_date=datetime(2026, 9, 21),
    schedule_interval='@daily',
    description='ELT DAG workflow for daily extraction of db data to dbt',
    catchup=False
)
  
elt_task = AirbyteTriggerSyncOperator(
    task_id='airbyte_postgres_postgres',
    airbyte_conn_id='airbyte',
    connection_id=CONN_ID,
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag
)

transform_task = DockerOperator(
    task_id='transform_data',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root/.dbt",
        "--project-dir",
        "/dbt",
    ],
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    mount_tmp_dir=False,
    mounts=[
        Mount(source='E:/Personal_Courses/Data_Engineering_Workshop/ELT/custom_postgres', target='/dbt', type='bind'),
        Mount(source='C:/Users/Hp/.dbt', target='/root/.dbt', type='bind')
    ],
    dag=dag,
)

elt_task >> transform_task

