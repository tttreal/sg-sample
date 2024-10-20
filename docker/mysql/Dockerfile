FROM mysql:8.4

ADD init/* /docker-entrypoint-initdb.d/

RUN mkdir -p /var/log/mysql && \
    touch /var/log/mysql/mysqld.log


