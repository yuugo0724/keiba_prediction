import dataclasses

@dataclasses.dataclass(frozen=True)
class ResultsCols:
  """
  学習データに使うデータフレームの列名
  """
  RANK: str = '着順'
  WAKU_NUM: str = '枠番'
  HORSE_NUM: str = '馬番'
  HORSE_NAME: str = '馬名'
  AGE: str = '性齢'
  LOAD: str = '斤量'
  JOCKEY: str = '騎手'
  TIME: str = 'タイム'
  ODDS: str = '単勝'
  POP: str = '人気'
  WEIGHT: str = '馬体重'
  TRAINER: str = '調教師'
  HORSE_OWNER: str = '馬主'
  PRIZE: str = '賞金(万)'
