from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Project, ProjectFile
from .forms import ProjectForm, ProjectFileForm
from notifications.utils import trigger_notification

@login_required
def project_update(request, project_id):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can edit project parameters.")
        return redirect('dashboard:home')
        
    project = get_object_or_404(Project, id=project_id)
    booking = project.booking
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            prev_progress = project.progress_percentage
            updated_project = form.save(commit=False)
            
            # Auto update states when completion hits 100%
            if updated_project.progress_percentage == 100:
                booking.status = 'Completed'
                booking.save()
            elif updated_project.progress_percentage < 100 and booking.status == 'Completed':
                booking.status = 'In Progress'
                booking.save()
                
            updated_project.save()
            messages.success(request, f"Project '{booking.project_title}' updated successfully.")
            
            # Trigger updates alert to clients
            if updated_project.progress_percentage != prev_progress:
                trigger_notification(
                    user=booking.client,
                    title="Project Progress Milestone Updated",
                    message=f"Your project '{booking.project_title}' has reached {updated_project.progress_percentage}%. Read admin notes inside the portal.",
                    send_email=True
                )
                
            if updated_project.progress_percentage == 100 and prev_progress != 100:
                trigger_notification(
                    user=booking.client,
                    title="Project Completed!",
                    message=f"Production on '{booking.project_title}' is fully complete (100%). Final assets are ready for download.",
                    send_email=True
                )
                
            return redirect('bookings:detail', booking_id=booking.booking_id)
    else:
        form = ProjectForm(instance=project)
        
    return render(request, 'projects/project_form.html', {
        'form': form,
        'project': project,
        'booking': booking
    })

@login_required
def project_upload_file(request, project_id):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can upload deliverables.")
        return redirect('dashboard:home')
        
    project = get_object_or_404(Project, id=project_id)
    booking = project.booking
    
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project_file = form.save(commit=False)
            project_file.project = project
            project_file.save()
            
            # Automatically update booking status to Delivered if it was completed
            if booking.status == 'Completed':
                booking.status = 'Delivered'
                booking.save()
                
            messages.success(request, f"Deliverable asset '{project_file.file_name}' uploaded successfully!")
            
            # Notify client
            trigger_notification(
                user=booking.client,
                title="New Deliverable Asset Available",
                message=f"A new visual asset '{project_file.file_name}' is ready for download in your dashboard panel.",
                send_email=True
            )
    else:
        messages.error(request, "Invalid action request.")
        
    return redirect('bookings:detail', booking_id=booking.booking_id)

@login_required
def project_delete_file(request, file_id):
    if request.user.role != 'admin':
        messages.error(request, "Access denied. Only administrators can delete deliverables.")
        return redirect('dashboard:home')
        
    project_file = get_object_or_404(ProjectFile, id=file_id)
    booking_id = project_file.project.booking.booking_id
    file_name = project_file.file_name
    
    project_file.file.delete(save=False)
    project_file.delete()
    
    messages.success(request, f"Asset '{file_name}' has been successfully deleted.")
    return redirect('bookings:detail', booking_id=booking_id)
