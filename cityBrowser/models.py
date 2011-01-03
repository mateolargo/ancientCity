from django.db import models

class Monument(models.Model):
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']

    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True)
    region = models.ForeignKey('Region', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    main_source = models.CharField(max_length=200, null=True, blank=True)

class Region(models.Model):
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order_index']

    name = models.CharField(max_length=100)
    encompassing_monument = models.ForeignKey(Monument, related_name='regions',  null=True, blank=True)
    order_index = models.IntegerField(unique=True, null=False, blank=False)

class Source(models.Model):
    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=100)
    monuments = models.ManyToManyField(Monument)
    #monument = models.ForeignKey(Monument, null=False, blank=False)
    bibliography = models.TextField(null=True, blank=True)
    
    class TYPES:
        IMAGE = 1
        PDF = 2
        TEXT = 3
        FLASH = 4
    TYPE_CHOICES = [(TYPES.__dict__[name], name) for name in dir(TYPES) if not name.startswith('_')]

    type = models.IntegerField(choices=TYPE_CHOICES)
    url = models.CharField(max_length=300, null=True, blank=True)
    thumbnail_url = models.CharField(max_length=300, null=True, blank=True)
    original_text = models.TextField(null=True, blank=True)
    english_text = models.TextField(null=True, blank=True)
