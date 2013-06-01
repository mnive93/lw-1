from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from main.models import *
from main.forms import *
import random
import datetime

# The following view function, lr, is to redirect an unauthenticated user to the home page if he tries to access a page, say Settings or Feed, that requires
# authentication. The one that follows that, nlr does the opposite of the lr function. If a logged in user tries to access a page that can be accessed only
# when logged out, such as the signup page or the landing page, he will be redirected to the feed page URL.

def lr(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/landing')
        return view(request, *args, **kwargs)
    return new_view

def nlr(view):
    def new_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/feed/')
        return view(request, *args, **kwargs)
    return new_view

def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)
    
def hello(request):
    if request.method=='POST':
        form = SignupFormA(request.POST)
        
        if form.is_valid():
            try:
                existingemail = SignupHandler.objects.get(emailaddress = form.cleaned_data['email'])
            except ObjectDoesNotExist:
                randomnumber = random.randint(0,100000)
                handlesignup = SignupHandler.objects.create(
                    emailaddress = form.cleaned_data['email'],
                    identifiernum = randomnumber
                )
                return HttpResponseRedirect('/signup/%s' % str(randomnumber))
            return HttpResponseRedirect('/signup/%s' % str(existingemail.identifiernum))
    else:
        form = SignupFormA()
    
    var = RequestContext(request, {
        'form':form
    })
    
    return render_to_response('registration/landing.html', var)

def signup(request, randnum):
    randomnumber = int(randnum)
    email = SignupHandler.objects.get(identifiernum = randomnumber).emailaddress
    
    if request.method == 'POST':
        form = SignupFormB(request.POST)
        
        if form.is_valid():
            splitname = form.cleaned_data['fullname'].split()
            firstname = splitname[0]
            lastname = ''
            
            for s in splitname[1:]:
                lastname += (s+' ')
            
            User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = email,
                first_name = firstname,
                last_name = lastname.strip()
            )
            
            return HttpResponseRedirect('/login/')
    else:
        form = SignupFormB()
        
    var = RequestContext(request, {
        'form':form,
        'email':email
    })
    
    return render_to_response('registration/signup.html', var)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/landing/')
    
def feed(request):        
    var = RequestContext(request, {
        'user':request.user,
    })
    
    return render_to_response('pages/feed.html', var)

def posting(request):
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            post = Posts.objects.create(user = request.user, text = form.cleaned_data['text'], time = datetime.datetime.now(), randomnumber = random.randint(0,100000))
    else:
        form = PostingForm()
        
    var = RequestContext(request, {
        'form':form
    })
    
    return render_to_response('includes/posting.html', var)
    
def profilepage(request, username):
    try:
        user = User.objects.get(username = username)
    except ObjectDoesNotExist:
        raise Http404()
    
    posts = Posts.objects.filter(user = user)
    
    var = RequestContext(request, {
        'username':user.username,
        'email':user.email,
        'fullname':user.get_full_name(),
        'posts':posts
    })
    
    return render_to_response('pages/profile.html', var)