# -*- coding: utf-8 -*-
"""横浜西口エリアマネジメント https://yokohamanishiguchi.or.jp/ RSS: /feed"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "nishiguchi", "https://yokohamanishiguchi.or.jp/feed",
        venue="横浜駅西口", area="yokohama_st",
    )
