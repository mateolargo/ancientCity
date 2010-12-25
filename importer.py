import sys
from django.core.management import setup_environ
#sys.path.append('') #path of project
import settings
setup_environ(settings)

from cityBrowser.models import *

import yaml

def clean(input):
    if not input or input == '':
        return input
    return input.strip().replace('<br>','\n')

stop = False

parsed_regions = yaml.load(open('data-migration/regions.yml'))
regions = {}
order = 1
for r in parsed_regions:
    region_id = int(r.get('region_id'))
    mon_id = int(r.get('assoc_city_id'))
    name = r.get('name')
    regions[region_id] = {'id': region_id, 'name': name, 'parent_mon_id': mon_id, 'order_index':(order)}
    order += 1

parsed_monuments = yaml.load(open('data-migration/monuments.yml'))
monuments = {}
for m in parsed_monuments:
    #print m
    mon_id = int(m.get('mon_id'))

    parent_id = m.get('parent_id')
    parent_id = int(parent_id) if parent_id else None

    name = m.get('name')
    description = clean(m.get('description'))
    diagram = m.get('diagram')

    image = m.get('image')
    image = int(image) if image else None

    region_id = m.get('region_id')
    region_id = int(region_id) if region_id else None

    monuments[mon_id] = {'id':mon_id, 'parent_id':parent_id, 'name':name, 'description':description,
                         'diagram':diagram, 'image':image, 'region_id':region_id}

parsed_sources = yaml.load(open('data-migration/sources.yml'))
sources = {}
for s in parsed_sources:
    #print s
    source_id = int(s.get('source_id'))
    title = s.get('name')
    bibliography = s.get('bibliography')
    original = s.get('original')
    english = s.get('english')
    source_type_id = int(s.get('src_type_id'))
    source_type_id = 3 if source_type_id == 5 else source_type_id
    url = s.get('url')
    thumbnail_url = s.get('thumbnail_url')

    if source_type_id > 3:
        continue

    sources[source_id] = {'id':source_id, 'title':title, 'bibliography':bibliography, 'original': original,
                          'english':english, 'type': source_type_id, 'url':url, 'thumbnail_url':thumbnail_url}

parsed_srs = yaml.load(open('data-migration/source_refs.yml'))
refs = []
for sr in parsed_srs:
    mon_id = sr.get('mon_id')
    source_id = sr.get('source_id')

    refs.append({'source_id':source_id,'mon_id':mon_id})

    if not mon_id or not source_id:
        stop = True
        print "Bad Reference:",mon_id,source_id

if stop:
    print "Stopping..."
    sys.exit()


for m in monuments.values():
    Monument.objects.get_or_create(id=m['id'],name=m['name'],description=m['description'])

for r in regions.values():
    mon = Monument.objects.get(id=r['parent_mon_id'])
    Region.objects.get_or_create(id=r['id'],name=r['name'],encompassing_monument=mon,order_index=r['order_index'])

for m in monuments.values():
    parent,reg = None, None
    if m['parent_id']:
        parent = Monument.objects.get(id=m['parent_id'])
    else:
        print "Root monument:",m

    if m['region_id']:
        reg = Region.objects.get(id=m['region_id'])
        
    mon = Monument.objects.get(id=m['id'])
    mon.region = reg
    mon.parent = parent
    mon.save()

for s in sources.values():
    Source.objects.get_or_create(id=s['id'],title=s['title'],bibliography=s['bibliography'],type=s['type'],
                                 url=s['url'],thumbnail_url=s['thumbnail_url'],original_text=s['original'],
                                 english_text=s['english'])

for sr in refs:
    source,mon = None, None
    try:
        source = Source.objects.get(id=sr['source_id'])
    except:
        pass

    try:
        mon = Monument.objects.get(id=sr['mon_id'])
    except:
        pass

    if not source or not mon:
        print "Skipping bad reference:",sr,source,mon
        continue

    source.monuments.add(mon)
    source.save()
