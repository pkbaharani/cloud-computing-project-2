from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse
# from django.utils import simplejson
from django.core import mail, serializers
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from datetime import datetime
from time import time
from .cloud_vision import validate_image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from google.cloud import storage
from django.conf import settings

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
# from .models import Users
from .models import GeneralFound as general
from .models import SensitiveFound
from .models import SensitiveLost
from .models import GeneralLost

# import cloudstorage


# Create your views here.
sender_id = 'sun.devils.lost.found@gmail.com'
# -instances=<cc2databse>=tcp:1433 -cloudcomputing-2-1199e18857f7.json
# google creds

def home(request):
    return HttpResponse(
        '<h1> Lost and Found Home. You can \n search lost item \n report any item found \n search sensitive item </h1>')


def obscene_detection(image):
    return validate_image(image, False)


@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(request, 'lostfound/signup.html')
    else:
        # user=User()
        username = request.POST["username"]
        password = request.POST['password']
        emailid = request.POST['emailid']

        # checking if user is already preesnt
        userCount = User.objects.filter(username=username).count()
        userCount_email = User.objects.filter(email=emailid).count()

        if userCount > 0 or userCount_email > 0:
            return render(request, 'lostfound/signup.html',
                          {"error_message": "Username or password is invalid", "message_error": True})
        # adding user to the table Users
        user = User.objects.create_user(username, emailid, password)
        # Users.add_to_class(username,emailid,password)
        print("User saved")

        return render(request, 'lostfound/signup.html', {"message": "regsitered", "message_error": False})


def get_timestamp():
    timestamp = int(time())

    # Give a format to the date
    # Displays something like: Aug. 27, 2017, 2:57 p.m.
    # formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp)
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return timestamp, date


def uploadgcp(image, username):
    #credentials = ServiceAccountCredentials.from_json_keyfile_dict(   gcreds)

    imagename = username + str(get_timestamp())
    # client = storage.Client(credentials=credentials,project='cloudcomputing-2')
    # client= storage.Client.from_service_account_json('creds.json')
    client = storage.Client()
    bucket = client.get_bucket('cc2-image-db')
    blob = bucket.blob(imagename, chunk_size=262144)
    '''
    with open("D:\\All Softwares Installation\\djtest\djtest1\\lostfound\\uploadimage.jpg", 'rb') as photo:
        blob.upload_from_file(image)
    '''
    blob.upload_from_file(image)
    url = blob.public_url
    print(url)
    return url
    # we need to now put this post details in sql


# cloud_sql_proxy.exe -instances=<cc2databse>=tcp:1433 -cloudcomputing-2-1199e18857f7.json

@csrf_exempt
def post_sensitive_item(request):
    username = request.user.username
    # userCount = Users.objects.filter(username=username).count()

    # if userCount < 1:

    # import pdb; pdb.set_trace()

    if not request.user.is_authenticated:
        return 1, "username not registered"
    sensitive = SensitiveFound()
    timestamp, date = get_timestamp()
    cardtype = request.POST['cardtype']
    print('saving row')
    description = request.POST['description']
    campuslocation = request.POST['campusSelect']
    address = request.POST['address']
    last_four_digit = request.POST['lastfourdigit']
    postid = 'foundsensitive-' + username + '-' + str(timestamp)

    title = request.POST['title']
    lost_found_date = request.POST['lost_found_date']
    sensitive.title = title
    sensitive.lost_found_date = lost_found_date

    sensitive.campuslocation = campuslocation
    sensitive.address = address
    sensitive.description = description
    sensitive.user = request.user
    sensitive.cardtype = cardtype
    sensitive.fourdigit = last_four_digit
    sensitive.timestamp = date
    color = ''
    if 'color' in request.POST:
        color = request.POST['color']
    else:
        color = 'NA'
    sensitive.color = color
    sensitive.postid = postid
    sensitive.displayflag = True
    sensitive.save()
    # to send email to both the parties if there is a match.
    check_sensitive_lost_repo(cardtype, campuslocation, color, last_four_digit, request.user, postid)

    return 0, "post successful"


@csrf_exempt
def post_lost_general_item(request):
    timestamp, date = get_timestamp()
    itemtype = request.POST['categorySelect']

    description = request.POST['description']
    campuslocation = request.POST['campusSelect']
    address = request.POST['address']
    title = request.POST['title']
    lost_found_date = request.POST['lost_found_date']
    username = request.user.username
    image = request.FILES['image']
    # userCount = Users.objects.filter(username=username).count()

    # if userCount < 1:
    if not request.user.is_authenticated:
        return 1, "username not registered"

    postid = 'lostgeneral-' + username + '-' + str(timestamp)
    lost_gen_item = GeneralLost()
    lost_gen_item.user = request.user
    lost_gen_item.description = description
    lost_gen_item.campuslocation = campuslocation
    lost_gen_item.itemtype = itemtype
    lost_gen_item.timestamp = date
    lost_gen_item.address = address
    lost_gen_item.title = title
    lost_gen_item.lost_found_date = lost_found_date

    url = ""
    if image != None:
        #flag = obscene_detection(image.file)
        #if flag == True:
        #    return 1, 'post unsuccessful'
        url = str(uploadgcp(image, username))

    lost_gen_item.imagelink = url
    lost_gen_item.postid = postid
    lost_gen_item.save()

    return 0, 'post successful'


@csrf_exempt
def post_general_item(request):
    timestamp, date = get_timestamp()
    itemtype = request.POST['categorySelect']
    description = request.POST['description']
    title = request.POST['title']
    lost_found_date = request.POST['lost_found_date']
    campuslocation = request.POST['campusSelect']
    address = request.POST['address']
    username = request.user.username

    image = request.FILES['image']
    # userCount = Users.objects.filter(username=username).count()
    # import pdb; pdb.set_trace()
    if not request.user.is_authenticated:
        return 1, "username not registered"

    postid = 'foundgeneral-' + username + '-' + str(timestamp)
    url = ""
    if image != None:
        # flag = obscene_detection(image.file)
        # if flag == True:
        #    return 1, 'post unsuccessful'
        url = str(uploadgcp(image, username))

    gen_item = general()
    gen_item.user = request.user
    gen_item.description = description
    gen_item.campuslocation = campuslocation
    gen_item.itemtype = itemtype
    gen_item.imagelink = url
    gen_item.timestamp = date
    gen_item.address = address
    gen_item.postid = postid
    gen_item.title = title
    gen_item.lost_found_date = lost_found_date

    gen_item.save()

    return 0, "post successful"


def validatecred(request):
    username = request.POST['username']
    password = request.POST['password']
    print('username is ', username, ' password is ', password)
    user = User.objects.filter(username=username)
    if len(user) == 0:
        return None

    user = User.objects.filter(username=username)
    print(user[0].password)
    if password != user[0].password:
        return None
    return user[0]


@csrf_exempt
def post_lost_sensitive_item(request):
    timestamp, date = get_timestamp()
    username = request.user.username
    # userCount = Users.objects.filter(username=username).count()

    # if userCount < 1:
    if not request.user.is_authenticated:
        return 1, 'username not registered'
    postid = 'lostsensitive-' + username + '-' + str(timestamp)

    # sensitive = SensitiveFound()
    # color=request.POST['color']
    cardtype = request.POST['cardtype']
    title = request.POST['title']
    lost_found_date = request.POST['lost_found_date']
    description = request.POST['description']
    campuslocation = request.POST['campusSelect']
    address = request.POST['address']
    last_four_digit = request.POST['lastfourdigit']

    # check_sensitive_found_repo(cardtype=cardtype,campuslocation=campuslocation,color=color,lastfourdigit=last_four_digit)
    lost = SensitiveLost()

    lost.fourdigit = last_four_digit
    lost.user = request.user
    lost.campuslocation = campuslocation
    lost.address = address
    color = ''
    if 'color' in request.POST:
        color = request.POST['color']
    lost.cardtype = cardtype
    lost.description = description
    lost.timestamp = date
    lost.postid = postid
    lost.title = title
    lost.lost_found_date = lost_found_date

    print(username)
    lost.displayflag = True
    lost.save()
    print(username)
    print("saving the row")
    # to send email to both the parties if there is a match.
    check_sensitive_found_repo(cardtype, campuslocation, color, last_four_digit, request.user, postid)
    return 0, "Post successful"


"""
@csrf_exempt

def display_lost_general_items(request):
    # called when some one reports that their item has been lost
    itemtype = request.GET['itemtype']
    campuslocation = request.GET['campuslocation']

    print('looking into ',itemtype,'  campuslocation ',campuslocation)
    #color = request.GET['color']
    gen=GeneralLost.objects.filter(campuslocation=campuslocation,itemtype=itemtype).order_by('timestamp')
    print(gen)
    response={}
    result={}
    if len(gen)==0:
        return HttpResponse('<h1> No result found  </h1>')
    for i in range ( len(gen)) :
        result['username']=gen[i].username
        result['imagelink'] = gen[i].imagelink
        result['itemtype'] = gen[i].itemtype
        result['description'] = gen[i].description
        result['campuslocation'] = gen[i].campuslocation
        result['address'] = gen[i].address
        response[i]=result

    return JsonResponse(response)"""


@csrf_exempt
def post_found_item(request):
    if request.method == "GET":
        return render(request, 'lostfound/post_form.html')

    else:
        category = request.POST["categorySelect"]
        if category == "Sensitive items":
            err_status, err_message = post_sensitive_item(request)
        else:
            err_status, err_message = post_general_item(request)

        if err_status == 1:
            return render(request, 'lostfound/post_form.html', {"error_message": err_message})
        else:
            return render(request, 'lostfound/post_form.html', {"message": err_message})


@csrf_exempt
def post_lost_item(request):
    if request.method == "GET":
        return render(request, 'lostfound/post_form.html')

    else:
        category = request.POST["categorySelect"]
        if category == "Sensitive items":
            err_status, err_message = post_lost_sensitive_item(request)
        else:
            err_status, err_message = post_lost_general_item(request)

        if err_status == 1:
            return render(request, 'lostfound/post_form.html', {"error_message": err_message})
        else:
            return render(request, 'lostfound/post_form.html', {"message": err_message})


@csrf_exempt
def display_general_items(request):
    # called when some one reports that their item has been lost

    if request.method == "GET":
        gen = general.objects.all().order_by('timestamp')[:30]
        print("Return all items")
        return render(request, 'lostfound/found.html', {"search": gen, })
    else:

        itemtype = request.POST['itemtype']
        campuslocation = request.POST['campuslocation']

        print('looking into ', itemtype, '  campuslocation ', campuslocation)
        # color = request.GET['color']
        gen = general.objects.filter(campuslocation=campuslocation, itemtype=itemtype).order_by('timestamp')[:30]
        print(gen)
        response = {}
        search = []
        print("Return filtered items")
        """if len(gen)==0:
            return HttpResponse('<h1> No result found  </h1>')
        for i in range ( len(gen)) :
            result={}
            result['username']=gen[i].username
            result['imagelink'] = gen[i].imagelink
            result['itemtype'] = gen[i].itemtype
            result['description'] = gen[i].description
            result['campuslocation'] = gen[i].campuslocation
            search.append(result)"""

    return render(request, 'lostfound/found.html', {"search": gen, })


@csrf_exempt
def display_general_lost_items(request):
    # called when some one reports that their item has been lost

    if request.method == "GET":
        gen = GeneralLost.objects.all().order_by('timestamp')[:30]
        print(gen)
        print("Return all items")
        return render(request, 'lostfound/lost.html', {"search": gen, })
    else:

        itemtype = request.POST['itemtype']
        campuslocation = request.POST['campuslocation']

        print('looking into ', itemtype, '  campuslocation ', campuslocation)
        # color = request.GET['color']
        gen = GeneralLost.objects.filter(campuslocation=campuslocation, itemtype=itemtype).order_by('timestamp')[:30]
        print(gen)
        response = {}
        search = []
        print("Return filtered items")
        """if len(gen)==0:
            return HttpResponse('<h1> No result found  </h1>')
        for i in range ( len(gen)) :
            result={}
            result['username']=gen[i].username
            result['imagelink'] = gen[i].imagelink
            result['itemtype'] = gen[i].itemtype
            result['description'] = gen[i].description
            result['campuslocation'] = gen[i].campuslocation
            search.append(result)"""

    print(gen)
    return render(request, 'lostfound/found.html', {"search": gen, })


def send_notification(username1, username2, user1_emailid, user2_emailid, resolve, cardtype, campuslocation,
                      lastfourdigit):
    resolutionlink = '\n please use the link below to mark this post as resolved \n' + str(resolve)

    subject = 'SunDevils Lost n Found: Your item may have found a potential match'
    body = ' \n There was a potential match to your post for your {} with last 4 digits as {} found at {}, please contact user '.format(
        cardtype, lastfourdigit, campuslocation) + str(username2) + ' at ' + str(user2_emailid)
    body = 'Hello ' + str(username1) + body + ','
    body = body + resolutionlink
    body = body + ' \n Regards, \n Sun Devils Lost and Found'
    body = str(body)

    # receipient= user1_emailid
    send_mail(
        subject,
        body,
        'sun.devil.lost.found@gmail.com',
        [user1_emailid],
        fail_silently=False,
    )


def check_sensitive_found_repo(cardtype, campuslocation, color, lastfourdigit, lost_user, lost_postid):
    # called when some one reports that their item has been lost
    sensitivefound = SensitiveFound.objects.filter(cardtype=cardtype, campuslocation=campuslocation,
                                                   fourdigit=lastfourdigit)

    if len(sensitivefound) == 0:
        return None

    for i in range(len(sensitivefound)):
        found_user = sensitivefound[i].user
        found_postid = sensitivefound[i].postid

        print("sending email to both the parties i.e receiver1 who has found the item = ", found_user.username,
              " and receiver 2 who has lost the item", lost_user.username)

        lost_emailid = lost_user.email
        found_emailid = found_user.email

        resolvelink = "http://" + settings.HOST_URL + "/lostfound/resolve/?postid=" + str(lost_postid)
        send_notification(username1=lost_user.username, username2=found_user.username, user1_emailid=lost_user.email,
                          user2_emailid=found_user.email, resolve=resolvelink, cardtype=cardtype,
                          campuslocation=campuslocation, lastfourdigit=lastfourdigit)

        '''
        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username, '  at user 1 email id ', lost_emailid,
              ' and user 2  email id ', found_emailid)
        '''

        resolvelink = "http://" + settings.HOST_URL + "/lostfound/resolve/?postid=" + str(found_postid)
        send_notification(username1=found_user.username, username2=lost_user.username, user1_emailid=found_user.email,
                          user2_emailid=lost_user.email, resolve=resolvelink, cardtype=cardtype,
                          campuslocation=campuslocation, lastfourdigit=lastfourdigit)

    '''
    for i in range (len(sensitive)):
        receiver1=sensitive[i].username
        print("sending email to both the parties i.e receiver1 who has found the item = ",lost_username," and receiver 2 who has lost the item", receiver1)

        #print("sending email to both the parties",sensitive[i].username)
        # send email to the username of lost and found both

    '''


def check_sensitive_lost_repo(cardtype, campuslocation, color, lastfourdigit, found_user, found_postid):
    # called when some one reports a found item.
    lost = SensitiveLost.objects.filter(cardtype=cardtype, campuslocation=campuslocation,
                                        fourdigit=lastfourdigit)
    if len(lost) == 0:
        return None

    found_username = found_user.username

    for i in range(len(lost)):
        lost_user = lost[i].user
        lost_username = lost_user.username
        lost_postid = lost[i].postid

        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username)
        lost_emailid = lost_user.email
        found_emailid = found_user.email

        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username, '  at user 1 email id ', lost_emailid,
              ' and user 2  email id ', found_emailid)

        resolvelink = "http://" + settings.HOST_URL + "/lostfound/resolve/?postid=" + str(lost_postid)
        send_notification(username1=lost_username, username2=found_username, user1_emailid=lost_emailid,
                          user2_emailid=found_emailid, resolve=resolvelink, cardtype=cardtype,
                          campuslocation=campuslocation, lastfourdigit=lastfourdigit)

        resolvelink = "http://" + settings.HOST_URL + "/lostfound/resolve/?postid=" + str(found_postid)
        send_notification(username1=found_username, username2=lost_username, user1_emailid=found_emailid,
                          user2_emailid=lost_emailid, resolve=resolvelink, cardtype=cardtype,
                          campuslocation=campuslocation, lastfourdigit=lastfourdigit)

        # send email to the username of lost and found both


@csrf_exempt
def login_user(request):
    # display login page
    if request.method == "GET":
        return render(request, 'lostfound/login.html')
    else:

        username = request.POST["username"]
        passwd = request.POST["password"]

        # user = validatecred(request)
        user = authenticate(request, username=username, password=passwd)
        if user is None:
            return render(request, 'lostfound/login.html', {"username": request.POST["username"],
                                                            "password": request.POST["password"],
                                                            "error_message": "Username or password is invalid",
                                                            "message_error": True})

        login(request, user)
        return HttpResponseRedirect('/lostfound/homepage/')


@csrf_exempt
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/lostfound/login/')


def resolvePost(request):
    # import pdb;pdb.set_trace()
    post = request.GET['postid']
    requesttype = post.split("-")[0]
    print(post)
    table = None
    if requesttype == 'lostsensitive':
        table = SensitiveLost
    if requesttype == 'foundgeneral':
        table = general
    if requesttype == 'lostgeneral':
        table = GeneralLost
    if requesttype == 'foundsensitive':
        table = SensitiveFound

    tab = table.objects.get(postid=post)
    tab.displayflag = False
    tab.save()

    return HttpResponse('<h1> successfully updated table  </h1>')


@csrf_exempt
def homepage(request):
    return render(request, 'lostfound/homepage.html')


def found(request):
    return HttpResponse('<h1> Report anything that you have found </h1>')


def sensitive_search(request):
    return HttpResponse('<h1> This is sensitive search page  </h1>')


def search(request):
    return HttpResponse('<h1> This is search page </h1>')


@csrf_exempt
def get_sensitive_item(request):
    # function not required
    cardtype = request.GET['cardtype']
    campuslocation = request.GET['campuslocation']
    color = request.GET['color']
    fourdigit = request.GET['fourdigit']

    sensitive = SensitiveFound.objects.filter(cardtype=cardtype, campuslocation=campuslocation, color=color,
                                              fourdigit=fourdigit)

    if len(sensitive) == 0:
        return None
    pass


def filter_general_item():
    pass

