# -*- coding: utf-8 -*-
import os
import re
import logging
from urllib import urlencode
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import mail
from bs4 import BeautifulSoup
import settings

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Pallet(ndb.Model):
    name = ndb.StringProperty(required=True)
    delivery = ndb.StringProperty(required=True)
    updated = ndb.StringProperty(required=True)
    item = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)


def exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as e:
            logger.error("Caught exception: %s", str(e))
            return None
    return wrapper

class Forecast(object):
    def __init__(self, html):
        bs = BeautifulSoup(html, "html.parser")
        self.item = bs.find("li", class_="palette_delivery_info_content_item")

    @exception
    def getDeliveryDate(self):
        e = self.item.find("div", class_="palette_delivery_info_heading")
        return re.sub(r"^\D+", "", e.contents[0].string).strip()

    @exception
    def getUpdatedDate(self):
        e = self.item.find("div", class_="palette_delivery_info_heading")
        return e.span.text.strip()

    @exception
    def getName(self):
        e = self.item.find("div", class_="palette_delivery_item_heading")
        return e.text.strip()

    @exception
    def getItem(self):
        e = self.item.find("div", class_="palette_delivery_item_content")
        return {
            "head": e.p.text.strip(),
            "list": [s.text.strip() for s in e.find_all("li")]
        }

def fetch_forecast():
    try:
        result = urlfetch.fetch("{}?{}".format(
            settings.PF_URL, urlencode(settings.PF_PARAMS)))
        if result.status_code == 200:
            return result.content
    except urlfetch.Error:
        logger.exception("Caught exception fetching url")
    if result.content is None:
        logger.error("no content")


def send_mail(msg):
    for rcpt in settings.ADDR_RCPT:
        mail.send_mail(
            sender=settings.ADDR_FROM,
            to=rcpt,
            subject=settings.SUBJECT,
            body=msg)


class UrlFetch(webapp2.RequestHandler):
    def get(self):
        html = fetch_forecast()
        if html is None:
            self.response.out.write("fetch error")
            return
        fc = Forecast(html)
        delivery_date = fc.getDeliveryDate()
        updated_date = fc.getUpdatedDate()
        if delivery_date is None or updated_date is None:
            self.response.out.write("no info.")
            return

        #update check
        if Pallet.query().filter(Pallet.updated == updated_date).get() is not None:
            self.response.out.write("Not changed. %s" % updated_date)
            return
        name = fc.getName()
        item = fc.getItem()
        p = Pallet(
            name=name,
            delivery=delivery_date,
            updated=updated_date,
            item=", ".join(item["list"]))
        p.put()

        # send Notification mail
        msg = u"{}({})\n{}\n{}\n--\n{}".format(
            delivery_date, updated_date,
            name, item["head"], "\n".join(item["list"]))
        send_mail(msg)

        self.response.out.write("%s" % msg)


class MainPage(webapp2.RequestHandler):
    def get(self):
        pallets = Pallet.query().order(-Pallet.created_at).fetch(10)
        template_values = {
            "pallets": pallets
        }
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/fetch", UrlFetch)], debug=True)
