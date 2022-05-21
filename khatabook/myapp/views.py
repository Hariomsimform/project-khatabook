from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib.auth import login, logout

def latest(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    temptodo = Todo.objects.filter(customer_of=user).order_by('-date_created')
    return render(request=request, template_name='myapp/index.html',
                  context={'allTodo':temptodo}
                  ) 

def latest_5(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    temptodo = Todo.objects.filter(customer_of=user).order_by('-date_created')[:5]
    return render(request=request, template_name='myapp/index.html',
                  context={'allTodo':temptodo}
                  ) 

def oldest(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    temptodo = Todo.objects.filter(customer_of=user).order_by('date_created')
    return render(request=request, template_name='myapp/index.html',
                  context={'allTodo':temptodo}
                  )  

def oldest_5(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    temptodo = Todo.objects.filter(customer_of=user).order_by('date_created')[:5]
    return render(request=request, template_name='myapp/index.html',
                  context={'allTodo':temptodo}
                  )  

def by_title(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    temptodo = Todo.objects.filter(customer_of=user).order_by('title')
    return render(request=request, template_name='myapp/index.html',
                  context={'allTodo':temptodo}
                  )  
                
def register(request):
    if request.method=='POST':
        user_name = request.POST['username']
        first_name =request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password'] 
        try:
            check_username = User.objects.get(username=user_name)
            check_email = User.objects.get(email=email)
        except:
            check_username=None
            check_email = None    
        if check_username and check_email:
            print
            return render(request=request, template_name='myapp/register.html',
                            context={'message':'Email and User Name Must Be Unique'}
                            )
        else:
            user = User.objects.create_user(username=user_name,first_name=first_name,
                                            last_name=last_name, email=email, 
                                            password=password)
            user.save()
            return render(request=request, template_name='myapp/login.html',
                            context={'message':'Account Created Successfully!'})
    else:
        return render(request=request, template_name='myapp/register.html')  

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password= password)
        if user is not None:
            auth.login(request, user)
            message='Welcome Again '+ user.first_name+ ' ' + user.last_name
            all_customer = Todo.objects.filter(customer_of=user)
            return render(request, 'myapp/index.html',
                            context={'message':message, 'allTodo':all_customer})
        else:
            return render(request=request,template_name="myapp/login.html",
                            context={'message':'Username and Password Not Same! Try Again'})
    else:
        return render(request, 'myapp/login.html')       

def logout_reqest(request):
	logout(request)
	return render(request=request,template_name='myapp/login.html',
                    context={'message':'Logout Successfully!'})

def add_customer(request):
    if request.method=='POST':
        title = request.POST['name']
        desc = request.POST['contact']
        user_id =request.user.id
        user = User.objects.get(id=user_id)
        customer = Todo(title=title, desc=desc,customer_of=user)
        customer.save()
    all_customer = Todo.objects.filter(customer_of=user)
    return render(request=request,template_name='myapp/index.html',
                    context={'allTodo':all_customer})

def home(request):
    user_id =request.user.id
    if user_id==None:
        redirect('login')
    else:    
        user = User.objects.get(id=user_id)
        all_customer = Todo.objects.filter(customer_of=user)
        return render(request=request,template_name='myapp/index.html',
                        context={'allTodo':all_customer,'id':user})
    return render(request=request, template_name='myapp/login.html')


def business_overview(request):
    user_id =request.user.id
    user = User.objects.get(id=user_id)
    todo_data = Todo.objects.filter(customer_of=user)
    total_sales=0
    paid_sales=0
    remain_payment_sales=0
    per_customer_sale = []
    today_sales=[]
    yesterday_sales=[]
    week_sales=[]
    month_sales=[]
    quarter_sales=[]
    year_sales=[] 
    for todo in todo_data:
        t_sales = PurchaseDetails.objects.filter(customer_id=todo.id).aggregate(Sum('total_price'))   
        p_sales = PurchaseDetails.objects.filter(customer_id=todo.id).aggregate(Sum('paid_price')) 
        try:
            total_sales+=t_sales['total_price__sum']
            paid_sales+=p_sales['paid_price__sum']
        except:
            total_sales+=0
            paid_sales+=0    
        customer_sale = PurchaseDetails.objects.filter(customer_id=todo.id).values('customer_id').annotate(
             Sum('total_price'),
             Sum('paid_price'),
             Sum('remain_price'),
             Count('customer_id')
            )
        per_customer_sale.append(customer_sale)  
        t_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__lte=datetime.today()-timedelta(days=0))
        today_sales.append(t_sales)    
        y_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__lte=datetime.today())
        yesterday_sales.append(y_sales)
        w_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__gte=datetime.today()-timedelta(days=7))
        week_sales.append(w_sales)    
        m_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__gte=datetime.today()-timedelta(days=30))
        month_sales.append(m_sales)    
        q_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__gte=datetime.today()-timedelta(days=90))
        quarter_sales.append(q_sales)    
        y_sales = PurchaseDetails.objects.all().filter(
            customer_id=todo.id,
            date_created__gte=datetime.today()-timedelta(days=365))  
        year_sales.append(y_sales)
    remain_payment_sales =total_sales-paid_sales
    sales_detail = [total_sales, paid_sales, remain_payment_sales]
    customer_list = []
    
    sales_data = [  today_sales,
                    yesterday_sales,
                    week_sales,
                    month_sales,
                    quarter_sales,
                    year_sales ]
    print(sales_data,'---------sales data')
    for temp in sales_data:
        print(temp)
    ss_data=[]
    for i in sales_data:
        s_data = []
        for j in i:
            temp_list = []
            temp_list.append(j[0].paid_price)
            temp_list.append(j[0].customer_id.title)
            temp_list.append(j[0].remain_price)
            temp_list.append(j[0].total_price)
            s_data.append(temp_list)       
        ss_data.append(s_data)

    for customer in per_customer_sale:
        temp_customer = []
        user = Todo.objects.get(id=customer[0]['customer_id'])
        temp_customer.append(user.title)
        temp_customer.append(user.desc)
        temp_customer.append(customer[0]['total_price__sum'])
        temp_customer.append(customer[0]['paid_price__sum'])
        temp_customer.append(customer[0]['remain_price__sum'])
        temp_customer.append(customer[0]['customer_id__count'])
        customer_list.append(temp_customer)
    return render(request, template_name='myapp/business.html',
                            context={'sales_detail':sales_detail,
                            'per_customer_sale':customer_list,
                            'sales_data':ss_data})

def search(request,id):
    if request.method == 'POST':
        value =request.POST['inputvalue']
        temptodo=Todo.objects.all().filter(title__icontains=value,customer_of = id)
        return render(request=request, template_name='myapp/index.html', 
                        context={'allTodo':temptodo}) 

    temptodo = Todo.query.order_by(Todo.title.asc()).all()
    return render('index.html', allTodo=temptodo)    

def products():
    allTodo = Todo.query.all()
    return 'this is products page'

def view(request,id):
    todo = Todo.objects.get(id=id)
    product_list = PurchaseDetails.objects.filter(customer_id =id)
    sum =0
    for i in product_list:
        sum+=i.remain_price
    return render(request=request,template_name='myapp/view.html',
                    context={'product_list':product_list, 'todo':todo, 'sum':sum})


def update(request, id):
    if request.method=='POST':
        item = request.POST['item']
        total_price = request.POST['totalprice']
        paid_amount = request.POST['paidamount']
        remain_amount = int(total_price)-int(paid_amount)
        todo = Todo.objects.get(id=id)
    
        purchase_detail = PurchaseDetails(product_name=item,
                                            total_price=total_price,
                                            paid_price=paid_amount,
                                            remain_price=remain_amount,
                                            customer_id=todo
                                            )
        purchase_detail.save()
        return redirect('/home/')   
    todo = Todo.objects.get(id=id)
    print(todo)
    return render(request=request,template_name='myapp/update.html',
                    context={'todo':todo})

def delete(request,id):
    todo = Todo.objects.get(id=id).delete()
    return redirect("/home/")