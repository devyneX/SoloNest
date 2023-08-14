from django import forms
from manager_app import models


class RoomRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = models.RoomRequest
        fields = ["assigned_room"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_room"].queryset = self.instance.get_available_rooms()


class RoomRequestRejectionForm(forms.ModelForm):
    class Meta:
        model = models.RoomRequest
        fields = ["rejection_reason"]
        widgets = {
            "rejection_reason": forms.Textarea(),
        }


class CleaningSearchForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )


class LaundrySelectionFrom(forms.ModelForm):
    pk = forms.BooleanField(required=False)

    class Meta:
        model = models.LaundryRequest
        fields = []