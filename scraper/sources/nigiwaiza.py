# -*- coding: utf-8 -*-
"""横浜にぎわい座 https://nigiwaiza.yafjp.org/perform/ RSS: /feed/"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "nigiwaiza", "https://nigiwaiza.yafjp.org/feed/",
        venue="横浜にぎわい座", area="sakuragicho", category="traditional",
    )
