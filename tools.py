def mapv(f,vec):
    return list(map(f,vec))

def zipv(*vec):
    return list(zip(*vec))

def to_tuple(it):
    if it is None:
        return None
    return tuple(it)