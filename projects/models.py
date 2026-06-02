from django.db import models
from bookings.models import Booking

class Project(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='project')
    assigned_team = models.TextField(blank=True, help_text="Assigned crew and team members")
    start_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(blank=True, null=True)
    progress_percentage = models.IntegerField(default=0, help_text="Value between 0 and 100")
    notes = models.TextField(blank=True, help_text="Notes/Comments visible to client")

    def __str__(self):
        return f"Project: {self.booking.project_title} ({self.progress_percentage}%)"

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='deliverables/')
    file_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.file_name and self.file:
            self.file_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name} for Project: {self.project.booking.project_title}"
