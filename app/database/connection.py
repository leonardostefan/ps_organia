import pandas as pd
from settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Engine do banco de dados sendo criada
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_session():
    """
    Cria uma sessão temporaria do BD
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """
    Criação automatica das tabelas caso ainda não existam
    # TODO
    """


def initial_populate():
    csv_df = pd.read_csv("/workspaces/ps_organia/anexo_avaliacoes.csv", sep=";")
    {}
    csv_df = csv_df.astype(
        {
            "costumer_name": "string",
            "text": "string",
            "sentiment": "string",
        }
    )
    csv_df["created_at"] = pd.to_datetime(csv_df["created_at"], format="%d/%m/%Y")
    csv_df.to_sql(
        "reviews",
        engine,
        if_exists="append",
        index=False,
    )
