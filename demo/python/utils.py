
def min_filtered_none(lst=()):
    """Ignores None and returns any other value for min, unless None is the only option then None is returned"""
    filtered = list(filter(lambda x: x is not None, lst))
    if len(filtered) == 0:
        return None
    else:
        return min(filtered)
