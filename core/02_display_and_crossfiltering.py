import streamlit as st
import pandas as pd

import altair as alt

from generic.database import postgres_connection_engine

st.markdown("""
## Displaying Data, Filtering and Cross Filtering
""")

@st.cache_data()
def get_data():
    return pd.read_sql("SELECT * FROM reporting.fake_transactions", con=postgres_connection_engine())
data = get_data()

st.markdown("### `st.dataframe` has a lot of flexibility")
with st.expander(""):
  with st.container():
      col1, col2 = st.columns(2)
      with col1:
          st.dataframe(data)
          st.code("""
          st.dataframe(data)
          """, language = "python")
       
      with col2:
        st.dataframe(
          data
          , column_config = {
            'account_number': st.column_config.Column(
              "Account #", 
              help = 'Which account the purchase occurred from',
            ),
            'company': st.column_config.Column(
              "Company", 
              help = 'Where the purchase occurred',
            ),
            'transaction_amount': st.column_config.NumberColumn(
              "Amount (£)", 
              help = 'Size of the transaction in GBP',
              format="£%.2f",
            ),
            'transaction_date': st.column_config.Column(
              "Date", 
              help = 'When the transaction occurred',
            ),
          }
          , hide_index = True
          , use_container_width = True
        )
        st.code("""
        st.dataframe(
          data
          , column_config = {
            'account_number': st.column_config.Column(
              "Account #", 
              help = 'Which account the purchase occurred from',
            ),
            'company': st.column_config.Column(
              "Company", 
              help = 'Where the purchase occurred',
            ),
            'transaction_amount': st.column_config.NumberColumn(
              "Amount (£)", 
              help = 'Size of the transaction in GBP',
              format="£%.2f",
            ),
            'transaction_date': st.column_config.Column(
              "Date", 
              help = 'When the transaction occurred',
            ),
          }
          , hide_index = True
          , use_container_width = True
        )""", language = "python") 

st.markdown("### Filters can be added to the dataframes")
with st.expander(""):
  
  companies = st.multiselect(
      label = 'Companies Filter', 
      options = data['company'].unique(),
      default = data['company'].unique()
  )
  dates = st.slider(
      label = 'Date Filter', 
      min_value = data['transaction_date'].min(), 
      max_value = data['transaction_date'].max(), 
      value = (data['transaction_date'].min(), data['transaction_date'].max())
  )
  filtered = (
     data[
      (data['company'].isin(companies)) & 
      (data['transaction_date'] >= dates[0]) & 
      (data['transaction_date'] <= dates[1])
     ]
  )

  st.dataframe(
    filtered
    , column_config = {
      'account_number': st.column_config.Column(
        "Account #", 
        help = 'Which account the purchase occurred from',
      ),
      'company': st.column_config.Column(
        "Company", 
        help = 'Where the purchase occurred',
      ),
      'transaction_amount': st.column_config.NumberColumn(
        "Amount (£)", 
        help = 'Size of the transaction in GBP',
        format="£%.2f",
      ),
      'transaction_date': st.column_config.Column(
        "Date", 
        help = 'When the transaction occurred',
      ),
    }
    , hide_index = True
    , use_container_width = True
  )
  st.write(f'Data: {data.shape[0]} rows')      
  st.write(f'Data: {filtered.shape[0]} rows')

st.markdown("### Cross filtering works*")
with st.expander(""):
  with st.container():
    col1 , col2 = st.columns(2)
    with col1:
      st.markdown("Altair supports cross filtering out of the box, so is the preferred option")

      # Create a selection object for the brush
      brush = alt.selection_single(fields=['company'], empty='none')

      # Create a bar chart showing transaction amounts by company
      company_chart = alt.Chart(data).mark_bar().encode(
        x='company:O',
        y='sum(transaction_amount):Q',
        color=alt.condition(brush, alt.value('orange'), alt.value('steelblue')),  # Change the colors as needed
        tooltip=['company', 'sum(transaction_amount)']
      ).add_params(
          brush
      ).properties(
          title='Amount by Company'
      )

      # Aggregate data to get sum of transaction_amount by account_number
      sum_by_account = data.groupby(['company', 'account_number']).transaction_amount.sum().reset_index()

      # Create a table showing the sum of transaction amounts by account number
      table = alt.Chart(sum_by_account).mark_text(align='center', color='white').encode(
        y=alt.Y('account_number:O', axis=alt.Axis(title='Account Number')),
        text='transaction_amount:Q',
        tooltip=['account_number', 'transaction_amount']
      ).transform_filter(
          brush
      ).properties(
          title='Amount by Account Number',
          width=300  # Adjust the width as needed
      )

      # Create an empty chart to display when no selection is made
      empty_chart = alt.Chart().mark_text(
          align='center',
          baseline='middle',
          size=20,
          color='gray'
      ).encode(
          text='text:N'
      ).properties(
          width=300,
          title=''
      )

      final_chart = alt.vconcat(
          company_chart,
          alt.layer(
            table.transform_filter(brush),
            empty_chart.transform_filter(~brush)
          )
          ).resolve_legend(
              color='independent'
          )

      # Show the chart
      st.altair_chart(final_chart)
    
    with col2:
      st.markdown("If you prefer plotly then `streamlit-plotly-events` can be used to achieve the same effect.")