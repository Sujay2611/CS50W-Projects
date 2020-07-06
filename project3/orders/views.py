from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import SignUpForm, RegularPizza, SicilianPizza, Pasta, Salad, DinnerPlatter, Sub, Extra, Topping, Item, Order
from django.contrib.auth.models import User
import sys

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user=User.objects.create_user(form.cleaned_data.get('firstname'),form.cleaned_data.get('lastname'),form.cleaned_data.get('email'),form.cleaned_data.get('username'))
            user.save()
            print(user,file=sys.stdout)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user,
        "regularpizza": RegularPizza.objects.all(),
        "sicilianpizza": SicilianPizza.objects.all(),
        "pasta": Pasta.objects.all(),
        "salad": Salad.objects.all(),
        "dinnerplatter": DinnerPlatter.objects.all(),
        "sub": Sub.objects.all(),
        "extra": Extra.objects.all(),
        "topping": Topping.objects.all()
    }
    return render(request, "users/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password1"]
    if(username=="admin" and password=="admin"):
        return HttpResponseRedirect(reverse("admin"))
    else:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def details(request,type,name,size,price,val):
    count=0
    if request.method == "GET":
        return render(request,"users/details.html",{"type":type,"name":name,"size":size,"price":price,"val":val,"topping": Topping.objects.all()})
    else:
        if(type=='RegularPizza' or type=='SicilianPizza'):
            name=name+" "+type
        if(size=='singlesize'):
            size=''
        alltoppings=''
        quantity=request.POST["count"]
        if(val>0 and val<4):
            firsttopping=request.POST["firsttopping"]
            alltoppings=alltoppings+firsttopping
            if(val>1):
                secondtopping=request.POST["secondtopping"]
                alltoppings=alltoppings+', '+secondtopping
                if(val>2):
                    thirdtopping=request.POST["thirdtopping"]
                    alltoppings=alltoppings+', '+thirdtopping
                else:
                    thirdtopping=''
            else:
                secondtopping=''
                thirdtopping=''
        elif(val==5):
            alltoppings='Sausage, Mushrooms, Spinach, Barbeque Chicken, Zucchini'
        else:
            firsttopping=''
            secondtopping=''
            thirdtopping=''
        extras=''
        if(type=='Subs'):
            extras=''
            if('cheese' in request.POST):
                cheese=request.POST["cheese"]
                extras=extras+cheese
                count+=1
                if('mushrooms' in request.POST):
                    mushrooms=request.POST["mushrooms"]
                    extras=extras+", "+mushrooms
                    count+=1
                    if('greenpeppers' in request.POST):
                        greenpeppers=request.POST["greenpeppers"]
                        extras=extras+", "+greenpeppers
                        count+=1
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                    else:
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                else:
                    if('greenpeppers' in request.POST):
                        greenpeppers=request.POST["greenpeppers"]
                        extras=extras+", "+greenpeppers
                        count+=1
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                    else:
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
            else:
                if('mushrooms' in request.POST):
                    mushrooms=request.POST["mushrooms"]
                    extras=extras+mushrooms
                    count+=1
                    if('greenpeppers' in request.POST):
                        greenpeppers=request.POST["greenpeppers"]
                        extras=extras+", "+greenpeppers
                        count+=1
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                    else:
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                else:
                    if('greenpeppers' in request.POST):
                        greenpeppers=request.POST["greenpeppers"]
                        extras=extras+greenpeppers
                        count+=1
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+", "+onions
                            count+=1
                    else:
                        if('onions' in request.POST):
                            onions=request.POST["onions"]
                            extras=extras+onions
                            count+=1
        price=str(float(price)+(0.5*count))
        item=Item.objects.create(user=request.user,name=name,size=size,price=price,toppings=alltoppings,extras=extras,quantity=quantity)
        item.save()
        return HttpResponseRedirect(reverse("cart"))


def cart(request):
    items=Item.objects.filter(user=request.user).all()
    subtotal=0
    for item in items:
        subtotal=subtotal+item.price*item.quantity
    context = {
    "items": items,
    "subtotal": round(subtotal,2)
    }
    return render(request,"users/cart.html",context)

def delete(request,id):
    Item.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse("cart"))

def confirm(request):
    items=Item.objects.filter(user=request.user).all()
    subtotal=0
    for item in items:
        subtotal=subtotal+item.price*item.quantity
    context = {
    "user": request.user,
    "items": items,
    "subtotal": round(subtotal,2)
    }
    return render(request,"users/order.html",context)

def finish(request):
    allitems=Item.objects.filter(user=request.user).all()
    subtotal=0
    for item in allitems:
        subtotal=subtotal+item.price*item.quantity
    order=Order.objects.create(user=request.user,subtotal=subtotal)
    for eachone in allitems:
        print(Item.objects.all(),file=sys.stdout)
        eachitem=Item.objects.get(user=request.user,name=eachone.name,price=eachone.price,quantity=eachone.quantity)
        order.items.add(eachitem)
        print(Item.objects.all(),file=sys.stdout)
    print(order,file=sys.stdout)
    order.save()
    return render(request,"users/success.html")


def admin(request):
    context = {
    "order": Order.objects.all()
    }
    return render(request,"users/admin.html",context)

def register(request):
    if request.method == "GET":
        return render(request, "users/register.html")
