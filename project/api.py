from tastypie.api import Api

from sucker.api.resources import PatentResource

v1_api = Api(api_name='v1')
v1_api.register(PatentResource())
