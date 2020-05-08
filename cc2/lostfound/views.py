from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse
#from django.utils import simplejson
from django.core import mail, serializers
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from time import time



from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from .models import Users
from .models import GeneralFound as general
from .models import SensitiveFound
from .models import SensitiveLost
from .models import GeneralLost

# Create your views here.
sender_id='sun.devils.lost.found@gmail.com'
#-instances=<cc2databse>=tcp:1433 -cloudcomputing-2-1199e18857f7.json
#google creds
gcreds={
  "type": "service_account",
  "project_id": "cloudcomputing-2-275420",
  "private_key_id": "1199e18857f7bf5c89b414374b4581155228b34e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDg1D7cgNZu5dAi\nRQXy7hOKmv1x91L8bYQGAOvDWQ+XhYS7r/56+ZE55kK8yOu9so93nL3PljgHYact\nIGB/4uOk9mK/vWnpLeWAUjiH3a/N0pk7ZPEsPrZdDy7uFAFRGsq7h1veoiI1M8Vq\nDMF1UGApCvDN/unHyWoHuM3E4D+oZKd6+kQ7ZLG3Org6d2KSeNwRL8u6FHD+j3gh\nD9eEKAg/rnoG0bGTf8wBbXaQdVD27pD2VEg+YVAeen3/v4qkLGQ8kibuWHe1oyK7\nl8zzun6O4HzbxwUuIj+WxxFdyXF+wwfhL4+Nt9Y55l8/ZxtIsEo3Uuh4Hx+2EACK\nMonQ2VWdAgMBAAECggEADS7Mx8ujJyoA//1pmaK1kR9A5KWSn1wBjYOQz2nBtQn+\nbC3n30iSaCF1ANJMJlmZuXL+mzUs8FvcvFPlbKI+ZF4RELqXwvUuu402pNrOE+S5\nGOc0j/pWYZMCFrIkGKAYSpInhCCgHlv8g5kfX9RYaxep4n5DsXQBLFY89IIMoYA3\nQW0vkj2blhbfh+mQ1D13d5wnd6dPulqIMQdskQl7fLxADj4RUUTg/op8COUt8z0Z\n1Zo/ZbaPAWcovCzrBmn8Ug6iAy+zXBGgEL8TaR7If0UBi9RxtC+gn5KM1+7Ub60X\nCx8rhGxBMbI1WPDfSTWS/Vx5LVeuhIj10wKIk58JgQKBgQDz0sSJKjYS4m9u8+OH\nJ5p//Xx+Gy0/D+Wm7ti8ntie/BpJiBftZmqbMUT9/2zUqsZY0bhu0BIsaN91s5Gd\nNaWE4mrGWGDiU6kcWl8YYtKwedXi/vPqrc8XfZIRco5vjerhh4wd5ZO42xO7uSHI\nB5mDknKxbG+nBoHaKzuBXphvgQKBgQDsDqPzsrid0Z2gqSaJNLiSqoSDz7dal5d6\nMA8gmCD+KNUKTmKodPOY4JTBSgUMXc7HSyi3EyTfMcF2XPUJxcwGI2El34zbXVj/\negLRGWUS+rXGKJIuXJhR3zQjpPghgEo0F8V6HHkUVIUf7Op95tAdAM/9oeMkzE2F\nsCIL4i60HQKBgQCp1QiChj1t//0gao70aFiMiDM735AvmdIb6chb8cTvUKi6ySnp\neWoOOU5WIaFbrKxF16bAwPu3pUDpSi/GMkTdf5xiFdM+MonbrvMIGGWq+OJLn8yk\njXZvZU7mCkY+W7rcZr7pYCz6GNbw7i4il3CNned3wBExZS3zmiNzpEFHgQKBgQDS\nk9DgEbutVZPXAW4WEcjhVWn3J/I5x2diocKs4ej0sboygnByNDomU5l/wCc2u+w9\nTqfYgSRwUrNxgkU5XZC+nQsJvR2rht9gsBgZLh1DTBGh3wlggEuFJacecQjE4evQ\nArCwWPwODcPgEfmxLJjUdqgUazj016gELXaBwVjGZQKBgQDcaLKdLo84sU8qB9ZW\nmAH+mQZTIq/2aVwtgicrg3GaT0RXmbbmd9JhaZ/qK8Xb+LFmHPxf9Os08VR4gdXp\njqYh7umwzbanpwaG5OaORRJkPTCkeUoVp0Dv92mVpshesXVb7KksS8so/q/m07qv\nUQw/mWjux2FFfAMjgtUweh1Umg==\n-----END PRIVATE KEY-----\n",
  "client_email": "cc-storage@cloudcomputing-2-275420.iam.gserviceaccount.com",
  "client_id": "106354581183450467619",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cc-storage%40cloudcomputing-2-275420.iam.gserviceaccount.com"
}

def home(request):
    return HttpResponse('<h1> Lost and Found Home. You can \n search lost item \n report any item found \n search sensitive item </h1>')



@csrf_exempt
def register(request):

    print(request)
    user=Users()

    username = request.POST["username"]
    print(username)
    password = request.POST['password']
    emailid = request.POST['emailid']

    print("server error")
    # checking if user is already preesnt
    userCount = Users.objects.filter(username=username).count()
    userCount_email = Users.objects.filter(emailid=emailid).count()
    print("server error")
    if userCount >0 or userCount_email>0:
        return HttpResponse('<h1>provided user id or email is already registered, please login </h1>')

    #adding user to the table Users

    user.username=username
    user.password=password
    user.emailid=emailid
    print("server error")
    user.save()
    #Users.add_to_class(username,emailid,password)

    return HttpResponse('<h1> user successfully registered </h1>')


def get_timestamp():

    timestamp=int(time())

    # Give a format to the date
    # Displays something like: Aug. 27, 2017, 2:57 p.m.
    #formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    print (timestamp)
    return timestamp



def uploadgcp(image,username):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        gcreds
    )

    imagename=username+str(get_timestamp())
    client = storage.Client(credentials=credentials,project='cloudcomputing-2')
    bucket = client.get_bucket('cc2-image-db')
    blob = bucket.blob(imagename,chunk_size=262144)
    '''
    with open("D:\\All Softwares Installation\\djtest\djtest1\\lostfound\\uploadimage.jpg", 'rb') as photo:
        blob.upload_from_file(image)
    '''
    blob.upload_from_file(image)
    url = blob.public_url
    print (url)
    return url
    # we need to now put this post details in sql
#cloud_sql_proxy.exe -instances=<cc2databse>=tcp:1433 -cloudcomputing-2-1199e18857f7.json

@csrf_exempt
def post_sensitive_item(request):
    username = request.POST['username']
    userCount = Users.objects.filter(username=username).count()

    if userCount < 1:
        return HttpResponse('<h1> username not registered </h1>')
    sensitive = SensitiveFound()
    timestamp=get_timestamp()
    cardtype = request.POST['cardtype']
    print('saving row')
    description = request.POST['description']
    campuslocation = request.POST['campuslocation']
    address = request.POST['address']
    last_four_digit=request.POST['lastfourdigit']
    postid='foundsensitive-'+username+'-'+str(timestamp)
    sensitive.campuslocation=campuslocation
    sensitive.address=address
    sensitive.description=description
    sensitive.username=username
    sensitive.cardtype=cardtype
    sensitive.fourdigit=last_four_digit
    sensitive.timestamp=timestamp
    color=''
    if 'color' in request.POST:
        color=request.POST['color']
    else:
        color='NA'
    sensitive.color=color
    sensitive.postid=postid

    sensitive.save()
    # to send email to both the parties if there is a match.
    check_sensitive_lost_repo(cardtype,campuslocation,color,last_four_digit,username,postid)

    return HttpResponse('<h1> post successful </h1>')


@csrf_exempt
def post_lost_general_item(request):

    timestamp=get_timestamp()
    itemtype = request.POST['itemtype']
    description = request.POST['description']
    campuslocation = request.POST['campuslocation']
    address = request.POST['address']
    username = request.POST['username']
    image = request.FILES['image']
    userCount = Users.objects.filter(username=username).count()

    if userCount < 1:
        return HttpResponse('<h1> username not registered </h1>')


    postid='lostgeneral-'+username+'-'+str(timestamp)
    lost_gen_item = general()
    lost_gen_item.username = username
    lost_gen_item.description = description
    lost_gen_item.campuslocation = campuslocation
    lost_gen_item.itemtype = itemtype
    lost_gen_item.timestamp = timestamp
    lost_gen_item.address = address
    url=""
    if image != None:
        url = str(uploadgcp(image, username))
    lost_gen_item.imagelink = url
    lost_gen_item.postid=postid
    lost_gen_item.save()

    return HttpResponse('<h1> post successful </h1>')


@csrf_exempt
def post_general_item(request):

    timestamp=get_timestamp()
    itemtype=request.POST['itemtype']
    description=request.POST['description']
    campuslocation=request.POST['campuslocation']
    address=request.POST['address']
    username=request.POST['username']
    image = request.FILES['image']
    userCount = Users.objects.filter(username=username).count()

    if userCount <1 :
        return HttpResponse('<h1> username not registered </h1>')

    postid='foundgeneral-'+username+'-'+str(timestamp)
    url = str(uploadgcp(image,username))

    gen_item=general()
    gen_item.username=username
    gen_item.description=description
    gen_item.campuslocation=campuslocation
    gen_item.itemtype=itemtype
    gen_item.imagelink=url
    gen_item.timestamp=timestamp
    gen_item.address=address
    gen_item.postid=postid

    gen_item.save()

    return HttpResponse('<h1> post successful </h1>')

@csrf_exempt
def validatecred(request):

    username=request.GET['username']
    password=request.GET['password']
    print('username is ', username, ' password is ', password)
    user=Users.objects.filter(username=username)
    if len(user) ==0:
        return HttpResponse('<h1> No such user present </h1>')

    user=Users.objects.filter(username=username)
    print(user[0].password)
    if password != user[0].password:
        return HttpResponse('<h1> wrong password </h1>')
    return HttpResponse('<h1> Login was successful  </h1>')

@csrf_exempt
def post_lost_sensitive_item(request):

    timestamp=get_timestamp()
    username = request.POST['username']
    userCount = Users.objects.filter(username=username).count()

    if userCount < 1:
        return HttpResponse('<h1> username not registered </h1>')
    postid='lostsensitive-'+username+'-'+str(timestamp)

    #sensitive = SensitiveFound()
    color=request.POST['color']
    cardtype = request.POST['cardtype']
    description = request.POST['description']
    campuslocation = request.POST['campuslocation']
    address = request.POST['address']
    last_four_digit = request.POST['lastfourdigit']



    #check_sensitive_found_repo(cardtype=cardtype,campuslocation=campuslocation,color=color,lastfourdigit=last_four_digit)
    lost=SensitiveLost()

    lost.fourdigit=last_four_digit
    lost.username = username
    lost.campuslocation = campuslocation
    lost.address = address
    lost.color = color
    lost.cardtype = cardtype
    lost.description = description
    lost.timestamp = timestamp
    lost.postid=postid

    lost.save()
    print("saving the row")
    # to send email to both the parties if there is a match.
    check_sensitive_found_repo(cardtype, campuslocation, color, last_four_digit,username,postid)
    return HttpResponse('<h1> Post successful </h1>')


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

    return JsonResponse(response)

@csrf_exempt
def display_general_items(request):
    # called when some one reports that their item has been lost
    itemtype = request.GET['itemtype']
    campuslocation = request.GET['campuslocation']

    print('looking into ',itemtype,'  campuslocation ',campuslocation)
    #color = request.GET['color']
    gen=general.objects.filter(campuslocation=campuslocation,itemtype=itemtype).order_by('timestamp')
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
        response[i]=result

    return JsonResponse(response)

def send_notification(username1,username2,user1_emailid,user2_emailid,resolve):

    resolutionlink='\n please use the link below to mark this post as resolved \n'+str(resolve)

    subject='There was subscription made to your post'
    body=' \n There was a potential match to your post, please contact user '+str(username2)+' at '+str(user2_emailid)
    body='Hello '+str(username1)+body+','
    body=body+resolutionlink
    body=body+' \n Regards, \n Sun Devils Lost and Found'
    body=str(body)

    #receipient= user1_emailid
    send_mail(
        subject,
        body,
        'sun.devil.lost.found@gmail.com',
        ['prateek.baharani25@gmail.com'],
        fail_silently=False,
    )
def check_sensitive_found_repo(cardtype,campuslocation,color,lastfourdigit,lost_username,lost_postid):
    # called when some one reports that their item has been lost
    sensitivefound = SensitiveFound.objects.filter(cardtype=cardtype, campuslocation=campuslocation,
                                              fourdigit=lastfourdigit)

    if len(sensitivefound) == 0:
        return None

    for i in range(len(sensitivefound)):
        found_username = sensitivefound[i].username
        found_postid =sensitivefound[i].postid

        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username)


        lost_emailid = Users.objects.filter(username=lost_username)[0].emailid
        found_emailid = Users.objects.filter(username=found_username)[0].emailid

        resolvelink = 'http://127.0.0.1:8000/lostfound/resolve/?postid='+str(lost_postid)
        send_notification(username1=lost_username, username2=found_username, user1_emailid=lost_emailid,
                          user2_emailid=found_emailid, resolve=resolvelink)

        '''
        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username, '  at user 1 email id ', lost_emailid,
              ' and user 2  email id ', found_emailid)
        '''

        resolvelink = 'http://127.0.0.1:8000/lostfound/resolve/?postid='+str(found_postid)
        send_notification(username1=found_username, username2=lost_username, user1_emailid=found_emailid,
                          user2_emailid=lost_emailid, resolve=resolvelink)


    '''
    for i in range (len(sensitive)):
        receiver1=sensitive[i].username
        print("sending email to both the parties i.e receiver1 who has found the item = ",lost_username," and receiver 2 who has lost the item", receiver1)

        #print("sending email to both the parties",sensitive[i].username)
        # send email to the username of lost and found both

    '''


def check_sensitive_lost_repo(cardtype,campuslocation,color,lastfourdigit,found_username,found_postid):
    # called when some one reports a found item.
    lost=SensitiveLost.objects.filter(cardtype=cardtype, campuslocation=campuslocation,
                                              fourdigit=lastfourdigit)
    if len(lost) == 0:
        return None

    for i in range(len(lost)):
        lost_username=lost[i].username
        lost_postid=lost[i].postid

        print("sending email to both the parties i.e receiver1 who has found the item = ",found_username," and receiver 2 who has lost the item", lost_username)
        lost_emailid=Users.objects.filter(username=lost_username)[0].emailid
        found_emailid=Users.objects.filter(username=found_username)[0].emailid

        print("sending email to both the parties i.e receiver1 who has found the item = ", found_username,
              " and receiver 2 who has lost the item", lost_username,'  at user 1 email id ',lost_emailid, ' and user 2  email id ',found_emailid )

        resolvelink = 'http://127.0.0.1:8000/lostfound/resolve/?postid='+str(lost_postid)
        send_notification(username1= lost_username,username2=found_username,user1_emailid=lost_emailid,user2_emailid=found_emailid,resolve=resolvelink)

        resolvelink = 'http://127.0.0.1:8000/lostfound/resolve/?postid='+str(found_postid)
        send_notification(username1=found_username, username2=lost_username, user1_emailid=found_emailid,user2_emailid=lost_emailid,resolve=resolvelink)


        # send email to the username of lost and found both

@csrf_exempt
def login(request):
    #display login page
    return render(request,'lostfound/login.html')


def resolvePost(request):
    post=request.GET['postid']
    requesttype=post.split("-")[0]
    print(post)
    table=None
    if requesttype == 'lostsensitive':
        table= SensitiveLost()
    if requesttype == 'foundgeneral' :
        table= general()
    if requesttype =='lostgeneral'  :
        table=GeneralLost()
    if requesttype == 'foundsensitive':
        table= SensitiveFound()

    #table.objects.filter(postid=post)[0].update(displayflag=False)
    return HttpResponse('<h1> successfully updated table  </h1>')

def found(request):
    return HttpResponse('<h1> Report anything that you have found </h1>')

def sensitive_search(request):
    return HttpResponse('<h1> This is sensitive search page  </h1>')


def search(request):
    return HttpResponse('<h1> This is search page </h1>')


@csrf_exempt
def get_sensitive_item(request):
    # function not required
    cardtype=request.GET['cardtype']
    campuslocation=request.GET['campuslocation']
    color=request.GET['color']
    fourdigit=request.GET['fourdigit']

    sensitive=SensitiveFound.objects.filter(cardtype=cardtype,campuslocation=campuslocation,color=color,fourdigit=fourdigit)

    if len(sensitive) == 0:
        return None
    pass

def filter_general_item():
    pass

