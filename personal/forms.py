from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    A class that implements the form to create an instance
    of the model Comment. Used in HTML.
    """

    class Meta:
        """
        Metadata of the Comment model.

        ...

        Attributes
        model:
            the model this metadata composes. In this case: Comment.
        fields:
            the tuple to be saved in the database.
        widgets:
            a dictionary that takes as attributes an string and a
            text input area. Be wider or shorter, the storage the
            name of the poster and the contents of the comment's
            body.
        """
        
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }
