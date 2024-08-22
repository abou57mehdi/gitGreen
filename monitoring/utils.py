import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
import plotly.express as px
from ftplib import FTP
import io

def generate_chart(df, chart_type, x_axis, y_axis):
    try:
        if chart_type == 'line':
            fig = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == 'scatter':
            if len(y_axis) == 1:
                fig = px.scatter(df, x=x_axis, y=y_axis[0])
            else:
                return None
        elif chart_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == 'pie':
            if len(y_axis) == 1:
                fig = px.pie(df, names=x_axis, values=y_axis[0], hole=0.3)
            else:
                return None
        else:
            return None

        return fig.to_html(full_html=False)
    except Exception as e:
        return None

def fetch_data_from_ftp(server, user, password, file_path):
    with FTP(server) as ftp:
        ftp.login(user=user, passwd=password)
        with io.BytesIO() as file:
            ftp.retrbinary(f'RETR {file_path}', file.write)
            file.seek(0)
            df = pd.read_csv(file)
    return df

def fetch_data_from_sql(host, user, password, database, query, db_type='postgresql'):
    if db_type == 'postgresql':
        engine = create_engine(f'postgresql://{user}:{quote(password)}@{host}/{database}')
    elif db_type == 'mysql':
        engine = create_engine(f'mysql+pymysql://{user}:{quote(password)}@{host}/{database}')
    else:
        raise ValueError("Unsupported database type")

    df = pd.read_sql(query, engine)
    return df
