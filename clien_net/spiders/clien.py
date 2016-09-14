# -*- coding: utf-8 -*-
import urlparse
from datetime import datetime

import scrapy
from ..items import PostItem


class ClienSpider(scrapy.Spider):
    name = "clien"
    allowed_domains = ["clien.net", "www.clien.net"]
    start_urls = (
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park',
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park&page=2',
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park&page=3',
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park&page=4',
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park&page=5',
    )

    def parse(self, response):
        for link in response.css('tr.mytr td.post_subject a'):
            post_url = link.xpath("./@href").extract_first()
            full_url = urlparse.urljoin(response.url, post_url.strip())

            yield scrapy.Request(full_url, self.parse_post)

    def parse_post(self, response):
        qs = dict(urlparse.parse_qsl(urlparse.urlparse(response.url).query))
        id = int(qs.get('wr_id'))

        title = response.css('div.view_title span::text').extract_first().strip()
        body = ''.join(
            response.xpath("//span[@id='writeContents']/node()").extract()
        )[18:-19]

        created_at, cnt_hit, cnt_vote = response.css('.post_info').re(r'.*(\d\d\d\d-\d\d-\d\d \d\d:\d\d).*(\d+).*(\d+).*')
        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M')
        cnt_comment = len(response.css('.reply_base'))

        post = PostItem(id=id, title=title, body=body, created_at=created_at,
                        site='clien.net', board='park',
                        cnt_hit=int(cnt_hit), cnt_vote=int(cnt_vote), cnt_comment=cnt_comment,)

        yield post
