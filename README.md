# clien.net spider 

## 설치 및 실행 

```
pip install -r requirements.txt

cd clien_net
scrapy crawl clien
```

수집 결과를 `out.json` 에 저장하기 

```
scrapy crawl --output=out.json --output-format=json clien
```