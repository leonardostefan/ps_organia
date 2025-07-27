#!/bin/sh

# Build de rascunho 

docker run  \
    -p 5400:5432 \
    -e POSTGRES_PASSWORD=1234 \
    -v ./app/database/data:/var/lib/postgres/data \
    --network my-network\
    -d \
    --name organia_db\
    postgres
