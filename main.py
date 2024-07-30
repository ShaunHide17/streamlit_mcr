import streamlit as st

st.set_page_config(page_title="Home", page_icon="", layout="wide")

## Core
data_and_caching = st.Page("core/01_data_and_caching.py", title="Data & Caching", default=True)
display_and_crossfiltering = st.Page("core/02_display_and_crossfiltering.py", title="Display & Cross-filtering")

## Extended
state_and_params = st.Page("extended/03_state_and_params.py", title="State & Params")
authentication = st.Page("extended/04_authentication.py", title="Authentication")
multipage_apps = st.Page("extended/05_multipage_apps.py", title="Multipage Apps")
customisation = st.Page("extended/06_customisation.py", title="Customisation")


navigation_dictionary = {
  "Core": [data_and_caching, display_and_crossfiltering],
  "Extended": [state_and_params, authentication, multipage_apps, customisation],  
}

pg = st.navigation(navigation_dictionary)
pg.run()