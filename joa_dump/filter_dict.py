import collections


def filter_dict(d, filter_key, filter_function):
    def filter_list(l, filter_key, filter_function):
        result = []
        for i in l:
            if isinstance(i, collections.Iterable):
                i = filter_list(i, filter_key, filter_function)
                if i is None:
                    continue
                result.append(i)
            elif isinstance(i, collections.Mapping):
                i = filter_dict(i, filter_key, filter_function)
                if i is None:
                    continue
                result.append(i)
            else:
                result.append(i)
        return result

    result = {}
    for (k, v) in d.iteritems():
        if isinstance(v, collections.Mapping):
            result[k] = filter_dict(v, filter_key, filter_function)
            if result[k] is None:
                del result[k]
        elif k == filter_key and not filter_function(v):
            return None
        else:
            result[k] = v

    return result

def role_is_in(role):
    def by_role(i):
        if role in i:
            return True
        else:
            return False
    return by_role

print "filter_dict"
print "role_is_in"

a_dict = {"something": "hi"}
b_dict = {'a': 'b', 'b':{'c':1, 'privacy': 'argo'}}
