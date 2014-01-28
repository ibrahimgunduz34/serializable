import importlib


def load_class(full_class_path):
    if full_class_path.find(".") > 0:
        module_path, class_name = full_class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    else:
        return importlib.import_module(full_class_path)


def get_object_path(obj):
    class_or_instance_name = hasattr(obj, '__name__') and \
        obj.__name__ or obj.__class__.__name__
    return "%s.%s" % (obj.__module__, class_or_instance_name)
