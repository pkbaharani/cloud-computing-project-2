from django.http import HttpResponse, HttpResponseRedirect
def base(request):
    return HttpResponseRedirect('/lostfound/login/')