from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os

pickle_path_list = []
dir_path = '/home/hato/src/scrapy/pickle/'
for dirpath, subdirs, pickles in os.walk(dir_path):
  for p in pickles:
    pickle_path_list.append(os.path.join(dirpath, p))

df_list=[]
for i in pickle_path_list:
  print(i)
  df_list.append(pd.read_pickle(i))

df = pd.concat(df_list)
#df1 = pd.read_pickle('/home/hato/src/scrapy/pickle/2021年10月24日日曜4回阪神6日3歳オープン国際牡・牝指定コース：3,000メートル芝・右')
#df2 = pd.read_pickle('/home/hato/src/scrapy/pickle/2018年12月23日祝日・日曜5回中山8日サラ系3歳以上オープン国際指定コース：2,500メートル芝・右')
#df = pd.concat([df1,df2])
df.to_csv('/home/hato/src/cre_train_data/pickle/master.csv', mode='w')

le = LabelEncoder()
df["馬名"] = le.fit_transform(df["馬名"])
df["性齢"] = le.fit_transform(df["性齢"])
df["騎手名"] = le.fit_transform(df["騎手名"])
base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')
#df["タイム"] = pd.to_datetime(df["タイム"], format='%M:%S.%f') - base_time
df["着差"] = le.fit_transform(df["着差"])
df["コーナー週過順位"] = le.fit_transform(df["コーナー週過順位"])
df["推定上がり"] = le.fit_transform(df["推定上がり"])
df["馬体重(増減)"] = le.fit_transform(df["馬体重(増減)"])
df["調教師名"] = le.fit_transform(df["調教師名"])

df.to_pickle('/home/hato/src/cre_train_data/pickle/test')
df.to_csv('/home/hato/src/cre_train_data/pickle/test.csv', mode='w')

column_list = []
for i in range(df.shape[0]):
  column_list.append(i)
df.index = column_list

order_list = []
for i,order in enumerate(df["着順"]):
  try:
    float(order)
  except ValueError:
    order_list.append(i)
df=df.drop(order_list)
print(df)

#time_list = []
#for i,time in enumerate(df["タイム"]):
#  if len(time) == 0:
#    time_list.append(i)
#print(time_list)
#df=df.drop(time_list)
#print(df["タイム"])

#print(pd.to_datetime(df["タイム"]).dt.total_seconds)
#df["タイム"] = df["タイム"].str.zfill(7)
#print(df)
#print(pd.to_datetime(df["タイム"].str.zfill(7),format='%M:%S.%f'))
#df = df.drop(index='中止')
base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')
df["タイム"] = pd.to_datetime(df["タイム"], format='%M:%S.%f') - base_time
#time_list = [i if len(i) == 0 else datetime.datetime.strptime(i, '%M:%S.%f') for i in df["タイム"]]
#for i in df["タイム"]:
#  print(len(i))
#print(pd.to_datetime(df["タイム"], unit='s'))

print(df["タイム"].dt.total_seconds())

