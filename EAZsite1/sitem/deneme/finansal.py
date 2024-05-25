import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import utils
import matplotlib.pyplot as plt
import seaborn as sns



class FinancialModel:
    
    def __init__(self, database_path="FinansalVeriler.db"):
        self.conn = sqlite3.connect(database_path)
        self.load_data()

    def load_data(self, sql_query="SELECT * FROM  FinansalBilgiler"):
        self.data = pd.read_sql(sql_query, self.conn)

    def create_scenario(self, x, gelir, gider, ozkynk, satis, pzrpy, pzharc, prsnlharc, prsnlsay, rakipsirkt):
        ortalama_gelir = x['Gelir'].mean() * gelir
        ortalama_gider = x['Gider'].mean() * gider
        ortalama_ozkaynaklar = x['OzKaynaklar'].mean() * ozkynk
        ortalama_satismiktari = x['SatisMiktari'].mean() * satis
        ortalama_pazarpayi = x['PazarPayi'].mean() * pzrpy
        ortalama_pazarharcama = x['PazarlamaHarcamalari'].mean() * pzharc
        ortalama_personelsayisi = x['PersonelSayisi'].mean() * prsnlsay
        ortalama_rakipsirketsayisi = x['RakipSirketSayisi'].mean() * rakipsirkt

        return np.array([ortalama_gelir, ortalama_gider, ortalama_ozkaynaklar, ortalama_satismiktari,
                         ortalama_pazarpayi, ortalama_pazarharcama, ortalama_personelsayisi,
                         ortalama_rakipsirketsayisi])
    
    def create_table(self,new_data,yeni_veriler,predicted_growth_rate,alt_metin):
        
        # Tahmini büyüme oranı ile birlikte grafiği çizin
        plt.figure(figsize=(10, 6))
        
        # Mevcut veriyi çizin
        plt.plot(new_data.ravel(), label='Mevcut Veri', marker='o')
        
        # Senaryo verisini çizin
        plt.plot(yeni_veriler.ravel(), label='Senaryo', marker='o')
        
        text_y_position = (max(new_data.ravel()) + min(new_data.ravel())) / 2  # Mevcut verinin ortasına yakın bir konum
        plt.text(len(new_data.ravel()) // 2, text_y_position, 
         f'Tahmini Büyüme Oranı: %{predicted_growth_rate[0][0] *10:.2f}\n ', 
         ha='center', va='center', fontsize=20, color='darkorange', fontweight='light')
       

        yeni_y_position = text_y_position - 0.2  # Metni biraz daha aşağıya almak için değeri değiştirin
        plt.text(len(new_data.ravel()) // 2, yeni_y_position, alt_metin, 
                 ha='center', va='center', fontsize=14, color='darkgreen', fontweight='normal')
        
       
        
        plt.title('Mevcut Veri, Senaryo ve Tahmin')
        plt.xlabel('Özellikler')
        plt.ylabel('Ölçekli Değerler')
        plt.legend()
        plt.show()
          
    def create_alltable(self):
        
        
        df=self.data
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, markers=True)
        plt.title('İş Performansı Verileri')
        plt.xlabel('Örnek Numarası')
        plt.ylabel('Değerler')
        plt.show()
        
        
        
        
        # Figür ve alt grafikleri oluşturun
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # İlk eksen (ax1) için çizgi grafiğini oluşturun
        color = 'tab:blue'
        ax1.set_ylabel('Gelir', color=color)
        ax1.plot(df.index, df['Gelir'], color=color, marker='o')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # İkinci eksen (ax2) için çizgi grafiğini oluşturun
        ax2 = ax1.twinx()
        color = 'tab:green'
        ax2.set_ylabel('Büyüme Oranı', color=color)
        ax2.plot(df.index, df['BuyumeOrani'], color=color, marker='s')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Ortak başlık ve göster
        plt.title('Gelir, Gider ve Büyüme Oranı')
        plt.show()
        
        
        
        # Figürü oluşturun
        plt.figure(figsize=(10, 6))
        
        # Çizgi grafiğini oluşturun
        sns.lineplot(data=df[['Gelir', 'Gider',"OzKaynaklar"]], markers=True)
        
        # Eksen etiketlerini ayarlayın
        plt.title('Gelir, Gider ve Büyüme Oranı')
        plt.xlabel('Gelir ve Gider')
        plt.ylabel('Değerler')
        
        # Göster
        plt.show()
        
        
        
        # Scatter plot oluşturun
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Gelir', y='PazarPayi', size='SatisMiktari', sizes=(50, 200), data=df, hue='OzKaynaklar', palette='viridis')
        
        # Eksen etiketlerini ve başlığı ayarlayın
        plt.title('Gelir, Satış Miktarı ve Özkaynaklara Göre Pazar Payı')
        plt.xlabel('Gelir')
        plt.ylabel('Pazar Payı')
        
        # Lejantı göster
        plt.legend(title='Özkaynaklar')
        
        # Göster
        plt.show()
        
        
        
        #Korelasyon Matrisi:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', linewidths=.5)
        plt.title('Özellikler Arasındaki Korelasyon Matrisi')
        plt.show()
        
        
        
        #Gelir ve Satış Miktarı) arasındaki ilişkiyi gösteren bir scatter plot kullanabilirsiniz.
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Gelir', y='SatisMiktari', data=df, hue='PazarPayi', palette='viridis')
        plt.title('Gelir ve Satış Miktarı İlişkisi')
        plt.xlabel('Gelir')
        plt.ylabel('Satış Miktarı')
        plt.show()
        
        
        
        
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Gelir', y='PazarPayi', data=df, hue='PersonelSayisi', size='PazarlamaHarcamalari', sizes=(50, 200), palette='viridis')
        plt.title('Gelir ve Pazar Payı İlişkisi')
        plt.xlabel('Gelir')
        plt.ylabel('Pazar Payı')
        plt.legend(title='Personel Sayısı')
        plt.show()
        
        
        
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='SatisMiktari', y='PazarPayi', data=df, hue='OzKaynaklar', palette='coolwarm')
        plt.title('Satış Miktarı ve Pazar Payı İlişkisi')
        plt.xlabel('Satış Miktarı')
        plt.ylabel('Pazar Payı')
        plt.legend(title='Özkaynaklar')
        plt.show()
        
        
        
        
        
        
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Gelir', y='BuyumeOrani', data=df, hue='PersonelSayisi', size='PazarlamaHarcamalari', sizes=(50, 200), palette='viridis')
        plt.title('Gelir ve Büyüme Oranı İlişkisi')
        plt.xlabel('Gelir')
        plt.ylabel('Büyüme Oranı')
        plt.legend(title='Personel Sayısı')
        plt.show()
        
        
        
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='PazarPayi', y='BuyumeOrani', data=df, hue='OzKaynaklar', palette='coolwarm')
        plt.title('Pazar Payı ve Büyüme Oranı İlişkisi')
        plt.xlabel('Pazar Payı')
        plt.ylabel('Büyüme Oranı')
        plt.legend(title='Özkaynaklar')
        plt.show()
        
    def deep_learning(self):
        
        x = self.data.iloc[:, :-1]  # bağımsız değişkenler
        y = self.data.iloc[:, -1]  # bağımlı değişken / büyüme oranı

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=2)

        sc = StandardScaler()
        X_train = sc.fit_transform(x_train)
        X_test = sc.transform(x_test)

        classifier = Sequential()
        classifier.add(Dense(128, activation='relu', input_dim=X_train.shape[1]))
        classifier.add(Dense(64, activation='relu'))
        classifier.add(Dense(1, activation='linear'))
        classifier.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error'])
        classifier.fit(X_train, y_train, epochs=50, batch_size=2, verbose=1)

        predict = classifier.predict(X_test)

        np.set_printoptions(suppress=True)
        
        #Son satır verisi
        new_data = self.data.iloc[-1, :-1].values.reshape(1, -1)

        eklenecek_degerler = self.create_scenario(x, 0.03, 0.02, 0.01, 0.01, 0.009, 0.02, 0.01, 0.00, 0.00)
        eklenecek_degerler2=self.create_scenario(x, 0.01, 0.05, 0.06, 0.03, 0.003, 0.01, 0.05, 0.03, 0.01)
        
        
        
        yeni_veriler = new_data + eklenecek_degerler
        yeni_veriler2=new_data+eklenecek_degerler2
        

        
        new_data_scl = sc.transform(yeni_veriler)
        new_data_scl2=sc.transform(yeni_veriler2)
        
        predicted_growth_rate = classifier.predict(new_data_scl)
        predicted_growth_rate2=classifier.predict(new_data_scl2)
        
        alt_metin = "\n\n\n\n\n\n  Senaryo: Ortalamalarına göre,\nGelir: %3 , Gider:%2 Öz Kaynaklar: %1 \n Pazar Payı: %1 Pazarlama Harcamları: %0.9 \nPersonel Sayısı: %0.2 Rakip Sirket Sayisi: %0.01 \n'lük bir artış "
        
        alt_metin2 = "\n\n\n\n\n\n  Senaryo: Ortalamalarına göre,\nGelir: %1 , Gider:%5 Öz Kaynaklar: %6 \n Pazar Payı: %3 Pazarlama Harcamları: %0.3 \nPersonel Sayısı: %0.2 Rakip Sirket Sayisi: %0.02 \n'lük bir artış "
        
        
        print(f"Tahmin Edilen Büyüme Oranı: {predicted_growth_rate[0][0] / 10}")
        print(f"Tahmin Edilen Büyüme Oranı: {predicted_growth_rate2[0][0] / 10}")

        r2 = r2_score(y_test, predict)
        print(f'R2 Score: {r2}')

        utils.cokluGrafik(x.mean())

        # Tahmini büyüme oranı ile birlikte grafiği çizin
        plt.figure(figsize=(10, 6))
        
        self.create_table(new_data, yeni_veriler,predicted_growth_rate,alt_metin)
        self.create_table(new_data, yeni_veriler2, predicted_growth_rate2,alt_metin2)
      
        
      
            
            
            
# Example usage:
financial_model = FinancialModel()
financial_model.create_alltable()
financial_model.deep_learning()
