from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from invites.forms import InviteForm
from invites.models import InviteEmails
from main.models import SignupHandler
import random

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

def landing(request):
    numberofemails = InviteEmails.objects.count()
    numberleft = locale.format('%d', 2500 - numberofemails, grouping = True)
    
    if request.method=='POST':
        form = InviteForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['emailaddress']
            try:
                emailadd = InviteEmails.objects.get(emailaddress = email)
            except ObjectDoesNotExist:
                randomnumber = random.randint(0,100000)
                emailadd = InviteEmails.objects.create(emailaddress = email, id=numberofemails+1)
                signuphandle = SignupHandler.objects.create(emailaddress = email, identifiernum = randomnumber)
                return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'success'}))
            return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'existing'}))
    else:
        form = InviteForm()
        
    var = RequestContext(request, {
        'form':form,
        'number':numberleft
    })
    
    return render_to_response('invites/landing.html', var)