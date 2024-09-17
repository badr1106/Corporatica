from rest_framework import serializers
from .models import ProcessedImage, TabularData, UploadedImage, ColorHistogram, SegmentationMask

class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImage
        fields = '__all__'

class TabularDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabularData
        fields = ['id', 'name', 'value', 'timestamp']

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'uploaded_at', 'processed']

class ColorHistogramSerializer(serializers.ModelSerializer):
    histogram_data = serializers.JSONField(source='get_histogram_data')

    class Meta:
        model = ColorHistogram
        fields = ['id', 'image', 'histogram_data', 'bins', 'created_at']

class SegmentationMaskSerializer(serializers.ModelSerializer):
    parameters = serializers.JSONField(source='get_parameters')

    class Meta:
        model = SegmentationMask
        fields = ['id', 'image', 'mask_image', 'algorithm', 'parameters', 'created_at']