import streamlit as st

st.markdown("""
## Multipage Apps
""")

with st.expander("How multipage apps used to be structured:"):
  st.code("""
  your_working_directory/
  ├── pages/
  │   ├── a_page.py
  │   └── another_page.py
  └── your_homepage.py
  """)

with st.expander("How multipage apps are now structured:"):
  st.markdown("""
  Single entry point acting as a router (e.g. `main.py`)
  """)
  st.code("""
  your_working_directory/
  ├── directory1/
  │   ├── page.py
  │   └── another_page.py
  ├── directory2/
  │   ├── page.py
  │   └── another_page.py        
  └── main.py
  """)
  st.markdown("""`main.py`""")
  st.code("""

  ## Directory1
  dir1_page = st.Page("directory1/page.py", title="Page Title", default=True)
  dir1_another_page = st.Page("directory1/another_page.py", title="Page Title")

  ## Directory1
  dir2_page = st.Page("directory2/page.py", title="Page Title", default=True)
  dir2_another_page = st.Page("directory2/another_page.py", title="Page Title")
          
  navigation_dictionary = {
    "Directory 1": [dir1_page, dir1_another_page],
    "Directory 2": [dir2_page, dir2_another_page],  
  }]
          
  pg = st.navigation(navigation_dictionary)
  pg.run()
  """)