# -*- coding: utf-8 -*-

import unittest
from google.appengine.ext import testbed

class PalletTestCase(unittest.TestCase):
    '''
    予報の段階
    '''
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            ADDR_FROM='from@example.jp',
            ADDR_RCPT='rcpt@example.jp',
            overwrite=True)
        from main import Forecast
        self.p1 = Forecast(open('tests/data/webpage20180924.html'))

    def tearDown(self):
        self.testbed.deactivate()

    def test_getName(self):
        name = self.p1.getName()
        self.assertEqual(u"ぱれっと　10選＋果物", name)

    def test_getDeliveryDate(self):
        date = self.p1.getDeliveryDate()
        self.assertEqual(u"10月1日（月）お届け分", date)

    def test_getUpdatedDate(self):
        upd = self.p1.getUpdatedDate()
        self.assertEqual(u"2018年9月24日更新", upd)

    def test_getItem(self):
        item = self.p1.getItem()
        self.assertEqual(u"以下の品目を中心に野菜約10種類+果物1-2種類", item['head'])
        self.assertEqual([u"にんじん", u"里芋", u"レタス", u"葉物", u"トマト", u"パプリカ", u"みかん"],
                         item['list'])

class PalletTestCase2(unittest.TestCase):
    '''
    確定の段階
    '''
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            ADDR_FROM='from@example.jp',
            ADDR_RCPT='rcpt@example.jp',
            overwrite=True)
        from main import Forecast
        self.p1 = Forecast(open('tests/data/webpage20180928.html'))

    def tearDown(self):
        self.testbed.deactivate()

    def test_getName(self):
        name = self.p1.getName()
        self.assertEqual(u"ぱれっと　10選＋果物", name)

    def test_getDeliveryDate(self):
        date = self.p1.getDeliveryDate()
        self.assertEqual(u"10月1日（月）お届け分", date)

    def test_getUpdatedDate(self):
        upd = self.p1.getUpdatedDate()
        self.assertEqual(u"2018年9月28日更新", upd)

    def test_getItem(self):
        item = self.p1.getItem()
        self.assertEqual(u"以下の品目を中心に野菜約10種類+果物1-2種類", item['head'])
        self.assertEqual([u"じゃがいも", u"れんこん", u"かぼちゃ", u"ブロッコリー", u"白菜", u"長ねぎ",
                          u"きゅうり", u"おくら", u"まいたけ", u"えん菜", u"柿", u"キウイフルーツ"],
                         item['list'])

class PalletTestCase3(unittest.TestCase):
    '''
    「表示可能なお届け予報の情報がありません。」
    '''
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            ADDR_FROM='from@example.jp',
            ADDR_RCPT='rcpt@example.jp',
            overwrite=True)
        from main import Forecast
        self.p1 = Forecast(open('tests/data/webpage20181008_pre.html'))

    def tearDown(self):
        self.testbed.deactivate()

    def test_getDeliveryDate(self):
        date = self.p1.getDeliveryDate()
        self.assertEqual(None, date)

    def test_getUpdatedDate(self):
        upd = self.p1.getUpdatedDate()
        self.assertEqual(None, upd)


if __name__ == '__main__':
    unittest.main()
