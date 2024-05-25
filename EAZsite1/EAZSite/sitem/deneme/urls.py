from django.urls import path
from .views import anasayfaView
from .views import chart
from django.conf.urls.static import static
from .views import upload_sql_file

urlpatterns=[
    path('',anasayfaView,name="anasayfa"),
    path('upload/', upload_sql_file, name='upload_sql_file'),
    path('upload_sql_file.html',upload_sql_file,name="anasayfa"),
    path('chart/',chart,name="chart"),
]