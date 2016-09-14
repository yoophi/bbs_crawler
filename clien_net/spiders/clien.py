# -*- coding: utf-8 -*-
import urlparse

import scrapy
from ..items import PostItem


class ClienSpider(scrapy.Spider):
    name = "clien"
    allowed_domains = ["clien.net", "www.clien.net"]
    start_urls = (
        'http://www.clien.net/cs2/bbs/board.php?bo_table=park',

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

        created_at, hit_cnt, vote_cnt = response.css('.post_info').re(r'.*(\d\d\d\d-\d\d-\d\d).*(\d+).*(\d+).*')

        post = PostItem(id=id, title=title, body=body, created_at=created_at, hit_cnt=int(hit_cnt), vote_cnt=int(vote_cnt))

        yield post
