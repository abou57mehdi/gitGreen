import plotly.graph_objects as go

def generate_table_2_4_visualization():
    data = {
        'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006],
        'Volume': [1634, 1691, 1752, 1813, 1871, 1918, 1969],
        'Mid-range': [3724, 4006, 4298, 4590, 5042, 5475, 5917],
        'High-end': [48611, 51088, 53699, 56309, 61251, 67023, 71509]
    }
    title = 'Estimated Average UEC (kWh/year) per Server, by Server Class, 2000 to 2006'
    yaxis_title = 'kWh/year'
    return create_figure(data, title, yaxis_title)

def generate_table_2_6_visualization():
    data = {
        'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006],
        'Server closet': [1.4, 1.7, 2.1, 2.4, 2.8, 3.3, 3.5],
        'Server room': [1.7, 2.1, 2.5, 2.9, 3.3, 3.9, 4.3],
        'Localized data center': [1.9, 2.3, 2.6, 2.9, 3.3, 3.8, 4.2],
        'Mid-tier data center': [1.7, 2.1, 2.3, 2.6, 3.0, 3.4, 3.7],
        'Enterprise-class data center': [4.8, 5.6, 6.1, 6.6, 7.3, 8.2, 8.8],
        'Total': [11.6, 13.9, 15.6, 17.4, 19.8, 22.6, 24.5]
    }
    title = 'Estimated Total Electricity Use of U.S. Servers (in billion kWh/year) by Space Type, 2000 to 2006'
    yaxis_title = 'billion kWh/year'
    return create_figure(data, title, yaxis_title)

def generate_table_2_7_visualization():
    data = {
        'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006],
        'Server closet': [0, 0, 0, 0, 0, 0, 0],
        'Server room': [0, 0, 0, 0, 0, 0, 0],
        'Localized data center': [0.28, 0.37, 0.46, 0.56, 0.66, 0.73, 0.86],
        'Mid-tier data center': [0.25, 0.33, 0.42, 0.50, 0.59, 0.66, 0.78],
        'Enterprise-class data center': [0.57, 0.74, 0.90, 1.07, 1.23, 1.35, 1.58],
        'Total': [1.10, 1.44, 1.79, 2.13, 2.49, 2.74, 3.22]
    }
    title = 'Estimated Energy Use (billion kWh/year) of Enterprise Storage Devices, by Space Type, 2000 to 2006'
    yaxis_title = 'billion kWh/year'
    return create_figure(data, title, yaxis_title)

def generate_table_3_2_visualization():
    data = {
        'Year': [2007, 2008, 2009, 2010, 2011],
        'Historical trends': [70.0, 81.3, 93.7, 109.3, 124.5],
        'Current efficiency trends': [67.4, 76.1, 85.0, 95.5, 107.4],
        'CAGR': [478.8, 431.4] # This column seems to be an anomaly in the context of a time series
    }
    title = 'Projected Annual and Cumulative Electricity Use (in billion kWh), Historical Trends and Current Efficiency Trends Scenarios'
    yaxis_title = 'billion kWh'
    return create_figure(data, title, yaxis_title)

def generate_table_3_10_visualization():
    data = {
        'Year': [2007, 2008, 2009, 2010, 2011],
        'Historical trends': [44.4, 51.2, 59.2, 69.2, 78.7],
        'Current efficiency trends': [42.8, 47.9, 53.6, 60.5, 67.9],
        'Improved operation': [34.8, 39.0, 43.5, 48.4, 53.1],
        'Best practice': [30.2, 30.0, 29.8, 29.7, 30.1],
        'State-of-the-art': [28.1, 25.7, 23.5, 21.4, 21.2]
    }
    title = 'Projected CO2 Emissions Associated with the Electricity Use of U.S. Servers and Data Centers (in MMTCO2/year), All Scenarios, 2007 to 2011'
    yaxis_title = 'MMTCO2/year'
    return create_figure(data, title, yaxis_title)

def generate_table_6_5_visualization():
    data = {
        'Metric': ['Capacity (kW)', 'Heat Rate (Btu/kWh)', 'NOx (lb/MWh)', 'SO2 (lb/MWh)', 'CO2 (lb/MWh)', 'NOx (lb/MW-year)', 'SO2 (lb/MW-year)', 'CO2 (tons/MW-year)'],
        'PEM Fuel Cell': [150, 9750, 0.100, 0.006, 1170, 2, 0.14, 14],
        'Diesel Generator': [600, 10000, 20.282, 2.900, 1650, 487, 69.60, 20]
    }
    title = 'Emission Benefits of Fuel Cell Backup Power'
    return create_bar_chart(data, title)

def create_figure(data, title, yaxis_title):
    fig = go.Figure()
    for key, values in data.items():
        if key != 'Year':
            fig.add_trace(go.Scatter(x=data['Year'], y=values, mode='lines+markers', name=key))
    
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=yaxis_title)
    return fig.to_html(full_html=False)

def create_bar_chart(data, title):
    fig = go.Figure(data=[
        go.Bar(name='PEM Fuel Cell', x=data['Metric'], y=data['PEM Fuel Cell']),
        go.Bar(name='Diesel Generator', x=data['Metric'], y=data['Diesel Generator'])
    ])
    fig.update_layout(barmode='group', title=title)
    return fig.to_html(full_html=False)

def generate_data_center_statistics_visualization():
    data = {
        'Country': ['United States', 'Germany', 'UK', 'People’s Republic of China', 'Canada', 'France', 'Australia', 'Netherlands', 'Russia', 'Japan'],
        'Data Center Count': [5375, 522, 517, 448, 335, 314, 306, 299, 255, 218]
    }
    
    if 'Country' not in data or 'Data Center Count' not in data:
        return "<p>Error: Required data is missing.</p>"

    if len(data['Country']) != len(data['Data Center Count']):
        return "<p>Error: Data lists have different lengths.</p>"

    fig = go.Figure(data=[go.Bar(x=data['Country'], y=data['Data Center Count'])])
    fig.update_layout(title='Top 10 Countries with the Most Data Centers',
                      xaxis_title='Country',
                      yaxis_title='Data Center Count')
    return fig.to_html(full_html=False)
