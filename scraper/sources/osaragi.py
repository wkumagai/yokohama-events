# -*- coding: utf-8 -*-
"""大佛次郎記念館 https://osaragijiro-museum.jp/event RSS: /feed"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "osaragi", "https://osaragijiro-museum.jp/feed",
        venue="大佛次郎記念館", area="yamashita", category="museum",
    )
