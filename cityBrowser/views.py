from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from ancientCity.cityBrowser.models import Monument, Region, Source
from django.conf import settings

def index(request):
    templatevars = {'ROOT_PATH': settings.ROOT_PATH,}
    response = render_to_response('index.html', templatevars, context_instance=RequestContext(request))    
    return response

def rome(request):
    #try:
        city = Monument.objects.get(name="Rome")
        return render_monument(request, city)
    #except:
    #    return HttpResponseNotFound()

def monument(request, mon_id):
    try:
        monument = Monument.objects.get(pk=mon_id)
        return render_monument(request, monument)
    except:
        return HttpResponseNotFound()
        #return render_to_response('404.html')

def render_monument(request, monument):
    breadcrumbs = [monument]
    parent = monument.parent
    while parent:
        breadcrumbs.append(parent)
        parent = parent.parent
    base_mon = breadcrumbs[-1]
    breadcrumbs = breadcrumbs[:-1]
    breadcrumbs.reverse()

    regions, children = monument.regions.all(), None
    temp_regions = None
    region_monuments = None
    if len(regions) > 0:
        temp_regions  = []
        for r in regions:
            mons = r.monument_set.all()
            if len(mons) > 0:
                temp_regions.append({'region':r,'monuments':mons})
        regions = temp_regions
    else:
        regions, children = None, monument.monument_set.all()

    img_sources = monument.source_set.filter(type=Source.TYPES.IMAGE) #Source.objects.filter(monument=monument,type=Source.TYPES.IMAGE)
    text_sources = monument.source_set.filter(type=Source.TYPES.TEXT) #Source.objects.filter(monument=monument,type=Source.TYPES.TEXT)
    link_sources = monument.source_set.filter(type=Source.TYPES.PDF) #Source.objects.filter(monument=monument,type=Source.TYPES.PDF)

    templatevars = {
        'monument': monument,
        'base_monument': base_mon,
        'breadcrumbs': breadcrumbs,
        'has_regions': regions != None,
        'regions': regions,
        'region_monuments': region_monuments,
        'children': children,
        'image_sources': img_sources,
        'text_source_count': len(text_sources)+len(link_sources),
        'text_sources': text_sources,
        'link_sources': link_sources,
        'ROOT_PATH': settings.ROOT_PATH,
    }

    response = render_to_response('monument.html', templatevars, context_instance=RequestContext(request))
    return response
