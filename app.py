import streamlit as st
import pandas as pd
import plotly.express as px

# Load IPL dataset
df =  pd.read_csv('IPL_2023-22_Sold_Players.csv')

# Remove commas from 'Price' column and convert to numeric
df['Price'] = df['Price'].str.replace(',', '').astype(float)

# Sidebar tabs
selected_tab = st.sidebar.radio("Navigation", ["Dashboard", "Data", "Insights"])

# Display content based on selected tab
if selected_tab == "Dashboard":
   st.write("## Welcome to the Dashboard")
   st.title(''':red[IPL] :orange[Data] :green[Dynamo] : :blue[Comprehensive] :violet[Insights] :gray[Dashboard]''')
   st.image('IPLLOGO.jpg')
    # Add dashboard content here

elif selected_tab == "Data":
    st.write("## IPL Data Overview")
    if st.checkbox('Show Raw Data'):
        st.dataframe(df)
    # Display raw data if checkbox is checked


    # Sidebar filters
        nationality_filter = st.sidebar.selectbox('Filter by Nationality', df['Nationality'].unique())
        type_filter = st.sidebar.selectbox('Filter by Type', df['Type'].unique())

        # Apply filters
        filtered_df = df[(df['Nationality'] == nationality_filter) & (df['Type'] == type_filter)]

        # Display filtered data
        st.write('### Filtered Data:')
        st.write(filtered_df)  # Display the IPL dataset


elif selected_tab == "Insights":
    st.write("## IPL Insights")
    # Apply filters and create filtered DataFrame
    team_filter = st.sidebar.selectbox('Filter by Team', df['Team'].unique())
    selected_types = st.sidebar.multiselect('Select Player Types', df['Type'].unique())

    if selected_types:
        filtered_df = df[df['Team'] == team_filter]
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_types)]

        if not filtered_df.empty:
            # Group by player type and calculate the total spend
            player_type_spend = filtered_df.groupby('Type')['Price'].sum().reset_index()

            # Create bar plot
            st.write("### Bar Plot")
            fig_bar = px.bar(player_type_spend, x='Type', y='Price', title=f'Total Spend by Player Type for {team_filter}', labels={'Price': 'Total Spend', 'Type': 'Player Type'})
            st.plotly_chart(fig_bar)

            # Create pie chart
            st.write("### Pie Chart")
            fig_pie = px.pie(player_type_spend, values='Price', names='Type', title=f'Spend Distribution by Player Type for {team_filter}', labels={'Type': 'Player Type'})
            st.plotly_chart(fig_pie)
        else:
            st.write("No data available for the selected filters.")
    else:
        st.write("Please select at least one player type.")



