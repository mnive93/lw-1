from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from invites.forms import InviteForm
from django.core.urlresolvers import reverse
from invites.models import InviteEmails, TwitterEmails
from main.models import SignupHandler
from twython import Twython

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

def emailInstanceCreate(email):
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

def beginTwitterAuth(request):
	"""
		The view function that initiates the entire handshake.
		For the most part, this is 100% drag and drop.
	"""
	# Instantiate Twython with the first leg of our trip.
	twitter = Twython(
		app_key = settings.APP_KEY,
		app_secret = settings.APP_SECRET,
        callback_url = 'http://localhost/result/'
	)

	# Request an authorization url to send the user to...
	auth_props = twitter.get_authentication_tokens()

	# Then send them over there, durh.
	request.session['request_token'] = auth_props
	return HttpResponseRedirect(auth_props['auth_url'])

def thanks(request, redirect_url=settings.LOGIN_REDIRECT_URL):
    twitter = Twython(
        app_token = settings.APP_KEY,
        app_secret = settings.APP_SECRET,
        oauth_token = request.session['request_token']['oauth_token'],
        oauth_token_secret = request.session['request_token']['oauth_token_secret'],
        oauth_callback = 'http://localhost/result'
    )
    
    authorized_tokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'], callback_url = 'http://localhost/result/')
    
    try:
        emailexists = InviteEmails.objects.get(emailaddress = authorized_tokens['email'])
    except ObjectDoesNotExist:
        emailInstanceCreate(authorized_tokens['email'])
        email=InviteEmails.objects.get(emailaddress = authorized_tokens['email'])
        TwitterEmails.objects.create(emailaddress = authorized_tokens['email'], username = authorized_tokens['screen_name'])
        
        return render_to_response('invites/result.html', RequestContext(request, {'email':email, 'result':'success'}))
    return render_to_response('invites/result.html', RequestContext(request, {'email':email, 'result':'existing'}))
    
    return HttpResponseRedirect(redirect_url)