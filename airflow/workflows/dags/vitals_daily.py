from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    'vitals_daily',
    default_args=default_args,
    schedule_interval=None
    # schedule_interval=timedelta(minutes=10)
)

start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(
    namespace='airflow',
    image="image-registry.openshift-image-registry.svc:5000/airflow/dag-runner:latest",
    cmds=["python","airflow/workflows/dags/vitals.py"],
    labels={"app": "airflow"},
    name="passing-test",
    task_id="passing-task",
    get_logs=True,
    image_pull_policy='Always',
    dag=dag
)

passing.set_upstream(start)