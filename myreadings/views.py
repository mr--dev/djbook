from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core import validators
from django.shortcuts import render

from myreadings.models import Book, Magazine, Publisher, Author, Wish, ReadRate
from math import ceil
import calendar

OFFSET = 15

def index(request):
    tot_books = Book.objects.count()
    tot_magazines = Magazine.objects.count()
    currently_reading_books = Book.objects.filter(currently_reading=True).all()
    now = datetime.now()
    mm = now.month
    yy = now.year
    currently_reading_magazines = Magazine.objects.filter(month=mm, published_date=yy).all()
    month_read_books = ReadRate.objects.filter(year=yy, month=mm).count()
      
    ctx = { 
        'tot_books': tot_books,
        'tot_magazines': tot_magazines,
        'currently_reading_books': currently_reading_books,
        'currently_reading_magazines': currently_reading_magazines,
        'month_read_books': month_read_books,
    }
    return render(request, 'myreadings/index.html', ctx)

def index_wishlist(request):
    wishlist = Wish.objects.all()
    return render(request, 'myreadings/index_wishlist.html', {'wishlist': wishlist})

def save_wishlist(request):
    wish = Wish()
    wish.title = request.POST['title']
    wish.author = request.POST['author']
    wish.publisher = request.POST['publisher']
    wish.save()
    
    # TODO: Remove unused publisher and author
    return HttpResponseRedirect('/myreadings/wish/')

def delete_wish(request, wish_id):
    Wish.objects.get(pk=wish_id).delete()
    return HttpResponseRedirect("/myreadings/book/search/")

def search_book(request):
    books = Book.objects
    search_param = { 'title': '', 'author': '', 'publisher': '', 'page': 1, 'total_pages': 1}
    if 'title' in request.GET:
        books = books.filter(title__contains=request.GET['title'])
        search_param['title'] = request.GET['title']
    if 'author' in request.GET:
        books = books.filter(author__author__contains=request.GET['author'])
        search_param['author'] = request.GET['author']
    if 'publisher' in request.GET:
        books = books.filter(publisher__publisher__contains=request.GET['publisher'])        
        search_param['publisher'] = request.GET['publisher']
    
    books = books.all().order_by('title').distinct()
    total_books = books.count()
    total_pages = int(ceil(total_books/float(OFFSET)))
    total_pages = total_pages if total_pages != 0 else 1
    search_param['total_pages'] = total_pages
    search_param['total_books'] = total_books

    if 'page' in request.GET:
        search_param['page'] = request.GET['page']
    
    page = int(search_param['page'])
    books = books[(page-1)*OFFSET:page*OFFSET]
        
    # Read Rate Params
    rr_options = dict()
    rr_options['year'] = range((datetime.now().year), 2000, -1)
    rr_options['month'] = list()
    for i in range(1, 13):
        rr_options['month'].append({'value': i, 'month_name': calendar.month_name[i]})
    rr_options['rate']= range(1, 6)
    
    return render(request, 'myreadings/book_search.html', {'books': books, 'search_param': search_param, 'rr_options': rr_options } )

def add_book(request):
    return render(request, 'myreadings/book.html', {'book': Book()})

def edit_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404
    return render(request, 'myreadings/book.html', {'book': book })

def details_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404
    return render(request, 'myreadings/book_details.html', {'book': book })

def delete_book(request, book_id):
    Book.objects.get(pk=book_id).delete()
    return HttpResponseRedirect("/myreadings/book/search/")

def save_book(request):
    bid = request.POST['book-id']
    
    # Maybe check for non existing book
    if bid == "None": b = Book()
    else: b = Book.objects.get(pk=bid)
    
    b.title = request.POST['title']
    b.isbn = request.POST['isbn']
    b.google_id = request.POST['google-id']
    b.published_date = -1 if request.POST['published-date'] == "" else request.POST['published-date'] 
    b.page_count = -1 if request.POST['page-count'] == "" else request.POST['page-count']
    b.description = request.POST['description']
    b.thumbnail = request.POST['thumbnail']
    b.ebook = True if 'ebook' in request.POST else False
    b.currently_reading = True if 'currently-reading' in request.POST else False
    
    #Update Publisher
    p = Publisher.objects.get_or_create(publisher=request.POST['publisher'])[0]
    b.publisher = p
    b.save()
    
    # Update Author
    b.author_set.clear()
    authors = request.POST['author'].split(", ")
    for a in authors:
        a = Author.objects.get_or_create(author=a)[0]
        b.author_set.add(a)
    
    # TODO: Remove unused publisher and author
    return HttpResponseRedirect('/myreadings/book/search/')

def read_book(request, year="all", month="all"):
    params = {'page': '1', 'total_pages': '1'}
    rr_options = dict()
    rr_options['year'] = [str(y) for y in range((datetime.now().year), 2000, -1)]
    rr_options['month'] = list()
    for i in range(1, 13):
        rr_options['month'].append({'value': str(i), 'month_name': calendar.month_name[i]})
        
    readrate = ReadRate.objects
    if year != "all":
        readrate = readrate.filter(year=year)
    if month != "all":
        readrate = readrate.filter(month=month)
    if 'page' in request.GET:
        params['page'] = int(request.GET['page'])
        
    total_read = readrate.count()
    total_pages = int(ceil(total_read/float(OFFSET)))
    total_pages = total_pages if total_pages != 0 else 1
    params['total_pages'] = total_pages
    params['total_read'] = total_read
    params['year'] = year
    params['month'] = month
    
    page = int(params['page'])
    readrate = readrate.all().order_by('-year', '-month')[(page-1)*OFFSET:page*OFFSET]

    return render(request, 'myreadings/book_read.html', {'readrate': readrate, 'params': params, 'rr_options': rr_options})

def books_by_author(request, author_id):
    a = Author.objects.get(pk=author_id)
    books = a.books.all()
    return render(request, 'myreadings/books_by_author.html', {'author': a, 'books': books })

def books_by_publisher(request, publisher_id):
    p = Publisher.objects.get(pk=publisher_id)
    books = p.book_set.all()
    return render(request, 'myreadings/books_by_publisher.html', {'publisher': p, 'books': books })

def search_magazine(request):    
    magazines = Magazine.objects
    search_param = { 'title': '', 'year': '', 'page': 1, 'total_pages': 1}
    if 'title' in request.GET:
        magazines = magazines.filter(title__contains=request.GET['title'])
        search_param['title'] = request.GET['title']
    if 'year' in request.GET and request.GET['year'] != "":    
        magazines = magazines.filter(published_date__contains=request.GET['year'])
        search_param['year'] = request.GET['year']

    magazines = magazines.all().order_by('-published_date', '-month', '-title').distinct()
    total_magazines = magazines.count()
    total_pages = int(ceil(total_magazines/float(OFFSET)))
    total_pages = total_pages if total_pages != 0 else 1
    search_param['total_pages'] = total_pages
    search_param['total_magazines'] = total_magazines

    if 'page' in request.GET:
        search_param['page'] = request.GET['page']
    
    page = int(search_param['page'])
    magazines = magazines[(page-1)*OFFSET:page*OFFSET]
        
    return render(request, 'myreadings/magazine_search.html', {'magazines': magazines, 'search_param': search_param} )

def add_magazine(request):
    return render(request, 'myreadings/magazine.html', {'magazine': Magazine()})

def edit_magazine(request, magazine_id):
    try:
        magazine = Magazine.objects.get(pk=magazine_id)
    except Magazine.DoesNotExist:
        raise Http404
    return render(request, 'myreadings/magazine.html', {'magazine': magazine })

def details_magazine(request, magazine_id):
    try:
        magazine = Magazine.objects.get(pk=magazine_id)
        magazines = Magazine.objects.filter(title=magazine.title).values('number', 'published_date', 'month', 'description').order_by('-number')
        
    except Magazine.DoesNotExist:
        raise Http404
    return render(request, 'myreadings/magazine_details.html', {'magazine': magazine, 'magazines': magazines })

def delete_magazine(request, magazine_id):
    Magazine.objects.get(pk=magazine_id).delete()
    return HttpResponseRedirect("/myreadings/book/search/")

def save_magazine(request):
    mid = request.POST['magazine-id']
    
    # Maybe check for non existing book
    if mid == "None": m = Magazine()
    else: m = Magazine.objects.get(pk=mid)
    
    m.title = request.POST['title']
    m.number = -1 if request.POST['number'] == "" else request.POST['number']
    m.published_date = -1 if request.POST['published-date'] == "" else request.POST['published-date']
    m.month = -1 if request.POST['month'] == "" else request.POST['month']
    m.description = request.POST['description']
    m.thumbnail = request.POST['thumbnail'] 
    m.save()
    
    return HttpResponseRedirect('/myreadings/magazine/search/')
