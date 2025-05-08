from django.shortcuts import render, redirect
from myapp.models import Pet,Cart, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q      
import razorpay    
import uuid     
from django.core.mail import send_mail  

# Create your views here.


def userLogin(request):
    if request.method=="GET":
        return render(request, 'login.html')
    else:
        u = request.POST["username"]
        p = request.POST["password"]
        user = authenticate(username=u, password=p)
        print("LOGIN user after authenticate",user)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {}
            context['error']='details are not correct'
            return render(request,'login.html', context)
        
def userlogout(request):
    logout(request)
    return redirect('/')




def register(request):
    if request.method=="GET":
        return render(request, 'register.html' )
    else:
        u = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirmpassword']

        context = {}

        if u=="" or e=="" and e=="@gmail.com" or p=="" or cp=="":
            context['error']='all the field are complusory'
            return render(request, 'register.html', context)
        elif p!= cp:
            context['error']='password and confirm password must be same.'
            return render(request, 'register.html', context)
        else:
            user = User.objects.create(username=u,email=e)
            user.set_password(p)                  
            user.save()

            return redirect("/login")


def index(request):
    user = request.user
    print("user logged in?", user.is_authenticated)
    context={}
    products=Pet.objects.all()
    context['pets']=products

    return render(request,'index.html', context)

def getPetById(request,petid):
    context={}
    petobj=Pet.objects.get(id=petid)
    context['pet']=petobj
    return render(request, 'details.html', context)


def filterByCategory(request,catName):
    context={}
    allPets=Pet.objects.filter(type=catName)
    context['pets']=allPets
    print(catName)
    print(allPets)
    return render(request,'index.html',context)


def sortByPrice(request, direction):
    if direction=='asc':
        column='price'
    else:
        column='-price'
    context={}
    allPets = Pet.objects.order_by(column)
    context['pets']=allPets
    return render(request,'index.html',context)


def filterByrange(request):
    min = request.GET['min']
    max = request.GET['max']

    c1 = Q(price__gte=min)
    c2 = Q(price__lte=max)
    Pets = Pet.objects.filter(c1 & c2)
    context={}
    context['pets']=Pets
    return render(request,'index.html',context)

def addTocart(request,petid):
    selectedpetObject = Pet.objects.get(id=petid)
    userid = request.user.id
    if userid is not None:
        loggedInUserObject = User.objects.get(id = userid)
        cart = Cart.objects.create(uid=loggedInUserObject, petid=selectedpetObject)
        cart.save() 
        return redirect('/')
    else:
        # context={'error': 'plz login first'}
        return redirect('/login')

def showMycart(request):
    userid = request.user.id
    print(userid)
    user = User.objects.get(id=userid)
    print(user)
    myCart =  Cart.objects.filter(uid = user)
    context = {'mycart': myCart}
    count = len(myCart)
    TotalBill = 0
    for cart in myCart:
        TotalBill += cart.petid.price * cart.quantity
    context ["count"]=count 
    context["TotalBill"] = TotalBill 
    return render(request,'mycart.html',context)


def removeCart(request, cartid):
    c = Cart.objects.filter(id=cartid)
    c.delete()
    return redirect('/showmycart')


def updateQuantity(request, cartid, operation):
    cart = Cart.objects.filter(id=cartid)

    if operation == 'incr':
        q = cart[0].quantity
        cart.update(quantity=q+1)
        return redirect('/showmycart')
    else:
        q = cart[0].quantity
        cart.update(quantity=q-1)
        return redirect('/showmycart')
    
def confirmOrder(request):
    userid = request.user.id
    print(userid)
    user = User.objects.get(id=userid)
    print(user)
    myCart =  Cart.objects.filter(uid = user)
    context = {'mycart': myCart}
    count = len(myCart)
    TotalBill = 0
    for cart in myCart:
        TotalBill += cart.petid.price * cart.quantity
    context ["count"]=count 
    context["TotalBill"] = TotalBill 
    return render (request,'confirm.html', context)



def contact(request):
    return render(request,'contact.html')



# we need to add details in ordertable 
# get current login user based on that we need to get current user card details 
# findout total bill amount


def makepayment(request):
    userid = request.user.id
    user = User.objects.get(id=userid)
    data = Cart.objects.filter(uid = userid)
    total = 0
    for cart in data :
        total += cart.petid.price*cart.quantity
    client=razorpay.Client(auth=("rzp_test_J3K0nbI279n8zQ","NL45n1iC9tkA6Dl0AS9svNPL"))
    data = { 'amount': total*100, 'currency':'INR', 'receipt': ''}
    payment=client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    context['user']=user

    return render(request,'pay.html', context)


def placeOrder(request):
    ordid = uuid.uuid4()
    userid = request.user.id
    cartlist = Cart.objects.filter(uid = userid)
    for cart in cartlist:
        order = Order.objects.create(orderid = ordid, userid = cart.uid, petid = cart.petid, quantity = cart.quantity)
        order.save()
    cartlist.delete()
   
    msg = "Thank You for Shopping with Us! We truly appreciate your purchase and your trust in us. We hope you enjoy your order and look forward to serving you again soon! your order id is : " +str(ordid)
    send_mail(
        "Order Place Successfully !!",
        msg,
        "rushikeshkarande1061@gmail.com",
        [request.user.email],
        fail_silently=False,
    )   
    return redirect('/')
    
