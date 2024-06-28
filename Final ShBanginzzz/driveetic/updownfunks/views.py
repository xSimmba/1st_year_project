from pyexpat.errors import messages
from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import File, Folder
from updownfunks.forms import FileUploadForm, FolderUploadForm, FolderCreateForm

from django.views.decorators.http import require_GET


from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import os
import zipfile


@require_GET
def favicon(request):
    return HttpResponse(
        '<svg href="/workspaces/sheBanginzzz/driveetic/static/icons8-star-16.png" viewBox="0 0 100 100">'
        + '<text y=".9em" font-size="90">👾</text>'
        + "</svg>",
        content_type="image/svg+xml",
    )


def index_view(request):
    if request.user.is_authenticated:
        return redirect('cdashboard')
    return render(request, 'updownfunks/index.html')


@login_required
def dashboard_view(request):
    user = request.user
    folder_list = Folder.objects.filter(
        created_by=user
    )
    files_list = File.objects.filter(
        uploaded_by = user,
        is_orphan = True,
    )
    return render(request, 'cdashboard.html', {'files_list': files_list, 'folder_list': folder_list})

@login_required
def file_upload_view(request, pk=None):
    if pk:
        folder = get_object_or_404(Folder, pk=pk)
    else:
        folder = None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.name = str(file.file)
            if folder:
                file.is_orphan = False
                file.folder = folder
                folder.save()
            else:
                file.is_orphan = True
            
            file.save()
            return redirect('cdashboard') 
    
    form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form, 'folder': folder})
    

@login_required
def file_download_view(request, pk):
    file = File.objects.get(pk=pk)
    if file.uploaded_by == request.user:
        response = FileResponse(file.file.open('rb'), as_attachment=True, filename=file.file.name)
        return response
    else:
        return redirect('cdashboard')

@login_required
def file_delete_view(request, pk):
    file = File.objects.get(pk=pk)
    if file.uploaded_by == request.user:
        file.delete()
        return redirect('cdashboard')
    else:
        return redirect('cdashboard')
    

@login_required
def create_folder_view(request):
    
    form = FolderCreateForm(request.POST or None) 

    if request.method == 'POST':
        form = FolderCreateForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.created_by = request.user
            folder.save()
            return redirect('cdashboard')
     
    return render(request, 'create_folder.html', {'form': form})

@login_required
def folder_detail_view(request, pk):
    user = request.user
    folder = get_object_or_404(Folder, id=pk)
    is_owner = user == folder.created_by

    if not is_owner:
        return redirect("cdashboard")
   
    return render(request, 'folder_detail.html', {'folder': folder})

@login_required
def delete_folder_view(request, pk):
    folder = Folder.objects.get(pk=pk)
    folder.delete()
    return redirect('cdashboard')



@login_required
def upload_folder_view(request, pk=None):
    if pk:
        folder = Folder.objects.get(pk=pk)
        if folder.created_by != request.user:
            return HttpResponseForbidden()
    else:
        folder = None

    if request.method == 'POST':
        form = FolderUploadForm(request.POST, request.FILES)
        if form.is_valid():
            folder = form.save(request.user)
            return redirect('cdashboard')
    else:
        form = FolderUploadForm()

    return render(request, 'upload_folder.html', {'form': form, 'folder': folder})

@login_required
def download_folder_view(request, folder_pk):
    folder = Folder.objects.get(pk=folder_pk)
    if folder.created_by == request.user:
        folder_path = folder.folder_path
        if not folder_path:  # Check if folder_path is not empty
            return HttpResponseBadRequest("Folder path is not valid")
        
        if os.path.isabs(folder_path):  # Check if folder_path is an absolute path
            parent_dir = folder_path  # If it's a root directory, use the folder_path as the parent_dir
        else:
            parent_dir = os.path.dirname(folder_path)
        
        if not parent_dir:  # Check if parent_dir is not empty
            return HttpResponseBadRequest("Parent directory is not valid")
        
        zip_file_name = f"{folder.name}.zip"
        zip_file_path = os.path.join(parent_dir, zip_file_name)
        
        # Ensure the parent directory exists
        os.makedirs(parent_dir, exist_ok=True)
        
        relroot = os.path.abspath(os.path.join(folder_path, os.pardir))
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk(folder_path):
                # add directory (needed for empty dirs)
                relpath = os.path.relpath(root, relroot)
                zip.write(root, relpath)
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename): # regular files only
                        arcname = os.path.join(relpath, file)
                        zip.write(filename, arcname)
        response = FileResponse(open(zip_file_path, 'rb'), as_attachment=True, filename=zip_file_name)
        return response
    else:
        return redirect('cdashboard')

@login_required
def move_file(request, file_pk):
    file = get_object_or_404(File, pk=file_pk)
    if request.method == 'POST':
        folder_pk = request.POST.get('move_to_folder')
        folder = get_object_or_404(Folder, pk=folder_pk)
        file.folder = folder
        file.save()
        return redirect('cdashboard')
    else:
        folder_list = Folder.objects.all()
        return render(request, 'move_file.html', {'folder_list': folder_list, 'file_pk': file_pk})