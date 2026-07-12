# -*- coding: utf-8 -*-
"""はまこれ横浜 https://hamakore.yokohama/eventcal/ RSS: /feed/(直近10件、商用メディアにつき転載範囲注意)"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "hamakore", "https://hamakore.yokohama/feed/",
        venue=None, area=None,
    )
