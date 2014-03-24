from tastypie.api import Api

from ma_sucker.api.resources import PatentResource

v1_api = Api(api_name='v1')
v1_api.register(PatentResource())
