import os
import re
import subprocess
import numpy as np
import pandas as pd
#from easydict import EasyDict

class create_dataframe:
  def __init__(self, lps, df_cols):
    self.lps = lps
    self.df_cols = df_cols
  
  def create_master_grades(self,race_date_list):
    # 取得したレース結果ファイルのパスリスト
    race_file_list = []
    # レース結果格納ディレクトリを再帰的に検索
    for current_dir, sub_dirs, files_list in os.walk(self.lps.DATA_GRADES_DIR):
      current_dir_jud = current_dir.replace(self.lps.DATA_GRADES_DIR,"")
      current_dir_jud = current_dir_jud.replace("/","")
      dir_jud = current_dir_jud in race_date_list
      if dir_jud:
        for file in files_list:
          race_file_list.append(os.path.join(current_dir,file))
    df_list = []
    for race_file in race_file_list:
      df_tmp = pd.read_pickle(race_file)
      df_list.append(df_tmp)
    df = pd.concat(df_list)
    df = df.reset_index(drop=True)
    df.to_pickle(self.lps.DATA_GRADES_MASTER, compression='zip')
  
  def create_master_horseid(self,grades_master):
    df_horse_id_master = grades_master[[self.df_cols.HORSE_ID,self.df_cols.HORSE_NAME]]
    df_horse_id_master = df_horse_id_master.drop_duplicates()
    df_horse_id_master = df_horse_id_master.reset_index(drop=True)
    df_horse_id_master.to_pickle(self.lps.DATA_HORSE_ID_MASTER)

  def create_master_jockeyid(self,grades_master):
    df_horse_id_master = grades_master[[self.df_cols.JOCKEY_ID,self.df_cols.JOCKEY_NAME]]
    df_horse_id_master = df_horse_id_master.drop_duplicates()
    df_horse_id_master = df_horse_id_master.reset_index(drop=True)
    df_horse_id_master.to_pickle(self.lps.DATA_JOCKEY_ID_MASTER)

  def create_master_trainerid(self,grades_master):
    df_horse_id_master = grades_master[[self.df_cols.TRAINER_ID,self.df_cols.TRAINER_NAME]]
    df_horse_id_master = df_horse_id_master.drop_duplicates()
    df_horse_id_master = df_horse_id_master.reset_index(drop=True)
    df_horse_id_master.to_pickle(self.lps.DATA_TRAINER_ID_MASTER)

