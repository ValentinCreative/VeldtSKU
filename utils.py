def list_mixed_to_str(data):
    return list(map(str, data))


def concat(data, separator):
    return separator.join(list_mixed_to_str(data))


def concat_sku(skus):
    return concat(skus, '-')


def concat_description(descriptions):
    return concat(descriptions, ' ')
