import streamlit as st
import pandas as pd

from generic.database import postgres_connection_engine

st.markdown("""
## Data and Caching
""")

with st.expander('Collect Data from CSV'):
    data = pd.read_csv('fake_transactions.csv')
    code = """
    data = pd.read_csv('fake_transactions.csv')
    """
    st.code(code, language="python")
    st.dataframe(data.head(3))

with st.expander('Collect Data from SQL'):
    data = pd.read_sql("SELECT * FROM reporting.fake_transactions", con=postgres_connection_engine())
    code = """
    data = pd.read_sql("SELECT * FROM reporting.fake_transactions", con=postgres_connection_engine())
    """
    st.code(code, language="python")
    st.dataframe(data.head(3))


with st.expander('Collecting longer datasets from SQL'):
    st.markdown("### Cached")
    @st.cache_data()
    def get_data():
        return pd.read_sql("SELECT * FROM reporting.fake_transactions_long", con=postgres_connection_engine())
    cached = get_data()
    code = """
    @st.cache_data()
    def get_data():
        return pd.read_sql("SELECT * FROM reporting.fake_transactions_long", con=postgres_connection_engine())
    cached = get_data()
    """
    st.code(code, language="python")
    st.dataframe(cached.head(10))

    
    st.markdown("### Uncached")
    uncached = pd.read_sql("SELECT * FROM reporting.fake_transactions_long", con=postgres_connection_engine())
    code = """
    uncached = pd.read_sql("SELECT * FROM reporting.fake_transactions_long", con=postgres_connection_engine())
    """
    st.code(code, language="python")
    st.dataframe(uncached.head(10))

with st.expander("Caching extends beyond data"):
    st.image('https://docs.streamlit.io/images/caching-high-level-diagram.png')

    

