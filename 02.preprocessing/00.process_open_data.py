import geopandas as gpd
import pandas as pd
import sys, os

def combine_geojson(fpath, facility):
    path_text = f'../01.rawdata/{fpath}/'
    path = os.listdir(path_text)
    n = 0
    a = 0
    p = 0
    processing_type = 0
    for filename in path:
        if (facility in filename) & (filename[-7:] == 'geojson') & (filename.split('_')[1] != 'p') & (filename.split('_')[1] != 'a'):
            if n == 0:
                gf = gpd.read_file(path_text + filename)
                gf = gf.to_crs(epsg=3826)
                n = n + 1
                processing_type = 0
                #print(gf.info)
            else:
                gf2 = gpd.read_file(path_text + filename)
                gf2 = gf2.to_crs(epsg=3826)
                gf = pd.concat([gf, gf2])
            print(filename)
        elif (facility in filename) & (filename[-7:] == 'geojson') & ((filename.split('_')[1] == 'p') | (filename.split('_')[1] == 'a')):
            print(filename,filename.split('_')[1])
            if (a == 0) & (filename.split('_')[1] == 'a'):
                gf = gpd.read_file(path_text + filename)
                gf = gf.to_crs(epsg=3826)
                a = a + 1
                processing_type = 1
                #print(1)
            elif (a != 0) & (filename.split('_')[1] == 'a'):
                gf2 = gpd.read_file(path_text + filename)
                gf2 = gf2.to_crs(epsg=3826)
                gf = pd.concat([gf, gf2])
                #print(2)
            elif (p == 0) & (filename.split('_')[1] == 'p'):
                gf3 = gpd.read_file(path_text + filename)
                gf3 = gf3.to_crs(epsg=3826)
                p = p + 1
                #print(3)
            elif (p != 0) & (filename.split('_')[1] == 'p'):
                gf4 = gpd.read_file(path_text + filename)
                gf4 = gf4.to_crs(epsg=3826)
                gf3 = pd.concat([gf3, gf4])
                #print(4)
    if processing_type == 1:
        gf.reset_index(inplace=True, drop=False)
        gf3.reset_index(inplace=True, drop=False)
        buffer_len = gf.area.mean() ** 0.5 / 2
        gf3['geometry'] = gf3.buffer(buffer_len, cap_style=3)
        intersection = gpd.overlay(gf,gf3,  how='intersection', keep_geom_type=True)
        drop_df_idx=intersection.loc[:,['full_id_2']]
        gf5 = gf3.merge(drop_df_idx,how='left', left_on='full_id', right_on='full_id_2')
        #print(gf3.info())
        drop_item = gf5[gf5['full_id_2'].isnull() == False].index
        try:
            gf3=gf3.drop(drop_item)
            gf = pd.concat([gf, gf3])
        except:
            gf = pd.concat([gf, gf3])
    
    if facility == 'placeofworkship':
        gf = gf.loc[:,['full_id', 'name', 'religion', 'geometry']]
    else:
        gf = gf.loc[:,['full_id', 'name', 'geometry']]
    gf.info()
    gf.head()
    gf.plot()
    gf.to_file(f"./{fpath}/{facility}.geojson", driver='GeoJSON')
    
def c_2_geojson(fpath, fname1, fname2):
    path = os.listdir(fpath)
    for filename in path:
        if (fname1 in filename) & (filename[-7:] == 'geojson'):
            gf1 = gpd.read_file(fpath + filename)
            gf1 = gf1.to_crs(epsg=3826)
        elif (fname2 in filename) & (filename[-7:] == 'geojson'):
            gf2 = gpd.read_file(fpath + filename)
            gf2 = gf2.to_crs(epsg=3826)
    gf3 = pd.concat([gf1, gf2])
    gf3 = gf3.loc[:,['full_id', 'name', 'geometry']]
    gf3.info()
    gf3.head()
    gf3.plot()
    gf3.to_file(fname1 + ".geojson", driver='GeoJSON')
            
        
if __name__ == '__main__':
    indicators = input("欲處理的六大指標: ")
    facilities = input("欲處理的設施名稱: ")
    combine_geojson(indicators,facilities)