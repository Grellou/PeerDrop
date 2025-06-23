import hashlib
from app.models.file_model import SharedFileModel

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file: # open file in binary mode
        for chunk in iter(lambda: file.read(4096), b""): # read file in 4096 byte chunks
            hasher.update(chunk) # update hash with each chunk 
    return hasher.hexdigest() # return final hash as hex string

def permission_to_download_file(file_data, user_id):
    # Check if file is public
    if file_data.is_public:
        return True
    # Check if user is owner of the file
    if file_data.owner_id == user_id:
        return True
    # Check if file is shared with user
    if SharedFileModel.query.filter(file_id=file_data.id, shared_with_user_id=user_id).first(): #type: ignore
        return True
    return False # if none of the above is true
