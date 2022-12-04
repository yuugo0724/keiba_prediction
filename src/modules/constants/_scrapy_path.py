import dataclasses

@dataclasses.dataclass(frozen=True)
class ScrapyPath:
  """
  スクレイピングするパスを定義
  """
  BASE_URL: str = 'https://db.netkeiba.com/race/list/'
