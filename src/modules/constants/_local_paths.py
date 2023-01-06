import os
import dataclasses

@dataclasses.dataclass(frozen=True)
class LocalPaths:
  """
  プロジェクトルートのディレクトリ
  """
  BASE_DIR: str = os.path.abspath('./')
  """
  dataディレクトリ
  """
  DATA_DIR: str = os.path.join(BASE_DIR, 'data')
  DATA_URL_DIR: str = os.path.join(DATA_DIR, 'url')
  DATA_TMP_DIR: str = os.path.join(DATA_DIR, 'tmp')
  DATA_TRAINDATA_DIR: str = os.path.join(DATA_DIR, 'train_data')
  DATA_PARAMETER_DIR: str = os.path.join(DATA_DIR, 'model_parameter')
  DATA_GRADES_DIR: str = os.path.join(DATA_DIR, 'grades')
  DATA_HORSE_GRADES_DIR: str = os.path.join(DATA_DIR, 'horse_grades')
  DATA_PEDIGREE_DIR: str = os.path.join(DATA_DIR, 'pedigree')
  DATA_MASTER_DIR: str = os.path.join(DATA_DIR, 'master')
  DATA_PRED_DIR: str = os.path.join(DATA_DIR, 'pred')
  DATA_JUUSHOU_DIR: str = os.path.join(DATA_DIR, 'juushou')
  """
  modelsディレクトリ
  """
  MODEL_DIR: str = os.path.join(BASE_DIR, 'models')
  """
  scrapyディレクトリ
  """
  # scrapyディレクトリ
  SCRAPY_DIR: str = os.path.join(BASE_DIR, 'scrapy')
  # scrapy(成績)のディレクトリ
  SCRAPY_KEIBA_DIR: str = os.path.join(SCRAPY_DIR, 'keiba')
  """
  data
  """
  # master
  DATA_GRADES_MASTER: str = os.path.join(DATA_MASTER_DIR, 'grades')
  DATA_HORSE_ID_MASTER: str = os.path.join(DATA_MASTER_DIR, 'horse_id')
  DATA_JOCKEY_ID_MASTER: str = os.path.join(DATA_MASTER_DIR, 'jockey_id')
  DATA_TRAINER_ID_MASTER: str = os.path.join(DATA_MASTER_DIR, 'trainer_id')
  DATA_TMP_PRED: str = os.path.join(DATA_TMP_DIR, 'pred_race_grades')
  DATA_JUUSHOU_LIST: str = os.path.join(DATA_JUUSHOU_DIR, 'juushou_list_')
  """
  プログラムのパス
  """
  PROC_COLL_URL: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_url.py')
  PROC_COLL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_grades.py')
  PROC_COLL_HORSE_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_horse_grades.py')
  PROC_COLL_PEDIGREE: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pedigree.py')
  PROC_COLL_PRED_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pred_grades.py')
  PROC_COLL_EVAL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_eval_grades.py')
  PROC_COLL_JUUSHOU: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_juushou.py')
  
  """
  ログのパス
  """
  LOG_COLL_URL: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_url.log')
  LOG_COLL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_grades.log')
  LOG_COLL_HORSE_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_horse_grades.log')
  LOG_COLL_PEDIGREE: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pedigree.log')
  LOG_COLL_PRED_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pred_grades.log')
  LOG_COLL_EVAL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_eval_grades.log')
  LOG_COLL_JUUSHOU: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_juushou.log')

  """
  ラベルエンコーディング
  """
  LABEL_XTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'label_x_train')
  LABEL_XTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'label_x_test')
  LABEL_YTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'label_y_train')
  LABEL_YTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'label_y_test')
  LABEL_LGBTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'label_lgb_train')
  LABEL_LGBEVAL: str = os.path.join(DATA_TRAINDATA_DIR, 'label_lgb_eval')
  LABEL_MODEL: str = os.path.join(MODEL_DIR, 'label_model')
  LABEL_PARAMETER_BESTPARAMS: str = os.path.join(DATA_PARAMETER_DIR, 'label_best_params')
  LABEL_PARAMETER_HISTORY: str = os.path.join(DATA_PARAMETER_DIR, 'label_history')
  
  """
  ダミー変数
  """
  DUMMIES_XTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_x_train')
  DUMMIES_XTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_x_test')
  DUMMIES_YTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_y_train')
  DUMMIES_YTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_y_test')
  DUMMIES_LGBTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_lgb_train')
  DUMMIES_LGBEVAL: str = os.path.join(DATA_TRAINDATA_DIR, 'dummies_lgb_eval')
  DUMMIES_MODEL: str = os.path.join(MODEL_DIR, 'dummies_model')
  DUMMIES_PARAMETER_BESTPARAMS: str = os.path.join(DATA_PARAMETER_DIR, 'dummies_best_params')
  DUMMIES_PARAMETER_HISTORY: str = os.path.join(DATA_PARAMETER_DIR, 'dummies_history')

  """
  カウントエンコーディング
  """
  COUNT_XTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'count_x_train')
  COUNT_XTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'count_x_test')
  COUNT_YTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'count_y_train')
  COUNT_YTEST: str = os.path.join(DATA_TRAINDATA_DIR, 'count_y_test')
  COUNT_LGBTRAIN: str = os.path.join(DATA_TRAINDATA_DIR, 'count_lgb_train')
  COUNT_LGBEVAL: str = os.path.join(DATA_TRAINDATA_DIR, 'count_lgb_eval')
  COUNT_MODEL: str = os.path.join(MODEL_DIR, 'count_model')
  COUNT_PARAMETER_BESTPARAMS: str = os.path.join(DATA_PARAMETER_DIR, 'count_best_params')
  COUNT_PARAMETER_HISTORY: str = os.path.join(DATA_PARAMETER_DIR, 'count_history')
  
class TrainDataPaths(LocalPaths):
  DATA_TRAINDATA_XTRAIN: str = ""
  DATA_TRAINDATA_YTRAIN: str = ""
  DATA_TRAINDATA_XTEST: str = ""
  DATA_TRAINDATA_YTEST: str = ""
  DATA_TRAINDATA_LGBTRAIN: str = ""
  DATA_TRAINDATA_LGBEVAL: str = ""
  DATA_PARAMETER_BESTPARAMS: str = ""
  DATA_PARAMETER_HISTORY: str = ""
  MODELS_MODEL: str = ""
  TRAIN_LABEL: str = 'label'
  TRAIN_DUMMIES: str = 'dummies'
  TRAIN_COUNT: str = 'count'
  PRED_LABEL: str = 'pred_label'
  PRED_DUMMIES: str = 'pred_dummies'
  PRED_COUNT: str = 'pred_count'
  MODEL_MULTICLASS_3: str = 'multiclass_3'
  MODEL_MULTICLASS_5: str = 'multiclass_5'
  MODEL_BINARYCLASS: str = 'binaryclass'
  CATEGORY_TYPE: str = ""
  MODEL_TYPE: str = ""
  PRED_JSON: str = ""
  def __init__(self, model_type, category_type):
    self.MODEL_TYPE = model_type
    self.CATEGORY_TYPE = category_type
    category_dict={
      self.TRAIN_LABEL:
        self.set_label_path,
      self.TRAIN_DUMMIES:
        self.set_dummies_path,
      self.TRAIN_COUNT:
        self.set_count_path,
      self.PRED_LABEL:
        self.set_label_path,
      self.PRED_DUMMIES:
        self.set_dummies_path,
      self.PRED_COUNT:
        self.set_count_path
      }
    category_dict[category_type](self.MODEL_TYPE)
  
  def set_label_path(self, model_type):
    self.DATA_TRAINDATA_XTRAIN = self.LABEL_XTRAIN + "_" + model_type
    self.DATA_TRAINDATA_YTRAIN = self.LABEL_YTRAIN + "_" + model_type
    self.DATA_TRAINDATA_XTEST = self.LABEL_XTEST + "_" + model_type
    self.DATA_TRAINDATA_YTEST = self.LABEL_YTEST + "_" + model_type
    self.DATA_TRAINDATA_LGBTRAIN = self.LABEL_LGBTRAIN + "_" + model_type
    self.DATA_TRAINDATA_LGBEVAL = self.LABEL_LGBEVAL + "_" + model_type
    self.DATA_PARAMETER_BESTPARAMS = self.LABEL_PARAMETER_BESTPARAMS + "_" + model_type
    self.DATA_PARAMETER_HISTORY = self.LABEL_PARAMETER_HISTORY + "_" + model_type
    self.MODELS_MODEL = self.LABEL_MODEL + "_" + model_type
    self.PRED_JSON = os.path.join(self.DATA_PRED_DIR, model_type + "_" + self.CATEGORY_TYPE + ".json")

  def set_dummies_path(self, model_type):
    self.DATA_TRAINDATA_XTRAIN = self.DUMMIES_XTRAIN + "_" + model_type
    self.DATA_TRAINDATA_YTRAIN = self.DUMMIES_YTRAIN + "_" + model_type
    self.DATA_TRAINDATA_XTEST = self.DUMMIES_XTEST + "_" + model_type
    self.DATA_TRAINDATA_YTEST = self.DUMMIES_YTEST + "_" + model_type
    self.DATA_TRAINDATA_LGBTRAIN = self.DUMMIES_LGBTRAIN + "_" + model_type
    self.DATA_TRAINDATA_LGBEVAL = self.DUMMIES_LGBEVAL + "_" + model_type
    self.DATA_PARAMETER_BESTPARAMS = self.DUMMIES_PARAMETER_BESTPARAMS + "_" + model_type
    self.DATA_PARAMETER_HISTORY = self.DUMMIES_PARAMETER_HISTORY + "_" + model_type
    self.MODELS_MODEL = self.DUMMIES_MODEL + "_" + model_type
    self.PRED_JSON = os.path.join(self.DATA_PRED_DIR, model_type + "_" + self.CATEGORY_TYPE + ".json")

  def set_count_path(self, model_type):
    self.DATA_TRAINDATA_XTRAIN = self.COUNT_XTRAIN + "_" + model_type
    self.DATA_TRAINDATA_YTRAIN = self.COUNT_YTRAIN + "_" + model_type
    self.DATA_TRAINDATA_XTEST = self.COUNT_XTEST + "_" + model_type
    self.DATA_TRAINDATA_YTEST = self.COUNT_YTEST + "_" + model_type
    self.DATA_TRAINDATA_LGBTRAIN = self.COUNT_LGBTRAIN + "_" + model_type
    self.DATA_TRAINDATA_LGBEVAL = self.COUNT_LGBEVAL + "_" + model_type
    self.DATA_PARAMETER_BESTPARAMS = self.COUNT_PARAMETER_BESTPARAMS + "_" + model_type
    self.DATA_PARAMETER_HISTORY = self.COUNT_PARAMETER_HISTORY + "_" + model_type
    self.MODELS_MODEL = self.COUNT_MODEL + "_" + model_type
    self.PRED_JSON = os.path.join(self.DATA_PRED_DIR, model_type + "_" + self.CATEGORY_TYPE + ".json")
