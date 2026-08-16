from django.db import models


class Job(models.Model):
    external_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=250)
    location = models.CharField(max_length=200, blank=True)
    apply_link = models.URLField(max_length=500)
    # tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated skill tags")
    description = models.TextField(blank=True)
    source = models.CharField(max_length=100, default='RemoteOK')
    posted_date = models.DateField(null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_date', '-scraped_at']

    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class BookmarkedJob(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookmarked_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} -> {self.job.job_title}"
