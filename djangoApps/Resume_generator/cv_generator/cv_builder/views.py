from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Profile
import pdfkit

def create_profile(request):
    if request.method == 'POST':
        profile = Profile(
            name=request.POST['name'],
            phone_number=request.POST['phone_number'],
            email=request.POST['email'],
            degree=request.POST['degree'],
            skills=request.POST['skills'],
            about=request.POST['about']
        )
        profile.save()
        return redirect('success', profile_id=profile.id)
    return render(request, 'cv_builder/create_profile.html')

def success(request, profile_id):
    return render(request, 'cv_builder/success.html', {'profile_id': profile_id})

def generate_pdf(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    html = render_to_string('cv_builder/resume.html', {'profile': profile})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response