from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson

from myreadings.models import Book, ReadRate

response_data = dict()

def read_rate_book(request):
    try:
        b = Book.objects.get(pk=int(request.POST['book_id']))
        rr = ReadRate()
        rr.book = b
        rr.year = request.POST['year']
        rr.month = request.POST['month']
        rr.rate = request.POST['rate']
        rr.save()
        status = 0
        message = "OK"
    except:
        status = 1
        message = "An Error Occured."
    response_data['status'] = status
    response_data['message'] = message
    return HttpResponse(simplejson.dumps(response_data))

def get_read_rate_book(request):
    rr_list = list()
    try:
        b = Book.objects.get(pk=int(request.POST['book_id']))
        rr_list = b.readrate_set.all().order_by('-year', '-month').values('id', 'year', 'month', 'rate')
        status = 0
        message = "OK"
    except Exception, e:
        print e
        status = 1
        message = "An Error Occured."
    response_data['status'] = status
    response_data['message'] = message
    response_data['rr_list'] = list(rr_list)
    return HttpResponse(simplejson.dumps(response_data))

def delete_read_rate(request):
    try:
        ReadRate.objects.get(pk=int(request.POST['readrate_id'])).delete()
        status = 0
        message = "OK"
    except Exception, e:
        print e
        status = 1
        message = "An Error Occured."
    response_data['status'] = status
    response_data['message'] = message
    return HttpResponse(simplejson.dumps(response_data))