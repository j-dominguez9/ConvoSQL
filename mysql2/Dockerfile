FROM docker.io/mysql/mysql-server
ENV MYSQL_ROOT_PASSWORD /run/secrets/mysql_pw
ENV MYSQL_DATABASE world_x
ENV MYSQL_TCP_PORT 3307
# ENV MYSQL_DATABASE classicmodels
# ENV MYSQL_DATABASE world_x
ADD ./world_x.sql /docker-entrypoint-initdb.d
# ADD ./databases/sakila-db/sakila-aschema.sql /docker-entrypoint-initdb.d
# ADD ./databases/sakila-db/sakila-data.sql /docker-entrypoint-initdb.d
# COPY ./databases/world_x-db/world_x.sql /docker-entrypoint-initdb.d
# COPY ./databases/mysqlsampledatabase.sql /docker-entrypoint-initdb.d
ENV MYSQL_USER vscode
ENV MYSQL_PASSWORD /run/secrets/mysql_pw
EXPOSE 3307
