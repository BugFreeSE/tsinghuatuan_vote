from tastypie.resources import ModelResource
from urlhandler.models import VoteAct, Candidate, VoteLog
from tastypie import fields


class VoteActResource(ModelResource):
    class Meta:
        queryset = VoteAct.objects.all()
        resource_name = 'VoteAct'


class CandidateResource(ModelResource):
    class Meta:
        VoteAct = fields.ForeignKey(VoteActResource, 'VoteAct')
        queryset = Candidate.objects.all()
        resource_name = 'Candidate'


class VoteLogResource(ModelResource):
    class Meta:
        queryset = VoteLog.objects.all()
        resource_name = 'VoteLog'