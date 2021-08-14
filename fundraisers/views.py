from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import fundraiser
from django.contrib import messages
from django.db import connection
from fundraising_website.utils import getDropDown, dictfetchall
import datetime



# Create your views here.
def order_items(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `fundraisers_fundraiser`, `order`, `type` WHERE fundraiser_id =  order_fundraiser_id AND type_id = fundraiser_type_id AND order_id = "+ str(orderID))
    fundraiserlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT order_total as totalCartCost  FROM `order` WHERE order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "fundraiserlist": fundraiserlist,
        "customerOrderDetails": customerOrderDetails[0],
        "totalCost":totalCost[0]
    }

    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'order-items.html', context)

# Create your views here.
def orderlisting(request):
    cursor = connection.cursor()
    heading = "All Donations Report"
    if (request.session.get('user_level_id', None) == 1):
        SQL = "SELECT * FROM `order`,`users_user`,`order_status`, `fundraisers_fundraiser` WHERE order_status = os_id AND order_user_id = user_id AND fundraiser_id = order_fundraiser_id"
    else:
        heading = "My Donations"
        customerID = str(request.session.get('user_id', None))
        SQL = "SELECT * FROM `order`,`users_user`,`order_status`, `fundraisers_fundraiser` WHERE order_status = os_id AND order_user_id = user_id AND fundraiser_id = order_fundraiser_id AND user_id = " + customerID
    cursor.execute(SQL)
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist,
        "heading": heading
    }

    # Message according Fundraiser #
   
    return render(request, 'order-listing.html', context)

# Create your views here.
def fundraiserlisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM fundraisers_fundraiser, users_user, type WHERE user_id = fundraiser_user_id AND type_id = fundraiser_type_id")
    fundraiserlist = dictfetchall(cursor)

    context = {
        "fundraiserlist": fundraiserlist
    }

    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'fundraisers-listing.html', context)

# Create your views here.
def payment(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    cursor.execute("SELECT order_total TotalCartValue FROM `order` WHERE order_id = " + str(orderID))
    orderTotal = dictfetchall(cursor)
    context = {
        "orderTotal": orderTotal[0]
    }
    if (request.method == "POST"):
        request.session['order_id'] = "0"
        return redirect('order-items/'+str(orderID))
    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'payment.html', context)

# Create your views here.
def order_edit(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `fundraisers_fundraiser`, `order`, order_item, users_user, type WHERE fundraiser_id =  oi_fundraiser_id AND oi_order_id = order_id AND user_id = fundraiser_user_id AND type_id = fundraiser_type_id AND order_id = "+ str(orderID))
    fundraiserlist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerOrderDetails = dictfetchall(cursor)
    customerOrderDetails = customerOrderDetails[0]
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `fundraisers_fundraiser`, `order`, order_item, users_user, type WHERE fundraiser_id =  oi_fundraiser_id AND oi_order_id = order_id AND user_id = fundraiser_user_id AND type_id = fundraiser_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "fundraiserlist": fundraiserlist,
        "protypelist":getDropDown('order_status', 'os_id', 'os_title', customerOrderDetails['order_status'], '1'),
        "customerOrderDetails": customerOrderDetails,
        "totalCost":totalCost[0]
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE `order`
                    SET order_status= %s WHERE order_id = %s
                """, (
            request.POST['order_status'],
            request.POST['order_id']
        ))
        messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
        return redirect('orderlisting')
    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'order-edit.html', context)

# Create your views here.
def fundraisers(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM fundraisers_fundraiser, users_user, type WHERE user_id = fundraiser_user_id AND type_id = fundraiser_type_id")
    fundraiserlist = dictfetchall(cursor)

    context = {
        "fundraiserlist": fundraiserlist
    }

    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'fundraisers.html', context)

# Create your views here.
def fundraiser_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM fundraisers_fundraiser, users_user, type WHERE user_id = fundraiser_user_id AND type_id = fundraiser_type_id AND type_id = "+ str(typeID))
    fundraiserlist = dictfetchall(cursor)

    context = {
        "fundraiserlist": fundraiserlist
    }

    # Message according Fundraiser #
    context['heading'] = "Fundraisers Details";
    return render(request, 'fundraisers.html', context)

def update(request, fundraiserId):
    fundraiserdetails = fundraiser.objects.get(fundraiser_id=fundraiserId)
    context = {
        "fn": "add",
        "procompanylist":getDropDown('users_user', 'user_id', 'user_name', fundraiserdetails.fundraiser_user_id, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name', fundraiserdetails.fundraiser_type_id, '1'),
        "fundraiserdetails":fundraiserdetails
    }
    if (request.method == "POST"):
        try:
            fundraiser_image = None
            fundraiser_image = fundraiserdetails.fundraiser_image
            if(request.FILES and request.FILES['fundraiser_image']):
                fundraiserImage = request.FILES['fundraiser_image']
                fs = FileSystemStorage()
                filename = fs.save(fundraiserImage.name, fundraiserImage)
                fundraiser_image = fs.url(fundraiserImage)

            addFundraiser = fundraiser(
            fundraiser_id = fundraiserId,
            fundraiser_name = request.POST['fundraiser_name'],
            fundraiser_type_id = request.POST['fundraiser_type_id'],
            fundraiser_user_id = request.POST['fundraiser_user_id'],
            fundraiser_goal = request.POST['fundraiser_goal'],
            fundraiser_image = fundraiser_image,                  
            fundraiser_description = request.POST['fundraiser_description'],
            fundraiser_from_date = request.POST['fundraiser_from_date'])
            addFundraiser.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["fundraiserdetails"] = fundraiser.objects.get(fundraiser_id = fundraiserId)
        messages.add_message(request, messages.INFO, "Fundraiser updated succesfully !!!")
        return redirect('fundraiserlisting')

    else:
        return render(request,'fundraisers-add.html', context)

def fundraiser_details(request, fundraiserId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account, to buy the fundraiser!!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM fundraisers_fundraiser, users_user, type WHERE user_id = fundraiser_user_id AND type_id = fundraiser_type_id AND fundraiser_id = "+fundraiserId)
    fundraiserdetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "fundraiserdetails":fundraiserdetails[0]
    }
    if (request.method == "POST"):
        if(request.session.get('order_id', None) == "0" or request.session.get('order_id', False) == False):
            customerID = request.session.get('user_id', None)
            orderDate = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO `order`
            SET order_fundraiser_id = %s, order_user_id=%s, order_date=%s, order_status=%s, order_total=%s
            """, (
                request.POST['fundraiser_id'],
                customerID,
                orderDate,
                1,
                request.POST['donation_amount']))
            request.session['order_id'] = cursor.lastrowid    
        
        orderID = request.session.get('order_id', None);
       
        context["fundraiserdetails"] = fundraiser.objects.get(fundraiser_id = fundraiserId)
        messages.add_message(request, messages.INFO, "Fundraiser updated succesfully !!!")
        return redirect('payment')
    else:
        return render(request,'fundraisers-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "procompanylist":getDropDown('users_user', 'user_id', 'user_name',0, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name',0, '1'),
        "heading": 'Fundraiser add'
    };
    if (request.method == "POST"):
        try:
            fundraiser_image = None

            if(request.FILES and request.FILES['fundraiser_image']):
                fundraiserImage = request.FILES['fundraiser_image']
                fs = FileSystemStorage()
                filename = fs.save(fundraiserImage.name, fundraiserImage)
                fundraiser_image = fs.url(fundraiserImage)

            addFundraiser = fundraiser(fundraiser_name = request.POST['fundraiser_name'],
            fundraiser_type_id = request.POST['fundraiser_type_id'],
            fundraiser_user_id = request.POST['fundraiser_user_id'],
            fundraiser_goal = request.POST['fundraiser_goal'],
            fundraiser_image = fundraiser_image,                  
            fundraiser_description = request.POST['fundraiser_description'],
            fundraiser_from_date = request.POST['fundraiser_from_date'])
            addFundraiser.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('fundraiserlisting')

    else:
        return render(request,'fundraisers-add.html', context)


def delete(request, prodId):
    try:
        deleteFundraiser = fundraiser.objects.get(fundraiser_id = prodId)
        deleteFundraiser.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "Fundraiser Deleted Successfully !!!")
    return redirect('fundraiserlisting')

def order(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM order_item")
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Orders #
    context['heading'] = "Fundraisers Order Details";
    return render(request, 'orders.html', context)
