from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.paginator import Paginator
from songline import Sendline
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import markdown as md
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *


# -------CheckAdmin--------
def CheckNotAdmin(request):
    if request.user.profile.usertype != 'admin':
        return True
    else:
        return False

# -------Generate Token--------


def GenerateToken(domain='http://localhost:8000/confirm/'):
    allchr = [chr(i) for i in range(65, 91)]
    allchr.extend([chr(i) for i in range(97, 123)])
    allchr.extend([str(i) for i in range(10)])
    email_token = ''
    for i in range(40):
        email_token += random.choice(allchr)

    url = domain + email_token
    # print(url)
    return (url, email_token)


def Confirm(request, token):
    try:
        check = VerifyEmail.objects.get()
        status = 'found'
        check.approved = True
        check.save()
        context = {'status': status, 'username': check.user.username,
                   'name': check.user.first_name}
    except:
        status = 'notfound'
        context = {'status': status}

    return render(request, 'myapp/confirm.html', context)


# -------Line Notify--------
token = 'q28Plk7483wV4CufUVoYChw7lXqb2Proo4H6diM4WJ0'
messenger = Sendline(token)

# -------------ສົ່ງເມລ໌ພາສາລາວ-------------


def sendthai(sendto, subj="ທົດສອບສົ່ງອີເມລລ໌", detail="ສະບາຍດີ!\nເຈົ້າສະບາຍດີບໍ?\n"):

    myemail = 'thitphavanh23@gmail.com'
    mypassword = 'hery18205208038'
    receiver = sendto

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = 'ຈາກ Phenomenal Bottega'
    msg['To'] = receiver
    text = detail

    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()

    s.login(myemail, mypassword)
    s.sendmail(myemail, receiver.split(','), msg.as_string())
    s.quit()
    print('ສົ່ງແລ້ວ!')

# -------------Start sending-------------


def EmailConfirm(email, name, token):
    subject = 'ຍືນຍັນການສະໝັກ Website E-Commerce !! Phenomenal Bottega'
    newmember_name = name
    content = '''
	ເນື່ອງຈາກຄວາມປອດໄພຂອງການເຂົ້າໃຊ້
	ກະລູນາຍືນຍັນອີເມລ໌ ຜ່ານລິ້ງຄ໌ດ້ານລຸ່ມ
	'''
    # link = 'http://phenomenal.com/confirm/ph12345'
    link = token

    msg = 'ສະບາຍດີ {} \n\n {} Verify Link : {}'.format(
        newmember_name, content, link)
    sendthai(email, subject, msg)

# HttpResponse ເປັນຟັງຊັ່ນສຳຫຼັບເຮັດໃຫ້ໂຊວ໌ຂໍ້ຄວາມໜ້າເວ໊ບໄດ້


def Home(request):
    product = Allproduct.objects.all().order_by('id').reverse()[
        :3]  # ແມ່ນການດຶງຂໍ້ມູນມາທັງໝົດ
    preorder = Allproduct.objects.filter(quantity__lte=0)
    # quantity__lte=0 (ຫາຄ່າທີີ່ quantity <= 0 - lte is <=)
    # quantity__gt=0 (ຫາຄ່າທີີ່ quantity > 0 - gt is >)
    # quantity__gte=10 (ຫາຄ່າທີີ່ quantity >= 5 - gte is >=)
    context = {'product': product, 'preorder': preorder}
    return render(request, 'myapp/home.html', context)

    # return HttpResponse('ສະບາຍດີ<h1>hello world</h1><h3>ສະບາຍດີບໍ?</h3')


def About(request):
    return render(request, 'myapp/about.html')


def Contact(request):
    return render(request, 'myapp/contact.html')


def AddProduct(request):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')

        new = Allproduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imageurl = imageurl
        new.quantity = quantity
        new.unit = unit

        # ------Save Image-------
        try:
            file_image = request.FILES['imageupload']
            file_image_name = request.FILES['imageupload'].name.replace(' ', '')
            print('FILE_iMAGE:', file_image)
            print('IMAGE_NAME:', file_image_name)
            fs = FileSystemStorage()
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            new.image = upload_file_url[6:]
        except:
            new.image = '/default.png'

        # ------Save Image-------

        new.save()

    return render(request, 'myapp/addproduct.html')


def Product(request):
    product = Allproduct.objects.all().order_by(
        'id').reverse()  # ແມ່ນການດຶງຂໍ້ມູນມາທັງໝົດ
    paginator = Paginator(product, 3)  # 1 ໜ້າໂຊວ 15 ອັນ
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product}
    return render(request, 'myapp/allproduct.html', context)


def ProductCatagory(request, code):
    select = Catagory.objects.get(id=code)
    product = Allproduct.objects.filter(catagoryname=select).order_by(
        'id').reverse()  # ແມ່ນການດຶງຂໍ້ມູນມາທັງໝົດ
    paginator = Paginator(product, 3)  # 1 ໜ້າໂຊວ 15 ອັນ
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product, 'catagoryname': select.catagoryname}
    return render(request, 'myapp/allproductcat.html', context)


def Register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        # ຍັງບໍ່ໄດ່ໃສ່ try except ເພື່ອປ້ອງກັນການສະໝັກຊ້ຳ
        # + alert ໄປໜ້າສະໝັກວ່າອີເມລ໌ນີ້ເຄີຍສະໝັກແລ້ວ
        # ສອນ ຄູ່ກັບຫົວຂໍ້ reset password

        newuser = User()
        newuser.username = email
        newuser.email = email
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.set_password(password)
        newuser.save()

        profile = Profile()
        profile.user = User.objects.get(username=email)
        profile.save()

        # ----------send email for verify------- *****<<<testing>>>
        token, token_code = GenerateToken()
        EmailConfirm(email, first_name, token)
        getuser = User.objects.get(username=email)
        addverify = VerifyEmail()
        addverify.user = getuser
        addverify.token = token_code
        addverify.save()

        sendthai(email, subject, msg)

        # from django.contrib.auth import authenticate, login
        user = authenticate(username=email, password=password)
        login(request, user)

    return render(request, 'myapp/register.html')


# localhost:8000/addtocart/3 = {% url 'addcart-page' pd.id %}
def AddtoCart(request, pid):
    print('CURRENT USER:', request.user)
    username = request.user.username
    user = User.objects.get(username=username)
    check = Allproduct.objects.get(id=pid)

    try:
        # ກໍລະນີທີ່ສິນຄ້າມີຊ້ຳ
        newcart = Cart.objects.get(user=user, productid=str(pid))
        #print('EXISTS: ', pcheck.exists())
        newquan = newcart.quantity + 1
        newcart.quantity = newquan
        calculate = newcart.price * newquan
        newcart.total = calculate
        newcart.save()

        # update ຈຳນວນຂອງກະຕ່າສິນຄ້າ ໃນຕອນນີ້
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

        return redirect('allproduct-page')
    except:
        newcart = Cart()
        newcart.user = user
        newcart.productid = pid
        newcart.productname = check.name
        newcart.price = int(check.price)
        newcart.quantity = 1
        calculate = int(check.price) * 1
        newcart.total = calculate
        newcart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

        return redirect('allproduct-page')


def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if request.method == 'POST':  # ใຊ້ສຳຫຼັບການລົບເທົ່ານັ້ນ
        data = request.POST.copy()
        productid = data.get('productid')
        print('PID', productid)
        item = Cart.objects.get(user=user, productid=productid)
        item.delete()
        context['status'] = 'delete'

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

    mycart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in mycart])
    total = sum([c.total for c in mycart])

    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total

    return render(request, 'myapp/mycart.html', context)


def MyCartEdit(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        # print(data)
        if data.get('clear') == 'clear':
            print(data.get('clear'))
            Cart.objects.filter(user=user).delete()
            updatequan = Profile.objects.get(user=user)
            updatequan.cartquan = 0
            updatequan.save()
            return redirect('mycart-page')

        editList = []
        for k, v in data.items():
            # print([k,v])
            # pv_16
            if k[:2] == 'pd':
                pid = int(k.split('_')[1])
                dt = [pid, int(v)]
                editList.append(dt)
        # print('EDITLIST:',editList) # [[17,10],[16,12]] 9=productid, 10=quantity

        for ed in editList:
            edit = Cart.objects.get(productid=ed[0], user=user)  # productid
            edit.quantity = ed[1]  # quantity
            calculate = edit.price * ed[1]
            edit.total = calculate
            edit.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()
        return redirect('mycart-page')

        '''if data.get('checksave') == 'checksave':
		return redirect('mycart-page')'''

    mycart = Cart.objects.filter(user=user)
    context['mycart'] = mycart
    return render(request, 'myapp/mycartedit.html', context)


def Checkout(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        tel = data.get('tel')
        address = data.get('address')
        shipping = data.get('shipping')
        payment = data.get('payment')
        other = data.get('other')
        page = data.get('page')
        if page == 'information':
            context = {}
            context['name'] = name
            context['tel'] = tel
            context['address'] = address
            context['shipping'] = shipping
            context['payment'] = payment
            context['other'] = other

            mycart = Cart.objects.filter(user=user)
            count = sum([c.quantity for c in mycart])
            total = sum([c.total for c in mycart])

            context['mycart'] = mycart
            context['count'] = count
            context['total'] = total

            return render(request, 'myapp/checkout2.html', context)

        if page == 'confirm':
            print('Cofirm')
            print(data)
            mycart = Cart.objects.filter(user=user)

            mid = str(user.id).zfill(4)
            dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
            orderid = 'OD' + mid + dateTime
            productorder = ''
            producttotal = 0

            for pd in mycart:
                order = OrderList()
                order.orderid = orderid
                order.productid = pd.productid
                order.productname = pd.productname
                order.price = pd.price
                order.quantity = pd.quantity
                order.total = pd.total
                order.save()
                productorder += '- {}\n'.format(pd.productname)
                producttotal += pd.total

            # Send to LINE Notify in Croup
            texttoline = 'ເລກຂົນສົ່ງ : {}\n---\n{}ຍອດລວມ : {:,.2f} ກີບ\n ({})'.format(
                orderid, productorder, producttotal, name)
            if producttotal > 500000:  # ເຊັກຍອດສິນຄ້າຫຼາຍກວ່າ 3500000
                messenger.sticker(4, 1, texttoline)
            else:
                messenger.sendtext(texttoline)

            orderPending = OrderPending()  # create order pending
            orderPending.orderid = orderid
            orderPending.user = user
            orderPending.name = name
            orderPending.tel = tel
            orderPending.address = address
            orderPending.shipping = shipping
            orderPending.payment = payment
            orderPending.other = other
            orderPending.save()

            # clear cart
            Cart.objects.filter(user=user).delete()
            updatequan = Profile.objects.get(user=user)
            updatequan.cartquan = 0
            updatequan.save()
            return redirect('mycart-page')

    return render(request, 'myapp/checkout1.html')


def OrderlistPage(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    order = OrderPending.objects.filter(user=user)

    '''
	- order
		- oderid : 0012134
		- user : 
		- name : ຜູ້ຮັບ

	'''

    for od in order:
        orderid = od.orderid
        odlist = OrderList.objects.filter(orderid=orderid)
        '''
	- orderlist
		- object (1)
			- orderid : D121313
			- product : iPhone
			- total : 500000
		- object (2)
			- orderid : D121313
			- product : iPad
			- total : 500000
		- object (3)
			- orderid : D121313
			- product : iWatch
			- total : 500000
		- object (4)
			- orderid : D121314
			- product : iMac
			- total : 500000

		'''
        total = sum([c.total for c in odlist])
        # total = sum([, 3000000, 1200000])
        od.total = total
        # ສັ່ງນັບວ່າ order ນີ້ມຈຳນວນຈັກອັນ
        # ສັ່ງນັບວ່າ order ນີ້ມີຈຳນວນຈັກອັນ
        count = sum([c.quantity for c in odlist])

        if od.shipping == 'ems':
            shipcost = sum([6000 if i == 0 else 4000 for i in range(count)])
        else:
            shipcost = sum([7000 if i == 0 else 3000 for i in range(count)])

        if od.payment == 'cod':
            shipcost += 2000  # shipcost = shipcost + 2000
        od.shipcost = shipcost

    paginator = Paginator(order, 6)  # 1 ໜ້າໂຊວ 15 ອັນ
    page = request.GET.get('page')
    order = paginator.get_page(page)
    context['allorder'] = order

    return render(request, 'myapp/orderlist.html', context)


def AllOrderlistPage(request):
    context = {}
    order = OrderPending.objects.all()

    for od in order:
        orderid = od.orderid
        odlist = OrderList.objects.filter(orderid=orderid)
        total = sum([c.total for c in odlist])
        od.total = total

        # ສັ່ງນັບວ່າ order ນີ້ມີຈຳນວນຈັກອັນ
        count = sum([c.quantity for c in odlist])

        if od.shipping == 'ems':
            shipcost = sum([6000 if i == 0 else 6000 for i in range(count)])
        else:
            shipcost = sum([7000 if i == 0 else 5000 for i in range(count)])

        if od.payment == 'cod':
            shipcost += 3000  # shipcost = shipcost + 2000
        od.shipcost = shipcost

    paginator = Paginator(order, 6)  # 1 ໜ້າໂຊວ 15 ອັນ
    page = request.GET.get('page')
    order = paginator.get_page(page)
    context['allorder'] = order

    return render(request, 'myapp/allorderlist.html', context)


def UploadSlip(request, orderid):
    print('ORDER ID:', orderid)

    if request.method == 'POST' and request.FILES['slip']:
        data = request.POST.copy()
        sliptime = data.get('sliptime')

        update = OrderPending.objects.get(orderid=orderid)
        update.sliptime = sliptime

        file_image = request.FILES['slip']
        file_image_name = request.FILES['slip'].name.replace(' ', '')
        print('FILE_iMAGE:', file_image)
        print('IMAGE_NAME:', file_image_name)
        fs = FileSystemStorage()
        filename = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(filename)
        update.slip = upload_file_url[6:]
        update.save()

    odlist = OrderList.objects.filter(orderid=orderid)
    total = sum([c.total for c in odlist])
    oddetail = OrderPending.objects.get(orderid=orderid)

    count = sum([c.quantity for c in odlist])  # ຄຳນວນຄ່າຂົນສົ່ງຕາມປະເພດການສົ່ງ
    if oddetail.shipping == 'ems':
        shipcost = sum([6000 if i == 0 else 4000 for i in range(count)])
    else:
        shipcost = sum([7000 if i == 0 else 3000 for i in range(count)])

    if oddetail.payment == 'cod':
        shipcost += 2000  # shipcost = shipcost + 2000

    context = {'orderid': orderid,
               'total': total,
               'shipcost': shipcost,
               'grandtotal': total + shipcost,
               'oddetail': oddetail,
               'count': count}

    return render(request, 'myapp/uploadslip.html', context)


def UpdatePaid(request, orderid, status):

    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    order = OrderPending.objects.get(orderid=orderid)
    if status == 'confirm':
        order.paid = True
        order.confirmed = True
        odlist = OrderList.objects.filter(orderid=orderid)
        for od in odlist:
            product = Allproduct.objects.get(id=od.productid)
            product.quantity = product.quantity - od.quantity
            product.save()

    elif status == 'cancel':
        order.paid = False
        order.confirmed = False
    order.save()
    return redirect('allorderlist-page')


def UpdateTracking(request, orderid):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    if request.method == 'POST':
        order = OrderPending.objects.get(orderid=orderid)
        data = request.POST.copy()
        trackingnumber = data.get('trackingnumber')
        order.trackingnumber = trackingnumber
        order.save()
        return redirect('allorderlist-page')

    order = OrderPending.objects.get(orderid=orderid)
    odlist = OrderList.objects.filter(orderid=orderid)
    total = sum([c.total for c in odlist])
    order.total = total

    # ສັ່ງນັບວ່າ order ນີ້ມີຈຳນວນຈັກອັນ
    count = sum([c.quantity for c in odlist])

    if order.shipping == 'ems':
        shipcost = sum([6000 if i == 0 else 4000 for i in range(count)])
    else:
        shipcost = sum([7000 if i == 0 else 3000 for i in range(count)])

    if order.payment == 'cod':
        shipcost += 2000  # shipcost = shipcost + 2000
    order.shipcost = shipcost

    context = {'order': order, 'odlist': odlist,
               'total': total, 'count': count}

    return render(request, 'myapp/updatetracking.html', context)


def MyOrder(request, orderid):
    username = request.user.username
    user = User.objects.get(username=username)

    order = OrderPending.objects.get(orderid=orderid)
    # ກວດສອບວ່າເປັນຂອງໂຕເອງບໍ
    if user != order.user:
        return redirect('allproduct-page')

    odlist = OrderList.objects.filter(orderid=orderid)
    total = sum([c.total for c in odlist])
    order.total = total

    # ສັ່ງນັບວ່າ order ນີ້ມີຈຳນວນຈັກອັນ
    count = sum([c.quantity for c in odlist])

    if order.shipping == 'ems':
        shipcost = sum([6000 if i == 0 else 4000 for i in range(count)])
    else:
        shipcost = sum([7000 if i == 0 else 3000 for i in range(count)])

    if order.payment == 'cod':
        shipcost += 2000  # shipcost = shipcost + 2000
    order.shipcost = shipcost

    context = {'order': order, 'odlist': odlist,
               'total': total, 'count': count}

    return render(request, 'myapp/myorder.html', context)


def ProductDetail(request, productid):
    # localhost:8000/product/10
    product = Allproduct.objects.get(id=productid)
    context = {'product': product}
    return render(request, 'myapp/productdetail.html', context)


@login_required
def EditProduct(request, productid):
    # localhost:8000/editproduct/10
    check = CheckNotAdmin(request)
    print('CHECK:', check)
    if check:
        return redirect('home-page')

    product = Allproduct.objects.get(id=productid)
    catagory = Catagory.objects.all()

    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')
        cat = data.get('catagory')
        cat = Catagory.objects.get(catagoryname=cat)
        instock = data.get('instock')

        product.name = name
        product.price = price
        product.detail = detail
        product.imageurl = imageurl
        product.quantity = quantity
        product.unit = unit
        product.catagoryname = cat

        if instock == 'instock_true':
            product.instock = True
        else:
            product.instock = False

        # ------Save Image-------
        # print('FILES:', [request.FILES])
        if 'imageupload' in request.FILES:
            file_image = request.FILES['imageupload']
            file_image_name = request.FILES['imageupload'].name.replace(' ', '')
            # print('FILE_iMAGE:', file_image)
            # print('IMAGE_NAME:', file_image_name)
            fs = FileSystemStorage()
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            product.image = upload_file_url[6:]
        else:
            print('NO')

        product.save()

    product = Allproduct.objects.get(id=productid)
    context = {'product': product, 'catagory': catagory}
    return render(request, 'myapp/editproduct.html', context)


def AllproductAPI(request):
    allproduct = Allproduct.objects.all()
    serializer = AllProductSerializer(allproduct, many=True)
    return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


def ProductDetailAPI(request, pid):
    allproduct = Allproduct.objects.get(id=pid)
    serializer = AllProductSerializer(allproduct)
    return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False})


@api_view(['GET'])
def api_get_product(request, pid):
    product = Allproduct.objects.get(id=pid)
    if request.method == 'GET':
        serializer = AllProductSerializer(product)
        return Response(serializer.data)


@api_view(['POST'])
def api_post_product(request):
    if request.method == 'POST':
        serializer = AllProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def api_update_product(request, pid):
    if request.method == 'PUT':
        product = Allproduct.objects.get(id=pid)
        serializer = AllProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['message'] = 'Update information'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def api_delete_product(request, pid):
    if request.method == 'DELETE':
        product = Allproduct.objects.get(id=pid)
        deleted = product.delete()
        data = {}
        if deleted:
            data['message'] = 'was already deleted'
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data['message'] = 'was not deleted'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


text = '''
[My Facebook](https://www.facebook.com/)
# Product from my store
**Premium** product from my store
*fast sell from our*
'''


def TestMd(request):
    print(md.markdown(text, extensions=['markdown.extensions.fenced_code']))
    context = {'text': text}
    return render(request, 'myapp/testmd.html', context)
