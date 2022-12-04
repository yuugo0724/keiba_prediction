from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
from modules.constants import LocalPaths

def bind_data():
  lp = LocalPaths()
  pickle_path_list = []
  tmp_dir = lp.DATA_TMP_DIR
  scrapy_pickle_dir = lp.SCRAPY_PICKLE_DIR
  for dirpath, subdirs, pickles in os.walk(scrapy_pickle_dir):
    for p in pickles:
      pickle_path_list.append(os.path.join(dirpath, p))
  df_list=[]
  for i in pickle_path_list:
    df_list.append(pd.read_pickle(i))
  df = pd.concat(df_list)
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
  base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')
  df["タイム"] = pd.to_datetime(df["タイム"], format='%M:%S.%f') - base_time
  #df["タイム"] = df["タイム"].dt.total_seconds()
  df["タイム"] = round(df["タイム"].dt.total_seconds(), 2)
  df["性齢"] = df["性齢"].replace(r"\D", "", regex=True)
  df["馬体重(増減)"] = df["馬体重(増減)"].replace("\+", "", regex=True)
  df.to_csv(os.path.join(tmp_dir,'shaping.csv'), mode='w')

  def encoding_data():
    lp = LocalPaths
    tmp_dir = lp.DATA_TMP_DIR
    master_dir = lp.DATA_MASTER_DIR
    df = pd.read_csv(os.path.join(tmp_dir,'shaping.csv'))
    df_master = pd.read_csv(os.path.join(master_dir,'master.csv'))
    bamei_list = []
    for bamei in df['馬名']:
      df_master.query('馬名' == bamei)
      bamei_list.append(df_master.query('馬名' == bamei))
