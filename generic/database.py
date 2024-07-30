import streamlit as st
import sqlalchemy as sql
import os

def postgres_connection_string():
    string = f'postgresql://{os.environ["postgres_db_user"]}:{os.environ["postgres_db_password"]}@{os.environ["postgres_db_server"]}:25060/tool?sslmode=require'
    return string

@st.cache_resource(ttl=3600)
def postgres_connection_engine():
    engine = sql.create_engine(postgres_connection_string())
    return engine