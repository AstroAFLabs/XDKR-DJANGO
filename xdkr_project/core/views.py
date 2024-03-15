from django.shortcuts import render, get_object_or_404, redirect
from .models import Document, Tag
from .forms import DocumentForm
from django.http import FileResponse
from django.db.models import Q
from django.db import transaction
import docx2txt
import spacy
from django.http import JsonResponse
from .utils import extract_text_from_docx, extract_keywords  # Importing utility functions

from .utils import extract_text_from_pdf, find_word_in_text  # Assuming you put the functions in a module named document_processing.py

# Create your views here.


# TO SERVE AND VIEW DOCUMENTS

def serve_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    file_path = document.uploaded_content.path
    return FileResponse(open(file_path, 'rb'), filename=document.uploaded_content.name)

# TO SHOW DOCUMENTS IN THE DB



def document_list(request):
    search_query = request.GET.get('search', '')
    tag_query = request.GET.getlist('tags')  # For multiple tag selection

    # Start with all documents
    documents = Document.objects.all()

    # Filter by search query if it's provided
    if search_query:
        documents = documents.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    # Filter by tags if any tag is selected
    if tag_query:
        documents = documents.filter(tags__name__in=tag_query).distinct()

    # Get all tags for the filtering options in the template
    tags = Tag.objects.all()

    # Return the filtered documents and all tags to the template
    return render(request, 'core/document_list.html', {'documents': documents, 'tags': tags})


    
# TO CREATE A DOCUMENT (STRANGELY ENOUGH)
    
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # First, save the form to create the document instance
                document = form.save(commit=False)
                document.save()

                # Process the new_tags field
                new_tags = form.cleaned_data.get('new_tags', '')
                if new_tags:
                    tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
                    for tag_name in tag_names:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        document.tags.add(tag)

                # Save many-to-many data for the form
                form.save_m2m()
            return redirect('document_list')
            
    else:
        form = DocumentForm()
    return render(request, 'core/document_form.html', {'form': form})

# TO OPEN UP AND EXAMINE A DOCUMENT'S STATS

def document_read(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'core/document_detail.html', {'document': document})

# TO MODIFY OR CHANGE A DOCUMENT
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'core/document_form.html', {'form': form})

# SELF EXPLANATORY REALLY.

def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
    #return redirect('document_list')
    return render(request, 'core/document_confirm_delete.html', {'document': document})
    
