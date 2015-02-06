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
    #TODO: Add the option to specify file types with a length argument (for identifying the number of chars) and a tuple(containing
    # all the extensions)
    def __init__(self, request, form_file_target_name, path, ext_tuple=None):
        self.request = request
        self.form_file_target_name = form_file_target_name
        self.path = path
        self.file = self.request.FILES.get(self.form_file_target_name, '')
        self.ext_tuple = ext_tuple
    
    def upload_file(self):
        upload_handled = self.__handle_file_upload(self.file, self.path)
        return upload_handled
    
    def file_name(self):
        return self.file.name
    
    def __handle_file_upload(self, f, path_to_save):
        # Return False if the file name is too big
        if not f or len(f.name) < 3 or len(f.name) > 100:
            return False
        
        if self.ext_tuple and (not len(self.ext_tuple) <= 0):
            break_into_extensions = self.file.name.split('.')
            extension_of_file = break_into_extensions[len(break_into_extensions) - 1]
            if extension_of_file not in self.ext_tuple:
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
