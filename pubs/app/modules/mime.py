import mimetypes

def get_file_extension(media_type: str) -> str:
    # Use the mimetypes module to get the file extension from the media_type
    extension = mimetypes.guess_extension(media_type)
    
    # If mimetypes cannot guess the extension, raise an error
    if not extension:
        raise ValueError(f"Unable to determine file extension for media type: {media_type}")
    
    return extension
