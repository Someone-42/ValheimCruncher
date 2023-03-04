import json
import inspect

def _get_constructor_args(elementType):
    # Gathering constructor parameter names
    return [param for param in dict(inspect.signature(elementType.__init__).parameters) if param != "self"]

def _get_matching_variables_as_strings(instance, attributeNames):
    res = []
    for attr in attributeNames:
        if attr in instance.__dict__:
            res.append(_serialize_var_to_string(instance.__dict__[attr]))
    return res

def _serialize_var_to_string(v):
    # Works for strings, ints, and floats, rest wasn't tested
    if isinstance(v, str):
        return f"\"{v}\""
    else:
        return str(v)

def _deserialize_string_to_variables(s):
    return eval(s)

def NewSaveFile(filename, elementType):
    attributes = _get_constructor_args(elementType)
    f = open(filename, 'w')
    f.write(" ".join(attributes) + '\n')
    f.close()

def SerializeAndSave(filename, element):
    """ Serializes element and saves it (appending) to file of filename """
    f = open(filename, 'r+')
    try:
        # Gathering attributes that are currently being saved in the file
        attributes = f.readline().strip().split(' ')

        v = _get_matching_variables_as_strings(element, attributes)

        f.seek(0, 2) # Going to the end of file
        f.write(" ".join(v) + '\n')
    except:
        print("An error happened while trying to serialize element", element)
    finally:
        f.close()

def DeSerializeFromSave(filename, elementType):
    """ Returns a collection of elements from save file (filename) """
    args = _get_constructor_args(elementType)

    f = open(filename, 'r')
    attributes = f.readline().strip().split(' ')
    lines = f.readlines()
    f.close()

    d = { attr: None for attr in args }
    
    s_args = set(args)
    s_attr = set(attributes)
    unknown, unused = list(s_args - s_attr), list(s_attr - s_args)

    if len(unknown) > 0:
        print(f"There are arguments needed to construct an object of type {elementType} : {', '.join(unknown)}.\n\tThey will be set to `None` by default")
    if len(unused) > 0:
        print(f"There are unused attributes saved in the file for type {elementType}, they will be discarded next time a save is performed : {', '.join(unused)}")

    data = [None] * len(lines)
    for i, line in enumerate(lines):
        for j, s in enumerate(line.strip().split(' ')):
            d[args[j]] = _deserialize_string_to_variables(s)
        data[i] = elementType(**d) # Unpacking variables (with attribute name) into constructor
    
    return data