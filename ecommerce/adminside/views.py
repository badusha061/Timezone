from itertools import groupby
from django.shortcuts import render , redirect
from django.contrib import messages , auth
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import  Q
from django.db.models import Sum
from django.views import View
from datetime import datetime
from datetime import date
from order.models import Order , OrderCancel , OrderItem , OrderReturn
import csv 
from django.http import HttpResponse
from fpdf import FPDF

from django.db.models import Prefetch
# Create your views here.


@login_required(login_url = 'adminside:admin_login')
def dashboard(request):
    
    if request.user.is_superuser:
        orders = Order.objects.order_by('id')[:10:]
        order = Order.objects.all()


   
        sales_data  = OrderItem.objects.values('order__created_at__date').annotate(total_sale = Sum('price')).order_by('-order__created_at__date')
        categories = [item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
        sales_values = [item['total_sale'] for item in sales_data]
        return_data = OrderItem.objects.filter(status__in=["Return", "Cancelled"]).values('order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
        return_values = [item['total_returns'] for item in return_data]
        print(return_values)
        print(sales_values)
        try:
            total_sale= 0 
            order = Order.objects.all()
            for i in order:
                i.total_price
                total_sale += i.total_price
        except:
            total_sale = 0

        
        try:            
            total_earning = 0 
            order_ear = Order.objects.filter(od_status = 'Delivered')
            for i in order_ear:
                total_earning += i.total_price
        except:
            total_earning = 0
        try:
            status_delivery = Order.objects.filter(od_status = 'Delivered').count()
            status_return = Order.objects.filter(od_status = 'Return').count()
            status_cancel = Order.objects.filter(od_status = 'Cancelled').count()
            total = status_delivery + status_return + status_cancel
            status_delivery = (status_delivery/100)*total
            status_cancel = (status_cancel/100)*total
            status_return = (status_return/100)*total
        except:
            status_delivery = 0
            status_cancel = 0 
            status_return = 0 
            
     
        print(orders)
        print(total_sale)
        print(total_earning)
        print(status_return)
        print(status_return)
        print(sales_values)
        context = {
            'orders':orders,
            'total_sale':total_sale,
            'total_earning':total_earning,
            'total_sale':total_sale,
            'status_return':status_return,
            'status_cancel':status_cancel,
            'status_delivery':status_delivery,
            'sales_values':sales_values,
            'return_values':return_values,
            'categories':categories 
        }
        return render(request,'adminside/dashboard.html',context)
    else:       
        return redirect( 'adminside:admin_login')


def admin_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request , username = username , password = password)

            #validatings the fiels is empty
            if username.strip() == '' or password == '':
                messages.error(request , 'fields empty !!!')
                return redirect('adminside:admin_login')
            
            if user and user.is_superuser:
                login(request , user)
                return redirect('adminside:dashboard')
            else:
                messages.error(request ,'Invalid credentials. Please try again.')
                return redirect('adminside:admin_login')
        return render(request, 'adminside/admin_login.html')
    except Exception as e:
        print(e)
        return render(request, 'adminside/admin_login.html')


@login_required(login_url = 'adminside:admin_login')
def user_mgt(request):
    try:
        users = User.objects.all().order_by('id')
        context = {
            'users': users
        }

        return render(request, 'adminside/usermgt.html', context)
    except Exception as e:
        print(e)
        return render(request, 'adminside/usermgt.html')


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('adminside:admin_login')


@login_required(login_url='admin_login')
def user_block(request,user_id):
    try:
        # user is block 
        user = User.objects.get(id = user_id)
        if user.is_active:  
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('adminside:user_mgt')
    except Exception as e:
        print(e)
        return redirect('adminside:user_mgt')

@login_required(login_url='admin_login')
def user_search(request):
    try:
        search = request.POST.get('search')

        # validatings the search is empty
        if search is None or  search.strip() == '':
            messages.error(request , 'field is empty')
            return redirect('adminside:user_mgt')
        users = User.objects.filter(Q(username__icontains = search)| Q(email__icontains = search))
        context = {
            'users':users
        }
        if users:
            pass
        else:
            users : False
            messages.error(request , 'Search is not found')
            return redirect('adminside:user_mgt')
        return render(request, 'adminside/usermgt.html',context)
    except Exception as e:
        print(e)
        return render(request, 'adminside/usermgt.html')


@login_required(login_url = 'adminside:admin_login')
def user_block_status(request):
    try:
        name = request.POST.get('name')
        if name == 'Active':
            users = User.objects.filter(is_active = True)
            context = {
                'users':users
            }
            return render(request , 'adminside/usermgt.html',context)
        if name == 'Blocked':
            users = User.objects.filter(is_active = False)
            context = {
                'users':users
            }
            return render(request ,'adminside/usermgt.html',context)
        if name == 'All':
            users = User.objects.all()
            context = {
                'users':users
            }
            return render(request, 'adminside/usermgt.html',context)
    except Exception as e:
        print(e)
        return render(request,'adminside/usermgt.html')

@login_required(login_url = 'adminside:admin_login')
def adminpage(request):
    return redirect('adminside:dashboard')



@login_required(login_url = 'adminside:admin_login')
def sales_report(request):
    try:
        start_date = None
        end_date = None
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        
            if start_date and end_date:
                start_date = datetime.strptime(start_date,'%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                print('start date and end date',start_date , end_date)
                if start_date > end_date:
                    messages.error(request, 'Start date must be end date')
                    return redirect('adminside:dashboard')
                if end_date > date.today():
                    messages.error(request,'End date cannot be in the future')
                    return redirect('adminside:dashboard')
                orders = Order.objects.filter(created_at__date__range=(start_date,end_date))
                print('the order is the ',orders)
                recend_order = orders.order_by('created_at')
                total_sale = sum(order.total_price for order in orders)
                total_count = orders.count()

                sales_by_status = {
                    'Pending':orders.filter(od_status = 'Pending').count(),
                    'Processing':orders.filter(od_status = 'Processing').count(),
                    'Shipped':orders.filter(od_status = 'Shipped').count(),
                    'Delivered':orders.filter(od_status = 'Delivered').count(),
                    'Cancelled':orders.filter(od_status = 'Cancelled').count(),
                    'Return':orders.filter(od_status = 'Return').count()
                    }

                sales_report = {
                    'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
                    'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
                    'total_sales': total_sale,
                    'total_orders': total_count,
                    'sales_by_status': sales_by_status,
                    'recent_orders': recend_order,
                }
                context = {
                        'sales_report':sales_report,
                }
                print('the total sale is the ',total_sale)
                return render(request,'adminside/salesreport.html',context)

        recend = Order.objects.order_by('created_at')[:10]
        orders = Order.objects.all()
        total_sale = sum(order.total_price for order in orders)
        total_count = orders.count()

        sales_by_status = {
            'Pending':orders.filter(od_status = 'Pending').count(),
            'Processing':orders.filter(od_status = 'Processing').count(),
            'Shipped':orders.filter(od_status = 'Shipped').count(),
            'Delivered':orders.filter(od_status = 'Delivered').count(),
            'Cancelled':orders.filter(od_status = 'Cancelled').count(),
            'Return':orders.filter(od_status = 'Return').count()
            }

        sales_report = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
            'total_sales': total_sale,
            'total_orders': total_count,
            'sales_by_status': sales_by_status,
            'recent_orders': recend,
        }
        context = {
                'sales_report':sales_report,
        }
        print('the total sale is the ',total_sale)
        return render(request,'adminside/salesreport.html',context)
    except Exception as e:
        print(e)
        return render(request, 'adminside/salesreport.html')


@login_required(login_url = 'adminside:admin_login')
def export_csv(request,start_date = None , end_date = None):
    try:
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename=Expenses' + \
            str(datetime.now()) + '.csv'
        
        writer = csv.writer(response)
        # heading for csv 
        writer.writerow(['user','total_price','payment_mode','tracking number', 'Order at','product_name','product_price','product_quantity'])
        if start_date and end_date:
            start_date_obj = datetime.strptime(start_date,'%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = Order.objects.filter(created_at__date__range=(start_date_obj, end_date_obj))
        else:
            orders = Order.objects.all()

        for order in orders:
            order_item = OrderItem.objects.filter(order = order).select_related('product')
            grouped_order_items = groupby(order_item, key=lambda x: x.order_id)
            for order_id , items_group in grouped_order_items:
                item_list = list(items_group)
                for order_item in item_list:
                    writer.writerow([
                        order.user.username if order_item == item_list[0] else " ",
                        order.total_price if order_item == item_list[0] else " ",
                        order.payment_mode if order_item == item_list[0] else " ",
                        order.tracking_no if order_item == item_list[0] else " ", 
                        order.created_at if order_item == item_list [0] else " ", 
                        order_item.product.product_name ,
                        order_item.product.product_price ,
                        order_item.quantity
                    ])
        return response
    except Exception as e:
        print(e)
        return render(request, 'adminside/salesreport.html')
@login_required(login_url = 'adminside:admin_login')
def pdf(request,start_date = None , end_date = None):
    try:
        response =HttpResponse(content_type = 'application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Expenses' + \
            str(datetime.now()) + '.pdf'
        
        w_pt = 8.5 * 40  # 8.5 inches width
        h_pt = 11 * 20   # 11 inches hieght 

        pdf = FPDF(format=(w_pt, h_pt))
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15) 

        #set the style 
        pdf.set_font('Arial', 'B', 12)

        # Header Information
        pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
        pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')
        
        data = [['user','Toatl price','Payement Mode','Tracking Number','Odered_at', 'Product Name','Product Price','Prduct Quantity']]
        if start_date and end_date:
                start_date_obj = datetime.strptime(start_date,'%Y-%m-%d').date()
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                orders = Order.objects.filter(created_at__date__range=(start_date_obj, end_date_obj)).prefetch_related(
                Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
                )
        else:
            orders = Order.objects.all().prefetch_related(
                Prefetch('orderitem_set', queryset = OrderItem.objects.select_related('product'))
            )
        for order in orders:
            order_item = order.orderitem_set.all()
            for index , order_item in enumerate(order_item):
                data.append([
                    order.user.username if index == 0 else "",
                    order.total_price if index == 0 else "",
                    order.payment_mode if index == 0 else "",
                    order.tracking_no if index == 0 else "",
                    str(order.created_at.date()) if index == 0 else "",
                    order_item.product.product_name , 
                    order_item.product.product_price ,
                    order_item.quantity,
                ])
        # Create Table
        col_width = 40  
        row_height = 10
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, str(item), border=1)
            pdf.ln()
        response.write(pdf.output(dest='S').encode('latin1'))  
        return response
    except Exception as e:
        print(e)
        return render(request, 'adminside/salesreport.html')