from django.db import models
import json

class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/')
    processing_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.processing_type} - {self.created_at}"

class TabularData(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.value}"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

class ColorHistogram(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='color_histograms')
    histogram_data = models.TextField() 
    bins = models.IntegerField(default=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_histogram_data(self, data):
        self.histogram_data = json.dumps(data)

    def get_histogram_data(self):
        return json.loads(self.histogram_data)

class SegmentationMask(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='segmentation_masks')
    mask_image = models.ImageField(upload_to='segmentation_masks/')
    algorithm = models.CharField(max_length=50)
    parameters = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def set_parameters(self, params):
        self.parameters = json.dumps(params)

    def get_parameters(self):
        return json.loads(self.parameters)