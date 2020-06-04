from functools import reduce

def jsonWrapper(data, fields):
    result = map(lambda x: { fields[i]: x[i] for i in range(len(fields)) }, data)
    return list(result)