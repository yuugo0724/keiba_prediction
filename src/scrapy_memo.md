# Scrapyの使用方法

## プロジェクトの作成
```
scrapy startproject [プロジェクト名]
```

下記ファイルが作成される

```
プロジェクト名/
├── scrapy.cfg
└── プロジェクト名
    ├── __init__.py
    ├── __pycache__
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        └── __pycache__
```

## Spiderの追加

```
cd [プロジェクト名]
scrapy genspider [スパイダー名] [クロール対象ドメイン名]
```

## スパイダーの起動

```
scrapy crawl [スパイダー名]
```

## itemをファイル出力

```
scrapy crawl [スパイダー名] -o [出力ファイル名]
```

## scrapy shellの起動

```
scrapy shell [ドメイン名]
```

対話式にスクレイピング

```
In [1]: response.css('title')
Out[1]: XXXXXXXXXXXXXXXXXXX
```



