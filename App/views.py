from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core.serializers import serialize
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from pytz import timezone


# Create your views here.


# view for getting details of vendors and saving new vendors data
@csrf_exempt
def vendors(request):

    if request.method == 'POST':            # if post requst then collect data from request body and create new vendor and save it
        data = json.loads(request.body.decode('utf-8'))
        
        name = data.get('name')
        contact_details = data.get('contact_details')
        address = data.get('address')
        vendor_code = data.get('vendor_code')
        on_time_delivery_rate = data.get('on_time_delivery_rate')
        quality_rating_avg = data.get('quality_rating_avg')
        average_response_rate = data.get('average_response_rate')
        fulfillment_rate = data.get('fulfillment_rate')

        obj = Vendor(name=name,contact_details=contact_details,address=address,vendor_code=vendor_code,on_time_delivery_rate=on_time_delivery_rate,quality_rating_avg=quality_rating_avg,average_response_rate=average_response_rate,fulfillment_rate=fulfillment_rate)
        obj.save()           # saving vendor instance
    
        return JsonResponse({'result' : 'Vendor data recorded.'})        # returning Json response

    # if request type is GET then return Json format data of all vendors
    if request.method == 'GET':
        vendrs = Vendor.objects.all()
        data = serialize("json", vendrs)
        return HttpResponse(data, content_type='application/json')



# view to edit or delete or get particular vendor data
@csrf_exempt
def vendorPutGet(request, vendor_id):
    # first check if we have vendor of given vendor_id
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
    except:
        return JsonResponse({'result' : f'{vendor_id} not present.'})

    # if request type is PUT then edit the fields given by user in json data
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))

        for key,value in data.items():
            setattr(vendor, key, value)

        vendor.save()
        return JsonResponse({'result' : f"{vendor_id}'s data updated successfully."})


    # if request is get then find the required vendor and return his/her data
    if request.method == 'GET':
        data = {'name' : vendor.name, 'contact_details': vendor.contact_details, 'address' : vendor.address, 'vendor_code' : vendor.vendor_code, 'on_time_delivery_rate':vendor.on_time_delivery_rate, 'quality_rating_avg' : vendor.quality_rating_avg, 'average_response_rate':vendor.average_response_rate,'fulfillment_rate' : vendor.fulfillment_rate}
        return JsonResponse(data)

    # if request is DELETE then deletes the required vendor
    if request.method == 'DELETE':
        vendor.delete()
        return JsonResponse({'result' : f"{vendor_id} deleted successfully."})



# view for purchase orders data (to return all purchase orders or create new purchase order)
@csrf_exempt
def purchaseOrders(request):
    # if request is post then saves new purchase order's data getting from request body
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        po_number = data.get('po_number')
        vendor_id = data.get('vendor')
        delivery_date = data.get('delivery_date')
        items = data.get('items')
        quantity = data.get('quantity')
        status = data.get('status')
        quality_rating = data.get('quality_rating')
        issue_date = data.get('issue_date')
        acknowledgment_date = data.get('acknowledgment_date')

        vendor = Vendor.objects.get(vendor_code=vendor_id)

        purchase = PurchaseOrder(po_number=po_number,vendor=vendor,delivery_date=delivery_date,items=items,quantity=quantity,status=status,quality_rating=quality_rating,issue_date=issue_date,acknowledgment_date=acknowledgment_date)

        purchase.save()
        return JsonResponse({'result' : 'Purchase Order is recorded successfully.'})

    # if request is get then return all purchase order data
    if request.method == 'GET':
        orders = PurchaseOrder.objects.all()
        data = serialize("json", orders)
        return HttpResponse(data)



# view for editing or deleting or getting particular purchase order details
@csrf_exempt
def POPutGetDelete(request, purchase_id):
    # first check if purchase order details present of required id
    try:
        purchase = PurchaseOrder.objects.get(po_number=purchase_id)
       
    except:
        return JsonResponse({'result' : f'{purchase_id} not present.'})

    # if request is PUT then edit required fields getting from request body
    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))

        for key,value in data.items():
            setattr(purchase, key, value)

        purchase.save()
        return JsonResponse({'result' : f"{purchase_id}'s data updated successfully."})


    # if request is get then return required purchase order details
    if request.method == 'GET':
        data_of_get = {'po_number':purchase.po_number, 'vendor' : purchase.vendor.vendor_code, 'order_date':purchase.order_date, 'delivery_date':purchase.delivery_date, 'items':purchase.items, 'quantity':purchase.quantity, 'status':purchase.status, 'quality_rating':purchase.quality_rating, 'issue_date':purchase.issue_date, 'acknowledgment_date':purchase.acknowledgment_date}

        return JsonResponse(data_of_get)

    # if request is DELETE then deletes the required purchase order details
    if request.method == 'DELETE':
        purchase.delete()
        return JsonResponse({'result' : f"{purchase_id} deleted successfully."})


# view to calculate performance metrix of vendor of given id
@csrf_exempt
def calculatePerformace(request, vendor_id):
    # check if vendor of given id present then get all orders which are issued to him/her
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
        orders = PurchaseOrder.objects.filter(vendor=vendor)
    except:
        return JsonResponse({'result' : f'{vendor_id} is not vendor of any orders.'})

    # calculate all required fields 
    if (request.method == 'GET') or (request.method == 'POST'):
        today = datetime.now()
        tz = timezone('UTC')
        on_time_delivery_rate = len([order for order in orders if (order.status == 'completed') and (order.delivery_date.astimezone(tz) - today.astimezone(tz)).days > 0]) / len(orders)

        quality_rating_avg = sum([order.quality_rating for order in orders])/len(orders)

        average_response_time = sum([abs((order.issue_date - order.acknowledgment_date).days) for order in orders])/len(orders)

        fulfillment_rate = len([order for order in orders if order.status == 'completed'])/len(orders)

        performance_record = HistoricalPerformance(vendor=vendor, date=today, on_time_delivery_rate=on_time_delivery_rate, quality_rating_avg=quality_rating_avg, average_response_time=average_response_time, fulfillment_rate=fulfillment_rate)
        performance_record.save()              # saving performance instance

        data = {'vendor' : vendor.vendor_code, 'date':today, 'on_time_delivery_rate':on_time_delivery_rate, 'quality_rating_avg':quality_rating_avg, 'average_response_time':average_response_time, 'fulfillment_rate':fulfillment_rate}

        return JsonResponse(data)
    

# view to acknowledge particular purchase order of given id and trigger vendor performance view
@csrf_exempt
def acknowledge(request, po_id):
    try:
        purchase = PurchaseOrder.objects.get(po_number = po_id)
    except:
        return JsonResponse({'status' : f'{po_id} is not present in purchase orders data.'})
    
    if request.method == 'POST':
        # data = json.loads(request.body.decode('utf-8'))
        setattr(purchase, "acknowledgment_date", datetime.now())

        purchase.save()

        vendor_id = purchase.vendor.vendor_code
        # vendorToUpdate = Vendor.objects.get(vendor_code=vendor)
        return HttpResponseRedirect(f'/vendors/{vendor_id}/performance')         # triggering vendor performance view
        
        

    








        
        




    

# http://127.0.0.1:8000/vendors/?name=Bhargav%20Gurav&contact_details=1569431659,%20akjsdui@gmail.com&address=wagh%20nagar%20jalgaon&vendor_code=V2&on_time_delivery_rate=5.5&quality_rating_avg=6.8&average_response_rate=2.6&fulfillment_rate=9.5


# curl -X POST http://127.0.0.1:8000/vendors/ -H "Content-Type: application/json" -d '{"name": "Bhargav Gurav", "contact_details": "1569431659, akjsdui@gmail.com", ...}'



# vendors function POST request input : 
# {
#   "name": "bhargav gurav",
#   "contact_details": "9016483154, abcxyz09@gmail.com",
#   "address": "wagh nagar, Jalgaon, India",
#   "vendor_code": "V2",
#   "on_time_delivery_rate": 5.0,
#   "quality_rating_avg": 4.6,
#   "average_response_rate": 4.7,
#   "fulfillment_rate": 9.8
# }


# vendorPutGet input for put :
# {
#   "name": "abhyang nanu",
#   "contact_details": "4396383154, abcxyz09@gmail.com",
#   "address": "disco nagar, Jalgaon, India"
# }


# purchase order input for post request : 
# {
#   "po_number": "P1",
#   "vendor": "V1",
#   "delivery_date": "2024-05-10 15:45Z",
#   "items": {
#     "maggie": 15,
#     "Jaggery": 2,
#     "Wheat": 10,
#     "Iron": 1
#   },
#   "quantity": 42,
#   "status": "pending",
#   "quality_rating": 4.5,
#   "issue_date": "2024-05-07 22:30Z",
#   "acknowledgment_date": "2024-05-12 07:15Z"
# }