# -*- coding: utf-8 -*-

from builtins import range
from datetime import timedelta

import airflow
import os
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

hook = os.environ['SLACK_HOOK']

args = {
    'owner': 'ubuntu',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='slack_test_with_custom_docker_image',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
)

t1 = BashOperator(
    task_id='envioSlackInDocker',
    bash_command="curl -X POST --data-urlencode payload=\"{'channel': '#ie-dev', 'username': 'webhookbot', 'text': 'Airflow te saluda desde Kubernetes con un contenedor custom', 'icon_emoji': ':ghost:'}\" " + hook,
    dag=dag,
    executor_config={
       "KubernetesExecutor": {"image":"dag_1:latest"}}
)

