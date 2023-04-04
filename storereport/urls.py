from django.urls import path
from storereport.views import *


app_name = 'storereport'
urlpatterns = [
    path('store-report/', html_to_pdf_view, name='store_report'),
]
