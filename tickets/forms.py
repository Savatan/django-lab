from django import forms
from .models import Ticket, Comment


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'service', 'priority', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inp'}),
            'description': forms.Textarea(attrs={'class': 'inp', 'rows': 5}),
            'service': forms.TextInput(attrs={'class': 'inp'}),
            'priority': forms.Select(attrs={'class': 'inp'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'inp'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'inp', 'rows': 3,
                                          'placeholder': 'Ваш комментарий...'}),
        }
