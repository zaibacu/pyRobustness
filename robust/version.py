VERSION = (1, 0, 0)


def get_version():
    return ".".join(map(lambda x: str(x), VERSION))