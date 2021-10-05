from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage

def upload_file(file):
    file_name = default_storage.save(file.name, file)
    print(default_storage.url(file_name))
