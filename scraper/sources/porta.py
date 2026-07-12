# -*- coding: utf-8 -*-
"""横浜ポルタ https://www.yokohamaporta.jp/news/ RSS: /feed/"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "porta", "https://www.yokohamaporta.jp/feed/",
        venue="横浜ポルタ", area="yokohama_st",
    )
