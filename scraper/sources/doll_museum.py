# -*- coding: utf-8 -*-
"""横浜人形の家 https://www.doll-museum.jp/exhibition RSS: /feed/"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "doll_museum", "https://www.doll-museum.jp/feed/",
        venue="横浜人形の家", area="yamashita", category="museum",
    )
