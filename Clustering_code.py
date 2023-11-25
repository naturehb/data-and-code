
import pandas as pd
import datetime
import converter
from sklearn.cluster import MiniBatchKMeans
file_name = r'Macao.xlsx'
df = pd.read_excel(file_name)

k = 19  
batch_size = 1000  
random_state = 9  


mod = MiniBatchKMeans(n_clusters=k, batch_size=batch_size, random_state=random_state)
def convert_to_mercartor(df):
    lng1, lat1= converter.wgs84tomercator(df['lon1'], df['lat1'])
    return lng1, lat1

df['coords'] = df.apply(convert_to_mercartor, axis = 1)
df[['x', 'y']] = df['coords'].apply(lambda x: pd.Series([x[0], x[1]]))
# print(df2)
y_pre = mod.fit_predict(df[['x', 'y']].to_numpy() )


r1 = pd.Series(mod.labels_).value_counts()
r2 = pd.DataFrame(mod.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
r.columns = ['Centroid Longitude', 'Centroid Latitude', 'Number of Clusters']


df = pd.DataFrame(r)
def convert_to_wgs84(r):
    lng1, lat1= converter.mercatortowgs84(r['Centroid Longitude'], r['Centroid Latitude'])
    return lng1, lat1
r['coords2'] = r.apply(convert_to_wgs84, axis = 1)
r[['lon2', 'lat2']] = r['coords2'].apply(lambda x: pd.Series([x[0], x[1]]))


res='1'
r[['Number of Clusters','lon2', 'lat2']] .to_csv(res+'.csv', index=False)