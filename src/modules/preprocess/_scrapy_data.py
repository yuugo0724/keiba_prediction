from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import os
from modules.constants import LocalPaths

def create_grades_master(race_list,data_master_grades):
  df_list = []
  for race in race_list:
    df_tmp = pd.read_pickle(race)
    df_list.append(df_tmp)
  df = pd.concat(df_list)
  df.to_pickle(data_master_grades)
  
def create_horse_id(race_list):
  df_list = []
  for race in race_list:
    df_tmp = pd.read_pickle(race)
    df_list.append(df_tmp['馬ID'])
  df = pd.concat(df_list)
  df = df.drop_duplicates()
  return df.values.tolist

def conv_int(df):
  df_conv = df['馬体重増減'].replace("+","")
  

def merge_data(data_list: list):
  df_list=[]
  for data in data_list:
    df_tmp = pd.read_pickle(data)
    #df_list.append(pd.read_pickle(data))
    df_list.append(df_tmp)
  df = pd.concat(df_list)
  df = df.dropna(how='any', axis=0)
  df['レース日'] = df['レース日'].replace("日.*", "日", regex=True)
  df['レース日'] = pd.to_datetime(df['レース日'], format='%Y年%m月%d日')
  df['着順'] = df['着順'].replace("\D",np.nan, regex=True)
  df = df.dropna(subset=['着順'])
  df = df.replace(',|・',"", regex=True)

  #df = df.dropna(subset=['着順'], axis=0)
  
  #column_list = []
  #for i in range(df.shape[0]):
  #  column_list.append(i)
  #df.index = column_list
  #order_list = []
  #for i,order in enumerate(df["着順"]):
  #  try:
  #    float(order)
  #  except ValueError:
  #    order_list.append(i)
  #df=df.drop(order_list)
  #base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')
  #df["タイム"] = pd.to_datetime(df["タイム"], format='%M:%S.%f') - base_time
  ##df["タイム"] = df["タイム"].dt.total_seconds()
  #df["タイム"] = round(df["タイム"].dt.total_seconds(), 2)
  #df["性齢"] = df["性齢"].replace(r"\D", "", regex=True)
  #df["馬体重(増減)"] = df["馬体重(増減)"].replace("\+", "", regex=True)
  return df

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

def create_master_horse_name(df):
  #lp = LocalPaths
  #master_dir = lp.DATA_MASTER_DIR
  #tmp_dir = lp.DATA_TMP_DIR
  #df = pd.read_csv(os.path.join(tmp_dir,'shaping.csv'), usecols=['馬名'])
  list_horse_name = df['馬名']
  #df_bamei = df_bamei.drop_duplicates(subset=["馬名"])
  #df_horse_name = df_horse_name.dropna(how='any', axis=0)
  #list_horse_name = list(filter(lambda x: x is not None, list_horse_name))
  list_horse_name = list(filter(None, list_horse_name))
  list_horse_name = list(dict.fromkeys(list_horse_name))
  #list_horse_name = list_horse_name.drop_duplicates()
  #list_horse_name = list_horse_name.dropna()
  #print(df_horse_name)
  #le = LabelEncoder()
  #df['encoded'] = le.fit_transform(df)
  #print(df)
  
  #encoding_list = list(range(list_horse_name.shape[0]))
  encoding_list = list(range(len(list_horse_name)))
  df_master_horse_name = pd.DataFrame(encoding_list, index=list_horse_name, columns=['馬名ID'])
  #df_master_horse_name = pd.DataFrame(
  #  data={'馬名': list_horse_name,
  #        'encoding': encoding_list}
  #)
  #df_master_horse_name.to_csv(os.path.join(master_dir,'master.csv'), mode='w')
  #df["性齢"] = le.fit_transform(df["性齢"])
  #df["騎手名"] = le.fit_transform(df["騎手名"])
  #df["着差"] = le.fit_transform(df["着差"])
  #df["コーナー週過順位"] = le.fit_transform(df["コーナー週過順位"])
  #df["推定上がり"] = le.fit_transform(df["推定上がり"])
  #df["馬体重(増減)"] = le.fit_transform(df["馬体重(増減)"])
  #df["調教師名"] = le.fit_transform(df["調教師名"])
  #df.to_pickle('/home/hato/src/cre_train_data/pickle/test')
  #df.to_csv('/home/hato/src/cre_train_data/pickle/test.csv', mode='w')
  return df_master_horse_name

def create_master_race(df):
  #list_race = df[['レース日','レースカテゴリ','レースクラス','レースルール','レース重量','レースコース']]
  #df = df.replace("\"|,|\[|\]|\{|\}|:","", regex=True)
  df_master_race = pd.DataFrame(
    data={'レース日': df['レース日'],
          'レースタイトル': df['レースタイトル'],
          'レースカテゴリ': df['レースカテゴリ'],
          'レースクラス': df['レースクラス'],
          'レースルール': df['レースルール'],
          'レース重量': df['レース重量'],
          'レースコース': df['レースコース']}
  )
  #df_master_race['レース日'] = df_master_race['レース日'].replace("日.*", "日", regex=True)
  #df_master_race['レース日'] = pd.to_datetime(df_master_race['レース日'], format='%Y年%m月%d日')
  #print(df_master_race['レース日'])
  #print(df_master_race['レース日'].replace(r"\D", "", regex=True))
  
  #list_race = list(filter(None, list_race))
  #list_race = list(dict.fromkeys(list_race))
  df_master_race = df_master_race.drop_duplicates()
  df_master_race = df_master_race.dropna()
  #print(df_master_race)
  encoding_list = list(range(len(df_master_race)))
  df_master_race = df_master_race.assign(レースID=encoding_list)
  #pd.DataFrame(encoding_list, index=list_race, columns=['encoding'])
  return df_master_race

def create_grades(df):
  lp = LocalPaths
  df_hourse = pd.read_csv(lp.MASTER_HOURSE_NAME, index_col=0)
  df['性齢'] = df['性齢'].replace("\D","", regex=True)
  df["馬体重(増減)"] = df["馬体重(増減)"].replace("\+", "", regex=True)
  df_race = pd.read_csv(lp.MASTER_RACE, parse_dates=[0])
  df = pd.merge(df, df_hourse, left_on=['馬名'], how='left', right_index=True)
  df = pd.merge(df, df_race, on=['レース日','レースコース','レースカテゴリ','レースルール','レース重量','レースコース'], how='left')
  
  df_grades = pd.DataFrame(
    data={'レースID': df['レースID'],
          'レース日': df['レース日'],
          'レースタイトル': df['レースタイトル_x'],
          'レースカテゴリ': df['レースカテゴリ'],
          'レースクラス': df['レースクラス_x'],
          'レースルール': df['レースルール'],
          'レース重量': df['レース重量'],
          'レースコース': df['レースコース'],
          '着順': df['着順'],
          '枠': df['枠'],
          '馬名ID': df['馬名ID'],
          '馬番': df['馬番'],
          '馬名': df['馬名'],
          '性齢': df['性齢'],
          '負担重量': df['負担重量'],
          '騎手名': df['騎手名'],
          '馬体重': df['馬体重'],
          '馬体重(増減)': df['馬体重(増減)'],
          '調教師名': df['調教師名'],
          '単勝人気': df['単勝人気']}
  )
  return df_grades

def category_proc(df):
  df = pd.get_dummies(df,columns=['レース日'])
  df = pd.get_dummies(df,columns=['レースタイトル'])
  df = pd.get_dummies(df,columns=['レースカテゴリ'])
  df = pd.get_dummies(df,columns=['レースクラス'])
  df = pd.get_dummies(df,columns=['レースルール'])
  df = pd.get_dummies(df,columns=['レース重量'])
  df = pd.get_dummies(df,columns=['レースコース'])
  df = pd.get_dummies(df,columns=['騎手名'])
  df = pd.get_dummies(df,columns=['調教師名'])

  return df

def tran_2data(df):
  #df_3 = df.loc[df['着順']<3,['着順']] = 1
  #df_3 = df_3.loc[df_3['着順']>3,['着順']] = 0
  df.loc[df['着順']<=3,['着順']] = 1
  df.loc[df['着順']>3,['着順']] = 0
  return df
  #return df_3
