import hashlib

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file: # open file in binary mode
        for chunk in iter(lambda: file.read(4096), b""): # read file in 4096 byte chunks
            hasher.update(chunk) # update hash with each chunk 
    return hasher.hexdigest() # return final hash as hex string
