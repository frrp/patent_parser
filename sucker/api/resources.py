# coding=utf-8

from tastypie.resources import ModelResource, ALL
from tastypie import fields
from ..models import Patent, Person, Citation, Claim


class PersonResource(ModelResource):
    class Meta:
        queryset = Person.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
        }

class CitationResource(ModelResource):
    class Meta:
        queryset = Citation.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
        }

class ClaimResource(ModelResource):
    class Meta:
        queryset = Claim.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
        }

class PatentResource(ModelResource):
    citations = fields.ToManyField(CitationResource, 'citations', full=True)
    forwardcitations = fields.ToManyField(CitationResource, 'forwardcitations', full=True)
    applicants = fields.ToManyField(PersonResource, 'applicants', full=True)
    inventors = fields.ToManyField(PersonResource, 'inventors', full=True)
    assignees = fields.ToManyField(PersonResource, 'assignees', full=True)
    examiners = fields.ToManyField(PersonResource, 'examiners', full=True)
    claims = fields.ToManyField(ClaimResource, 'applicants', full=True)

    class Meta:
        queryset = Patent.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'title': ALL,
            'document_number': ALL,
        }
