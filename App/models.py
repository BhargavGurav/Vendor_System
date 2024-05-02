from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_rate = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor_code


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now_add=False)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=False)
    acknowledgment_date = models.DateTimeField(null=True, auto_now_add=False) 
    
    def __str__(self):
        return self.po_number 

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=False)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor
    
    



    
