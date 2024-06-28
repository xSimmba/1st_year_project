import zipfile
from django import forms
from.models import File, Folder

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class FolderUploadForm(forms.Form):
    zip_file = forms.FileField(label='Select a zip file')

    def save(self, user):
        folder = Folder(created_by=user)
        folder.save()
        zip_file = self.cleaned_data.get('zip_file')
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(folder.folder_path)
        return folder
    
class FolderCreateForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }