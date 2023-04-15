FROM docker.io/mysql/mysql-server
ENV MYSQL_ROOT_PASSWORD /run/secrets/mysql_pw
ENV MYSQL_DATABASE sakila
ENV MYSQL_TCP_PORT 3306
ADD ./databases/ /docker-entrypoint-initdb.d
ENV MYSQL_USER vscode
ENV MYSQL_PASSWORD /run/secrets/mysql_pw
EXPOSE 3306
