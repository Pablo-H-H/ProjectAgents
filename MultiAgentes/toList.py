def toList(array):
    uniList = []
    
    for element in array:
        if isinstance(element, list):
            uniList.extend(toList(element))  # Recursively flatten
        else:
            uniList.append(element)
    
    return uniList