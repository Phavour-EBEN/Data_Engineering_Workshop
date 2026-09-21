from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_elt_script():
    result = subprocess.run(['python', '/opt/airflow/elt/elt_script.py'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"ELT script failed with error: {result.stderr}")
    else:
        print(result.stdout)



dag = DAG(
    dag_id='elt_dag',
    start_date=datetime(2026, 9, 21),
    schedule_interval='@daily',
    description='ELT DAG workflow for daily extraction of db data to dbt',
    catchup=False
)
  
elt_task = PythonOperator(
    task_id='elt_task',
    python_callable=run_elt_script,
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

