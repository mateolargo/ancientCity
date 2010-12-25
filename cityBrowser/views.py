from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from ancientCity.cityBrowser.models import Monument, Region, Source

def index(request):
    return HttpResponse("Hello, World!")

def rome(request):
    city = Monument.objects.get(name="Rome")
    regions = city.regions.all()

    img_sources = city.source_set.filter(type=Source.TYPES.IMAGE) #Source.objects.filter(monument=monument,type=Source.TYPES.IMAGE)
    text_sources = city.source_set.filter(type=Source.TYPES.TEXT) #Source.objects.filter(monument=monument,type=Source.TYPES.TEXT)
    link_sources = city.source_set.filter(type=Source.TYPES.PDF) #Source.objects.filter(monument=monument,type=Source.TYPES.PDF)
    
    templatevars = {
        'city': city,
        'regions': regions,
        'imageSources': img_sources,
        'textSources': text_sources,
        'linkSources': link_sources,
    }

    response = render_to_response('city.html', templatevars, context_instance=RequestContext(request))

    return response

def monument(request, mon_id):
    try:
        monument = Monument.objects.get(pk=mon_id)
    except:
        return HttpResponseNotFound()
        #return render_to_response('404.html')

    breadcrumbs = [monument]
    parent = monument.parent
    while parent:
        breadcrumbs.append(parent)
        parent = parent.parent
    base_mon = breadcrumbs[-1]
    breadcrumbs = breadcrumbs[:-1]
    breadcrumbs.reverse()

    children = monument.monument_set.all()

    img_sources = monument.source_set.filter(type=Source.TYPES.IMAGE) #Source.objects.filter(monument=monument,type=Source.TYPES.IMAGE)
    text_sources = monument.source_set.filter(type=Source.TYPES.TEXT) #Source.objects.filter(monument=monument,type=Source.TYPES.TEXT)
    link_sources = monument.source_set.filter(type=Source.TYPES.PDF) #Source.objects.filter(monument=monument,type=Source.TYPES.PDF)

    templatevars = {
        'monument': monument,
        'base_monument': base_mon,
        'breadcrumbs': breadcrumbs,
        'children': children,
        'image_sources': img_sources,
        'text_source_count': len(text_sources)+len(link_sources),
        'text_sources': text_sources,
        'link_sources': link_sources,
    }

    response = render_to_response('monument.html', templatevars, context_instance=RequestContext(request))
    return response
