# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadSQLForm
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import os
from django.conf import settings
from .models import SQLFile  # SQLFile modelini ekledik
from io import BytesIO


def anasayfaView(request):
    return render(request, 'index.html')

def financial_chart(request):
    return render(request, 'finansal_chart.html')


def chart(request):
    return render(request, 'show_charts.html')

def upload_sql_file(request):
    if request.method == 'POST':
        form = UploadSQLForm(request.POST, request.FILES)
        if form.is_valid():
            sql_file = form.save(commit=False)
            sql_file.content = sql_file.file.read()
            sql_file.save()
            return redirect('anasayfa')
    else:
        form = UploadSQLForm()

    return render(request, 'upload_sql_file.html', {'form': form})

def get_calisan_performans_db():
    static_dir = os.path.join(settings.BASE_DIR, 'static', 'calisan_performans')
    
    sql_file = SQLFile.objects.last()

    if sql_file and sql_file.file:
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        model_content_path = os.path.join(static_dir, 'CalisanPerformans.db')

        with open(model_content_path, 'wb') as destination:
            destination.write(sql_file.file.read())

        return model_content_path
    elif os.path.exists(static_dir):
        return os.path.join(static_dir, 'CalisanPerformans.db')
    else:
        return None

def show_charts(request):
    db_file_path = get_calisan_performans_db()

    if db_file_path:
        conn = sqlite3.connect(db_file_path)
        sql_query = "SELECT * FROM CalisanPerformansi"
        data = pd.read_sql(sql_query, conn)
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'calisan_performans')

        # Scatter Plot 1
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='Yas', y='Projeler', hue='Memnuniyet', size='Memnuniyet', data=data, palette='viridis', sizes=(50, 200))
        plt.title('Yaş ve Projeler Bazında Memnuniyet')
        plt.xlabel('Yaş')
        plt.ylabel('Projeler')
        plt.legend(title='Memnuniyet', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Statik dizini kullanarak dosyayı kaydetme
        plt.savefig(os.path.join(static_dir, 'scatter_plot1.png'))
        plt.close()

        # Scatter Plot 2
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='Yas', y='AylikMaas', hue='PerformansDegerlendirme', data=data, palette='viridis', s=100)
        plt.title('Yaş ve Aylık Maaşa Göre Performans Değerlendirmesi')
        plt.xlabel('Yaş')
        plt.ylabel('Aylık Maaş')
        plt.legend(title='Performans')
        plt.savefig(os.path.join(static_dir, 'scatter_plot2.png'))
        plt.close()

        # Line Plot
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Departman', y='PerformansDegerlendirme', data=data, marker='o', label='Performans')
        sns.lineplot(x='Departman', y='Memnuniyet', data=data, marker='o', label='Memnuniyet')
        plt.title('Departmana Göre Performans ve Memnuniyet')
        plt.xlabel('Departman')
        plt.ylabel('Değerlendirme')
        plt.legend()
        plt.savefig(os.path.join(static_dir, 'line_plot.png'))
        plt.close()

        # Scatter Plot 3
        plt.figure(figsize=(10, 6))
        plt.scatter(data['AylikMaas'], data['HizmetSuresi'], c=data['PerformansDegerlendirme'], cmap='viridis', s=100)
        plt.colorbar(label='Performans Değerlendirmesi')
        plt.xlabel('Aylık Maaş')
        plt.ylabel('Hizmet Süresi')
        plt.title('Performans Değerlendirmesi - Aylık Maaş vs Hizmet Süresi')
        plt.savefig(os.path.join(static_dir, 'scatter_plot3.png'))
        plt.close()


        return render(request, 'show_charts.html')
    else:
        return HttpResponse("CalisanPerformans.db dosyası bulunamadı.")



def urun_show_charts(request):
    db_file_path = os.path.join(settings.BASE_DIR, 'static', 'UrunSwot.db')

    if os.path.exists(db_file_path):
        conn = sqlite3.connect(db_file_path)
        sql_query = "SELECT * FROM UrunAnalizTablosu"
        veri_df = pd.read_sql(sql_query, conn)
        conn.close()

        # Grafikleri oluşturan fonksiyonu çağır
        grafikler_urun(veri_df)

        return render(request, 'urun_show_charts.html')
    else:
        return HttpResponse("UrunSwot.db dosyası bulunamadı.")

def grafikler_urun(veri_df):
    yas_araliklari = [20, 30, 40, 50]
    yas_etiketleri = ['20-29', '30-39', '40-49']
    veri_df['Yaş Grubu'] = pd.cut(veri_df['Yas'], bins=yas_araliklari, labels=yas_etiketleri, right=False)

    # Yaş Gruplarına Göre Müşteri Sayısı Grafiği
    plt.figure(figsize=(10, 6))
    sns.countplot(x='Yaş Grubu', data=veri_df, palette='viridis')
    plt.title('Yaş Gruplarına Göre Müşteri Sayısı')
    plt.xlabel('Yaş Grubu')
    plt.ylabel('Müşteri Sayısı')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'yas_gruplari_musteri_sayisi.png'))
    plt.close()

    # Gelir Seviyesi Dağılımı Grafiği
    plt.figure(figsize=(12, 6))
    sns.histplot(x='GelirDuzeyi', data=veri_df, bins=30, color='skyblue', kde=True)
    plt.title('Gelir Düzeyine Göre Dağılım')
    plt.xlabel('Gelir Düzeyi')
    plt.ylabel('Müşteri Sayısı')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'gelir_duzeyi_dagilimi.png'))
    plt.close()

    
    # Eğitim Seviyesine Göre Ürün Memnuniyeti
    plt.figure(figsize=(10, 6))
    sns.countplot(x='UrunMemnuniyeti', hue='EgitimSeviyesi', data=veri_df)
    plt.title('Eğitim Seviyesine Göre Ürün Memnuniyeti')
    plt.xlabel('Memnuniyet Durumu (1: Memnun, 0: Memnun Değil)')
    plt.ylabel('Müşteri Sayısı')
    plt.legend(title='Eğitim Seviyesi', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'egitim_memnuniyet_urun.png'))
    plt.close()

    # Şehire Göre Ürün Memnuniyeti Grafiği
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Sehir', hue='UrunMemnuniyeti', data=veri_df)
    plt.title('Şehire Göre Ürün Memnuniyeti')
    plt.xlabel('Şehir')
    plt.ylabel('Müşteri Sayısı')
    plt.legend(title='Memnuniyet Durumu', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'sehir_memnuniyet_urun.png'))
    plt.close()

    # Meslek Gruplarına Göre Ürün Memnuniyeti Grafiği
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Meslek', hue='UrunMemnuniyeti', data=veri_df)
    plt.title('Meslek Gruplarına Göre Ürün Memnuniyeti')
    plt.xlabel('Meslek')
    plt.ylabel('Müşteri Sayısı')
    plt.legend(title='Memnuniyet Durumu', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'meslek_memnuniyet_urun.png'))
    plt.close()

    # Müşteri Segmentasyonu Grafiği
    plt.figure(figsize=(12, 6))
    segmentasyon = veri_df.groupby(['Yaş Grubu', 'GelirDuzeyi']).size().unstack()
    segmentasyon.plot(kind='bar', stacked=True, colormap='viridis')
    plt.title('Müşteri Segmentasyonu')
    plt.xlabel('Yaş Grubu ve GelirDuzeyi')
    plt.ylabel('Müşteri Sayısı')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'musteri_segmentasyonu.png'))
    plt.close()

    # Cinsiyete Göre Ürün Memnuniyeti
    plt.figure(figsize=(10, 6))
    sns.countplot(x='UrunMemnuniyeti', hue='Cinsiyet', data=veri_df)
    plt.title('Cinsiyete Göre Ürün Memnuniyeti')
    plt.xlabel('Memnuniyet Durumu (1: Memnun, 0: Memnun Değil)')
    plt.ylabel('Müşteri Sayısı')
    plt.legend(title='Cinsiyet', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'urun_swot', 'cinsiyet_memnuniyet_urun.png'))
    plt.close()


