from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import Service
from notifications.utils import notify_admin
from .forms import ContactForm

def home_view(request):
    services = Service.objects.filter(active=True)[:6]
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Your message has been received! Our team will contact you shortly.")
            
            # Send notification to admin
            notify_admin(
                title=f"New Contact Inquiry: {contact.subject}",
                message=f"Received a contact inquiry from {contact.name} ({contact.email}):\n\n{contact.message}"
            )
            return redirect('website:home')
    else:
        form = ContactForm()
        
    return render(request, 'website/home.html', {
        'services': services,
        'contact_form': form
    })

def about_view(request):
    return render(request, 'website/about.html')

def services_view(request):
    services = Service.objects.filter(active=True)
    return render(request, 'website/services.html', {'services': services})

def portfolio_view(request):
    portfolio_items = [
        {'title': 'Corporate Anthem', 'category': 'video', 'desc': 'Brand identity launch video.', 'image': 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Autumn Glow', 'category': 'photo', 'desc': 'Lifestyle portrait shoot.', 'image': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&w=600&q=80'},
        {'title': 'SaaS Dashboard', 'category': 'design', 'desc': 'Vector interface dashboard branding.', 'image': 'https://img.magnific.com/free-vector/identity-technology-set_1284-10818.jpg?semt=ais_hybrid&w=740&q=80'},
        {'title': 'Kinetic Typography', 'category': 'motion', 'desc': 'Logo intro animation.', 'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Luxe Real Estate', 'category': 'photo', 'desc': 'Commercial villa photography.', 'image': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80'},
        {'title': 'Product Showcase', 'category': 'video', 'desc': 'Cinematic advertisement for high-end watch.', 'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80'},
    ]
    return render(request, 'website/portfolio.html', {'portfolio_items': portfolio_items})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Your message has been received! We will follow up via email soon.")
            
            # Send notification
            notify_admin(
                title=f"New Contact Inquiry: {contact.subject}",
                message=f"Received contact inquiry from {contact.name} ({contact.email}):\n\n{contact.message}"
            )
            return redirect('website:contact')
    else:
        form = ContactForm()
        
    return render(request, 'website/contact.html', {'form': form})

def faq_view(request):
    return render(request, 'website/faq.html')
