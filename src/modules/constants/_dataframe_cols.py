from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class DataFrameCols:
  """
  データフレームの列名
  """
  RACE_ID: str = 'レースID'
  RACE_INFO: str = 'レース情報'
  RACE_NAME: str = 'レース名'
  RACE_METERS: str = '距離'
  RACE_AROUND: str = '回り'
  RACE_WEATHER: str = '天候'
  RACE_TYPE: str = 'タイプ'
  RACE_STATUS: str = '馬場状態'
  RANK: str = '着順'
  WAKU_NUM: str = '枠番'
  HORSE_NUM: str = '馬番'
  HORSE_NAME: str = '馬名'
  SEXUAL_AGE: str = '性齢'
  LOAD: str = '斥量'
  JOCKEY_NAME: str = '騎手'
  TIME: str = 'タイム'
  ODDS: str = '単勝'
  POP: str = '人気'
  WEIGHT: str = '馬体重'
  WEIGHT_INC_DEC: str = '馬体重増減'
  TRAINER_NAME: str = '調教師'
  HORSE_ID: str = '馬ID'
  JOCKEY_ID: str = '騎手ID'
  TRAINER_ID: str = '調教師ID'
  SEX: str = '性'
  AGE: str = '齢'
  PLACE: str = '競馬場'

  HORSEID_LABEL: str = '馬ID_LABEL'
  JOCKEYID_LABEL: str = '騎手ID_LABEL'
  TRAINERID_LABEL: str = '調教師ID_LABEL'

  def scrapy_grades_cols(self):
    COL_DATAFRAME: list = [
                            self.RACE_ID,
                            self.RACE_NAME,
                            self.RACE_INFO,
#                            self.RACE_METERS,
#                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
#                            self.RACE_TYPE,
#                            self.RACE_STATUS,
                            self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_NUM,
                            self.HORSE_NAME,
                            self.SEXUAL_AGE,
                            self.LOAD,
                            self.JOCKEY_NAME,
                            self.TIME,
                            self.ODDS,
                            self.POP,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_NAME,
                            self.HORSE_ID,
                            self.JOCKEY_ID,
                            self.TRAINER_ID
                          ]
    return COL_DATAFRAME

  def train_data_cols_dummies(self):
    COL_DATAFRAME: list = [
                            self.RACE_METERS,
                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            self.RACE_TYPE,
                            #self.RACE_STATUS,
                            self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_NAME,
                            self.LOAD,
                            self.JOCKEY_NAME,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_NAME,
                            self.SEX,
                            self.AGE
                          ]
    return COL_DATAFRAME

  def pred_data_cols_dummies(self):
    COL_DATAFRAME: list = [
                            self.RACE_METERS,
                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            self.RACE_TYPE,
                            #self.RACE_STATUS,
                            #self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_NAME,
                            self.LOAD,
                            self.JOCKEY_NAME,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_NAME,
                            self.SEX,
                            self.AGE
                          ]
    return COL_DATAFRAME

  def train_data_cols_label(self):
    COL_DATAFRAME: list = [
                            self.RACE_METERS,
                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            self.RACE_TYPE,
                            #self.RACE_STATUS,
                            self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_ID,
                            self.LOAD,
                            self.JOCKEY_ID,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_ID,
                            self.SEX,
                            self.AGE
                          ]
    return COL_DATAFRAME

  def pred_data_cols_label(self):
    COL_DATAFRAME: list = [
                            self.RACE_METERS,
                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            self.RACE_TYPE,
                            #self.RACE_STATUS,
                            #self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_ID,
                            self.LOAD,
                            self.JOCKEY_ID,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_ID,
                            self.SEX,
                            self.AGE
                          ]
    return COL_DATAFRAME

  def dummies_cols(self):
    COL_DATAFRAME: list = [
                            #self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            #self.RACE_TYPE,
                            #self.RACE_STATUS,
                            self.HORSE_NAME,
                            self.JOCKEY_NAME,
                            self.TRAINER_NAME
                            #self.SEX
                          ]
    return COL_DATAFRAME
  
  def dummies_cols_common(self):
    COL_DATAFRAME: list = [
                            self.RACE_AROUND,
                            self.RACE_TYPE,
                            self.SEX
                          ]
    return COL_DATAFRAME

  def pred_data_cols(self):
    COL_DATAFRAME: list = [
                            self.RACE_ID,
                            self.RACE_NAME,
                            self.RACE_INFO,
#                            self.RACE_METERS,
#                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
#                            self.RACE_TYPE,
#                            self.RACE_STATUS,
                            #self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_NUM,
                            self.HORSE_NAME,
                            self.SEXUAL_AGE,
                            self.LOAD,
                            self.JOCKEY_NAME,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_NAME,
                            self.HORSE_ID,
                            self.JOCKEY_ID,
                            self.TRAINER_ID
                          ]
    return COL_DATAFRAME

  def pred_keiba_cols(self):
    COL_DATAFRAME: list = [
                            self.RACE_METERS,
                            self.RACE_AROUND,
                            #self.RACE_WEATHER,
                            self.RACE_TYPE,
                            #self.RACE_STATUS,
                            #self.RANK,
                            self.WAKU_NUM,
                            self.HORSE_NAME,
                            self.LOAD,
                            self.JOCKEY_NAME,
                            self.WEIGHT,
                            self.WEIGHT_INC_DEC,
                            self.TRAINER_NAME,
                            self.SEX,
                            self.AGE
                          ]
    return COL_DATAFRAME

  def drop_id_cols(self):
    COL_DATAFRAME: list = [
                            self.HORSE_ID,
                            self.JOCKEY_ID,
                            self.TRAINER_ID
                          ]
    return COL_DATAFRAME
  

