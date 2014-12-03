# -*- coding:utf-8 -*-
import random
import string
import datetime
from urlhandler.models import *
from queryhandler.settings import QRCODE_URL
from django.db.models import F
from django.db import transaction

from userpage.safe_reverse import *
from queryhandler.weixin_reply_templates import *
from queryhandler.weixin_text_templates import *
from queryhandler.handler_check_templates import *
from queryhandler.weixin_msg import *
from weixinlib.settings import WEIXIN_EVENT_KEYS
from weixinlib.custom_menu import modify_custom_menu
from weixinlib.settings import WEIXIN_CUSTOM_MENU_TEMPLATE
from weixinlib.custom_menu import get_custom_menu
import json


def get_user(openid):
    try:
        return User.objects.get(weixin_id=openid, status=1)
    except:
        return None


def get_reply_single_ticket(msg, ticket, now, ext_desc=''):
    return get_reply_single_news_xml(msg, get_item_dict(
        title=get_text_one_ticket_title(ticket, now),
        description=ext_desc + get_text_one_ticket_description(ticket, now),
        pic_url=get_text_ticket_pic(ticket),
        url=s_reverse_ticket_detail(ticket.unique_id)
    ))


def get_reply_multi_tickets(msg, tickets, now, ext_desc=''):
    articles = []
    for ticket in tickets:
        articles.append(get_item_dict(
            title=get_text_one_ticket_title(ticket, now),
            description=ext_desc + get_text_one_ticket_description(ticket, now),
            pic_url=get_text_ticket_pic(ticket),
            url=s_reverse_ticket_detail(ticket.unique_id)))
    return get_reply_news_xml(msg, articles)


#check user is authenticated or not
def is_authenticated(openid):
    return get_user(openid) is not None