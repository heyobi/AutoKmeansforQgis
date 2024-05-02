import os
import numpy as np
import datetime
import time
import geopandas as gp

saniye = 60
dakika = 60 * saniye


# Hedef tarih ve saat
hedef_tarih = datetime.datetime(year=2024, month=4, day=27, hour=17, minute=0, second=0)

# Şu anki zamanı al
su_an = datetime.datetime.now()

print("Zamanlayıcı başladı!")
# Hedef tarihe kadar bekle
while su_an < hedef_tarih:
    time.sleep(dakika*30)
    time.sleep((hedef_tarih - su_an).total_seconds())
    su_an = datetime.datetime.now()

# bekleme bittiğinde kod çalışsın

#Tanımlar:
def Label_eleminator(input_path,output_path,dn_value):
    poligonlar = gp.read_file(input_path)
    for i in range(len(poligonlar.DN)):
        if poligonlar.DN[i] == dn_value:
            poligonlar.DN[i] = 1
        else:
            poligonlar.DN[i] = 0
   
    poligonlar.to_file(output_path, driver='GeoJSON') 
    return

def main_function(data_yol):
    data1_path = r"C:\Users\polar\Desktop\kiyi_etiket" +"\\" + data_yol
    folderlist = []
    for foldername, subfolders, filenames in os.walk(data1_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            folderlist.append(file_path)

            #print(file_path)

    for i in folderlist:
        folder_name, file_name = i.split('\\')[-2:]

        #print(folder_name,file_name)   
        inputPath = f'C:/Users/polar/Desktop/kiyi_etiket/{data_yol}/{folder_name}/{file_name}'
        outputPath = f'C:/Users/polar/Desktop/kiyi_etiket/{data_yol}/{folder_name}/{file_name}'.rsplit(".JPG", 1)[0]+'_Kmeans.tif'
        centro_outPath = outputPath.rsplit(".tif", 1)[0] + "_centroids.out"
    
        processing.run("otb:KMeansClassification",
                {'in':inputPath, #DJI_20230214233118_0446_V.JPG/DJI_20230214233118_0446_V_1.JPG
                    'out':outputPath,
                    'nc':5, #Numner Of Clases
                    'ts':None,
                    'maxit':1000,
                    'centroids.in':'',
                    'centroids.out':centro_outPath,
                    'sampler':'periodic',
                    'sampler.periodic.jitter':0,
                    'vm':None,'nodatalabel':0,
                    'cleanup':True,'rand':0,
                    'outputpixeltype':5})
        #print(file_name,"Classification Completed")
    
        inputPath = outputPath
        outputPath = outputPath.rsplit(".tif", 1)[0] + '_poligonized.geojson'
    
        processing.run("gdal:polygonize",
                {'INPUT':inputPath,
                    'BAND':1,
                    'FIELD':'DN',
                    'EIGHT_CONNECTEDNESS':False,
                    'EXTRA':'',
                    'OUTPUT':outputPath})
        #print(file_name,"Poliganization Completed")

    

    
    
    
        with open(centro_outPath, 'r') as file:
            lines = file.readlines()
        data = np.array([[float(num) for num in line.split()] for line in lines])
        row_means = np.mean(data, axis=1)
        min_mean = np.min(row_means)
        min_index = np.argmin(row_means)
    
        #print("En düşük ortalama:", min_mean)
        #print("En düşük ortalama satırının indeksi:", min_index)
        #print("En düşük ortalama satırı:", data[min_index])
    

        inputPath = outputPath
        #print(inputPath)
        outputPath = outputPath.rsplit('.geojson')[0] + '_Labeled'+'.geojson'
        Label_eleminator(inputPath,outputPath,min_index)
    
    
    
        inputPath = outputPath
        outputPath = outputPath.rsplit(".geojson", 1)[0] + '_rasterized.tif'
    
        processing.run("gdal:rasterize", {'INPUT':inputPath,
                                    'FIELD':'DN',
                                    'BURN':0,
                                    'USE_Z':False,
                                    'UNITS':0,
                                    'WIDTH':2540,
                                    'HEIGHT':1878,
                                    'EXTENT':None,
                                    'NODATA':10,
                                    'OPTIONS':'',
                                    'DATA_TYPE':5,
                                    'INIT':None,'INVERT':False,'EXTRA':'',
                                    'OUTPUT':outputPath})
        #print(file_name,"Rasterization Completed")

#main
print("Zamanlayıcı sona erdi!")

#data1 için kod
print
main_function("data1")
print("data1 bitti!")

#data2 için kod
print("data2 için kod başladı!")
main_function("data2")
print("data2 bitti!")



#data3 için kod
print("data3 için kod başladı!")
main_function("data3")
print("data3 bitti!")

