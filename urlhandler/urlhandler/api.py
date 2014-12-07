from tastypie.resources import ModelResource
from urlhandler.models import VoteAct


class VoteActResource(ModelResource):
    class Meta:
        queryset = VoteAct.objects.all()
        resource_name = 'VoteAct'