from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': days_ago(2),
	'email': ['airflow@example.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

#Inicializacion del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
	'practica2_ORG',
	default_args=default_args,
	description='Practica 2 de Cloud Computing, realiza el despliegue de 2 apis y 1 base de datos MongoDB',
	schedule_interval=timedelta(days=1),
)

#Creamos el directorio, raiz de tareas
PrepararEntorno = BashOperator(
	task_id = 'PrepararEntorno',
	bash_command='mkdir -p /tmp/workflow/ && mkdir -p /tmp/workflow/V1/ && mkdir -p /tmp/workflow/V2/',
	dag=dag,
)

#Podemos usar wget, curl y otros comandos como tales
CapturaDatosA = BashOperator(
	task_id = 'CapturaDatosA',
	bash_command='wget --output-document /tmp/workflow/humidity.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
	dag=dag,
)

CapturaDatosB = BashOperator(
	task_id = 'CapturaDatosB',
	bash_command='wget --output-document /tmp/workflow/temperature.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
	dag=dag,
)

DescomprimirDatosA = BashOperator(
    	task_id = 'DescomprimirDatosA',
    	bash_command='unzip /tmp/workflow/humidity.csv -d /tmp/workflow',
	dag=dag,
)

DescomprimirDatosB = BashOperator(
    	task_id = 'DescomprimirDatosB',
    	bash_command='unzip /tmp/workflow/temperature.csv -d /tmp/workflow',
	dag=dag,
)

CombinarDatosAB = BashOperator(
    	task_id = 'CombinarDatosAB',
    	bash_command='cut -d , -f 1,4 </tmp/workflow/temperature.csv >/tmp/workflow/temp.csv && cut -d , -f 4 </tmp/workflow/humidity.csv >/tmp/workflow/hum.csv && paste -d"," <(cut -d"," -f-2 /tmp/workflow/temp.csv) /tmp/workflow/hum.csv <(cut -d"," -f3- /tmp/workflow/temp.csv) > /tmp/workflow/output.csv',
	dag=dag,
)

RenombrarColumnas = BashOperator(
	task_id = 'RenombrarColumnas',
	bash_command='sed -i "1s/.*/DATE, TEMP, HUM/" /tmp/workflow/output.csv',
	dag=dag,
)

ClonacionRamaV1 = BashOperator(
	task_id = 'ClonacionRamaV1',
	bash_command='git clone --single-branch -b master https://github.com/OscarRubioGarcia/CC2Airflow.git /tmp/workflow/V1/',
	dag=dag,
)

ClonacionRamaV2 = BashOperator(
	task_id = 'ClonacionRamaV2',
	bash_command='git clone --single-branch -b version_2 https://github.com/OscarRubioGarcia/CC2Airflow.git /tmp/workflow/V2/',
	dag=dag,
)

PreparacionDeEntornoFinal = BashOperator(
	task_id = 'PreparacionDeEntornoFinal',
	bash_command='cp -fr /tmp/workflow/V1/mongo /tmp/workflow/mongo && cp -f /tmp/workflow/output.csv /tmp/workflow/mongo/output.csv && cp -f /tmp/workflow/V1/docker-compose.yml /tmp/workflow/docker-compose.yml',
	dag=dag,
)

EjecucionDockerV1V2DB = BashOperator(
	task_id = 'EjecucionDockerV1V2DB',
	bash_command='cd /tmp/workflow && docker-compose up -d --force-recreate --build',
	dag=dag,
)


#Hago las 2 ramas, la de la BD y la del codigo
PrepararEntorno.set_downstream(ClonacionRamaV1)
PrepararEntorno.set_downstream(ClonacionRamaV2)
PrepararEntorno.set_downstream(CapturaDatosA)
PrepararEntorno.set_downstream(CapturaDatosB)

#Rama de la base, captura datos
CapturaDatosA.set_downstream(DescomprimirDatosA)
CapturaDatosB.set_downstream(DescomprimirDatosB)

#Rama de la base, descomprime datos
DescomprimirDatosA.set_downstream(CombinarDatosAB)
DescomprimirDatosB.set_downstream(CombinarDatosAB)

#Rama de la base, combina datos
CombinarDatosAB.set_downstream(RenombrarColumnas)

#Final, lanzar dockers
RenombrarColumnas.set_downstream(PreparacionDeEntornoFinal)
ClonacionRamaV1.set_downstream(PreparacionDeEntornoFinal)
ClonacionRamaV2.set_downstream(PreparacionDeEntornoFinal)
PreparacionDeEntornoFinal.set_downstream(EjecucionDockerV1V2DB)