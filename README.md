# BBS Crawler

게시판의 데이터를 수집하여 보기 편하게 표현하기 위해 만들었습니다. scrapy 를 사용합니다.

## 설치 및 실행 

```
pip install -r requirements.txt

cd clien_net
scrapy crawl clien
```

수집 결과를 `mongodb` 에 저장하기 (기본 설정입니다. `/clien_net/settings.py` 에 
`clien_net.pipelines.MongoPipeline` 이 설정되어 있습니다.)

```
scrapy crawl clien
```

수집 결과를 `out.json` 에 저장하기 

```
scrapy crawl --output=out.json --output-format=json clien
```
