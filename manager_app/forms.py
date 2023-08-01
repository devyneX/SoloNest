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
