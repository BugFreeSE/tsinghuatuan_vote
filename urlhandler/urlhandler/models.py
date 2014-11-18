#-*- coding: UTF-8 -*-
from django.db import models
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
#    pic = models.ImageField('pic',upload_to="uploadImages")
    pic_url = models.CharField(max_length=255)
#    remain_tickets = models.IntegerField()
    menu_url = models.CharField(max_length=255, null=True)
    # Something about status:
    # -1: deleted
    # 0: saved but not published
    # 1: published
    # Something about seat_status:
    # 0: no seat
    # 1: seat B and seat C


class User(models.Model):
    weixin_id = models.CharField(max_length=255)
    stu_id = models.CharField(max_length=255)
    status = models.IntegerField()
    seed = models.FloatField(default=1024)
    book_activity = models.ForeignKey(Activity, null=True)
    need_multi_ticket = models.BooleanField()
    book_distinct = models.CharField(max_length=255)


class District(models.Model):
    total_tickets = models.IntegerField()
    remain_tickets = models.IntegerField()
    activity = models.ForeignKey(Activity)
    name = models.CharField(max_length=255)

class Seat(models.Model):
    row = models.CharField(max_length=3)
    column = models.CharField(max_length=3)

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

'''
class UserSession(models.Model):
    stu_id = models.CharField(max_length=255)
    session_key = models.CharField(max_length=255)
    session_status = models.IntegerField(1)

    def generate_session(self,stu_id):
        try:
            stu = User.objects.get(stu_id=stu_id)
            sessions = UserSession.objects.filter(stu_id = stu_id)
            if sessions:
                for session in sessions:
                    session.delete()
            s = UserSession(stu_id=stu_id,session_key=uuid.uuid4(),session_status = 0)
            s.save()
            return True
        except:
            return False

    def is_session_valid(self,stu_id,session_key):
        try:
            s = UserSession.objects.get(stu_id=stu_id,session_key=session_key)
            if(s.session_status == 0):
                s.session_status = 1
                s.save()
                return True
            else:
                s.delete()
                return False
        except:
            return False

    def can_print(self,stu_id,session_key):
        try:
            s = UserSession.objects.get(stu_id=stu_id,session_key=session_key)
            return True
        except:
            return False
'''
