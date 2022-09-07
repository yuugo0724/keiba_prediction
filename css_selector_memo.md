# CSSセレクタとxpathの対応表

|取得対象|CSS3|XPath|
|-|-|-|
|全ての要素|*|//*|
|全てのP要素|p|//p|
|全ての子要素|p > *|//p/*|
|ID指定|#foo|//*[@id='foo']|
|クラス指定|#foo|//*[@id='foo']|
|属性指定|*[title]|//*[contains(@class,'foo')]|
|全てのPの最初の子要素|p > *:first-child|//p/*[0]|
|子要素Aを持つ全てのP|不可|//p[a]|
|次の要素|p + *|//p/following-sibling::*[0]|

# メモ

## optionタグのvalueを取得
対象URL:https://www.jra.go.jp/datafile/seiseki/replay/2022/jyusyo.html  
### CSS3  
response.css("select[class='dropdown-select bn-list'] option::attr(value)").extract()

### XPath
response.xpath('//option/@value').extract()
