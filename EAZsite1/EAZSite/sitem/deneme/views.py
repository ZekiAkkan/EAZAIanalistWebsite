from django.shortcuts import render, redirect
from .forms import UploadSQLForm
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def anasayfaView(request):
    return render(request, 'index.html')

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

def show_charts(request):
    conn = sqlite3.connect("CalisanPerformans.db")
    sql_query = "SELECT * FROM CalisanPerformansi"
    data = pd.read_sql(sql_query, conn)

    # Scatter Plot 1
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='Yas', y='Projeler', hue='Memnuniyet', size='Memnuniyet', data=data, palette='viridis', sizes=(50, 200))
    plt.title('Yaş ve Projeler Bazında Memnuniyet')
    plt.xlabel('Yaş')
    plt.ylabel('Projeler')
    plt.legend(title='Memnuniyet', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('scatter_plot1.png')
    plt.close()

    # Scatter Plot 2
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='Yas', y='AylikMaas', hue='PerformansDegerlendirme', data=data, palette='viridis', s=100)
    plt.title('Yaş ve Aylık Maaşa Göre Performans Değerlendirmesi')
    plt.xlabel('Yaş')
    plt.ylabel('Aylık Maaş')
    plt.legend(title='Performans')
    plt.savefig('scatter_plot2.png')
    plt.close()

    # Line Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Departman', y='PerformansDegerlendirme', data=data, marker='o', label='Performans')
    sns.lineplot(x='Departman', y='Memnuniyet', data=data, marker='o', label='Memnuniyet')
    plt.title('Departmana Göre Performans ve Memnuniyet')
    plt.xlabel('Departman')
    plt.ylabel('Değerlendirme')
    plt.legend()
    plt.savefig('line_plot.png')
    plt.close()

    # Scatter Plot 3
    plt.figure(figsize=(10, 6))
    plt.scatter(data['AylikMaas'], data['HizmetSuresi'], c=data['PerformansDegerlendirme'], cmap='viridis', s=100)
    plt.colorbar(label='Performans Değerlendirmesi')
    plt.xlabel('Aylık Maaş')
    plt.ylabel('Hizmet Süresi')
    plt.title('Performans Değerlendirmesi - Aylık Maaş vs Hizmet Süresi')
    plt.savefig('scatter_plot3.png')
    plt.close()

    return render(request, 'show_charts.html')