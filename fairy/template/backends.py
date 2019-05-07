from django.template.backends.jinja2 import Jinja2 as BaseJinja2
from django.utils.module_loading import import_string


class Jinja2(BaseJinja2):
    def __init__(self, params):
        params = params.copy()  # type: dict
        options = params.pop('OPTIONS').copy()

        self.filters = options.pop('filters', [])

        params['OPTIONS'] = options

        super().__init__(params)  # 初始化

        # 导入 filters
        for filters_func_name in self.filters:
            filters_func = import_string(filters_func_name)
            self.env.filters.update(filters_func())
