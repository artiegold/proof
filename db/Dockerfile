FROM postgres 

WORKDIR /usr/src/db

ENV PGDATA /var/lib/postgresql/data/
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB proof

COPY create_tables.sql /docker-entrypoint-initdb.d/

CMD ["postgres"]



