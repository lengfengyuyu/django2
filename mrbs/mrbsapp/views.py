from django.shortcuts import render

# Create your views here.
from .models import Usr
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import auth

from .models import *
import datetime
import json

def __getBookInfoByHtml(request,book_date=None):
    """

    :param book_date: 预定日期
    :return: 当日的预定信息（html格式)
    """
    if not book_date:
        book_date = datetime.datetime.now().date()
    book_list = Book.objects.filter(date=book_date)
    time_list = Book.choices

    room_list = Room.objects.all()

    html_str = ''
    time_count = 13
    for room in room_list:
        html_str += '<tr><td>{}({})</td>'.format(room.caption, room.num)

        for x in time_list:
            flag = False
            for book in book_list:
                if book.room.id == room.id and book.time_id == x[0]:
                    flag = True
                    break
            if flag:
                if request.user.id == book.user.id:
                    html_str += '<td class="bitem item_my"  room_id={} time_id={}>{}</td>'.format(room.id,
                                                                                                  x[0],
                                                                                                  book.user.username)
                else:
                    html_str += '<td class="bitem item_notme"  room_id={} time_id={}>{}</td>'.format(room.id,
                                                                                                     x[0],
                                                                                                     book.user.username)
            else:
                html_str += '<td class="bitem" room_id={} time_id={}></td>'.format(room.id, x[0])
        html_str += '</tr>'

    return time_list,html_str

def index(request):
    time_list,html_str = __getBookInfoByHtml(request)
    ctime = datetime.datetime.now().date()

    return render(request, "mrbs/index.html", locals())

def ginfo(request):
    if request.method == "POST":
        book_date = request.POST.get('book_date', datetime.datetime.now().date())
        book_date= json.loads(book_date)
        book_date = datetime.datetime.strptime(book_date, "%Y-%m-%d")
        html_str = __getBookInfoByHtml(request,book_date=book_date)

        return HttpResponse(json.dumps(html_str))

def login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = auth.authenticate(username=u, password=p)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('mrbsapp:mrbs_index'))
    return render(request, "mrbs/login.html")



def booking(request):
    if request.method == "POST":
        book_date = request.POST.get('book_date')
        user = request.POST.get('user')
        book_data = request.POST.get('book_data')
        book_date = json.loads(book_date)
        book_date = datetime.datetime.strptime(book_date, "%Y-%m-%d")

        book_data = json.loads(book_data)

        ret = {"status":1,"msg":""}
        for opt,optList in book_data.items():
            try:
                if opt == "ADD":
                    for rid,tlist in optList.items():
                        for tid in tlist:
                            Book.objects.create(user=request.user,date=book_date,room_id=rid,time_id=tid)
                else:
                    for rid,tlist in optList.items():
                        for tid in tlist:
                            Book.objects.filter(user=request.user,date=book_date,room_id=rid,time_id=tid).delete()
                # add -create
            except Exception as e:
                print(e)
                ret['status'] = 0
                ret['msg']=e
            # del update
        return HttpResponse(json.dumps(ret))
