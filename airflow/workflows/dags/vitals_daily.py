from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.email_operator import EmailOperator

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

passing = KubernetesPodOperator(
    namespace='airflow',
    image="image-registry.openshift-image-registry.svc:5000/airflow/dag-runner:latest",
    cmds=["python","sepsis/vitals.py"],
    labels={"app": "airflow"},
    name="vitals-train",
    task_id="vitals-train",
    get_logs=True,
    image_pull_policy='Always',
    dag=dag
)

# Example e-mail notification
#success_msg = EmailOperator(
#    dag=dag,
#    task_id='success_msg',
#    to=['nsayre@redhat.com'],
#    subject='[SUCCESS] -- vitals pipeline',
#    html_content=(
#        '''
#        <h3>&#127939; Run details:</h3>
#            <p><b>DAG:</b> vitals_daily
#            <p><b>Status:</b> &#9989; Success
#        <br></br>
#        '''
#    )
#)

passing
