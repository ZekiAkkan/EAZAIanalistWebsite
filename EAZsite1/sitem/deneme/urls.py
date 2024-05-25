from django.conf import settings
from django.urls import path
from .views import anasayfaView
from .views import urun_show_charts
from .views import show_charts
from .views import financial_chart
from django.conf.urls.static import static
from .views import upload_sql_file
from django.conf.urls.static import static

urlpatterns=[
    path('',anasayfaView,name="anasayfa"),
    path('upload/', upload_sql_file, name='upload_sql_file'),
    path('upload_sql_file.html',upload_sql_file,name="upload"),
    path('show_charts.html',show_charts,name="chart"),
    path('urun_show_charts.html',urun_show_charts,name="chart"),
    path('urun_analiz_result.html',urun_show_charts,name="chart"),
    path('finansal_chart.html',financial_chart,name="chart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)