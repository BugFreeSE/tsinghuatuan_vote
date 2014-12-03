# -*- coding:utf-8 -*-

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from urlhandler.models import User, Activity, Ticket, SettingForm, District, Seat
from urlhandler.settings import STATIC_URL
import urllib, urllib2
import datetime
from django.utils import timezone
from django.forms import *
from queryhandler.tickethandler import get_user
from django.db.models import F
import json
from queryhandler.settings import SITE_DOMAIN


def home(request):
    return render_to_response('mobile_base.html')


