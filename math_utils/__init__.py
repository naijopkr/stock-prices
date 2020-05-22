def geometric_mean(values):
    product = 1
    for value in values:
        product *= value

    return product ** (1/len(values))
