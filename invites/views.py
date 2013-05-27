from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from invites.forms import InviteForm
from invites.models import InviteEmails

def landing(request):
    if request.method=='POST':
        form = InviteForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['emailaddress']
            try:
                emailadd = InviteEmails.objects.get(emailaddress = email)
            except ObjectDoesNotExist:
                emailadd = InviteEmails.objects.create(emailaddress = email)
                return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'success'}))
            return render_to_response('invites/result.html', RequestContext(request, {'email':emailadd, 'result':'existing'}))
    else:
        form = InviteForm()
        
    var = RequestContext(request, {
        'form':form
    })
    
    return render_to_response('invites/landing.html', var)