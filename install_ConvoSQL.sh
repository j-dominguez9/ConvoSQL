#!/bin/sh

# cd term_project

# Creating mysql password
PW=$(date | base64)
echo ${PW:0:12} > .mysql_pw
podman secret create mysql_pw .mysql_pw

# Requesting OpenAI API keys
echo Please provide OpenAI API Key:
read openai_api
echo "OAI_API="$openai_api > .env

echo Please provide OpenAI ORG key:
read openai_org
echo "OAI_ORG="$openai_org >> .env

cp .env ./app/.env


# Create podman network for application pod
podman network create --subnet 192.168.55.0/24 --gateway 192.168.55.3 --subnet fd52:2a5a:747e:3acd::/64 --gateway fd52:2a5a:747e:3acd::10 mysql-proj-net

#Create pod to house application
podman pod create --network=mysql-proj-net -p 80:8501 mysql-proj-pod

# Building and running first MySQL db container
podman build -t mysql_im . --no-cache
podman run -dt --rm --secret mysql_pw --name=mysql_cont --pod mysql-proj-pod mysql_im

# Building and running second MySQL db container
cd mysql2

podman build -t mysql2_im . --no-cache
podman run -dt --rm --secret mysql_pw --name=mysql2_cont --pod mysql-proj-pod mysql2_im

#Building and running Application
cd ..
cd app

podman build -t py_app --no-cache .
podman run -it --rm --pod mysql-proj-pod --secret mysql_pw --name py_app_cont py_app


