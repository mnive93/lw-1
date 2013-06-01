from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from invites.forms import InviteForm
from django.core.urlresolvers import reverse
from invites.models import InviteEmails
from main.models import SignupHandler
from pyfb import Pyfb

import tweepy
import random
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

numberofemails = InviteEmails.objects.count()
numberleft = locale.format('%d', 2500 - numberofemails, grouping = True)

def landing(request):
    form = InviteForm()
        
    var = RequestContext(request, {
        'form':form,
        'number':numberleft
    })
    
    return render_to_response('invites/landing.html', var)

def emailInstanceCreate(email, fb=False, twitter=False):
    randomnumber = random.randint(0,100000)
    emailadd = InviteEmails.objects.create(emailaddress = email, id=numberofemails+1)
    signuphandle = SignupHandler.objects.create(emailaddress = email, identifiernum = randomnumber)

def processInviteRequest(request):
    if request.method=='POST':
        form = InviteForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['emailaddress']
            try:
                emailadd = InviteEmails.objects.get(emailaddress = email)
            except ObjectDoesNotExist:
                emailInstanceCreate(email)
                emailadd = InviteEmails.objects.get(emailaddress = email)
                return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'success'}))
            return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'existing'}))
        return HttpResponse('Error.')
    else:
        return HttpResponseRedirect('/')

def auth(request):
    oauth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)

    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)

    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret) 
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    oauth.set_request_token(token[0], token[1])
    # get the access token and store
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key
    request.session['access_secret_tw'] = oauth.access_token.secret

    emailInstanceCreate(authorized_tokens['email'])

    response = HttpResponseRedirect('/result/')
    return response

def check_key(request):
    """
    Check to see if we already have an access_key stored, if we do then we have already gone through 
    OAuth. If not then we haven't and we probably need to.
    """
    try:
        access_key = request.session.get('access_key_tw', None)
        if not access_key:
            return False
    except KeyError:
        return False
    return True

def info(request):
    if check_key(request):
        api = get_api(request)
        user = api.me()
        return render_to_response('invites/twttr.html', {'user' : user})
    else:
        return HttpResponseRedirect(reverse('main'))

def facebook_login(request):
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=settings.FACEBOOK_REDIRECT_URL))

def facebook_login_success(request):
    code = request.GET.get('code')    
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    facebook.get_access_token(settings.FACEBOOK_SECRET_KEY, code, redirect_uri=settings.FACEBOOK_REDIRECT_URL)
    me = facebook.get_myself()

    try:
        email = InviteEmails.objects.get(emailaddress = me.email)
    except ObjectDoesNotExist:
        emailInstanceCreate(me.email)
        email = InviteEmails.objects.get(emailaddress = me.email)

        return render_to_response('invites/result.html', RequestContext(request, {'email':email, 'result':'success'}))
    return render_to_response('invites/result.html', RequestContext(request, {'email':email, 'result':'existing'}))