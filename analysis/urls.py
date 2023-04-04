from django.urls import path
from analysis.views import *


app_name = 'analysis'
urlpatterns = [
    path('series/', work_with_series, name='work_with_series'),
    path('dataframe/', work_with_dataframe, name='work_with_dataframe'),
    path('chart/', work_with_chart_1, name='work_with_chart_1'),
]
