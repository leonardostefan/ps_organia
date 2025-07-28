-- Cria um novo banco de dados
CREATE DATABASE organia;

-- Conecta no banco recém-criado e cria uma tabela dentro dele
\connect organia;


CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    costumer_name TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
