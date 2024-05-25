# models.py

from django.db import models

class SQLFile(models.Model):
    file = models.FileField(upload_to='sql_files')
    content = models.TextField(blank=True)  # İsteğe bağlı: Boş bırakabilirsiniz.
    uploaded_at = models.DateTimeField(auto_now_add=True)
