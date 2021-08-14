from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.fundraisers, name="fundraisers"),
    url(r'^filters/(?P<typeID>\w{0,50})/$', views.fundraiser_filter, name="fundraiser_filter"),
    url(r'^fundraiser-listing$', views.fundraiserlisting, name="fundraiserlisting"),
    url(r'^payment$', views.payment, name="payment"),
    url(r'^order-listing$', views.orderlisting, name="orderlisting"),
    url(r'^order-edit/(?P<orderID>\w{0,50})/$', views.order_edit, name="order_edit"),
    url(r'^add$', views.add, name="add"),
    url(r'^order-items/(?P<orderID>\w{0,50})/$', views.order_items, name="order_items"),
    url(r'^fundraiser-details/(?P<fundraiserId>\w{0,50})/$', views.fundraiser_details, name="fundraiser_details"),
    url(r'^update/(?P<fundraiserId>\w{0,50})/$', views.update, name="update"),
    url(r'^delete/(?P<prodId>\w{0,50})/$', views.delete, name="delete"),
    url(r'^order$', views.order, name="order"),
]
