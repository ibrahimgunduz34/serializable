from serializable.utils import get_object_path, load_class


class AbstractObject(object):
    GET_ACTION_KEY = 'get_'
    SET_ACTION_KEY = 'set_'

    def __create_object_meta(self, obj, data={}):
        """
        create meta structure of object.

        arguments:
            :param obj:
        """
        return {'object_type': get_object_path(obj), 'data': {}}

    def serialize(self, **kwargs):
        """
        serializes object to dictionary.

        arguments:
            :param kwargs: contains some serialization options.
            :return: dict
        """
        data = self.__create_object_meta(self)
        for key in self.attributes:
            value = self.__get_value(key)
            if hasattr(self, 'schema') and \
                    key in self.schema:
                if issubclass(self.schema[key], AbstractObject):
                    serialized_value = value.serialize(**kwargs)
                    item_dict = {key: serialized_value}
                else:
                    data_type = self.schema[key]
                    value = value and data_type(value) or data_type()
                    item_dict = {key: value}
            else:
                item_dict = {key: value}
            data['data'].update(item_dict)
        return data

    def __validate_serialized_data(self, data):
        """
        validates serialized data object.

        arguments:
            :param data: data argument.
            :return: boolean value.
            :thrown: ValueError
        """
        if 'object_type' not in data or 'data' not in data:
            raise ValueError('It is not valid serialized object!')
        return True

    def __is_object_meta(self, data):
        """
        returns True when data have valid object structure.

        arguments:
            :param data: data argument.
            :return: boolean value.
        """
        return isinstance(data, dict) and \
            len(data) == 2 and \
            'object_type' in data and \
            'data' in data

    def deserialize(self, data):
        """
        deserialize object from the specified data parameter.

        arguments:
            :param data: dict
            :return: family of this class.
        """
        self.__validate_serialized_data(data)
        object_type = data['object_type']
        if not get_object_path(self) == object_type:
            raise TypeError(
                "Data structure doesn't match with this object. "
                "Object should be instance of %s for this data." %
                object_type)
        for key, value in data['data'].items():
            if self.__is_object_meta(value):
                obj = load_class(value['object_type'])
                self.__set_value(key, obj(**value['data']))
            else:
                self.__set_value(key, value)

    def to_hash(self, **kwargs):
        """
        converts to hash current state of the object.

        arguments:
            :param kwargs: expected arguments by the serialize method.
            :return: string
        """
        raise NotImplemented('method is not implemented yet!')

    def __init__(self, **kwargs):
        """
        object constructor. You can pass object members with kwargs
        on construction time.

        arguments:
            :param kwargs: object members as keyword arguments.
        """
        self.__data = {}
        if hasattr(self, 'schema'):
            for key, value in self.schema.items():
                self.__set_value(key, value())
        if hasattr(self, 'defaults'):
            self.__set_data(**self.defaults)
        self.__set_data(**kwargs)

    def __set_value(self, key, value):
        """
        set a value to attribute of the object.

        arguments:
            :param key: name of the object attribute.
            :param value: value of the object attribute.
            :return: current object instance.
        """
        if key not in self.attributes:
            raise KeyError('%s is not a member of the object.' % key)
        if hasattr(self, 'schema') and \
                key in self.schema and \
                not isinstance(value, self.schema.get(key)):
            raise TypeError('%s shold be instance of %s' %
                            (key, type(self.schema.get(key))))
        self.__data.update({key: value})
        return self

    def __get_value(self, key):
        """
        get value from attribute of the object.

        arguments:
            :param key: name of the object attribute.
            :return: value of the object attribute.
        """
        if key not in self.attributes:
            raise KeyError('%s is not a member of the object.' % key)
        data = self.__data.get(key)
        return data

    def __set_data(self, **kwargs):
        """
        set data to object from the specified keyword
        arguments as bulk.

        arguments:
            :param kwargs: attribute-value pairs.
        """
        if kwargs:
            for key, value in kwargs.items():
                self.__set_value(key, value)
        return self

    def __get_action(self, name):
        """
        returns action type of the called method.

        arguments:
            :param name: name of the called method.
            :return: action key.
        """
        if name.startswith(self.GET_ACTION_KEY):
            return self.GET_ACTION_KEY
        elif name.startswith(self.SET_ACTION_KEY):
            return self.SET_ACTION_KEY
        else:
            raise KeyError('%s is not a member of the object.' % name)

    def __get_attribute_name(self, name):
        """
        returns name of the attribute by the
        called method name.

        arguments:
            :param name: name of the called method.
            :return: attribute name.
        """
        action = self.__get_action(name)
        return name[len(action):]

    def __dispatch(self, callback, action, attribute):
        """
        calls the specified callback method by the action.

        arguments:
            :param callback:
        """
        def wrapper(*args):
            if action == self.GET_ACTION_KEY:
                return callback(attribute)
            elif action == self.SET_ACTION_KEY:
                return callback(attribute, *args)
        return wrapper

    def __getattr__(self, name):
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            action = self.__get_action(name)
            attribute = self.__get_attribute_name(name)
            if action == self.GET_ACTION_KEY:
                callback = self.__get_value
            elif action == self.SET_ACTION_KEY:
                callback = self.__set_value
            else:
                raise AttributeError(
                    '%s is not a member of the object.' % name)
            return self.__dispatch(callback, action, attribute)
