# -*- coding: utf-8 -*-
"""横浜BUNTAI https://yokohama-buntai.jp/event/ RSS: /feed/"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "buntai", "https://yokohama-buntai.jp/feed/",
        venue="横浜BUNTAI", area="kannai",
    )
