from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from ancientCity.cityBrowser.models import Monument, Region, Source

def index(request):
    return HttpResponse("Hello, World!")

def rome(request):
    rome = Monument.objects.get(name="Rome")
    regions = rome.regions.all()
    #regions = Region.objects.filter(monument=rome)
    imgSources = Source.objects.filter(monument=rome,type=Source.TYPES.IMAGE)
    textSources = Source.objects.filter(monument=rome,type=Source.TYPES.TEXT)
    linkSources = Source.objects.filter(monument=rome,type=Source.TYPES.PDF)
    
    for r in regions:
        print r.monument_set.all()
    templatevars = {
        'city': rome,
        'regions': regions,
        'imageSources': imgSources,
        'textSources': textSources,
        'linkSources': linkSources,
    }

    response = render_to_response('city.html', templatevars, context_instance=RequestContext(request))

    return response

'''
def city(request):
    city = City.objects.get(name="Rome")
    regions = Region.objects.filter(city=city)
    templatevars = {
        'city': city,
        'regions': regions
    }

    response = render_to_response('city.html', templatevars, context_instance=RequestContext(request))

    return response
'''

def monument(request):
    pass
