from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import HttpResponse
import pandas as pd
import plotly.express as px
from .visualizations import (
    generate_table_2_4_visualization,
    generate_table_2_6_visualization,
    generate_table_2_7_visualization,
    generate_table_3_2_visualization,
    generate_table_3_10_visualization,
    generate_table_6_5_visualization,
    generate_data_center_statistics_visualization
)
import psycopg2
import ftplib
import csv
from io import StringIO
from .utils import fetch_data_from_sql,fetch_data_from_ftp,generate_chart
import pandas as pd
import plotly.express as px
from .forms import UploadFileForm, DataSourceForm





# Article list view
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'monitoring/article_list.html', {'articles': articles})

# Article detail view with visualization
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    if article.table_name == 'Table 2-4':
        visualization = generate_table_2_4_visualization()
    elif article.table_name == 'Table 2-6':
        visualization = generate_table_2_6_visualization()
    elif article.table_name == 'Table 2-7':
        visualization = generate_table_2_7_visualization()
    elif article.table_name == 'Table 3-2':
        visualization = generate_table_3_2_visualization()
    elif article.table_name == 'Table 3-10':
        visualization = generate_table_3_10_visualization()
    elif article.table_name == 'Table 6-5':
        visualization = generate_table_6_5_visualization()
    elif article.table_name == 'Data Center Statistics':
        visualization = generate_data_center_statistics_visualization()
    else:
        visualization = None

    return render(request, 'monitoring/article_detail.html', {'article': article, 'visualization': visualization})

# File upload and visualization view
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            chart_type = form.cleaned_data['chart_type']
            x_axis_index = form.cleaned_data['x_axis'] - 1  # Convert to zero-based index
            y_axis_indices = [int(x) - 1 for x in form.cleaned_data['y_axis'].split(',')]

            try:
                if not file.name.endswith('.csv'):
                    return render(request, 'monitoring/upload_file.html', {
                        'form': form,
                        'error': 'Invalid file type. Please upload a CSV file.'
                    })
                
                df = pd.read_csv(file)
                
                if x_axis_index < 0 or x_axis_index >= len(df.columns):
                    return render(request, 'monitoring/upload_file.html', {
                        'form': form,
                        'error': 'Invalid X-Axis column number.'
                    })

                if any(index < 0 or index >= len(df.columns) for index in y_axis_indices):
                    return render(request, 'monitoring/upload_file.html', {
                        'form': form,
                        'error': 'Invalid Y-Axis column numbers.'
                    })

                x_axis = df.columns[x_axis_index]
                y_axis = [df.columns[i] for i in y_axis_indices]

                if chart_type == 'line':
                    fig = px.line(df, x=x_axis, y=y_axis)
                elif chart_type == 'scatter':
                    if len(y_axis) == 1:
                        fig = px.scatter(df, x=x_axis, y=y_axis[0])
                    else:
                        return render(request, 'monitoring/upload_file.html', {
                            'form': form,
                            'error': 'Scatter plot requires only one y-axis column.'
                        })
                elif chart_type == 'bar':
                    fig = px.bar(df, x=x_axis, y=y_axis)
                elif chart_type == 'pie':
                    if len(y_axis) == 1:
                        fig = px.pie(df, names=x_axis, values=y_axis[0], hole=0.3)
                    else:
                        return render(request, 'monitoring/upload_file.html', {
                            'form': form,
                            'error': 'Pie chart requires only one y-axis column.'
                        })
                else:
                    return render(request, 'monitoring/upload_file.html', {
                        'form': form,
                        'error': 'Unsupported chart type.'
                    })

                plot_div = fig.to_html(full_html=False)

                return render(request, 'monitoring/upload_file.html', {
                    'form': form,
                    'plot_div': plot_div
                })
                
            except Exception as e:
                return render(request, 'monitoring/upload_file.html', {
                    'form': form,
                    'error': f'An error occurred while processing the file: {e}'
                })
    else:
        form = UploadFileForm()

    return render(request, 'monitoring/upload_file.html', {'form': form})

from django.shortcuts import render
from .forms import DataSourceForm
from .utils import fetch_data_from_sql, fetch_data_from_ftp, generate_chart

def visualize_data(request):
    sql_graph = None
    ftp_graph = None
    form = DataSourceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            source_type = form.cleaned_data['source_type']
            chart_type = form.cleaned_data['chart_type']
            x_axis = form.cleaned_data['x_axis']
            y_axis = form.cleaned_data['y_axis']

            if isinstance(y_axis, str):
                y_axis = [col.strip() for col in y_axis.split(',')]

            if source_type == 'ftp':
                ftp_server = form.cleaned_data['ftp_server']
                ftp_user = form.cleaned_data['ftp_user']
                ftp_password = form.cleaned_data['ftp_password']
                ftp_file_path = form.cleaned_data['ftp_file_path']

                try:
                    ftp_df = fetch_data_from_ftp(ftp_server, ftp_user, ftp_password, ftp_file_path)

                    if x_axis not in ftp_df.columns:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'ftp_error': f'Invalid X-Axis column: {x_axis}.'
                        })

                    invalid_y_axes = [y for y in y_axis if y not in ftp_df.columns]
                    if invalid_y_axes:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'ftp_error': f'Invalid Y-Axis columns: {", ".join(invalid_y_axes)}.'
                        })

                    ftp_graph = generate_chart(ftp_df, chart_type, x_axis, y_axis)
                    if not ftp_graph:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'ftp_error': 'Error generating chart from FTP data.'
                        })

                except Exception as e:
                    ftp_error = f"Error fetching or processing FTP data: {str(e)}"
                    return render(request, 'visualize.html', {
                        'form': form,
                        'ftp_error': ftp_error
                    })

            elif source_type == 'sql':
                sql_host = form.cleaned_data['sql_host']
                sql_user = form.cleaned_data['sql_user']
                sql_password = form.cleaned_data['sql_password']
                sql_database = form.cleaned_data['sql_database']
                sql_query = form.cleaned_data['sql_query']
                db_type = form.cleaned_data['db_type']

                try:
                    sql_df = fetch_data_from_sql(sql_host, sql_user, sql_password, sql_database, sql_query, db_type)

                    if x_axis not in sql_df.columns:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'sql_error': f'Invalid X-Axis column: {x_axis}.'
                        })

                    invalid_y_axes = [y for y in y_axis if y not in sql_df.columns]
                    if invalid_y_axes:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'sql_error': f'Invalid Y-Axis columns: {", ".join(invalid_y_axes)}.'
                        })

                    sql_graph = generate_chart(sql_df, chart_type, x_axis, y_axis)
                    if not sql_graph:
                        return render(request, 'visualize.html', {
                            'form': form,
                            'sql_error': 'Error generating chart from SQL data.'
                        })

                except Exception as e:
                    sql_error = f"Error fetching or processing SQL data: {str(e)}"
                    return render(request, 'visualize.html', {
                        'form': form,
                        'sql_error': sql_error
                    })

    return render(request, 'visualize.html', {
        'form': form,
        'ftp_graph': ftp_graph,
        'sql_graph': sql_graph,
    })
