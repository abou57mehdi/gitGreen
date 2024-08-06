from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import HttpResponse
import pandas as pd
import plotly.express as px
from .forms import UploadFileForm
from .visualizations import (
    generate_table_2_4_visualization,
    generate_table_2_6_visualization,
    generate_table_2_7_visualization,
    generate_table_3_2_visualization,
    generate_table_3_10_visualization,
    generate_table_6_5_visualization,
    generate_data_center_statistics_visualization  # Make sure to add this function
)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'monitoring/article_list.html', {'articles': articles})



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
        visualization = generate_data_center_statistics_visualization()  # Ensure this function is implemented
    else:
        visualization = None

    return render(request, 'monitoring/article_detail.html', {'article': article, 'visualization': visualization})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            chart_type = form.cleaned_data['chart_type']
            x_axis_index = form.cleaned_data['x_axis'] - 1  # Convert to zero-based index
            y_axis_indices = [int(x) - 1 for x in form.cleaned_data['y_axis'].split(',')]

            try:
                # Check file type
                if not file.name.endswith('.csv'):
                    return render(request, 'monitoring/upload_file.html', {
                        'form': form,
                        'error': 'Invalid file type. Please upload a CSV file.'
                    })
                
                # Read the CSV file
                df = pd.read_csv(file)
                
                # Validate x_axis_index and y_axis_indices
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

                # Create Plotly figure based on chart type
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

                # Convert the figure to HTML
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
