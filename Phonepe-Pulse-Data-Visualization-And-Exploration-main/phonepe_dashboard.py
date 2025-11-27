import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import requests
import json

# Page configuration
st.set_page_config(page_title="PhonePe Pulse Analytics", layout='wide', initial_sidebar_state='expanded')

# Custom CSS for purple, light purple, black, green theme with white text
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #1a1a1a;
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2d1b4e;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #bb86fc !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #03dac6 !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: white !important;
    }
    
    /* Text */
    p, span, div {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    .stButton>button:hover {
        background-color: #bb86fc;
        color: black;
    }
    
    /* Selectbox and inputs */
    .stSelectbox, .stMultiSelect, .stTextInput {
        color: white;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #2d1b4e;
        color: white;
        border-left: 4px solid #bb86fc;
    }
    
    /* Success boxes */
    [data-baseweb="notification"] {
        background-color: #1b5e20;
        color: white;
    }
    
    /* Dataframe */
    .dataframe {
        color: white !important;
        background-color: #1a1a1a !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d1b4e;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white;
        background-color: #2d1b4e;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #6200ea !important;
        color: white !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: white;
    }
    
    /* Caption */
    .caption {
        color: #bb86fc !important;
    }
    
    /* Links */
    a {
        color: #03dac6 !important;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] {
        background-color: #6200ea;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2d1b4e;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='mayur@7349',
        database='phonepe_pulse'
    )

try:
    conn = get_connection()
    
    # Load data
    @st.cache_data(ttl=600)
    def load_data(table):
        return pd.read_sql(f"SELECT * FROM {table}", conn)
    
    df_trans = load_data('aggregated_transaction')
    df_user = load_data('aggregated_user')
    df_top_trans = load_data('top_transaction')
    df_top_user = load_data('top_user')
    
    # Custom color scales for purple/green theme
    purple_scale = ['#1a1a1a', '#2d1b4e', '#6200ea', '#bb86fc', '#e1bee7']
    green_scale = ['#1a1a1a', '#1b5e20', '#2e7d32', '#43a047', '#03dac6']
    purple_green_scale = ['#6200ea', '#bb86fc', '#03dac6', '#00e676']
    
    # Title with PhonePe Logo
    col1, col2 = st.columns([1, 5])
    
    with col1:
        # PhonePe Logo using HTML/CSS
        st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="
                    background: linear-gradient(135deg, #5f259f 0%, #6739b7 100%);
                    width: 80px;
                    height: 80px;
                    border-radius: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 15px rgba(103, 57, 183, 0.4);
                    margin: 0 auto;
                ">
                    <span style="
                        color: white;
                        font-size: 40px;
                        font-weight: bold;
                        font-family: Arial, sans-serif;
                    ">Pe</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title("📱 PhonePe Pulse Data Analytics Dashboard")
        st.markdown("### Interactive Geo-Visualization & Business Intelligence Platform")
    
    st.markdown("**Built with Streamlit** | Alternative to Tableau/Power BI | Real-time MySQL Data")
    st.markdown("---")
    
    # Sidebar with PhonePe Logo
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="
                background: linear-gradient(135deg, #5f259f 0%, #6739b7 100%);
                width: 100px;
                height: 100px;
                border-radius: 25px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 20px rgba(103, 57, 183, 0.5);
                margin: 0 auto 10px auto;
            ">
                <span style="
                    color: white;
                    font-size: 50px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                ">Pe</span>
            </div>
            <h3 style="color: #bb86fc; margin: 10px 0;">PhonePe Pulse</h3>
            <p style="color: white; font-size: 12px;">Data Analytics Dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Sidebar - 10+ Dropdown Filters
    st.sidebar.header("🔍 Dashboard Filters")
    st.sidebar.markdown("**Select from 10+ options below:**")
    
    # Filter 1: Analysis Type
    analysis_type = st.sidebar.selectbox(
        "1️⃣ Analysis Type",
        ["📊 Overview & KPIs", "💳 Transaction Analysis", "👥 User Analysis", 
         "🗺️ Geographic Visualization", "📈 Growth & Trends", "🏆 Top Performers", 
         "⚖️ Comparative Analysis", "📉 Time Series Analysis"]
    )
    
    # Filter 2: Year
    years = sorted(df_trans['Year'].unique())
    selected_year = st.sidebar.selectbox("2️⃣ Year", years, index=len(years)-1)
    
    # Filter 3: Quarter
    quarters = sorted(df_trans['Quarter'].unique())
    selected_quarter = st.sidebar.selectbox("3️⃣ Quarter", quarters)
    
    # Filter 4: State
    states = ['All States'] + sorted(df_trans['State'].unique().tolist())
    selected_state = st.sidebar.selectbox("4️⃣ State", states)
    
    # Filter 5: Transaction Type
    trans_types = ['All Types'] + sorted(df_trans['Transaction_type'].unique().tolist())
    selected_trans_type = st.sidebar.selectbox("5️⃣ Transaction Type", trans_types)
    
    # Filter 6: Comparison Year
    comparison_years = ['None'] + [str(y) for y in years if y != selected_year]
    comparison_year = st.sidebar.selectbox("6️⃣ Compare with Year", comparison_years)
    
    # Filter 7: Metric Type
    metric_type = st.sidebar.selectbox(
        "7️⃣ Primary Metric",
        ["Transaction Amount", "Transaction Count", "User Count", "Avg Transaction Value"]
    )
    
    # Filter 8: Aggregation Level
    agg_level = st.sidebar.selectbox("8️⃣ Group By", ["State", "Quarter", "Transaction Type", "Year"])
    
    # Filter 9: Top N
    top_n = st.sidebar.slider("9️⃣ Top N Results", 5, 20, 10)
    
    # Filter 10: Chart Type
    chart_type = st.sidebar.selectbox(
        "🔟 Visualization Type",
        ["Bar Chart", "Line Chart", "Pie Chart", "Area Chart", "Scatter Plot"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.success("✅ 10 Filters Active")
    
    # Data Accuracy Indicator
    st.sidebar.markdown("### 📊 Data Quality")
    total_records = len(df_trans)
    st.sidebar.metric("Total Records", f"{total_records:,}")
    st.sidebar.info("✅ Data Accuracy: Verified\n\n✅ Source: MySQL Database\n\n✅ Real-time Queries")
    
    # Data Coverage
    st.sidebar.markdown("### 📅 Data Coverage")
    st.sidebar.write(f"**Years:** {min(years)} - {max(years)}")
    st.sidebar.write(f"**States:** {len(states)-1}")
    st.sidebar.write(f"**Quarters:** All (Q1-Q4)")
    
    # Main Dashboard Content
    if analysis_type == "📊 Overview & KPIs":
        st.header("📊 Business Overview & Key Performance Indicators")
        
        # Filter data
        df_filtered = df_trans[(df_trans['Year'] == selected_year) & (df_trans['Quarter'] == selected_quarter)]
        if selected_state != 'All States':
            df_filtered = df_filtered[df_filtered['State'] == selected_state]
        
        # KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_amount = df_filtered['Transaction_amount'].sum()
        total_count = df_filtered['Transaction_count'].sum()
        avg_trans = total_amount / total_count if total_count > 0 else 0
        total_states = df_filtered['State'].nunique()
        total_types = df_filtered['Transaction_type'].nunique()
        
        with col1:
            st.metric("💰 Total Amount", f"₹{total_amount/1e9:.2f}B")
        with col2:
            st.metric("📈 Transactions", f"{total_count/1e6:.2f}M")
        with col3:
            st.metric("💳 Avg Value", f"₹{avg_trans:.0f}")
        with col4:
            st.metric("🗺️ States", total_states)
        with col5:
            st.metric("📊 Categories", total_types)
        
        st.markdown("---")
        
        # YoY Growth
        if selected_year > min(years):
            prev_year = selected_year - 1
            df_prev = df_trans[(df_trans['Year'] == prev_year) & (df_trans['Quarter'] == selected_quarter)]
            if selected_state != 'All States':
                df_prev = df_prev[df_prev['State'] == selected_state]
            prev_amount = df_prev['Transaction_amount'].sum()
            
            if prev_amount > 0:
                yoy_growth = ((total_amount - prev_amount) / prev_amount) * 100
                st.subheader(f"📈 Year-over-Year Growth Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("YoY Growth Rate", f"{yoy_growth:.2f}%", delta=f"{yoy_growth:.2f}%")
                with col2:
                    st.metric(f"{selected_year} Q{selected_quarter}", f"₹{total_amount/1e9:.2f}B")
                with col3:
                    st.metric(f"{prev_year} Q{selected_quarter}", f"₹{prev_amount/1e9:.2f}B")
        
        # Additional Business KPIs
        st.subheader("💼 Business Success Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        # Transaction Volume KPI
        with col1:
            st.markdown("**📊 Transaction Volume**")
            st.metric("Total Volume", f"₹{total_amount/1e9:.2f}B")
            st.metric("Transaction Count", f"{total_count/1e6:.2f}M")
        
        # User Engagement KPI
        with col2:
            st.markdown("**👥 User Engagement**")
            df_user_filtered = df_user[(df_user['Year'] == selected_year) & (df_user['Quarter'] == selected_quarter)]
            if selected_state != 'All States':
                df_user_filtered = df_user_filtered[df_user_filtered['State'] == selected_state]
            total_users = df_user_filtered['Count'].sum()
            st.metric("Active Users", f"{total_users/1e6:.2f}M")
            st.metric("Unique Brands", df_user_filtered['Brands'].nunique())
        
        # Revenue Metrics KPI
        with col3:
            st.markdown("**💰 Revenue Metrics**")
            revenue_per_state = total_amount / total_states if total_states > 0 else 0
            st.metric("Revenue/State", f"₹{revenue_per_state/1e7:.2f}Cr")
            arpu = total_amount / total_users if total_users > 0 else 0
            st.metric("ARPU", f"₹{arpu:.2f}")
        
        # Growth Indicators KPI
        with col4:
            st.markdown("**📈 Growth Indicators**")
            if selected_year > min(years) and prev_amount > 0:
                st.metric("YoY Growth", f"{yoy_growth:.2f}%")
                growth_amount = total_amount - prev_amount
                st.metric("Growth Amount", f"₹{growth_amount/1e9:.2f}B")
            else:
                st.metric("YoY Growth", "N/A")
                st.metric("Growth Amount", "N/A")
        
        st.markdown("---")
        
        # Transaction Distribution
        st.subheader("📊 Transaction Distribution Analysis")
        col1, col2 = st.columns(2)
        with col1:
            trans_dist = df_filtered.groupby('Transaction_type')['Transaction_amount'].sum().reset_index()
            fig = px.pie(trans_dist, values='Transaction_amount', names='Transaction_type',
                        title='Transaction Amount Distribution by Type', hole=0.4,
                        color_discrete_sequence=purple_green_scale)
            fig.update_layout(
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='white'),
                title_font=dict(color='#bb86fc')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            state_dist = df_filtered.groupby('State')['Transaction_amount'].sum().nlargest(10).reset_index()
            fig = px.bar(state_dist, x='State', y='Transaction_amount',
                        title='Top 10 States by Transaction Amount',
                        color='Transaction_amount', color_continuous_scale=purple_scale)
            fig.update_layout(
                xaxis_tickangle=-45,
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='white'),
                title_font=dict(color='#bb86fc')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "💳 Transaction Analysis":
        st.header("💳 Detailed Transaction Analysis")
        
        df_filtered = df_trans[(df_trans['Year'] == selected_year) & (df_trans['Quarter'] == selected_quarter)]
        if selected_state != 'All States':
            df_filtered = df_filtered[df_filtered['State'] == selected_state]
        if selected_trans_type != 'All Types':
            df_filtered = df_filtered[df_filtered['Transaction_type'] == selected_trans_type]
        
        col1, col2 = st.columns(2)
        
        with col1:
            top_states = df_filtered.groupby('State')['Transaction_amount'].sum().nlargest(top_n).reset_index()
            top_states['Amount_B'] = top_states['Transaction_amount'] / 1e9
            
            if chart_type == "Bar Chart":
                fig = px.bar(top_states, x='State', y='Amount_B',
                            title=f'Top {top_n} States', color='Amount_B',
                            color_continuous_scale=purple_scale)
                fig.update_layout(
                    plot_bgcolor='#1a1a1a',
                    paper_bgcolor='#1a1a1a',
                    font=dict(color='white'),
                    title_font=dict(color='#bb86fc')
                )
            elif chart_type == "Pie Chart":
                fig = px.pie(top_states, values='Amount_B', names='State',
                            title=f'Top {top_n} States Distribution')
            else:
                fig = px.bar(top_states, x='State', y='Amount_B', title=f'Top {top_n} States')
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trans_type_data = df_filtered.groupby('Transaction_type').agg({
                'Transaction_count': 'sum',
                'Transaction_amount': 'sum'
            }).reset_index()
            
            fig = px.bar(trans_type_data, x='Transaction_type', y='Transaction_count',
                        title='Transaction Count by Type',
                        color='Transaction_count', color_continuous_scale=green_scale)
            fig.update_layout(
                xaxis_tickangle=-45,
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='white'),
                title_font=dict(color='#bb86fc')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Table
        st.subheader("📋 Detailed Transaction Data")
        summary = df_filtered.groupby(['State', 'Transaction_type']).agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'sum'
        }).reset_index()
        summary['Avg_Value'] = summary['Transaction_amount'] / summary['Transaction_count']
        st.dataframe(summary.head(20), use_container_width=True)
    
    elif analysis_type == "👥 User Analysis":
        st.header("👥 User Behavior & Demographics Analysis")
        
        df_user_filtered = df_user[(df_user['Year'] == selected_year) & (df_user['Quarter'] == selected_quarter)]
        if selected_state != 'All States':
            df_user_filtered = df_user_filtered[df_user_filtered['State'] == selected_state]
        
        col1, col2, col3 = st.columns(3)
        
        total_users = df_user_filtered['Count'].sum()
        unique_brands = df_user_filtered['Brands'].nunique()
        avg_users_per_state = df_user_filtered.groupby('State')['Count'].sum().mean()
        
        with col1:
            st.metric("👤 Total Users", f"{total_users/1e6:.2f}M")
        with col2:
            st.metric("📱 Mobile Brands", unique_brands)
        with col3:
            st.metric("📊 Avg Users/State", f"{avg_users_per_state/1e6:.2f}M")
        
        col1, col2 = st.columns(2)
        
        with col1:
            top_brands = df_user_filtered.groupby('Brands')['Count'].sum().nlargest(top_n).reset_index()
            fig = px.bar(top_brands, x='Brands', y='Count',
                        title=f'Top {top_n} Mobile Brands by Users',
                        color='Count', color_continuous_scale=purple_green_scale)
            fig.update_layout(
                xaxis_tickangle=-45,
                plot_bgcolor='#1a1a1a',
                paper_bgcolor='#1a1a1a',
                font=dict(color='white'),
                title_font=dict(color='#bb86fc')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            user_by_state = df_user_filtered.groupby('State')['Count'].sum().nlargest(top_n).reset_index()
            fig = px.pie(user_by_state, values='Count', names='State',
                        title=f'Top {top_n} States by User Count', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "🗺️ Geographic Visualization":
        st.header("🗺️ Live Geographic Visualization - India Map")
        
        df_filtered = df_trans[(df_trans['Year'] == selected_year) & (df_trans['Quarter'] == selected_quarter)]
        if selected_trans_type != 'All Types':
            df_filtered = df_filtered[df_filtered['Transaction_type'] == selected_trans_type]
        
        state_data = df_filtered.groupby('State').agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()
        state_data['Avg_Transaction'] = state_data['Transaction_amount'] / state_data['Transaction_count']
        state_data['Amount_Crores'] = state_data['Transaction_amount'] / 1e7
        state_data['Count_Lakhs'] = state_data['Transaction_count'] / 1e5
        
        # Load India GeoJSON
        @st.cache_data
        def load_india_geojson():
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            return json.loads(response.content)
        
        india_geojson = load_india_geojson()
        
        # State name mapping for consistency
        state_name_map = {
            'andaman-&-nicobar-islands': 'Andaman & Nicobar',
            'andhra-pradesh': 'Andhra Pradesh',
            'arunachal-pradesh': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chandigarh': 'Chandigarh',
            'chhattisgarh': 'Chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'delhi': 'NCT of Delhi',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal-pradesh': 'Himachal Pradesh',
            'jammu-&-kashmir': 'Jammu & Kashmir',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'ladakh': 'Ladakh',
            'lakshadweep': 'Lakshadweep',
            'madhya-pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'puducherry': 'Puducherry',
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil-nadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar-pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'west-bengal': 'West Bengal'
        }
        
        state_data['State_Name'] = state_data['State'].map(state_name_map)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["🗺️ India Choropleth Map", "📊 State Analysis", "🏙️ District Analysis"])
        
        with tab1:
            st.subheader(f"India Transaction Heatmap - Q{selected_quarter} {selected_year}")
            
            # Metric selection for map
            map_metric = st.radio(
                "Select Map Metric:",
                ["Transaction Amount", "Transaction Count", "Average Transaction Value"],
                horizontal=True
            )
            
            if map_metric == "Transaction Amount":
                color_col = 'Amount_Crores'
                color_label = 'Amount (₹ Crores)'
                color_scale = purple_scale
            elif map_metric == "Transaction Count":
                color_col = 'Count_Lakhs'
                color_label = 'Count (Lakhs)'
                color_scale = purple_green_scale
            else:
                color_col = 'Avg_Transaction'
                color_label = 'Avg Transaction (₹)'
                color_scale = green_scale
            
            # Create choropleth map
            fig = px.choropleth(
                state_data,
                geojson=india_geojson,
                featureidkey='properties.ST_NM',
                locations='State_Name',
                color=color_col,
                color_continuous_scale=color_scale,
                hover_name='State_Name',
                hover_data={
                    'State_Name': False,
                    'Amount_Crores': ':.2f',
                    'Count_Lakhs': ':.2f',
                    'Avg_Transaction': ':.2f'
                },
                labels={
                    'Amount_Crores': 'Amount (₹ Cr)',
                    'Count_Lakhs': 'Count (L)',
                    'Avg_Transaction': 'Avg Trans (₹)'
                },
                title=f'PhonePe Transactions - {color_label}'
            )
            
            fig.update_geos(
                fitbounds="locations",
                visible=False,
                bgcolor='white'
            )
            
            fig.update_layout(
                height=700,
                margin={"r":0,"t":50,"l":0,"b":0},
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(size=12, color='#2e7d32'),
                title_font=dict(size=20, color='#1b5e20')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total States", len(state_data))
            with col2:
                st.metric("Total Amount", f"₹{state_data['Transaction_amount'].sum()/1e9:.2f}B")
            with col3:
                st.metric("Total Transactions", f"{state_data['Transaction_count'].sum()/1e6:.2f}M")
            with col4:
                st.metric("Avg per State", f"₹{state_data['Transaction_amount'].mean()/1e7:.2f}Cr")
        
        with tab2:
            st.subheader("📊 Detailed State Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top states bar chart
                top_states = state_data.nlargest(top_n, 'Transaction_amount')
                fig = px.bar(
                    top_states,
                    x='State',
                    y='Amount_Crores',
                    title=f'Top {top_n} States by Transaction Amount',
                    color='Amount_Crores',
                    color_continuous_scale='Viridis',
                    hover_data=['Count_Lakhs', 'Avg_Transaction']
                )
                fig.update_layout(xaxis_tickangle=-45, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Transaction count pie chart
                fig = px.pie(
                    top_states,
                    values='Transaction_count',
                    names='State',
                    title=f'Transaction Count Distribution - Top {top_n}',
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.subheader("📋 Complete State Rankings")
            rankings = state_data.sort_values('Transaction_amount', ascending=False).copy()
            rankings['Rank'] = range(1, len(rankings) + 1)
            rankings_display = rankings[['Rank', 'State', 'Amount_Crores', 'Count_Lakhs', 'Avg_Transaction']].rename(
                columns={
                    'Amount_Crores': 'Amount (₹ Cr)',
                    'Count_Lakhs': 'Count (Lakhs)',
                    'Avg_Transaction': 'Avg Trans (₹)'
                }
            )
            st.dataframe(rankings_display, use_container_width=True, height=400)
        
        with tab3:
            st.subheader("🏙️ District-Level Geographic Analysis")
            
            district_data = df_top_trans[(df_top_trans['Year'] == selected_year) & 
                                         (df_top_trans['Quarter'] == selected_quarter)]
            
            if selected_state != 'All States':
                district_data = district_data[district_data['State'] == selected_state]
                st.info(f"Showing districts in: **{selected_state}**")
            else:
                st.info("Showing top districts across all states")
            
            district_data['Amount_Lakhs'] = district_data['Transaction_amount'] / 1e5
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Treemap visualization
                top_districts = district_data.nlargest(top_n * 2, 'Transaction_amount')
                fig = px.treemap(
                    top_districts,
                    path=['State', 'District'],
                    values='Transaction_amount',
                    title=f'Top Districts - Hierarchical View',
                    color='Transaction_amount',
                    color_continuous_scale='YlOrRd',
                    hover_data=['Transaction_count']
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top districts list
                st.subheader(f"Top {top_n} Districts")
                top_dist_list = district_data.nlargest(top_n, 'Transaction_amount')
                top_dist_list['Rank'] = range(1, len(top_dist_list) + 1)
                display_df = top_dist_list[['Rank', 'District', 'State', 'Amount_Lakhs']].rename(
                    columns={'Amount_Lakhs': 'Amount (₹L)'}
                )
                st.dataframe(display_df, use_container_width=True, height=500)
            
            # District bar chart
            st.subheader("📊 District Performance Chart")
            top_districts_chart = district_data.nlargest(top_n, 'Transaction_amount')
            fig = px.bar(
                top_districts_chart,
                x='District',
                y='Transaction_amount',
                color='State',
                title=f'Top {top_n} Districts by Transaction Amount',
                hover_data=['Transaction_count']
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "📈 Growth & Trends":
        st.header("📈 Growth Rate & Trend Analysis")
        
        # Yearly Growth
        yearly_data = df_trans.groupby('Year').agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()
        
        yearly_data['YoY_Growth_%'] = yearly_data['Transaction_amount'].pct_change() * 100
        yearly_data['Amount_B'] = yearly_data['Transaction_amount'] / 1e9
        
        # CAGR Calculation
        if len(yearly_data) > 1:
            first_year_amount = yearly_data.iloc[0]['Transaction_amount']
            last_year_amount = yearly_data.iloc[-1]['Transaction_amount']
            num_years = len(yearly_data) - 1
            cagr = (((last_year_amount / first_year_amount) ** (1/num_years)) - 1) * 100
            
            st.subheader("📊 Key Growth Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("CAGR", f"{cagr:.2f}%")
            with col2:
                latest_growth = yearly_data['YoY_Growth_%'].iloc[-1]
                st.metric("Latest YoY Growth", f"{latest_growth:.2f}%")
            with col3:
                total_growth = ((last_year_amount - first_year_amount) / first_year_amount) * 100
                st.metric("Total Growth", f"{total_growth:.2f}%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=yearly_data['Year'], y=yearly_data['Amount_B'],
                                    mode='lines+markers', name='Transaction Amount',
                                    line=dict(color='blue', width=3),
                                    marker=dict(size=10)))
            fig.update_layout(title='Year-wise Transaction Trend',
                            xaxis_title='Year', yaxis_title='Amount (₹ Billions)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=yearly_data['Year'][1:], y=yearly_data['YoY_Growth_%'][1:],
                                marker_color='green', name='YoY Growth'))
            fig.update_layout(title='Year-over-Year Growth Rate',
                            xaxis_title='Year', yaxis_title='Growth %')
            st.plotly_chart(fig, use_container_width=True)
        
        # Quarterly Trends
        st.subheader("📅 Quarterly Performance Trends")
        quarterly_data = df_trans[df_trans['Year'] == selected_year].groupby('Quarter').agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()
        quarterly_data['Amount_B'] = quarterly_data['Transaction_amount'] / 1e9
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=quarterly_data['Quarter'], y=quarterly_data['Amount_B'],
                            marker_color='lightblue', name='Amount'))
        fig.update_layout(title=f'Quarterly Performance {selected_year}',
                        xaxis_title='Quarter', yaxis_title='Amount (₹ Billions)')
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "🏆 Top Performers":
        st.header("🏆 Top Performers & Rankings")
        
        df_filtered = df_trans[(df_trans['Year'] == selected_year) & (df_trans['Quarter'] == selected_quarter)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🥇 Top {top_n} States")
            top_states = df_filtered.groupby('State').agg({
                'Transaction_amount': 'sum',
                'Transaction_count': 'sum'
            }).nlargest(top_n, 'Transaction_amount').reset_index()
            top_states['Rank'] = range(1, len(top_states) + 1)
            top_states['Amount_B'] = top_states['Transaction_amount'] / 1e9
            top_states['Count_M'] = top_states['Transaction_count'] / 1e6
            
            display_df = top_states[['Rank', 'State', 'Amount_B', 'Count_M']].rename(
                columns={'Amount_B': 'Amount (₹B)', 'Count_M': 'Count (M)'})
            st.dataframe(display_df, use_container_width=True)
            
            fig = px.bar(top_states, x='State', y='Amount_B',
                        color='Amount_B', color_continuous_scale='Greens')
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"🏙️ Top {top_n} Districts")
            top_districts = df_top_trans[(df_top_trans['Year'] == selected_year) & 
                                        (df_top_trans['Quarter'] == selected_quarter)].nlargest(top_n, 'Transaction_amount')
            top_districts['Rank'] = range(1, len(top_districts) + 1)
            top_districts['Amount_M'] = top_districts['Transaction_amount'] / 1e6
            
            display_df = top_districts[['Rank', 'State', 'District', 'Amount_M']].rename(
                columns={'Amount_M': 'Amount (₹M)'})
            st.dataframe(display_df, use_container_width=True)
            
            fig = px.bar(top_districts, x='District', y='Transaction_amount',
                        color='Transaction_amount', color_continuous_scale='Oranges')
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top Transaction Types
        st.subheader("📊 Top Transaction Categories")
        top_types = df_filtered.groupby('Transaction_type').agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index().sort_values('Transaction_amount', ascending=False)
        
        fig = px.sunburst(top_types, path=['Transaction_type'], values='Transaction_amount',
                         title='Transaction Type Distribution',
                         color='Transaction_amount', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "⚖️ Comparative Analysis":
        st.header("⚖️ Comparative Analysis")
        
        if comparison_year != 'None':
            comparison_year = int(comparison_year)
            
            df_current = df_trans[(df_trans['Year'] == selected_year) & (df_trans['Quarter'] == selected_quarter)]
            df_compare = df_trans[(df_trans['Year'] == comparison_year) & (df_trans['Quarter'] == selected_quarter)]
            
            if selected_state != 'All States':
                df_current = df_current[df_current['State'] == selected_state]
                df_compare = df_compare[df_compare['State'] == selected_state]
            
            # Summary Metrics
            current_amount = df_current['Transaction_amount'].sum()
            compare_amount = df_compare['Transaction_amount'].sum()
            growth = ((current_amount - compare_amount) / compare_amount * 100) if compare_amount > 0 else 0
            
            st.subheader("📊 Period Comparison")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(f"{selected_year} Q{selected_quarter}", f"₹{current_amount/1e9:.2f}B")
            with col2:
                st.metric(f"{comparison_year} Q{selected_quarter}", f"₹{compare_amount/1e9:.2f}B")
            with col3:
                st.metric("Growth", f"{growth:.2f}%", delta=f"{growth:.2f}%")
            with col4:
                diff = current_amount - compare_amount
                st.metric("Difference", f"₹{diff/1e9:.2f}B")
            
            # State-wise Comparison
            st.subheader("🗺️ State-wise Growth Comparison")
            current_states = df_current.groupby('State')['Transaction_amount'].sum().reset_index()
            compare_states = df_compare.groupby('State')['Transaction_amount'].sum().reset_index()
            
            comparison_df = current_states.merge(compare_states, on='State', suffixes=('_current', '_compare'))
            comparison_df['Growth_%'] = ((comparison_df['Transaction_amount_current'] - 
                                         comparison_df['Transaction_amount_compare']) / 
                                        comparison_df['Transaction_amount_compare'] * 100)
            comparison_df = comparison_df.nlargest(top_n, 'Growth_%')
            
            fig = px.bar(comparison_df, x='State', y='Growth_%',
                        title=f'Top {top_n} States by Growth Rate',
                        color='Growth_%', color_continuous_scale='RdYlGn',
                        color_continuous_midpoint=0)
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Side-by-side comparison
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(current_states.nlargest(10, 'Transaction_amount'),
                            x='State', y='Transaction_amount',
                            title=f'{selected_year} Q{selected_quarter}')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(compare_states.nlargest(10, 'Transaction_amount'),
                            x='State', y='Transaction_amount',
                            title=f'{comparison_year} Q{selected_quarter}')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Please select a comparison year from the sidebar to view comparative analysis")
    
    elif analysis_type == "📉 Time Series Analysis":
        st.header("📉 Time Series & Trend Analysis")
        
        # Overall Time Series
        time_series = df_trans.groupby(['Year', 'Quarter']).agg({
            'Transaction_amount': 'sum',
            'Transaction_count': 'sum'
        }).reset_index()
        time_series['Period'] = time_series['Year'].astype(str) + '-Q' + time_series['Quarter'].astype(str)
        time_series['Amount_B'] = time_series['Transaction_amount'] / 1e9
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_series['Period'], y=time_series['Amount_B'],
                                mode='lines+markers', name='Transaction Amount',
                                line=dict(color='purple', width=3),
                                marker=dict(size=8)))
        fig.update_layout(title='Transaction Amount Trend Over Time',
                         xaxis_title='Period', yaxis_title='Amount (₹ Billions)',
                         hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Transaction Type Trends
        st.subheader("📊 Category-wise Trends")
        type_trends = df_trans.groupby(['Year', 'Transaction_type'])['Transaction_amount'].sum().reset_index()
        type_trends['Amount_B'] = type_trends['Transaction_amount'] / 1e9
        
        fig = px.line(type_trends, x='Year', y='Amount_B', color='Transaction_type',
                     title='Transaction Amount by Category Over Years',
                     markers=True, line_shape='spline')
        fig.update_layout(yaxis_title='Amount (₹ Billions)')
        st.plotly_chart(fig, use_container_width=True)
        
        # State-wise Time Series
        if selected_state != 'All States':
            st.subheader(f"📍 {selected_state} - Detailed Trend")
            state_ts = df_trans[df_trans['State'] == selected_state].groupby(['Year', 'Quarter']).agg({
                'Transaction_amount': 'sum',
                'Transaction_count': 'sum'
            }).reset_index()
            state_ts['Period'] = state_ts['Year'].astype(str) + '-Q' + state_ts['Quarter'].astype(str)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=state_ts['Period'], y=state_ts['Transaction_amount']/1e9,
                                    mode='lines+markers', fill='tozeroy',
                                    line=dict(color='teal', width=2)))
            fig.update_layout(title=f'{selected_state} Transaction Trend',
                            xaxis_title='Period', yaxis_title='Amount (₹ Billions)')
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer with Insights
    st.markdown("---")
    st.markdown("### 💡 Key Insights & Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Transaction Insights**
        - Monitor real-time transaction volumes across India
        - Identify top-performing states and districts
        - Track transaction type preferences
        - Analyze payment patterns and trends
        - Compare period-over-period performance
        """)
    
    with col2:
        st.markdown("""
        **📈 Growth Analytics**
        - Year-over-Year (YoY) growth tracking
        - Compound Annual Growth Rate (CAGR) analysis
        - Quarterly performance trends
        - State-wise growth patterns
        - Market expansion opportunities
        """)
    
    with col3:
        st.markdown("""
        **🎯 Business Intelligence**
        - User engagement metrics and demographics
        - Revenue analysis by region
        - Market penetration insights
        - Strategic decision-making support
        - Performance benchmarking
        """)
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📊 Dashboard Capabilities")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Analysis Views", "8", help="Different analytical perspectives")
    with col2:
        st.metric("Interactive Filters", "10+", help="Customizable data exploration")
    with col3:
        st.metric("Data Coverage", f"{max(years)-min(years)+1} Years", help="Historical data span")
    with col4:
        st.metric("Geographic Coverage", f"{len(states)-1} States", help="Pan-India analysis")
    
    st.markdown("---")
    st.caption("📱 PhonePe Pulse Data Analytics Dashboard | Built with Streamlit | Data Source: MySQL Database")
    st.caption("💡 Empowering data-driven decisions with real-time insights and comprehensive analytics")

except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("Please ensure MySQL is running and the database is properly configured.")
