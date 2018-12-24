# gae-radishboya-forecast
## About
This app monitors web page ([らでいぃっしゅぼーや](https://www.radishbo-ya.co.jp) [ぱれっとお届け予報ページ](https://www.radishbo-ya.co.jp/shop/app/information/palette_forecast/)) for changes and send notification via email when delivery announcement updates.

## Requirements
- [Google Cloud SDK for Python][]
- [BeautifulSoup][]

## Install
### Libraries
```bash
$ cd /your/project
$ pip install -t lib beautifulsoup4
```

### mailaddress.yaml
- Rename *mailaddress.yaml.sample* to *mailaddress.yaml*
- Open mailaddrss.yaml and set *ADDR_FROM* and *ADDR_RCPT*.
  - ADDR_FROM: Sender email address
  - ADDR_RCPT: Recipient email addresses
- You must register your sender emails as authorized senders. See [who can send email](https://cloud.google.com/appengine/docs/standard/python/mail/#who_can_send_mail).
- You can insert multiple addresses in ADDR_RCPT, use a semi-colon (;) to separate each address.

### settings.py
Set the query parameters.  
https://www.radishbo-ya.co.jp/shop/app/information/palette_forecast/

## Deploy
```bash
$ gcloud app deploy
$ gcloud app deploy cron.yaml
```

[Google Cloud SDK for Python]: https://cloud.google.com/appengine/docs/standard/python/download
[BeautifulSoup]:
https://www.crummy.com/software/BeautifulSoup/