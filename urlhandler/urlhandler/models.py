#-*- coding: UTF-8 -*-
from django.db import models
from django import forms
import uuid


class Activity(models.Model):
    name = models.CharField(max_length=255)
#    key = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=255)
    book_start = models.DateTimeField()
    book_end = models.DateTimeField()
#    seat_status = models.IntegerField(default=0)
#    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic = models.ImageField(upload_to="uploadImages/")
#    pic_url = models.CharField(max_length=255)
#    remain_tickets = models.IntegerField()
    menu_url = models.CharField(max_length=255, null=True)
    # Something about status:
    # -1: deleted
    # 0: saved but not published
    # 1: published
    # Something about seat_status:
    # 0: no seat
    # 1: seat B and seat C

class District(models.Model):
    total_tickets = models.IntegerField()
    remain_tickets = models.IntegerField()
    activity = models.ForeignKey(Activity)
    name = models.CharField(max_length=255)
    has_seat = models.BooleanField() #标记是否有座位

class District(models.Model):
    total_tickets = models.IntegerField()
    remain_tickets = models.IntegerField()
    activity = models.ForeignKey(Activity)
    name = models.CharField(max_length=255)
    has_seat = models.BooleanField() #标记是否有座位


class User(models.Model):
    weixin_id = models.CharField(max_length=255)
    stu_id = models.CharField(max_length=255)
    status = models.IntegerField()
    seed = models.FloatField(default=1024)
    book_activity = models.ForeignKey(Activity, null=True)
    need_multi_ticket = models.BooleanField(default=False)
    book_district = models.ForeignKey(District, null=True)
    abandon_seats = models.CharField(max_length=1023, null=True)


class Seat(models.Model):
    row = models.IntegerField() #坐标
    column = models.IntegerField() #坐标
    seat_number = models.CharField(max_length=20) #座位号
    district = models.ForeignKey(District)
    is_sold = models.BooleanField(default=False) #标记是否卖出


class Ticket(models.Model):
    stu_id = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255)
#    activity = models.ForeignKey(Activity)
    district = models.ForeignKey(District)
    status = models.IntegerField()
#    seat = models.CharField(max_length=255)
    seat = models.ForeignKey(Seat, null=True)
    # Something about isUsed
    # 0: ticket order is cancelled
    # 1: ticket order is valid
    # 2: ticket is used


class SettingForm(forms.Form):
    book_activity = forms.CharField(label='抢票活动', widget=forms.Select())
    need_multi_ticket = forms.BooleanField(label='连续两张票', required=False)
    book_district = forms.CharField(label='抢票区域', widget=forms.Select())
    abandon_seats = forms.CharField(label='abandon_seats', required=False)


class VoteAct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    key = models.CharField(max_length=255)
    config = models.IntegerField()
    begin_vote = models.DateTimeField()
    end_vote = models.DateTimeField()
    status = models.IntegerField()

class Candidate(models.Model):
    activity_id = models.ForeignKey(VoteAct)
    name = models.CharField(max_length=255)
    key = models.IntegerField()
    description = models.TextField()
    votes = models.IntegerField()
    status = models.IntegerField()


class VoteLog(models.Model):
    stu_id = models.IntegerField()
    activity_id = models.ForeignKey(VoteAct)