from django import forms
from .models import Document
from .models import Tag


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'uploaded_content', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }

    # Optionally, add a field for creating new tags on the fly
    new_tags = forms.CharField(required=False, help_text="Add tags, separated by commas")

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        self.save_m2m()  # Needed for saving many-to-many relationships

        # Handle new tags creation
        new_tags = self.cleaned_data.get('new_tags', '')
        if new_tags:
            tag_names = [name.strip() for name in new_tags.split(',') if name.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance

