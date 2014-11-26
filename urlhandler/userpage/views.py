#-*- coding:utf-8 -*-

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

def home(request):
    return render_to_response('mobile_base.html')


###################### Validate ######################
# request.GET['openid'] must be provided.
def validate_view(request, openid):
    if User.objects.filter(weixin_id=openid, status=1).exists():
        isValidated = 1
    else:
        isValidated = 0
    studentid = ''
    if request.GET:
        studentid = request.GET.get('studentid', '')
    return render_to_response('validation.html', {
        'openid': openid,
        'studentid': studentid,
        'isValidated': isValidated,
        'now': datetime.datetime.now() + datetime.timedelta(seconds=-5),
    }, context_instance=RequestContext(request))


# Validate Format:
# METHOD 1: learn.tsinghua
# url: https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp
# form: { userid:2011013236, userpass:***, submit1: 登录 }
# success: check substring 'loginteacher_action.jsp'
# validate: userid is number
def validate_through_igeek(secret):
    encrypted = {'secret' : secret}
    postData = urllib.urlencode(encrypted)
    request_url = 'http://auth.igeek.asia/v1'
    req = urllib2.Request(url=request_url, data=postData)
    req.add_header('Context-Type','application/x-www-form-urlencoded')
    res_data = urllib2.urlopen(req)
    try:
        res = res_data.read()
    except:
        return 'Unknown error'
    res_dict = eval(res)
    if res_dict['code'] == 0:
        return 'Accepted'
    elif res_dict['code'] == 1:
        return 'Rejected'
    elif res_dict['code'] == -3:
        return 'Out of date'
    else:
        return 'Error'


# METHOD 2 is not valid, because student.tsinghua has not linked to Internet
# METHOD 2: student.tsinghua
# url: http://student.tsinghua.edu.cn/checkUser.do?redirectURL=%2Fqingxiaotuan.do
# form: { username:2011013236, password:encryptedString(***) }
# success: response response is null / check response status code == 302
# validate: username is number
def validate_through_student(userid, userpass):
    return 'Error'


def validate_post(request):
    if (not request.POST) or (not 'openid' in request.POST) or \
            (not 'username' in request.POST):
        raise Http404
    userid = request.POST['username']
    if not userid.isdigit():
        raise Http404
    secret = request.POST['secret']
    validate_result = validate_through_igeek(secret)
    if validate_result == 'Accepted':
        openid = request.POST['openid']
        try:
            User.objects.filter(stu_id=userid).update(status=0)
            User.objects.filter(weixin_id=openid).update(status=0)
        except:
            return HttpResponse('Error')
        try:
            currentUser = User.objects.get(stu_id=userid)
            currentUser.weixin_id = openid
            currentUser.status = 1
            try:
                currentUser.save()
            except:
                return HttpResponse('Error')
        except:
            newuser = User.objects.create(weixin_id=openid, stu_id=userid, status=1)
            newuser.save()
            # try:
            #
            # except:
            #     return HttpResponse('Error')
    return HttpResponse(validate_result)

def get_timestamp(request):
    request_url = 'http://auth.igeek.asia/v1/time'
    req = urllib2.Request(url=request_url)
    r = urllib2.urlopen(req)
    timestamp = r.read()
    return HttpResponse(timestamp)

###################### Activity Detail ######################

def details_view(request, activityid):
    activity = Activity.objects.filter(id=activityid)
    if not activity.exists():
        raise Http404  #current activity is invalid
    act_name = activity[0].name
    # act_key = activity[0].key
    act_place = activity[0].place
    act_bookstart = activity[0].book_start
    act_bookend = activity[0].book_end
    act_begintime = activity[0].start_time
    act_endtime = activity[0].end_time
    act_districts = District.objects.filter(activity=activity[0])
    act_totaltickets = 0
    act_ticket_remain = 0
    for dis in act_districts:
        act_totaltickets = act_totaltickets + dis.total_tickets
        act_ticket_remain = act_ticket_remain + dis.remain_tickets
    act_text = activity[0].description
    act_abstract = act_text
    MAX_LEN = 256
    act_text_status = 0
    if len(act_text) > MAX_LEN:
        act_text_status = 1
        act_abstract = act_text[0:MAX_LEN]+u'...'
    act_photo = SITE_DOMAIN + activity[0].pic.url
    cur_time = timezone.now() # use the setting UTC
    act_seconds = 0
    if act_bookstart <= cur_time <= act_bookend:
        act_delta = act_bookend - cur_time
        act_seconds = act_delta.total_seconds()
        act_status = 0 # during book time
    elif cur_time < act_bookstart:
        act_delta = act_bookstart - cur_time
        act_seconds = act_delta.total_seconds()
        act_status = 1 # before book time
    else:
        act_status = 2 # after book time
    variables=RequestContext(request,{'act_name':act_name,'act_text':act_text, 'act_photo':act_photo,
                                      'act_bookstart':act_bookstart,'act_bookend':act_bookend,'act_begintime':act_begintime,
                                      'act_endtime':act_endtime,'act_totaltickets':act_totaltickets,'act_key':2333,
                                      'act_place':act_place, 'act_status':act_status, 'act_seconds':act_seconds,'cur_time':cur_time,
                                      'act_abstract':act_abstract, 'act_text_status':act_text_status,'act_ticket_remain':act_ticket_remain})
    return render_to_response('activitydetails.html', variables)


def ticket_view(request, uid):
    ticket = Ticket.objects.filter(unique_id=uid)
    if not ticket.exists():
        raise Http404  #current activity is invalid
    activity = Activity.objects.filter(id=ticket[0].district.activity_id)
    act_id = activity[0].id
    act_name = activity[0].name
    # act_key = activity[0].key
    act_begintime = activity[0].start_time
    act_endtime = activity[0].end_time
    act_place = activity[0].place
    ticket_status = ticket[0].status
    now = datetime.datetime.now()
    if act_endtime < now:#表示活动已经结束
        ticket_status = 3
    ticket_seat = ticket[0].seat
    seat_matrix = None
    if ticket_seat:
        seats = Seat.objects.filter(district=ticket[0].district)
        seat_matrix = parse_seats(seats, ticket[0])['seat_matrix']
    act_photo = "http://qr.ssast.org/fit/"+uid
    variables=RequestContext(request, {'act_id': act_id, 'act_name': act_name,'act_place': act_place, 'act_begintime': act_begintime,
                                       'act_endtime': act_endtime,'act_photo': act_photo, 'ticket_status': ticket_status,
                                       'ticket_seat': ticket_seat,
                                       'ticket_uid': uid, 'seat_matrix': seat_matrix})
    return render_to_response('activityticket.html', variables)


def help_view(request):
    variables=RequestContext(request,{'name':u'“紫荆之声”'})
    return render_to_response('help.html', variables)


def setting_view(request, openid):
    if request.method == 'GET':
        activity_list = get_bookable_activity_list()
        district_list = get_district_list(activity_list)
        seat_list = get_bookable_seat_list(district_list)
        variables = RequestContext(request, {'activity_list': activity_list, 'form': SettingForm(),
                                             'district_list': district_list, 'seat_list':seat_list, 'openid': openid})
        return render_to_response('setting.html', variables)
    else:
        '''
        form = SettingForm(request.POST)
        if form.is_valid():
            pass
        else:
            return HttpResponseRedirect(request.path)
        user_obj = get_user(openid)
        if user_obj is None:
            pass
        else:
            user_obj.book_activity = Activity.objects.get(id=form.cleaned_data['book_activity'])
            user_obj.book_district = District.objects.get(id=form.cleaned_data['book_district'])
            user_obj.need_multi_ticket = form.cleaned_data['need_multi_ticket']
            #user_obj.abandon_seats =
            user_obj.save()'''
        raise Http404


def setting_view_post(request):
    if request.method == 'GET':
        raise Http404
    else:
        form = SettingForm(request.POST)
        if form.is_valid():
            pass
        else:
            return HttpResponseRedirect(request.path)
        openid = request.POST['openid']
        user_obj = get_user(request.POST['openid'])
        if user_obj is None:
            pass
        else:
            user_obj.book_activity = Activity.objects.get(id=form.cleaned_data['book_activity'])
            user_obj.book_district = District.objects.get(id=form.cleaned_data['book_district'])
            user_obj.need_multi_ticket = form.cleaned_data['need_multi_ticket']
            user_obj.abandon_seats = form.cleaned_data['abandon_seats']
            user_obj.save()
            return HttpResponse(json.dumps('success'), content_type='application/json')
        raise Http404

def activity_menu_view(request, actid):
    activity = Activity.objects.get(id=actid)
    return render_to_response('activitymenu.html', {'activity': activity})


def helpact_view(request):
    variables=RequestContext(request,{})
    return render_to_response('help_activity.html', variables)


def helpclub_view(request):
    variables=RequestContext(request,{})
    return render_to_response('help_club.html', variables)


def helplecture_view(request):
    variables=RequestContext(request,{})
    return render_to_response('help_lecture.html', variables)


def get_bookable_activity_list():
    now = datetime.datetime.now();
    activity_set = Activity.objects.filter(status=1, book_end__gte=now).order_by('book_start')
    return activity_set


def get_district_list(activity_list):
    district_list = [];
    for activity in activity_list:
        district_list.extend(District.objects.filter(activity=activity.id))
    return district_list

def get_bookable_seat_list(district_list):
    bookable_seat_list = [];
    for district in district_list:
        bookable_seat_list.extend(Seat.objects.filter(district=district.id))
    return bookable_seat_list

def cancel_ticket(request, ticket_uid):

    tickets = Ticket.objects.filter(unique_id=ticket_uid)

    if not tickets.exists():
        return render_to_response("cancelticket.html", {"reply": "ticket does not exist"})
    else:
        ticket = tickets[0]
        if ticket.district.activity.book_end >= datetime.datetime.now():
            ticket.status = 0
            ticket.save()
            District.objects.filter(id=ticket.district.id).update(remain_tickets=F('remain_tickets')+1)
            return render_to_response("cancelticket.html", {"reply": "success"})
        else:
            return render_to_response("cancelticket.html", {"reply": "out of date"})

def parse_seats(seats, ticket):
    rows = 0
    cols = 0
    for seat in seats:
        if seat.row > rows:
            rows = seat.row
        if seat.column > cols:
            cols = seat.column
    seatMatrix = [[0 for col in range(cols+1)] for row in range(rows+1)]
    myrow = ticket.seat.row
    mycol = ticket.seat.column
    # 0 表示没有座位
    # 1 表示待出售
    # 2 表示已出售
    if ticket is None:
        for seat in seats:
            if seat.is_sold:
                seatMatrix[seat.row][seat.column] = 2
            else:
                seatMatrix[seat.row][seat.column] = 1
    else:
        for seat in seats:
            if myrow == seat.row and mycol == seat.column:
                seatMatrix[seat.row][seat.column] = 3
            else:
                seatMatrix[seat.row][seat.column] = 4

    preDict = dict()
    preDict['rows'] = rows+1
    preDict['cols'] = cols+1
    preDict['seat_matrix'] = seatMatrix
    return preDict

def view_seats(request, ticket_uid):
    tickets = Ticket.objects.filter(unique_id=ticket_uid)
    if not tickets.exists():
        raise Http404
    ticket = tickets[0]
    district = ticket.district
    seats = Seat.objects.filter(district=district)
    if not seats.exists():
        raise Http404

    return render_to_response("userviewseats.html", parse_seats(seats, ticket))
