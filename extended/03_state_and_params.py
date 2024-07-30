import streamlit as st


st.markdown("""
## Session State and Params
""")

with st.container():
  col1, col2 = st.columns(2)

  with col1:
    st.markdown("""
    Streamlit has a default execution model which refreshes the entire page on every component 
    interaction. This can be problematic when you want to maintain "state" across multiple interactions.
    Or share a view of data between users.
                
    Example problems:
      - A user wants to navigate between pages but not lose filter selections
      - A user wants to refresh a page but not lose filter selections
      - A user wants to share the interactive view with a colleague
                
    Caching does not solve these problems... but session state and url parameters can.
    """
    )

selection_list = ["A","B","C","D","E"]
st.divider()
with st.container():
  col1, col2 = st.columns(2)
  with col1:
    select = st.selectbox(
      'No pertistence between app navigation',
      selection_list
    )
    if st.checkbox('Code',key='code1'):
      st.code("""
      select = st.selectbox(
        'No pertistence between app navigation',
        selection_list
      )
      """)

  with col2:
    if "selected_item" not in st.session_state:
      st.session_state['selected_item'] = 'A'

    def update_selected_item():
      st.session_state['selected_item'] = st.session_state['persisted_between_navigation']

    select = st.selectbox(
      'Session state persists between app navigation',
      selection_list,
      index = selection_list.index(st.session_state['selected_item']),
      key = 'persisted_between_navigation',
      on_change =  update_selected_item
    )
    if st.checkbox('Code',key='code2'):
      st.code("""
      if "selected_item" not in st.session_state:
        st.session_state['selected_item'] = 'A'

      def update_selected_item():
        st.session_state['selected_item'] = st.session_state['item']

      select = st.selectbox(
        'Session state persists between app navigation',
        selection_list,
        index = selection_list.index(st.session_state['selected_item']),
        key = 'persisted_between_navigation',
        on_change =  update_selected_item
      )
      """)

st.divider()
with st.container():
  col1, col2 = st.columns(2)
  with col1:
    select = st.selectbox(
      'No pertistence between refreshes',
      selection_list,
      key = 'no_persistence_between_refreshes',
    )
    if st.checkbox('Code',key='code3'):
      st.code("""
      select = st.selectbox(
        'No pertistence between refreshes',
        selection_list,
        key = 'no_persistence_between_refreshes',
      )
      """)

  with col2:

    # Instantiate the session state
    if "persisted_item" not in st.session_state:
      st.session_state['persisted_item'] = 'A'

    # Update the session state
    if "persisted_item" in st.query_params:
      st.session_state['persisted_item'] = st.query_params['persisted_item']

    def update_persisted_item():
      st.session_state['persisted_item'] = st.session_state['persistence_between_refreshes']
      st.query_params['persisted_item'] = st.session_state['persisted_item']

    select = st.selectbox(
      'Persistence between refreshes',
      selection_list,
      index = selection_list.index(st.session_state['persisted_item']),
      key = 'persistence_between_refreshes', 
      on_change = update_persisted_item
    )
    if st.checkbox('Code',key='code4'):
      st.code("""
      # Instantiate the session state
      if "persisted_item" not in st.session_state:
        st.session_state['persisted_item'] = 'A'

      # Update the session state
      if "persisted_item" in st.query_params:
        st.session_state['persisted_item'] = st.query_params['persisted_item']

      def update_persisted_item():
        st.session_state['persisted_item'] = st.session_state['persistence_between_refreshes']
        st.query_params['persisted_item'] = st.session_state['persisted_item']

      select = st.selectbox(
        'Persistence between refreshes',
        selection_list,
        index = selection_list.index(st.session_state['persisted_item']),
        key = 'persistence_between_refreshes', 
        on_change = update_persisted_item
      )
      """)
  st.markdown("Note: experimental_get_query_params() and experimental_set_query_params() were deprecated in 1.30.0")