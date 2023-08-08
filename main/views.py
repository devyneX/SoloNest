from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = "main/home.html"


class AboutView(TemplateView):
    template_name = "main/abouts.html"
    
class ServicesView(TemplateView):
    template_name = "main/services.html"

class ContactView(TemplateView):
    template_name = "main/contact.html"