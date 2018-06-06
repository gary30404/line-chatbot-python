
# -*- coding: UTF-8 -*-
import requests
import random
import configparser
from flask import Flask, request, abort
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'YOUR_Subscription_Key',
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'ok'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("event.reply_token:", event.reply_token)
    #print("event.message.text:", event.message.text)
    buttons_template = TemplateSendMessage(
        alt_text = '介紹張植鈞',
        template = ButtonsTemplate(
            title = '你好，我是維尼！',
            text='讓我來介紹張植鈞給你認識吧！\n你想了解什麼呢？',
            thumbnail_image_url='https://i.imgur.com/NAPMFdI.jpg',
            actions=[
                MessageTemplateAction(
                    label='他是誰',
                    text='他是怎麼樣的人？'
                ),
                MessageTemplateAction(
                    label='他的興趣',
                    text='他的興趣有哪些？'
                ),
                MessageTemplateAction(
                    label='他的專長',
                    text='他的專長有哪些？'
                ),
                MessageTemplateAction(
                    label='他的作品',
                    text='他的作品有哪些？'
                )
            ]
        )
    )

    image_carousel_template_message = TemplateSendMessage(
        alt_text='張植鈞的興趣',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/tOmStZQ.jpg',
                    action=PostbackTemplateAction(
                        label='他喜歡做菜',
                        text=None,
                        data='itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/zHDaIZT.jpg',
                    action=PostbackTemplateAction(
                        label='旅遊是他生活中的調味料',
                        text=None,
                        data='itemid=2'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/tuCoVdK.jpg',
                    action=PostbackTemplateAction(
                        label='他熱愛海洋',
                        text=None,
                        data='itemid=3'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/8zFkQG6.jpg',
                    action=PostbackTemplateAction(
                        label='運動是他生活的一部分',
                        text=None,
                        data='itemid=4'
                    )
                )
            ]
        )
    )

    params = {
        # Query parameter
        'q': event.message.text,
        # Optional request parameters, set to default values
        'timezoneOffset': '0',
        'verbose': 'false',
        'spellCheck': 'false',
        'staging': 'false',
    }
    try:
        r = requests.get('YOUR_URL', headers=headers, params=params)
        #print(r.json())
        if (r.json()['topScoringIntent']['intent'] == '問候') and (len(r.json()['entities'])!=0):
            mes = '哈哈哈XD'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
        elif (r.json()['topScoringIntent']['intent'] == '問候') and (len(r.json()['entities'])==0):
            mes = '哈囉，我是維尼！\n有什麼可以幫忙的嗎？'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
        elif (r.json()['topScoringIntent']['intent'] == '介紹') and (len(r.json()['entities']) != 0):
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '個性'):
                mes = '張植鈞個性開朗，喜歡交朋友，雖然有點悶騷，但是待人和善，遇到困難總不退縮，他喜歡解決困難所獲得的成就感。\n想認識他嗎？快來和他交朋友吧！\nhttps://www.facebook.com/profile.php?id=100002195446142'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '興趣'):
                line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '專長'):
                mes = '說到專長，他比較擅長的程式語言是Python，前一陣子在做資料處理和深度學習相關的開發，不過像是Java, C++...也有接觸過！\nhttps://gary30404.github.io/#about\n問問他過去的一些經驗吧！'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '作品'):
                mes = 'Website:\nhttps://gary30404.github.io\nGithub:\nhttps://github.com/gary30404\nBlogs:\nhttps://medium.com/@gary30404\n'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '工作'):
                mes = 'Snapask:\nhttps://snapask.com\n在Snapask我是擔任Android實習生，負責程式debug和後台的維護。\nNTHU Vision Lab:\nhttps://www.youtube.com/watch?v=i68kPU7sp3A\nDigital Drift:\nhttp://2bite.com\n我負責這個app的辨識功能。\nNTU IOX Center:\nhttps://gary30404.github.io/images/poster.pdf\n這個研究是在協助酒駕慣犯控制自己的行為，我負責的是臉部辨識系統及前後台的維護。'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '女友'): 
                mes = 'https://www.instagram.com/fangfangfanghsu/'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '生日'):
                mes = '1994/10/22'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '星座'):
                mes = '張植鈞是天秤座'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '電話'):
                mes = '0988300781'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '歲數'):
                mes = '張植鈞今年23歲'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
            if (r.json()['topScoringIntent']['intent'] == '介紹') and (r.json()['entities'][0]['type'] == '電子郵件'):
                mes = 'mailto:gary30404@gmail.com'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
        elif (r.json()['topScoringIntent']['intent'] == '介紹') and (len(r.json()['entities']) == 0):
            line_bot_api.reply_message(event.reply_token, buttons_template)
        else:
            mes = '我太笨了，'+event.message.text+'是什麼意思？'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=mes))
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    #print("package_id:", event.message.package_id)
    #print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    #print("package_id:", event.message.package_id)
    #print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    # image recognition TBD...
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='我看不懂這是什麼！'))

if __name__ == '__main__':
    app.run()
