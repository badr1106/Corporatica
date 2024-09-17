import os
import cv2
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.decorators import api_view, parser_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
import torch
from transformers import pipeline
from .models import ProcessedImage, TabularData, UploadedImage, ColorHistogram, SegmentationMask
from .serializers import (
    ProcessedImageSerializer, TabularDataSerializer, UploadedImageSerializer,
    ColorHistogramSerializer, SegmentationMaskSerializer
)
from .image_processing import generate_color_histogram, generate_segmentation_mask
from .image_manipulation import resize_image, crop_image, convert_image_format
from .text_analysis import summarize_text, extract_keywords, analyze_sentiment
from .text_processing import search_text, categorize_text, custom_query

device = 0 if torch.cuda.is_available() else -1

class ProcessedImageViewSet(viewsets.ModelViewSet):
    queryset = ProcessedImage.objects.all()
    serializer_class = ProcessedImageSerializer

class TabularDataViewSet(viewsets.ModelViewSet):
    queryset = TabularData.objects.all()
    serializer_class = TabularDataSerializer

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        if not images:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_images = []
        for image in images:
            serializer = UploadedImageSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save()
                uploaded_images.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(uploaded_images, status=status.HTTP_201_CREATED)

class ColorHistogramView(APIView):
    def post(self, request, image_id):
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        bins = request.data.get('bins', 256)
        histogram_data = generate_color_histogram(image.image.path, bins=bins)
        
        histogram = ColorHistogram.objects.create(image=image, bins=bins)
        histogram.set_histogram_data(histogram_data)
        histogram.save()

        serializer = ColorHistogramSerializer(histogram)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SegmentationMaskView(APIView):
    def post(self, request, image_id):
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        algorithm = request.data.get('algorithm', 'slic')
        parameters = request.data.get('parameters', {})

        mask = generate_segmentation_mask(image.image.path, algorithm=algorithm, **parameters)
        
        mask_filename = f"mask_{image_id}_{algorithm}.png"
        mask_path = os.path.join('segmentation_masks', mask_filename)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, mask_path), mask)

        segmentation_mask = SegmentationMask.objects.create(
            image=image,
            mask_image=mask_path,
            algorithm=algorithm
        )
        segmentation_mask.set_parameters(parameters)
        segmentation_mask.save()

        serializer = SegmentationMaskSerializer(segmentation_mask)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ResizeImageView(APIView):
    def post(self, request, image_id):
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        width = int(request.data.get('width'))
        height = int(request.data.get('height'))
        output_path = os.path.join(settings.MEDIA_ROOT, f"resized_{image_id}.jpg")
        resize_image(image.image.path, output_path, width, height)

        return Response({"message": "Image resized successfully", "output_path": output_path}, status=status.HTTP_200_OK)

class CropImageView(APIView):
    def post(self, request, image_id):
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        left = int(request.data.get('left'))
        top = int(request.data.get('top'))
        right = int(request.data.get('right'))
        bottom = int(request.data.get('bottom'))
        output_path = os.path.join(settings.MEDIA_ROOT, f"cropped_{image_id}.jpg")
        crop_image(image.image.path, output_path, left, top, right, bottom)

        return Response({"message": "Image cropped successfully", "output_path": output_path}, status=status.HTTP_200_OK)

class ConvertImageFormatView(APIView):
    def post(self, request, image_id):
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

        format = request.data.get('format')
        output_path = os.path.join(settings.MEDIA_ROOT, f"converted_{image_id}.{format.lower()}")
        convert_image_format(image.image.path, output_path, format)

        return Response({"message": "Image format converted successfully", "output_path": output_path}, status=status.HTTP_200_OK)

class TextSummarizationView(APIView):
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        summary = summarize_text(text)
        return Response({"summary": summary}, status=status.HTTP_200_OK)

class KeywordExtractionView(APIView):
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        keywords = extract_keywords(text)
        return Response({"keywords": keywords}, status=status.HTTP_200_OK)

class SentimentAnalysisView(APIView):
    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        sentiment = analyze_sentiment(text)
        return Response({"sentiment": sentiment}, status=status.HTTP_200_OK)

class TextSearchView(APIView):
    def post(self, request):
        text = request.data.get('text')
        query = request.data.get('query')
        if not text or not query:
            return Response({"error": "Text and query are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        results = search_text(text, query)
        return Response({"results": results}, status=status.HTTP_200_OK)

class TextCategorizationView(APIView):
    def post(self, request):
        text = request.data.get('text')
        categories = request.data.get('categories')
        if not text or not categories:
            return Response({"error": "Text and categories are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        result = categorize_text(text, categories)
        return Response({"result": result}, status=status.HTTP_200_OK)

class CustomQueryView(APIView):
    def post(self, request):
        text = request.data.get('text')
        query = request.data.get('query')
        if not text or not query:
            return Response({"error": "Text and query are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        results = custom_query(text, query)
        return Response({"results": results}, status=status.HTTP_200_OK)
    
class AnalyzeTabularDataView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            df = pd.DataFrame(data['data'])
            analysis = {
                "mean": df.mean().to_dict(),
                "median": df.median().to_dict(),
                "mode": df.mode().iloc[0].to_dict(),
                "quartiles": df.quantile([0.25, 0.5, 0.75]).to_dict(),
                "outliers": df.apply(lambda x: np.abs(x - x.mean()) > 3*x.std()).sum().to_dict()
            }
            return Response(analysis, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AnalyzeImageView(APIView):
    parser_classes = [FileUploadParser]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file']
            image = Image.open(file)
            
            histogram = image.histogram()
            
            gray_image = image.convert('L')
            threshold = 128
            segmented = gray_image.point(lambda p: p > threshold and 255)
            
            buffered = io.BytesIO()
            segmented.save(buffered, format="PNG")
            segmented_base64 = base64.b64encode(buffered.getvalue()).decode()

            return Response({
                "histogram": histogram,
                "segmented_image": segmented_base64
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AnalyzeTextView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            text = data.get('text', '')
            
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
            summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

            sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=device)
            sentiment = sentiment_analyzer(text)[0]

            return Response({
                "summary": summary[0]['summary_text'],
                "sentiment": sentiment['label'],
                "sentiment_score": sentiment['score']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReadRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello World"}, status=status.HTTP_200_OK)

class ColorHistogramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ColorHistogram.objects.all()
    serializer_class = ColorHistogramSerializer

class SegmentationMaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SegmentationMask.objects.all()
    serializer_class = SegmentationMaskSerializer
