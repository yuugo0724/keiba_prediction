import os
import re
import subprocess
import numpy as np
import pandas as pd
#from easydict import EasyDict

class scrapy_proc:
  def __init__(self, lps):
    self.lps = lps
    self.url_file_list = []
    self.target_url_file_list = []
  
  def coll_urls(self,race_date_list):
    # scrapyのスクリプトを配置したディレクトリへ移動
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    # ログ出力の設定
    with open(self.lps.LOG_COLL_URL, 'w') as f:
      # race_date_list(日付指定のリスト)ごとにスクレイピングを実行
      for race_date in race_date_list:
        date_dir = os.path.join(self.lps.DATA_URL_DIR,race_date[0:4])
        # 出力先ディレクトリを作成(既に存在していてもエラーを出さない)
        os.makedirs(date_dir, exist_ok=True)
        """
        引数1 : 実行するスクリプトのパス
        引数2 : スクレイピング対象のrace_date
        引数3 : スクレイピング結果を配置するディレクトリ
        """
        scrapy_cmd = ["python3",self.lps.PROC_COLL_URL,race_date,date_dir,self.lps.DATA_URL_DIR]
        scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
        scrapy_proc.wait()
    # 元のディレクトリに戻る
    os.chdir(self.lps.BASE_DIR)

  def create_path_list(self):
    # 取得したurlファイルのパスリストを定義
    url_file_list = []
    # 取得したurlファイルを再帰的に検索
    for current_dir, sub_dirs, files_list in os.walk(self.lps.DATA_URL_DIR):
      for file in files_list:
        # urlファイルのパスをurl_file_listにappend
        url_file_list.append(os.path.join(current_dir,file))
    self.url_file_list = url_file_list
  
  def create_race_path_list(self,race_date_list):
    # 取得対象のurlファイル名のリスト
    target_url_file_list = []
    # race_date_list(日付指定のリスト)ごとにスクレイピング対象のurlファイルパスを検索
    for race_date in race_date_list:
      # urlファイルパスを検索するための正規表現を定義
      date_match = '.*/' + race_date + '.csv'
      # 正規表現にマッチしたurlファイルパスを格納
      target_url_files = [url_file for url_file in self.url_file_list if re.match(date_match,url_file)]
      # 正規表現にマッチしないものは除外
      if target_url_files:
        # 取得対象のurlファイル名のリストに追加
        target_url_file_list.extend(target_url_files)
    self.target_url_file_list = target_url_file_list
  
  def coll_grades(self):
    # scrapyのスクリプトを配置したディレクトリへ移動
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    # ログ出力の設定
    with open(self.lps.LOG_COLL_GRADES, 'w') as f:
      # 取得対象のurlファイルリストをループ
      for url_file in self.target_url_file_list:
        # urlファイル名は日付 + .csv
        # 拡張子なしのファイル名を取得して取得対象の年(date_y)と月(date_m)を定義
        file_name = url_file.split('/')[-1].split('.')[0]
        date_y = file_name[0:4]
        date_m = file_name[4:6]
        # urlファイルを読み込む
        race_url_list = np.ravel(pd.read_csv(url_file,header=0).values.tolist())
        # スクレイピング結果を配置するパスを定義
        date_dir = os.path.join(self.lps.DATA_GRADES_DIR,date_y,date_m)
        # ディレクトリの作成(既に存在していてもエラーを出さない)
        os.makedirs(date_dir, exist_ok=True)
        # スクレイピング対象のurlをループ
        for race_url in race_url_list:
          # urlから数値のみを抜き出してrace_idを定義
          # スクレイピングの出力ファイル名をrace_idにしたい
          race_id = re.sub("\D","", race_url)
          """
          引数1 : 実行するスクリプトのパス
          引数2 : 取得対象のurl
          引数3 : 出力ファイル名(race_id)
          引数4 : 出力ファイルのディレクトリ
          """
          scrapy_cmd = ["python3",self.lps.PROC_COLL_GRADES,race_url,race_id,date_dir]
          scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
          scrapy_proc.wait()
    # 元のディレクトリに戻る
    os.chdir(self.lps.BASE_DIR)
  
  def coll_horse_grades(self, horse_id_list):
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    with open(self.lps.LOG_COLL_HORSE_GRADES, 'w') as f:
      for horse_id in horse_id_list:
        scrapy_cmd = ["python3",self.lps.PROC_COLL_HORSE_GRADES,horse_id,self.lps.DATA_HORSE_GRADES_DIR]
        scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
        scrapy_proc.wait()
    os.chdir(self.lps.BASE_DIR)
  
  def coll_predigree(self, horse_id_list):
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    with open(self.lps.LOG_COLL_PEDIGREE, 'w') as f:
      for horse_id in horse_id_list:
        scrapy_cmd = ["python3",self.lps.PROC_COLL_PEDIGREE,horse_id,self.lps.DATA_HORSE_GRADES_DIR]
        scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
        scrapy_proc.wait()
    os.chdir(self.lps.BASE_DIR)

  def coll_pred_grades(self, pred_url):
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    with open(self.lps.LOG_COLL_PRED_GRADES, 'w') as f:
      scrapy_cmd = ["python3",self.lps.PROC_COLL_PRED_GRADES,pred_url,self.lps.DATA_TMP_DIR]
      scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
      scrapy_proc.wait()
    os.chdir(self.lps.BASE_DIR)

  def coll_eval_grades(self, pred_url):
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    with open(self.lps.LOG_COLL_EVAL_GRADES, 'w') as f:
      scrapy_cmd = ["python3",self.lps.PROC_COLL_EVAL_GRADES,pred_url,self.lps.DATA_TMP_DIR]
      scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
      scrapy_proc.wait()
    os.chdir(self.lps.BASE_DIR)

  def coll_juushou(self, juushou_date_list, data_juushou):
    os.chdir(self.lps.SCRAPY_KEIBA_DIR)
    with open(self.lps.LOG_COLL_JUUSHOU, 'w') as f:
      for juushou_year in juushou_date_list:
        data_juushou_list = data_juushou + juushou_year
        scrapy_cmd = ["python3",self.lps.PROC_COLL_JUUSHOU,juushou_year,data_juushou_list]
        scrapy_proc = subprocess.Popen(scrapy_cmd, stdout=f, stderr=f)
        scrapy_proc.wait()
    os.chdir(self.lps.BASE_DIR)
