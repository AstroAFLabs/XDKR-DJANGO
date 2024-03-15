# utils.py
from django.http import JsonResponse
from django.shortcuts import render
from docx import Document
import spacy
import fitz  # PyMuPDF
# Load the spaCy model
# TO EXTRACT TEXT FROM DOCUMENTS

nlp = spacy.load("en_core_web_sm")

doc = nlp("This is a test sentence.")



# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def find_word_in_text(text, word):
    # Process the text
    doc = nlp(text)

    # Search for the word
    return any(token.text == word for token in doc)


# EXTRACT TEXT FROM A PDF FILE:

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Function to extract text from a docx file
def extract_text_from_docx(file):
    doc = Document(file)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

# Function to extract keywords using spaCy
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_stop != True and token.is_punct != True]
    return keywords

# View to handle document uploads and processing
def process_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES['myfile']
            text = extract_text_from_docx(myfile)
            keywords = extract_keywords(text)
            return JsonResponse({'keywords': keywords})
        else:
            return JsonResponse({'error': 'Form is not valid'})
    else:
        form = DocumentForm()
    return render(request, 'document_form.html', {'form': form})
