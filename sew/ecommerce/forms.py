from django import forms
from .models import Contact,Review,Subscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }
class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=15)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # You can add phone number validation logic here if necessary
        return phone


