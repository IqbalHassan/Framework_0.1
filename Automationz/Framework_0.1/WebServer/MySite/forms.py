from django import forms

class Comment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    docfile = forms.FileField(
        label='Attach file',
        #help_text='max. 42 megabytes'
    )
    commented_by=forms.CharField(widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['comment'].widget.attrs['cols'] = 75
        self.fields['comment'].widget.attrs['rows'] = 5
        self.fields['comment'].widget.attrs['placeholder']='Comment Here...'
        self.fields['commented_by'].widget=forms.HiddenInput()
        
class tc_file_upload(forms.Form):
    docfile=forms.FileField(label='Attach file')
    def __init__(self,*args,**kwargs):
        super(tc_file_upload,self).__init__(*args,**kwargs)
        