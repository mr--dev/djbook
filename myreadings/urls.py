from django.conf.urls import patterns, url
from myreadings import views, ajax

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^book/search/$', views.search_book, name='search_book'),
   url(r'^book/add/$', views.add_book, name='add_book'),
   url(r'^book/read/$', views.read_book, name='read_book'),
   url(r'^book/read/(?P<year>\d+)/$', views.read_book, name='read_book'),
   url(r'^book/read/(?P<year>\d+)/(?P<month>\d+)/$', views.read_book, name='read_book'),
   url(r'^book/author/(?P<author_id>\d+)/$', views.books_by_author, name='books_by_author'),
   url(r'^book/publisher/(?P<publisher_id>\d+)/$', views.books_by_publisher, name='books_by_publisher'),
   url(r'^book/(?P<book_id>\d+)/edit/$', views.edit_book, name='edit_book'),
   url(r'^book/(?P<book_id>\d+)/delete/$', views.delete_book, name='delete_book'),
   url(r'^book/(?P<book_id>\d+)/details/$', views.details_book, name='details_book'),
   url(r'^book/save/$', views.save_book, name='save_book'),
   
   url(r'^magazine/search/$', views.search_magazine, name='search_magazine'),
   url(r'^magazine/add/$', views.add_magazine, name='add_magazine'),
   url(r'^magazine/(?P<magazine_id>\d+)/edit/$', views.edit_magazine, name='edit_magazine'),
   url(r'^magazine/(?P<magazine_id>\d+)/delete/$', views.delete_magazine, name='delete_magazine'),
   url(r'^magazine/(?P<magazine_id>\d+)/details/$', views.details_magazine, name='details_magazine'),
   url(r'^magazine/save/$', views.save_magazine, name='save_magazine'),
   
   url(r'^wish/$', views.index_wishlist, name='index_wishlist'),
   url(r'^wish/save/$', views.save_wishlist, name='save_wishlist'),
   url(r'^wish/(?P<wish_id>\d+)/delete/$', views.delete_wish, name='delete_wish'),
   
   # AJAX
   url(r'^book/ajax/readrate/$', ajax.read_rate_book, name='read_rate_book'),
   url(r'^book/ajax/getreadrate/$', ajax.get_read_rate_book, name='get_read_rate_book'),
   url(r'^book/ajax/readrate/delete/$', ajax.delete_read_rate, name='delete_read_rate'),
)