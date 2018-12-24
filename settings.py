# -*- coding: utf-8 -*-
import os

# ぱれっと予報
PF_URL = "https://www.radishbo-ya.co.jp/shop/app/information/palette_forecast/"
# 検索パラメータ例 地域: 大阪, 曜日: 月曜, 配送便: 専用車, 商品: ぱれっと10選+果物
PF_PARAMS = {
    "pf_center": 20,
    "pf_rday": 0,
    "pf_deliver": 0,
    "pf_product": "1-000-0214"
}

# Notification mail
SUBJECT = u"らでぃっしゅぼーや"
ADDR_FROM = os.environ.get('ADDR_FROM').strip()
ADDR_RCPT = [s.strip() for s in os.environ.get('ADDR_RCPT').split(';')]
