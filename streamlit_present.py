import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="WIP Analysis Dashboard", 
                   layout="wide",
                   initial_sidebar_state="expanded",
                   page_icon=":watch:")


# Create sidebar tabs
st.sidebar.markdown("<h1 style='font-size:30px;'>Chart Selection Box</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("Select the chart type:", ["Interactive Bar Chart", 'Interactive Line Chart', "Line Chart", "Pie Chart"])


# Load data
data = pd.read_csv('wip.csv')
data.columns = ['production_line', 'work_order_IDs', 'product_type', 'timestamps', 'Station', 'WIP_quantity'] 
data['timestamps'] = pd.to_datetime(data['timestamps'])


# Start 

if page == "Interactive Bar Chart":
    st.title("Interactive Bar Chart")
    
    # Create all possible combinations
    
    timestamps = data['timestamps'].unique()
    work_orders = data['work_order_IDs'].unique()
    stations = data['Station'].unique()

    all_combinations = pd.MultiIndex.from_product([work_orders, stations, timestamps], names=['work_order_IDs', 'Station', 'timestamps']).to_frame(index=False)
    df_full = pd.merge(all_combinations, data, on=['work_order_IDs', 'Station', 'timestamps'], how='left').fillna(0)
    
    mapping = {
        'WO002': {'production_line': 'Line1', 'product_type': 'TYPEB'},
        'WO004': {'production_line': 'Line2', 'product_type': 'TYPEB'},
        'WO001': {'production_line': 'Line1', 'product_type': 'TYPEA'},
        'WO003': {'production_line': 'Line2', 'product_type': 'TYPEC'}
    }
    
    df_full['production_line'] = df_full['work_order_IDs'].map(lambda x: mapping[x]['production_line'] if x in mapping else None)
    df_full['product_type'] = df_full['work_order_IDs'].map(lambda x: mapping[x]['product_type'] if x in mapping else None)
    
    #--------------------------------------------------------START Draw------------------------------------------------------------------------
    
    # First interactive chart
    st.subheader("Changes in WIP over a period of time by production line") 
    fig1 = px.bar(df_full, x='Station', y='WIP_quantity',
                 animation_frame='timestamps',  
                 color='product_type',  
                 facet_col='production_line', 
                 labels={'work_order_IDs': 'Work Order IDs', 'WIP_quantity': 'WIP Quantity', 'product_type': 'Product Type', 'Station': 'Station'},
    )
    fig1.update_layout(
        xaxis_title='Station',
        yaxis_title='WIP Quantity',
        legend_title='Product Type',
        width=1000,
        height=600,
    )
    fig1.update_yaxes(range=[0, 1000])
    
    st.plotly_chart(fig1)

    # Second interactive chart 
    st.subheader("Changes in WIP over a period of time by Work Order IDs")
    fig2 = px.bar(df_full, x='Station', y='WIP_quantity',
                 animation_frame='timestamps',  
                 color='product_type',  
                 facet_col='work_order_IDs', 
                 labels={'work_order_IDs': 'Work Order IDs', 'WIP_quantity': 'WIP Quantity', 'product_type': 'Product Type', 'Station': 'Station'}
    )
    fig2.update_layout(
        xaxis_title='Station',
        yaxis_title='WIP Quantity',
        legend_title='Product Type',
        width=1000,
        height=600,
    )
    fig2.update_yaxes(range=[0, 1000])
    
    st.plotly_chart(fig2)
    
    #--------------------------------------------------------End Draw--------------------------------------------------------------------------
    
    
elif page == "Interactive Line Chart":      
    st.title("Interactive Line Chart")

    production_lines = data['production_line'].unique()
    work_order_ids = data['work_order_IDs'].unique()

    # Set default values
    default_line = production_lines[0]
    default_work_order = work_order_ids[0]
  
    # Select production line and work order
    selected_line = st.selectbox("Select Production Line", production_lines, index=0)
    selected_work_order = st.selectbox("Select Work Order", work_order_ids, index=0)

    filtered_data = data[(data['production_line'] == selected_line) & (data['work_order_IDs'] == selected_work_order)]

    #--------------------------------------------------------START Draw------------------------------------------------------------------------
    
    if not filtered_data.empty:
        # Plot line chart
        st.subheader("Production Line: {}, Work Order: {}".format(selected_line, selected_work_order))
        fig = px.line(filtered_data, x='timestamps', y='WIP_quantity', color='Station',
                      labels={'timestamps': 'Time', 'WIP_quantity': 'WIP Quantity'},
                      markers=True)
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='WIP Quantity',
            legend_title='Station',
            width=800,
            height=600,
        )
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected production line and work order.")
        
    #--------------------------------------------------------End Draw--------------------------------------------------------------------------
    

elif page == "Line Chart":
    st.title("WIP Quantity Over Time by Station")
    
    df_line1_work1 = data[(data['production_line'] == 'Line1') & (data['work_order_IDs'] == 'WO001')]
    df_line1_work2 = data[(data['production_line'] == 'Line1') & (data['work_order_IDs'] == 'WO002')]
    df_line2_work3 = data[(data['production_line'] == 'Line2') & (data['work_order_IDs'] == 'WO003')]
    df_line2_work4 = data[(data['production_line'] == 'Line2') & (data['work_order_IDs'] == 'WO004')]

    datasets = [df_line1_work1, df_line1_work2, df_line2_work3, df_line2_work4]
    titles = ['Line 1, Work 1', 'Line 1, Work 2', 'Line 2, Work 3', 'Line 2, Work 4']
    
    #--------------------------------------------------------START Draw------------------------------------------------------------------------
    
    # Line1 (Work01 & Work02)
    st.subheader("Production Line 1") 
    subcols1 = st.columns(2)
    for j in range(2):
        index = j
        if index < len(datasets):
            with subcols1[j]:
                plt.figure(figsize=(10, 6))
                d = datasets[index]
                for station in d['Station'].unique():
                    station_data = d[d['Station'] == station]
                    plt.plot(station_data['timestamps'], station_data['WIP_quantity'], label=station)
                plt.xlabel('Time')
                plt.ylabel('WIP Quantity')
                plt.title(titles[index])
                plt.legend(title='Station')
                plt.grid(True)
                st.pyplot(plt)
                plt.clf()
    
    # Line2 (Work03 & Work04)
    st.subheader("Production Line 2") 
    subcols3 = st.columns(2)
    for j in range(2):
        index = 2 + j
        if index < len(datasets):
            with subcols3[j]:
                plt.figure(figsize=(10, 6))
                d = datasets[index]
                for station in d['Station'].unique():
                    station_data = d[d['Station'] == station]
                    plt.plot(station_data['timestamps'], station_data['WIP_quantity'], label=station)
                plt.xlabel('Time')
                plt.ylabel('WIP Quantity')
                plt.title(titles[index])
                plt.legend(title='Station')
                plt.grid(True)
                st.pyplot(plt)
                plt.clf()
                
    #--------------------------------------------------------End Draw--------------------------------------------------------------------------


elif page == "Pie Chart":
    
    st.title("WIP Quantity Distribution by Production Line")
    
    max_wip_data = data.groupby(['production_line', 'work_order_IDs', 'product_type'])['WIP_quantity'].max().reset_index()
    color_map = {'TYPEA': '#66b3ff', 'TYPEB': '#ff9999', 'TYPEC': '#99ff99'}
    lines = max_wip_data['production_line'].unique()
    
    
    #--------------------------------------------------------START Draw------------------------------------------------------------------------
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 8))
    for i, line in enumerate(lines):
        line_data = max_wip_data[max_wip_data['production_line'] == line]
        
        labels = line_data['work_order_IDs']
        sizes = line_data['WIP_quantity']
        colors = [color_map[p] for p in line_data['product_type']]
        
        wedges, texts, autotexts = ax[i].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax[i].set_title(f'WIP Quantity Distribution for {line}')
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[p], markersize=10, label=p) for p in color_map]
        ax[i].legend(handles=handles, title='Product Type', loc='best')

    plt.tight_layout()
    st.pyplot(fig)
    
    #--------------------------------------------------------End Draw--------------------------------------------------------------------------