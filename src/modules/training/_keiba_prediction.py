import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from optuna.integration import lightgbm as lgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

class data_training:
  def __init__(self, lps, tdp, df_cols):
    self.lps = lps
    self.tdp = tdp
    self.df_cols = df_cols
    self.x_train = pickle.load(open(self.tdp.DATA_TRAINDATA_XTRAIN, 'rb'))
    self.y_train = pickle.load(open(self.tdp.DATA_TRAINDATA_YTRAIN, 'rb'))
    self.x_test = pickle.load(open(self.tdp.DATA_TRAINDATA_XTEST, 'rb'))
    self.y_test = pickle.load(open(self.tdp.DATA_TRAINDATA_YTEST, 'rb'))
    self.lgb_train = pickle.load(open(self.tdp.DATA_TRAINDATA_LGBTRAIN, 'rb'))
    self.lgb_eval = pickle.load(open(self.tdp.DATA_TRAINDATA_LGBEVAL, 'rb'))
    self.model = ""
    self.best_params = {}
    self.history = {}
    self.y_pred = []

  def train_lgb(self):
    train_dict = {
      self.tdp.MODEL_MULTICLASS_3:self.lgb_multiclass_3,
      self.tdp.MODEL_MULTICLASS_5:self.lgb_multiclass_5,
      self.tdp.MODEL_BINARYCLASS:self.lgb_binaryclass
    }
    train_dict[self.tdp.MODEL_TYPE]()

  def lgb_multiclass_3(self):
    params = {
      'task': 'train',            # トレーニング用
      'boosting_type': 'gbdt',    # 勾配ブースティング決定木
      'objective': 'multiclass',  # 目的：多クラス分類
      'num_class': 4,             # 分類クラス数
      'metric': 'multi_logloss',  # 評価指標は多クラスのLog損失
      'verbosity': -1             # ログ出力なし
    }
    # ハイパーパラメータの自動調整
    # 調整後のパラメータ : best_params
    # 調整過程のパラメータ : history
    self.model = lgb.train(params,
                      self.lgb_train,
                      valid_sets = [self.lgb_train,self.lgb_eval],
                      valid_names=['train', 'valid'],
    #                  num_boost_round = 100,
                      early_stopping_rounds=10,
                      evals_result=self.history
                      )
    self.best_params = self.model.params
    # モデルを保存
    pickle.dump(self.model, open(self.tdp.MODELS_MODEL, 'wb'))
    # best_paramsの保存
    pickle.dump(self.best_params, open(self.tdp.DATA_PARAMETER_BESTPARAMS, 'wb'))
    # historyの保存
    pickle.dump(self.history, open(self.tdp.DATA_PARAMETER_HISTORY, 'wb'))

  def lgb_multiclass_5(self):
    params = {
      'task': 'train',            # トレーニング用
      'boosting_type': 'gbdt',    # 勾配ブースティング決定木
      'objective': 'multiclass',  # 目的：多クラス分類
      'num_class': 6,             # 分類クラス数
      'metric': 'multi_logloss',  # 評価指標は多クラスのLog損失
      'verbosity': -1             # ログ出力なし
    }
    # ハイパーパラメータの自動調整
    # 調整後のパラメータ : best_params
    # 調整過程のパラメータ : history
    self.model = lgb.train(params,                                  # 学習の経過を保存する変数
                      self.lgb_train,                               # データセット
                      valid_sets = [self.lgb_train,self.lgb_eval],  # モデル検証のデータセット
                      valid_names=['train', 'valid'],               # 学習経過で表示する名所
    #                  num_boost_round = 100,                       # 学習の回数
                      early_stopping_rounds = 10,                   # アーリーストッピング
                      verbose_eval = 100,                           # 学習の経過の表示(100回毎)
                      evals_result=self.history                     # 学習の経過を保存
                      )
    self.best_params = self.model.params
    # モデルを保存
    pickle.dump(self.model, open(self.tdp.MODELS_MODEL, 'wb'))
    # best_paramsの保存
    pickle.dump(self.best_params, open(self.tdp.DATA_PARAMETER_BESTPARAMS, 'wb'))
    # historyの保存
    pickle.dump(self.history, open(self.tdp.DATA_PARAMETER_HISTORY, 'wb'))

  def lgb_binaryclass(self):
    params = {
      'task': 'train',             # トレーニング用
      'boosting_type': 'gbdt',    # 勾配ブースティング決定木
      'objective': 'binary',       # 目的：二値分類
      'metric': 'binary_logloss',  # 評価指標はAUC
      #'verbosity': -1,             # ログ出力なし
      #'num_iterations': 100
    }
    # ハイパーパラメータの自動調整
    # 調整後のパラメータ : best_params
    # 調整過程のパラメータ : history
    verbose_eval = 10 # 100イテレーション毎に学習結果を出力
    callbacks = [
      lgb.early_stopping(10), # early_stopping用コールバック関数
      lgb.log_evaluation(verbose_eval) # コマンドライン出力用コールバック関数
    ]
    self.model = lgb.train(params,
                      self.lgb_train,
                      verbose_eval=verbose_eval, # 100イテレーション毎に学習結果を出力
                      valid_sets = [self.lgb_train,self.lgb_eval],
                      valid_names=['train', 'valid'],
#                      num_boost_round = 10,
                      early_stopping_rounds=10,
#                      callbacks=callbacks,
                      evals_result=self.history
                      )
    self.best_params = self.model.params
    # モデルを保存
    pickle.dump(self.model, open(self.tdp.MODELS_MODEL, 'wb'))
    # best_paramsの保存
    pickle.dump(self.best_params, open(self.tdp.DATA_PARAMETER_BESTPARAMS, 'wb'))
    # historyの保存
    pickle.dump(self.history, open(self.tdp.DATA_PARAMETER_HISTORY, 'wb'))

  def load_parameter(self):
    self.model = pickle.load(open(self.tdp.MODELS_MODEL, 'rb'))
    self.best_params = pickle.load(open(self.tdp.DATA_PARAMETER_BESTPARAMS, 'rb'))
    self.history = pickle.load(open(self.tdp.DATA_PARAMETER_HISTORY, 'rb'))
    preds = self.model.predict(self.x_test, num_iteration=self.model.best_iteration)
    self.y_pred = []
    for pred in preds:
      self.y_pred.append(np.argmax(pred))
    
  def show_parameter(self):
    # best_paramsが辞書型で返って来るのでデータフレームに格納して表示
    df_params = pd.DataFrame.from_dict(self.best_params, orient="index")
    print(df_params)

  def show_mixed_array(self):
    mixed_dict = {
      self.tdp.MODEL_MULTICLASS_3:self.show_multiclass_3_mixed_array,
      self.tdp.MODEL_MULTICLASS_5:self.show_multiclass_5_mixed_array,
      self.tdp.MODEL_BINARYCLASS:self.show_binaryclass_mixed_array
    }
    mixed_dict[self.tdp.MODEL_TYPE]()

  def show_multiclass_3_mixed_array(self):
    cm = confusion_matrix(self.y_test, self.y_pred, labels=[0, 1, 2, 3])
    columns_labels = ['pred_1着','pred_2着','pred_3着','pred_その他']
    index_labels = ['act_1着','act_2着','act_3着','act_その他']
    cm = pd.DataFrame(cm, columns=columns_labels, index=index_labels)
    #正解率など評価指標の計算
    print('正解率(accuracy_score):{}'.format(accuracy_score(self.y_test, self.y_pred)))
    #適合率、再現率、F1値はマクロ平均を取る
    print('再現率(recall_score):{}'.format(recall_score(self.y_test, self.y_pred, average='macro')))
    print('適合率(precision_score):{}'.format(precision_score(self.y_test, self.y_pred, average='macro')))
    print('F1値(f1_score):{}'.format(f1_score(self.y_test, self.y_pred, average='macro')))
    #print(confusion_matrix(self.y_test, self.y_pred, labels=[0, 1, 2, 3]))
    print(cm.to_markdown())

  def show_multiclass_5_mixed_array(self):
    cm = confusion_matrix(self.y_test, self.y_pred, labels=[0, 1, 2, 3, 4, 5])
    columns_labels = ['pred_1着','pred_2着','pred_3着','pred_4着','pred_5着','pred_その他']
    index_labels = ['act_1着','act_2着','act_3着','act_4着','act_5着','act_その他']
    cm = pd.DataFrame(cm, columns=columns_labels, index=index_labels)
    #正解率など評価指標の計算
    print('正解率(accuracy_score):{}'.format(accuracy_score(self.y_test, self.y_pred)))
    #適合率、再現率、F1値はマクロ平均を取る
    print('再現率(recall_score):{}'.format(recall_score(self.y_test, self.y_pred, average='macro')))
    print('適合率(precision_score):{}'.format(precision_score(self.y_test, self.y_pred, average='macro')))
    print('F1値(f1_score):{}'.format(f1_score(self.y_test, self.y_pred, average='macro')))
    #print(confusion_matrix(self.y_test, self.y_pred, labels=[0, 1, 2, 3]))
    print(cm.to_markdown())

  def show_binaryclass_mixed_array(self):
#    cm = confusion_matrix(self.y_test, self.y_pred, labels=[0, 1])
    cm = confusion_matrix(self.y_test, self.y_pred)
    columns_labels = ['pred_1着','pred_その他']
    index_labels = ['act_1着','act_その他']
    cm = pd.DataFrame(cm, columns=columns_labels, index=index_labels)
    #正解率など評価指標の計算
    print('正解率(accuracy_score):{}'.format(accuracy_score(self.y_test, self.y_pred)))
    #適合率、再現率、F1値はマクロ平均を取る
    print('再現率(recall_score):{}'.format(recall_score(self.y_test, self.y_pred)))
    print('適合率(precision_score):{}'.format(precision_score(self.y_test, self.y_pred)))
    print('F1値(f1_score):{}'.format(f1_score(self.y_test, self.y_pred)))
    print(cm.to_markdown())

  def show_report(self):
    report_dict = {
      self.tdp.MODEL_MULTICLASS_3:self.show_report_multiclass_3,
      self.tdp.MODEL_MULTICLASS_5:self.show_report_multiclass_5,
      self.tdp.MODEL_BINARYCLASS:self.show_report_binaryclass
    }
    report_dict[self.tdp.MODEL_TYPE]()

  def show_report_multiclass_3(self):
    """
    classification_report()
      precision : 適合率 誤検出の割合
      recall    : 再現率 取りこぼしの割合
      f1-score  : F1値
      support   : 各クラス事の数
    """
    d_report = classification_report(self.y_test, self.y_pred, target_names=['1着','2着','3着','その他'])
    #d_report = classification_report(self.y_test, self.y_pred, digits=5, output_dict=True)
    #df_report = pd.DataFrame(d_report)
    #print(df_report)
    print(d_report)

  def show_report_multiclass_5(self):
    """
    classification_report()
      precision : 適合率 誤検出の割合
      recall    : 再現率 取りこぼしの割合
      f1-score  : F1値
      support   : 各クラス事の数
    """
    d_report = classification_report(self.y_test, self.y_pred, target_names=['1着','2着','3着','4着','5着','その他'])
    #d_report = classification_report(self.y_test, self.y_pred, digits=5, output_dict=True)
    #df_report = pd.DataFrame(d_report)
    #print(df_report)
    print(d_report)

  def show_report_binaryclass(self):
    """
    classification_report()
      precision : 適合率
      recall    : 再現率
      f1-score  : F1値
      support   : 各クラス事の数
    """
    d_report = classification_report(self.y_test, self.y_pred, target_names=['1着','その他'])
    #d_report = classification_report(self.y_test, self.y_pred, digits=5, output_dict=True)
    #df_report = pd.DataFrame(d_report)
    #print(df_report)
    print(d_report)

  def show_graph(self):
    graph_dict = {
      self.tdp.MODEL_MULTICLASS_3:self.show_graph_multiclass,
      self.tdp.MODEL_MULTICLASS_5:self.show_graph_multiclass,
      self.tdp.MODEL_BINARYCLASS:self.show_graph_bainaryclass
    }
    graph_dict[self.tdp.MODEL_TYPE]()
  
  def show_graph_multiclass(self):
    plt.plot(self.history["train"]["multi_logloss"], color = "red", label = "train")
    plt.plot(self.history["valid"]["multi_logloss"], color = "blue", label = "valid")
    plt.legend()
    plt.show()
  
  def show_graph_bainaryclass(self):
    plt.plot(self.history["train"]["auc"], color = "red", label = "train")
    plt.plot(self.history["valid"]["auc"], color = "blue", label = "valid")
    plt.legend()
    plt.show()
  
  def model_predict(self, pred_data):
    self.load_parameter()
    rank_info = []
    predict_data_info = self.model.predict(pred_data)
    predict_data = predict_data_info
    pred_df = pd.read_pickle(self.lps.DATA_TMP_PRED)
    #print("■予測順位(馬ごと)")
    #for pred in predict_data:
    #  print(np.argmax(pred) + 1)
    rank_list = np.argmax(predict_data, axis=0)
    predict_data = np.delete(predict_data, rank_list[0], axis=0)
    rank_info.append(rank_list[0])
    rank_list = np.argmax(predict_data, axis=0)
    predict_data = np.delete(predict_data, rank_list[0], axis=0)
    rank_info.append(rank_list[1])
    rank_list = np.argmax(predict_data, axis=0)
    predict_data = np.delete(predict_data, rank_list[0], axis=0)
    rank_info.append(rank_list[2])
    for i, rank in enumerate(rank_info):
      print(str(i+1) + "着:" + pred_df[self.df_cols.HORSE_NAME].iloc[rank])

  def model_predict_detail(self, pred_data):
    self.load_parameter()
    predict_data_info = self.model.predict(pred_data)
    pred_df = pd.read_pickle(self.lps.DATA_TMP_PRED)
    pred_cols_df = pd.read_pickle(self.tdp.DATA_TRAINDATA_YTRAIN)
    pred_cols = list(pred_cols_df.drop_duplicates())
    pred_cols.sort()
    pred_cols_list = []
    for col in pred_cols:
      if col < len(pred_cols) - 1:
        col = str(col + 1) + "着"
      else:
        col = "その他"
      pred_cols_list.append(col)
    #pred_cols = ['1着','2着','3着','その他']
    pred_detail_df = pd.DataFrame(predict_data_info,index=[pred_df[self.df_cols.HORSE_NAME].values],columns=[pred_cols_list])
    print(pred_detail_df)
    pred_detail_df.to_json(self.tdp.PRED_JSON, force_ascii=False)
    #for i, predict in enumerate(predict_data_info):
    #  print(pred_df[self.df_cols.HORSE_NAME].iloc[i] + " : " + str(predict[0]) + " " + str(predict[1]) + " " + str(predict[2]) + " " + str(predict[3]))

  def show_feature_importance(self, imp_type):
    # feature importanceを表示
    importance = pd.DataFrame(self.model.feature_importance(importance_type=imp_type), index=self.x_train.columns, columns=['importance'])
    importance = importance.sort_values('importance', ascending=False)
    print(importance)

  def model_binary_predict(self, pred_data):
    self.load_parameter
    predict_data_info = self.model.predict(pred_data)
    print(predict_data_info)
  