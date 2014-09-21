'''
Bismillahi Rahmanir Rahim, ALLAHU AKBAR
@author: Sazid
'''

import os

# FileUploader class
class FileUploader():
    '''
    This class is responsible for handling custom file uploads
    NOTE: You must create the required directory first
    '''
    def __init__(self, request, form_file_target_name, path):
        self.request = request
        self.form_file_target_name = form_file_target_name
        self.path = path
        self.file = self.request.FILES.get(self.form_file_target_name, '')
    
    def upload_file(self):
        upload_handled = self.__handle_file_upload(self.file, self.path)
        return upload_handled
    
    def file_name(self):
        return self.file.name
    
    def __handle_file_upload(self, f, path_to_save):
        # Return False if the file name is too big
        if len(f.name) < 3 or len(f.name) > 100:
            return False
        
        path_to_file = os.path.join(path_to_save, f.name)
        
        try:
            with open(path_to_file, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return True
        except IOError:
            print "Can't open file for writing"
            return False

