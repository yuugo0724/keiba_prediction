# LightGBMのハイパーパラメータの種類

## よく調整するもの
|パラメータ名<br>(Training API)|パラメータ名<br>(Scikit-learn API)|説明|因数|
|:----|:---|:---|:----|
|lambda_l1|reg_alpha|L1正則化項の係数|0~ (float｜log)<br>デフォルト：0|
|lambda_l2|reg_lambda|L2正則化項の係数|0~(float｜log)<br>デフォルト：0|
|num_leaves|num_leaves|1本の木の最大葉枚数|0~131072(int)<br>デフォルト：31|
|feature_fraction|colsample _bytree|各決定木においてランダムに抽出される列の割合|0~1(float)<br>デフォルト：1.0|
|bagging_fraction|subsample|各決定木においてランダムに抽出される標本の割合|0~1(int)<br>デフォルト：1.0|
|bagging_freq|subsample_freq|ここで指定したイテレーション毎にバギング実施|0~(int)<br>デフォルト：0|
|min_data_in_leaf|min_child_samples|1枚の葉に含まれる最小データ数|0~(int)<br>デフォルト：20|

## 各パラメータの大小と過剰適合の関係
|小 <<<<<|パラメータ名|<<<<< 大|
|:---|:---|:---|
|過剰適合|lambda_l1<br>(reg_alpha)|保守的|
|過剰適合|lambda_l2<br>(reg_lambda)|保守的|
|保守的|num_leaves|過剰適合|
|保守的|feature_fraction<br>(colsample _bytree)|過剰適合|
|保守的|bagging_fraction<br>(subsample)|過剰適合|
|保守的|bagging_freq<br>(subsample_freq)|過剰適合|
|過剰適合|min_data_in_leaf<br>(min_child_samples)|保守的|

## その他のパラメータ
|パラメータ名|説明|引数|
|:---|:---|:---|
|verbosity|学習途中の情報を表示するかどうか|>1：Debug<br>1：Info<br>0：Error(Warning)<br>-1：Fatal<br>デフォルト：1|
|n_estimators|ブースティングのラウンド数|0~ (int) デフォルト：100|
|random_state|乱数シードの値|int|
|n_jobs|LightGBM に使用するスレッド数|0：デフォルトの数<br>-1：最大数で指定（おそらく）<br>デフォルト：0|

## 各手法のパラメータ
- 回帰問題：'regression'
- 分類問題：'binary'
- 多クラス類問題：'multiclass'

## Objective(目的関数)
### regression
mean_squared_errorを誤差関数として使う回帰  
metric(誤差関数の測定方法)としては、絶対値誤差関数(L1)ならばmae、２乗誤差関数(L2)ならばmseと指定する  
### regression_l1
mean_absolute_errorを誤差関数として使う回帰
### binary
二値分類のlogloss
### multiclass
多クラス分類、softmax  
"num_class"でクラス数も一緒に与えて上げる必要がある
### multiclassova
多クラス分類をOneVsAllでときます。同様に"num_class"でクラス数も一緒に与えて上げる必要がある
### cross_entropy
クロスエントロピー
