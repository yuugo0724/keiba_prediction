import pandas as pd
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df_tmp = pd.read_csv('/home/hato/src/data/tmp/shaping.csv')
df_master = pd.read_csv('/home/hato/src/data/master/master.csv',index_col=0)
df_tmp = df_tmp.dropna(subset=['馬名'])
print(df_master)
print(df_tmp['馬名'])
for bamei in df_tmp['馬名']:
  #print(bamei)
  print(df_master.loc[bamei,'encoding'])
