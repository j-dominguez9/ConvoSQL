FROM docker.io/python:3.11
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY  app.py Translator.py
COPY ./pages/ /app/pages/
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN ["apt-get", "update"]
# RUN ["apt-get", "install", "-y", "nano"]
EXPOSE 8501
EXPOSE 80
ENTRYPOINT ["streamlit", "run", "Translator.py"]
#"--server.port=8501", "--server.address=0.0.0.0"