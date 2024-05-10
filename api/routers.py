from django.conf import settings

from rest_framework import routers


class APIRootRouter(routers.SimpleRouter):
    router = routers.DefaultRouter()

    def register(self, *args, **kwargs):
        self.router.register(*args, **kwargs)
        super().register(*args, **kwargs)


def api_urls():
    from importlib import import_module, util
    for app in settings.API_APPS:
        module = app + '.urls'
        module_spec = util.find_spec(module)
        if module_spec:
            import_module(module)

    return APIRootRouter.router.urls
