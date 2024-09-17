from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProcessedImageViewSet, TabularDataViewSet, ImageUploadView, UploadedImageViewSet,
    ColorHistogramView, SegmentationMaskView, ColorHistogramViewSet, SegmentationMaskViewSet,
    ResizeImageView, CropImageView, ConvertImageFormatView,
    TextSummarizationView, KeywordExtractionView, SentimentAnalysisView,
    TextSearchView, TextCategorizationView, CustomQueryView,
    AnalyzeImageView,
    AnalyzeTabularDataView,
    AnalyzeTextView
)

router = DefaultRouter()
router.register(r'processed-images', ProcessedImageViewSet)
router.register(r'tabular-data', TabularDataViewSet)
router.register(r'uploaded-images', UploadedImageViewSet)
router.register(r'color-histograms', ColorHistogramViewSet)
router.register(r'segmentation-masks', SegmentationMaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', ImageUploadView.as_view(), name='upload_images'),
    path('color-histogram/<int:image_id>/', ColorHistogramView.as_view(), name='color_histogram'),
    path('segmentation-mask/<int:image_id>/', SegmentationMaskView.as_view(), name='segmentation_mask'),
    path('resize-image/<int:image_id>/', ResizeImageView.as_view(), name='resize_image'),
    path('crop-image/<int:image_id>/', CropImageView.as_view(), name='crop_image'),
    path('convert-image-format/<int:image_id>/', ConvertImageFormatView.as_view(), name='convert_image_format'),
    path('text-summarization/', TextSummarizationView.as_view(), name='text_summarization'),
    path('keyword-extraction/', KeywordExtractionView.as_view(), name='keyword_extraction'),
    path('sentiment-analysis/', SentimentAnalysisView.as_view(), name='sentiment_analysis'),
    path('text-search/', TextSearchView.as_view(), name='text_search'),
    path('text-categorization/', TextCategorizationView.as_view(), name='text_categorization'),
    path('custom-query/', CustomQueryView.as_view(), name='custom_query'),
    path('api/image/analyze', AnalyzeImageView.as_view(), name='analyze_image'),
    path('api/tabular/analyze', AnalyzeTabularDataView.as_view(), name='analyze_tabular_data'),
    path('api/text/analyze', AnalyzeTextView.as_view(), name='analyze_text'),
]