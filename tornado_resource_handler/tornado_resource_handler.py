import re
from functools import wraps
from inspect import signature, Parameter

from tornado.web import RequestHandler


class ResourceHandlerMeta(type):

    _methods = ['index', 'show', 'edit', 'update', 'destroy', 'new', 'create']

    def __new__(cls, clsname, bases, context):

        if clsname == 'ResourceHandler':
            return super().__new__(cls, clsname, bases, context)

        def flexiable(func):
            parameter_names = map(lambda p: p.name, signature(func).parameters.values())

            @wraps(func)
            def new_func(self, *args, **kwargs):
                filtered_kwargs = {k: v for k, v in filter(lambda kv: kv[0] in parameter_names, kwargs.items())}
                return func(self, **filtered_kwargs)
            return new_func

        for key, value in context.items():
            if key not in ResourceHandlerMeta._methods:
                continue
            parameters = signature(value).parameters.values()
            if not any(map(lambda p: p.kind == Parameter.KEYWORD_ONLY, parameters)):
                context[key] = flexiable(value)

        return super().__new__(cls, clsname, bases, context)


class ResourceHandler(RequestHandler, metaclass=ResourceHandlerMeta):

    prefix = ''

    async def get(self, resource_id, action, **kwargs):
        if resource_id is None:
            result = self.index(**kwargs)
        elif resource_id == 'new':
            result = self.new(**kwargs)
        elif action is None:
            result = self.show(id=resource_id, **kwargs)
        elif action == 'edit':
            result = self.edit(id=resource_id, **kwargs)
        if result is not None:
            await result

    async def patch(self, resource_id, action, **kwargs):
        result = self.update(id=resource_id, **kwargs)
        if result is not None:
            await result

    async def delete(self, resource_id, action, **kwargs):
        result = self.destroy(id=resource_id, **kwargs)
        if result is not None:
            await result

    async def post(self, resource_id, action, **kwargs):
        result = self.create(**kwargs)
        if result is not None:
            await result

    @classmethod
    def get_resource_name(cls):
        if hasattr(cls, 'resource_name'):
            resource_name = cls.resource_name
        else:
            resource_name = re.sub(r'Handler$', '', cls.__name__)
            resource_name = re.sub(r'(?<!^)(?=[A-Z])', '_', resource_name).lower()
        return resource_name

    @classmethod
    def routes(cls, prefix='', nested=None, target_kwargs=None):
        routes = []
        target_kwargs = target_kwargs or {}
        nested = nested or []

        nested_prefix = rf'{prefix}/{cls.prefix}/(?P<parent_name>{cls.get_resource_name()})/?(?P<parent_id>[\w\d-]+)?/'
        for sub_route in nested:
            sub_route = list(sub_route)
            sub_route[0] = cls._normalize_matcher(f'{nested_prefix}{sub_route[0]}')
            sub_route[2] = {
                **target_kwargs,
                **sub_route[2]
            }
            routes.append(tuple(sub_route))
        route = cls._normalize_matcher(
            rf'{prefix}/{cls.prefix}/{cls.get_resource_name()}/?(?P<resource_id>[\w\d-]+)?/?(?P<action>[\w\d-]+)?/?')
        routes += [(route, cls, target_kwargs)]
        return routes

    @classmethod
    def _normalize_matcher(self, matcher):
        return re.sub(r'/+', r'/', matcher)
