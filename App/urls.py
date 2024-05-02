from django.urls import path 
from . import views


urlpatterns = [
    
    path('vendors/', views.vendors, name='vendors'),                                 # url for getting all vendors and creating new vendor object
    path('vendors/<str:vendor_id>', views.vendorPutGet, name='vendorPutGet'),        # put, delete, get particular vendor
    path('purchase_orders/', views.purchaseOrders, name='purchaseOrders'),           # get all purchase orders
    path('purchase_orders/<str:purchase_id>', views.POPutGetDelete, name='POPutGetDelete'),           # put, delete, get particular purchase order
    path('vendors/<str:vendor_id>/performance', views.calculatePerformace, name='calculatePerformace'),   # calculate performance of vendor
    path('purchase_orders/<str:po_id>/acknowledge', views.acknowledge, name='acknowledge'),           # acknowledge particular purchase order

]
