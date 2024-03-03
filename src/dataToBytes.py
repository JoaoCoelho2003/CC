# dataToBytes: transform the data from bytes to string
def arrayBytesToString(array):
    return [chunk.decode('utf-8') for chunk in array.split(b'\0')]

# dataToBytes: transform the data from string to bytes
def arrayStringToBytes(array):
    return b'\0'.join([chunk.encode('utf-8') for chunk in array])
