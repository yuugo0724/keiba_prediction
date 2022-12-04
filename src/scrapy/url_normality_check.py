import requests
import os
import numpy as np
import pandas as pd

if os.path.isfile("url_normality_check.log"):
  os.system("rm -rf url_normality_check.log")
for url in np.ravel(pd.read_csv('./csv/grades_urls.csv',header=0).values.tolist()):
  res = requests.get(url)
  print(url)
  print("status: " + str(res.status_code))
