import os
import dataclasses

@dataclasses.dataclass(frozen=True)
class LocalPaths:
  """
  プロジェクトのディレクトリ
  """
  # プロジェクトルートのディレクトリ
  BASE_DIR: str = os.path.abspath('./')
  """
  DATA
  """
  DATA_DIR: str = os.path.join(BASE_DIR, 'data')
  DATA_MASTER_DIR: str = os.path.join(DATA_DIR, 'master')
  DATA_URL_DIR: str = os.path.join(DATA_DIR, 'url')
  DATA_TMP_DIR: str = os.path.join(DATA_DIR, 'tmp')
  DATA_GRADES_DIR: str = os.path.join(DATA_DIR, 'grades')
  DATA_HORSE_GRADES_DIR: str = os.path.join(DATA_DIR, 'horse_grades')
  DATA_PEDIGREE_DIR: str = os.path.join(DATA_DIR, 'pedigree')
  DATA_GRADES_MASTER: str = os.path.join(DATA_MASTER_DIR, 'grades')
  DATA_HORSE_ID_MASTER: str = os.path.join(DATA_MASTER_DIR, 'horse_id')
  """
  scrapyのディレクトリ
  """
  # scrapyのルートディレクトリ
  SCRAPY_DIR: str = os.path.join(BASE_DIR, 'scrapy')
  # scrapy(成績)のディレクトリ
  SCRAPY_KEIBA_DIR: str = os.path.join(SCRAPY_DIR, 'keiba')

  """
  プログラムのパス
  """
  PROC_COLL_URL: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_url.py')
  PROC_COLL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_grades.py')
  PROC_COLL_HORSE_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_horse_grades.py')
  PROC_COLL_PEDIGREE: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pedigree.py')
  
  """
  ログのパス
  """
  LOG_COLL_URL: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_url.log')
  LOG_COLL_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_grades.log')
  LOG_COLL_HORSE_GRADES: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_horse_grades.log')
  LOG_COLL_PEDIGREE: str = os.path.join(SCRAPY_KEIBA_DIR, 'coll_pedigree.log')
  