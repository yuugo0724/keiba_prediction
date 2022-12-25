from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import os
import re
import pickle
from optuna.integration import lightgbm as lgb
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class dataframe_grades:
  def __init__(self, grades_master, lps, tdp, df_cols, race_info):
    self.lps = lps
    self.tdp = tdp
    self.grades_master = grades_master
    self.df_cols = df_cols
    self.race_info = race_info
    self.place_dict = self.race_info.PLACE_DICT
    self.race_type_dict = self.race_info.RACE_TYPE_DICT
    self.x_train, self.x_test, self.y_train, self.y_test = "","","",""
    self.x_train_rus_std, self.x_test_std = "",""
    self.lgb_train, self.lgb_eval = "",""
    self.horseid_master = pd.read_pickle(self.lps.DATA_HORSE_ID_MASTER)
    self.jockeyid_master = pd.read_pickle(self.lps.DATA_JOCKEY_ID_MASTER)
    self.trainerid_master = pd.read_pickle(self.lps.DATA_TRAINER_ID_MASTER)
  
  def train_data_model_type(self):
    select_model_dict = {
      self.tdp.MODEL_MULTICLASS_3:self.setting_multiclass_3,
      self.tdp.MODEL_MULTICLASS_5:self.setting_multiclass_5,
      self.tdp.MODEL_BINARYCLASS:self.setting_binaryclass
    }
    select_model_dict[self.tdp.MODEL_TYPE]()

  def train_split_raceinfo(self):
    race_info_list = self.grades_master[self.df_cols.RACE_INFO]
    race_info_type = []
    race_info_meter = []
    race_info_around = []
    race_info_status = []
    for race_info in race_info_list:
      s_race_info = race_info.split('/')
      s_info = re.sub(" ","",s_race_info[0])
      around_info = re.findall("右|左",s_info)
      if around_info:
        race_info_around.append(around_info[0])
      else:
        race_info_around.append('')
      race_info_meter.append(re.sub("\D","",s_info))
      type_info = s_race_info[2]
      type_info = re.sub(" ","",type_info)
      type_info = type_info.split(':')
      race_info_type.append(re.sub(" ","",type_info[0]))
      race_info_status.append(re.sub(" ","",type_info[1]))
    self.grades_master[self.df_cols.RACE_METERS] = race_info_meter
    self.grades_master[self.df_cols.RACE_AROUND] = race_info_around
    self.grades_master[self.df_cols.RACE_TYPE] = race_info_type
    self.grades_master[self.df_cols.RACE_STATUS] = race_info_status
  
  def pred_split_raceinfo(self):
    race_info_list = self.grades_master[self.df_cols.RACE_INFO]
    race_info_type = []
    race_info_meter = []
    race_info_around = []
#    race_info_status = []
    for race_info in race_info_list:
      race_info = re.sub(" ","",race_info)
      around_info = re.findall("右|左",race_info)
      if around_info:
        race_info_around.append(around_info[0])
      else:
        race_info_around.append('')
      race_info_meter_list = re.findall(r'[0-9]+m',race_info)
      race_info_meter_list = re.sub("m","",race_info_meter_list[0])
      race_info_meter.append(race_info_meter_list)
      type_info = re.findall('芝|ダ|障',race_info)
      type_info = self.race_info.RACE_TYPE_DICT[type_info[0]]
      race_info_type.append(type_info)
#      race_info_status.append(re.sub(" ","",type_info[1]))
    self.grades_master[self.df_cols.RACE_METERS] = race_info_meter
    self.grades_master[self.df_cols.RACE_AROUND] = race_info_around
    self.grades_master[self.df_cols.RACE_TYPE] = race_info_type
#    self.grades_master[self.df_cols.RACE_STATUS] = race_info_status
  
  def remove_missing_values(self):
    self.grades_master = self.grades_master.dropna(how='any')
  
  def conversion_values(self):
    conv_weight_inc_dec_list = self.grades_master[self.df_cols.WEIGHT_INC_DEC].replace("+","").astype('int')
    self.grades_master[self.df_cols.WEIGHT_INC_DEC] = conv_weight_inc_dec_list

  def pred_conversion_values(self):
    inc_dec_list = []
    inc_dec_info = self.grades_master[self.df_cols.WEIGHT_INC_DEC]
    for inc_dec in inc_dec_info:
      inc_dec = re.sub("\+","",inc_dec)
      try:
        inc_dec = int(inc_dec)
      except:
        inc_dec = 0
      inc_dec_list.append(inc_dec)
    self.grades_master[self.df_cols.WEIGHT_INC_DEC] = inc_dec_list

#    try:
#      conv_weight_inc_dec_list = self.grades_master[self.df_cols.WEIGHT_INC_DEC].replace("+","").astype('int')
#      self.grades_master[self.df_cols.WEIGHT_INC_DEC] = conv_weight_inc_dec_list
#      print("■pred_conversion_values")
#      print(self.grades_master[self.df_cols.WEIGHT_INC_DEC])
#    except:
#      pass
#    print("■pred_conversion_values")
#    print(self.grades_master)


  def split_sexual_age(self):
    sexual_age = self.grades_master[self.df_cols.SEXUAL_AGE]
    sex = sexual_age.replace('[0-9]+',"", regex=True)
    age = sexual_age.replace("\D","", regex=True)
    self.grades_master[self.df_cols.SEX] = sex
    self.grades_master[self.df_cols.AGE] = age.astype(int)
#    print("■split_sexual_age")
#    print(self.grades_master)
  
  def select_place_name(self, place = None):
    place_id_list = []
    race_id_list = self.grades_master[self.df_cols.RACE_ID]
    for place_id in race_id_list:
      place_id_list.append(self.place_dict[place_id[4:6]])
    self.grades_master[self.df_cols.PLACE] = place_id_list
    if place is not None:
      # 競馬場指定
      self.grades_master = self.grades_master[self.grades_master[self.df_cols.PLACE]==place]
#    print("■select_place_name")
#    print(self.grades_master)

  def select_G_race(self):
    self.grades_master = self.grades_master[self.grades_master[self.df_cols.RACE_NAME].str.contains('G1|G2|G3')]
  
  def select_race_type(self, race_type: list = ['芝','ダート','障']):
    self.grades_master = self.grades_master[self.grades_master[self.df_cols.RACE_TYPE].isin(race_type)]
#    print("■select_race_type")
#    print(self.grades_master)
  
  def category_process(self):
    category_dict={
      self.tdp.TRAIN_LABEL:[
        self.df_cols.train_data_cols_label(),
        self.label_encoding_process
        ],
      self.tdp.TRAIN_DUMMIES:[
        self.df_cols.train_data_cols_dummies(),
        self.update_dummies
        ],
      self.tdp.TRAIN_COUNT:[
        self.df_cols.train_data_cols_label(),
        self.count_encoding_process
        ],
      self.tdp.PRED_LABEL:[
        self.df_cols.pred_data_cols_label(),
        self.label_encoding_process
        ],
      self.tdp.PRED_DUMMIES:[
        self.df_cols.pred_data_cols_dummies(),
        self.update_dummies
        ],
      self.tdp.PRED_COUNT:[
        self.df_cols.pred_data_cols_label(),
        self.count_encoding_process
        ]
      }
    self.grades_master = self.grades_master[category_dict[self.tdp.CATEGORY_TYPE][0]]
    self.grades_master = pd.get_dummies(self.grades_master,columns=self.df_cols.dummies_cols_common())
    category_dict[self.tdp.CATEGORY_TYPE][1]()

  def pred_merge_dummies(self):
    pred_df = pd.read_pickle(self.tdp.DATA_TRAINDATA_XTRAIN)
    pred_cols = pred_df.columns.values
    for col in pred_cols:
      if col in self.grades_master:
        pass
      else:
        self.grades_master[col]=0
    self.grades_master = self.grades_master[pred_cols]

  def conversion_int(self):
    # to_numericで整数に変換できないデータをNoneに変換
    self.grades_master[self.df_cols.RANK] = pd.to_numeric(self.grades_master[self.df_cols.RANK],errors='coerce')
    self.grades_master[self.df_cols.RACE_METERS] = pd.to_numeric(self.grades_master[self.df_cols.RACE_METERS],errors='coerce')
    # Noneが格納されている行を削除
    self.grades_master = self.grades_master.dropna(how='any', axis=0)
    # 整数型に変換
    self.grades_master[self.df_cols.RANK] = self.grades_master[self.df_cols.RANK].astype('int')
    self.grades_master[self.df_cols.RACE_METERS] = self.grades_master[self.df_cols.RACE_METERS].astype('int')
    
    self.grades_master[self.df_cols.WAKU_NUM] = self.grades_master[self.df_cols.WAKU_NUM].astype(int)
    self.grades_master[self.df_cols.LOAD] = self.grades_master[self.df_cols.LOAD].astype(float)
    self.grades_master[self.df_cols.WEIGHT] = self.grades_master[self.df_cols.WEIGHT].astype(int)
    
  def pred_conversion_int(self):
    # 整数型に変換
    try:
      self.grades_master[self.df_cols.RACE_METERS] = self.grades_master[self.df_cols.RACE_METERS].astype('int')    
    except:
      pass
    try:
      self.grades_master[self.df_cols.WAKU_NUM] = self.grades_master[self.df_cols.WAKU_NUM].astype(int)
    except:
      pass
    try:
      self.grades_master[self.df_cols.LOAD] = self.grades_master[self.df_cols.LOAD].astype(float)
    except:
      pass
    try:
      self.grades_master[self.df_cols.WEIGHT] = self.grades_master[self.df_cols.WEIGHT].astype(int)
    except:
      pass
#    print("■pred_conversion_int")
#    print(self.grades_master)

    
  def setting_multiclass_3(self):
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==1,[self.df_cols.RANK]] = 0
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==2,[self.df_cols.RANK]] = 1
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==3,[self.df_cols.RANK]] = 2
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]>3,[self.df_cols.RANK]] = 3

  def setting_multiclass_5(self):
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==1,[self.df_cols.RANK]] = 0
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==2,[self.df_cols.RANK]] = 1
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==3,[self.df_cols.RANK]] = 2
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==4,[self.df_cols.RANK]] = 3
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]==5,[self.df_cols.RANK]] = 4
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]>5,[self.df_cols.RANK]] = 5

  def setting_binaryclass(self):
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]<4,[self.df_cols.RANK]] = 0
    self.grades_master.loc[self.grades_master[self.df_cols.RANK]>3,[self.df_cols.RANK]] = 1

  def update_dummies(self):
    self.grades_master = pd.get_dummies(self.grades_master,columns=self.df_cols.dummies_cols())

#  def update_dummies_common(self):
#    self.grades_master = pd.get_dummies(self.grades_master,columns=self.df_cols.dummies_cols_common())
  
  def label_encoding_process(self):
#    for i, horseid in enumerate(list(self.grades_master[self.df_cols.HORSE_ID])):
#      if horseid not in self.horseid_master[self.df_cols.HORSE_ID]:
#        horsename = self.horseid_master[self.df_cols.HORSE_NAME].iloc[i]
#        horseinfo = [[horseid,horsename]]
#        horseinfo_df = pd.DataFrame(horseinfo,columns=[self.df_cols.HORSE_ID,self.df_cols.HORSE_NAME])
#        self.horseid_master = pd.concat([self.horseid_master, horseinfo_df], ignore_index=True)
    horseid_list = list(self.horseid_master[self.df_cols.HORSE_ID])
    horseid_label_list = list(self.horseid_master.index)
    horseid_cols = [self.df_cols.HORSE_ID, self.df_cols.HORSEID_LABEL]
    self.horseid_master = pd.DataFrame(columns=horseid_cols)
    self.horseid_master[self.df_cols.HORSEID_LABEL] = horseid_label_list
    self.horseid_master[self.df_cols.HORSE_ID] = horseid_list
    #jockeyid_master = pd.read_pickle(self.lps.DATA_JOCKEY_ID_MASTER)
    jockeyid_list = list(self.jockeyid_master[self.df_cols.JOCKEY_ID])
    jockeyid_label_list = list(self.jockeyid_master.index)
    jockeyid_cols = [self.df_cols.JOCKEY_ID, self.df_cols.JOCKEYID_LABEL]
    self.jockeyid_master = pd.DataFrame(columns=jockeyid_cols)
    self.jockeyid_master[self.df_cols.JOCKEY_ID] = jockeyid_list
    self.jockeyid_master[self.df_cols.JOCKEYID_LABEL] = jockeyid_label_list

    #trainerid_master = pd.read_pickle(self.lps.DATA_TRAINER_ID_MASTER)
    trainerid_label_list = list(self.trainerid_master.index)
    trainerid_list = list(self.trainerid_master[self.df_cols.TRAINER_ID])
    trainerid_cols = [self.df_cols.TRAINER_ID, self.df_cols.TRAINERID_LABEL]
    self.trainerid_master = pd.DataFrame(columns=trainerid_cols)
    self.trainerid_master[self.df_cols.TRAINER_ID] = trainerid_list
    self.trainerid_master[self.df_cols.TRAINERID_LABEL] = trainerid_label_list

    self.grades_master = pd.merge(self.grades_master, self.horseid_master, on = self.df_cols.HORSE_ID, how = 'left')
    self.grades_master = pd.merge(self.grades_master, self.jockeyid_master, on = self.df_cols.JOCKEY_ID, how = 'left')
    self.grades_master = pd.merge(self.grades_master, self.trainerid_master, on = self.df_cols.TRAINER_ID, how = 'left')
    self.grades_master = self.grades_master.fillna(0)
    self.grades_master = self.grades_master.drop(columns = self.df_cols.drop_id_cols())

  def count_encoding_process(self):
    count_col = 'count'
    horseid_list = self.grades_master[self.df_cols.HORSE_ID]
    count_horse = pd.DataFrame(horseid_list,columns=[self.df_cols.HORSE_ID])
    count_horse[count_col] = count_horse.groupby(self.df_cols.HORSE_ID)[self.df_cols.HORSE_ID].transform(count_col)
    count_horse = count_horse.drop_duplicates()

    jockeyid_list = self.grades_master[self.df_cols.JOCKEY_ID]
    count_jockey = pd.DataFrame(jockeyid_list,columns=[self.df_cols.JOCKEY_ID])
    count_jockey[count_col] = count_jockey.groupby(self.df_cols.JOCKEY_ID)[self.df_cols.JOCKEY_ID].transform(count_col)
    count_jockey = count_jockey.drop_duplicates()

    trainerid_list = self.grades_master[self.df_cols.TRAINER_ID]
    count_trainer = pd.DataFrame(trainerid_list,columns=[self.df_cols.TRAINER_ID])
    count_trainer[count_col] = count_trainer.groupby(self.df_cols.TRAINER_ID)[self.df_cols.TRAINER_ID].transform(count_col)
    count_trainer = count_trainer.drop_duplicates()

    self.grades_master = pd.merge(self.grades_master, count_horse, on = self.df_cols.HORSE_ID, how = 'left')
    self.grades_master = pd.merge(self.grades_master, count_jockey, on = self.df_cols.JOCKEY_ID, how = 'left')
    self.grades_master = pd.merge(self.grades_master, count_trainer, on = self.df_cols.TRAINER_ID, how = 'left')

    self.grades_master = self.grades_master.dropna(how='any', axis=0)
    self.grades_master = self.grades_master.drop(columns = self.df_cols.drop_id_cols())

  def blank_conversion(self):
    self.grades_master.loc[self.grades_master[self.df_cols.WEIGHT]=='',[self.df_cols.WEIGHT]] = 0
    #self.grades_master.loc[self.grades_master[self.df_cols.WEIGHT]==' ',[self.df_cols.WEIGHT]] = 0
    #self.grades_master.loc[self.grades_master[self.df_cols.WEIGHT_INC_DEC]==' ',[self.df_cols.WEIGHT_INC_DEC]] = 0
    #self.grades_master = self.grades_master.fillna(0)

  def data_preprocess(self):
    # 説明変数
    self.x_train = self.grades_master.drop([self.df_cols.RANK], axis=1)
    # 目的変数
    self.y_train = self.grades_master[self.df_cols.RANK]
    rank_list = self.y_train.drop_duplicates()
    # クラス別の目的変数の数をカウント
    y_train_list = []
    for rank in rank_list:
      y_train_list.append(len([i for i in self.y_train if i == rank]))
    # 最小の目的変数の数を定義
    y_train_min_list = []
    for y in y_train_list:
      y_train_min_list.append(y)
    y_train_min = min(y_train_min_list)
    # 最小の目的変数の数でアンダーサンプリング
    count_y = y_train_min
    sampling_key = range(len(y_train_min_list))
    if self.tdp.MODEL_TYPE == self.tdp.MODEL_BINARYCLASS:
      sampling_value = [count_y,count_y * 2]
    else:
      sampling_value = [count_y] * len(y_train_min_list)
    sampling_dict = dict(zip(sampling_key,sampling_value))
    rus = RandomUnderSampler(sampling_strategy=sampling_dict)
    x_train_rus, y_train_rus = rus.fit_resample(self.x_train, self.y_train)
    # 学習データと検証データを7:3で分ける
    self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x_train_rus, y_train_rus, test_size=0.3)
#    # 説明変数を標準化
#    sc = StandardScaler()
#    self.x_train_rus_std = pd.DataFrame(sc.fit_transform(self.x_train), columns=self.x_train.columns)
#    self.x_test_std = pd.DataFrame(sc.transform(self.x_test), columns=self.x_test.columns)
    # 学習データの作成
    self.lgb_train = lgb.Dataset(self.x_train, self.y_train)
    self.lgb_eval = lgb.Dataset(self.x_test, self.y_test)
    # 学習データの保存
    self.save_train_data()

  def pred_data_preprocess(self):
    sc = StandardScaler()
    self.grades_master = pd.DataFrame(sc.fit_transform(self.grades_master), columns=self.grades_master.columns)


  def save_train_data(self):
    pickle.dump(self.x_train, open(self.tdp.DATA_TRAINDATA_XTRAIN, 'wb'))
    pickle.dump(self.y_train, open(self.tdp.DATA_TRAINDATA_YTRAIN, 'wb'))
    pickle.dump(self.x_test, open(self.tdp.DATA_TRAINDATA_XTEST, 'wb'))
    pickle.dump(self.y_test, open(self.tdp.DATA_TRAINDATA_YTEST, 'wb'))
    pickle.dump(self.lgb_train, open(self.tdp.DATA_TRAINDATA_LGBTRAIN, 'wb'))
    pickle.dump(self.lgb_eval, open(self.tdp.DATA_TRAINDATA_LGBEVAL, 'wb'))

  def show_grades_master(self):
    print(self.grades_master.dtypes)
    print(self.grades_master)
  
  def output_grades_master(self):
    self.grades_master[self.grades_master['回り']==''].to_csv('/home/keiba/src/data/tmp/grades_master.csv')
  
  def tmp_del_shougai(self):
    self.grades_master = self.grades_master[self.grades_master[self.df_cols.RACE_AROUND]!='障']

class dataframe_horse_grades:
  def __init__(self, horse_grades_master):
    self.horse_grades_master = horse_grades_master

class dataframe_pedigree:
  def __init__(self, pedigree_master):
    self.pedigree_master = pedigree_master
