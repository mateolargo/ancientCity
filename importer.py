import sys
from django.core.management import setup_environ
#sys.path.append('') #path of project
import settings
setup_environ(settings)

from cityBrowser.models import *

import yaml

def clean(input):
    return input

parsed_regions = yaml.load(open('data-migration/regions.yml'))
regions = {}
order = 1
for r in parsed_regions:
    region_id = int(r.get('region_id'))
    mon_id = int(r.get('assoc_city_id'))
    name = r.get('name')
    regions[region_id] = {'id': region_id, 'name': name, 'parent_mon_id': mon_id, 'order_index':(order)}
    order += 1
#print regions

parsed_monuments = yaml.load(open('data-migration/monuments.yml'))
monuments = {}
for m in parsed_monuments:
    #print m
    mon_id = int(m.get('mon_id'))

    parent_id = m.get('parent_id')
    parent_id = int(parent_id) if parent_id else None

    name = m.get('name')
    description = clean(m.get('description', ''))
    diagram = m.get('diagram')

    image = m.get('image')
    image = int(image) if image else None

    region_id = m.get('region_id')
    region_id = int(region_id) if region_id else None

    monuments[mon_id] = {'id':mon_id, 'parent_id':parent_id, 'name':name, 'description':description,
                         'diagram':diagram, 'image':image, 'region_id':region_id}
#print monuments

parsed_sources = yaml.load(open('data-migration/sources.yml'))
sources = {}
for s in parsed_sources:
    print s
    source_id = int(s.get('source_id'))
    name = s.get('name')
    bibliography = s.get('bibliography')
    original = s.get('original')
    english = s.get('english')
    source_type_id = int(s.get('source_type_id'))
