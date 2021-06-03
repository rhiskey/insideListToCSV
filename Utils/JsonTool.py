def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """

    #  Populate the dictionary with object meta data
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)

    return obj_dict


def dict_to_obj(d):
    # checking whether object d is a
    # instance of class list
    if isinstance(d, list):
        d = [dict_to_obj(x) for x in d]

    # if d is not a instance of dict then
    # directly object is returned
    if not isinstance(d, dict):
        return d

    # declaring a class
    class C:
        pass

    # constructor of the class passed to obj
    obj = C()

    for k in d:
        obj.__dict__[k] = dict_to_obj(d[k])

    return obj

