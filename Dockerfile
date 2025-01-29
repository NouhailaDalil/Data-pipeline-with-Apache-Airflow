FROM apache/airflow:2.10.4
ADD requirements.txt .
RUN pip install --no-deps apache-airflow==${AIRFLOW_VERSION} -r requirements.txt