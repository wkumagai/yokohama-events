# -*- coding: utf-8 -*-
"""横浜赤レンガ倉庫1号館(ホール) https://akarenga.yafjp.org/event RSS: /feed/"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "akarenga_hall", "https://akarenga.yafjp.org/feed/",
        venue="横浜赤レンガ倉庫1号館", area="mm",
    )
