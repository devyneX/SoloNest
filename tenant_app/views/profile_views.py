from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from tenant_app import forms


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "tenant_app/profile.html", {"profile": user.profile})


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = forms.ProfileUpdateForm(instance=user.profile)
        return render(request, "tenant_app/profile_update.html", {"form": form})

    def post(self, request):
        user = request.user
        form = forms.ProfileUpdateForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect("tenant:profile")
        return render(request, "tenant_app/profile_update.html", {"form": form})
