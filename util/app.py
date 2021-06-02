import importlib
import importlib.util
import sys

from aiohttp import web


class SubappLoadingFailure(Exception):
    def __init__(self, *args, subapp_name: str):
        self.subapp_name = subapp_name

        super().__init__(*args)


class SubappModuleMissingEntrypoint(SubappLoadingFailure):
    pass


class MiscSubappLoadingFailure(SubappLoadingFailure):
    def __init__(self, *args, subapp_name: str, original: Exception):
        self.original = original

        super().__init__(*args, subapp_name=subapp_name)


class CustomApp(web.Application):
    def load_subapp(self, subapp_module_name: str):
        module_spec = importlib.util.find_spec(subapp_module_name)
        module = importlib.util.module_from_spec(module_spec)

        sys.modules[subapp_module_name] = module

        try:
            module_spec.loader.exec_module(module)
        except Exception as error:
            del sys.modules[subapp_module_name]
            raise MiscSubappLoadingFailure(subapp_name=subapp_module_name, original=error)

        try:
            setup_func = getattr(module, "setup")
        except AttributeError:
            del sys.modules[subapp_module_name]
            raise SubappModuleMissingEntrypoint(subapp_name=subapp_module_name)

        try:
            setup_func(self)
        except Exception as error:
            del sys.modules[subapp_module_name]
            raise MiscSubappLoadingFailure(subapp_name=subapp_module_name, original=error)
