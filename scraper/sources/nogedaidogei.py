# -*- coding: utf-8 -*-
"""野毛大道芸 https://nogedaidogei.com/ RSS: /feed/(春のみ開催・年1回程度の更新)"""
from common import scrape_rss


def scrape():
    return scrape_rss(
        "nogedaidogei", "https://nogedaidogei.com/feed/",
        venue="野毛大道芸", area="sakuragicho", category="festival",
    )
