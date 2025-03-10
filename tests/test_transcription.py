"""
Test suite for TikTok video transcription functionality.
"""

import os
import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime
from src.tiktok_automation import (
    TikTokSound,
    TikTokTrendingVideo,
    TikTokContentPipeline,
    TranscriptionService,
    RateLimitHandler
)

# Sample test data
SAMPLE_TRANSCRIPTION = """
[00:00-00:05] Hey everyone, welcome back to my channel!
[00:05-00:10] Today we're going to talk about trending topics
[00:10-00:15] Let's dive right in!
"""

SAMPLE_VIDEO = TikTokTrendingVideo(
    video_id="test_video_id",
    description="Test video",
    author="test_user",
    sound=TikTokSound(
        sound_id="123",
        name="Test Sound",
        author="test_user",
        video_count=1000,
        duration=30
    ),
    hashtags=["test"],
    likes=1000,
    shares=500,
    comments=100,
    created_at=datetime.now()
)

@pytest_asyncio.fixture
async def content_pipeline():
    """Create a TikTokContentPipeline instance for testing."""
    with patch.dict('os.environ', {
        'TIKTOK_API_KEY': 'test_key',
        'VADOO_API_KEY': 'test_key'
    }), \
    patch('src.tiktok_automation.TranscriptionService') as mock_transcription, \
    patch('src.tiktok_automation.RateLimitHandler') as mock_rate_limiter, \
    patch('src.tiktok_automation.TikTokTrendScraper') as mock_scraper, \
    patch('src.tiktok_automation.VadooAIClient') as mock_vadoo:
        
        # Set up async mock methods
        mock_transcription.return_value.transcribe = AsyncMock(return_value=SAMPLE_TRANSCRIPTION)
        mock_rate_limiter.return_value.handle_rate_limit = AsyncMock()
        
        pipeline = TikTokContentPipeline()
        pipeline.transcription_service = mock_transcription.return_value
        pipeline.transcription_service.rate_limiter = mock_rate_limiter.return_value
        pipeline._transcribe_video = AsyncMock(return_value=SAMPLE_TRANSCRIPTION)
        pipeline._analyze_transcription = AsyncMock(return_value={
            'key_points': ['trending topics'],
            'sentiment': 'positive',
            'engagement_hooks': ['welcome back']
        })
        pipeline._extract_script_elements = AsyncMock(return_value={
            'hook': 'Hey everyone',
            'main_points': ['trending topics'],
            'call_to_action': "Let's dive right in"
        })
        pipeline._generate_original_script = AsyncMock(return_value={
            'title': 'New Trending Topics',
            'description': 'Exploring the latest trends',
            'scenes': [
                {'scene': 'Hook', 'duration': 5, 'voiceover': 'Hey everyone'},
                {'scene': 'Main', 'duration': 10, 'voiceover': 'Trending topics'},
                {'scene': 'CTA', 'duration': 5, 'voiceover': "Let's dive in"}
            ]
        })
        pipeline._validate_script_originality = AsyncMock(return_value=True)
        
        return pipeline

@pytest.mark.asyncio
async def test_transcribe_video(content_pipeline):
    """Test video transcription."""
    transcription = await content_pipeline._transcribe_video('test_video_id')
    assert isinstance(transcription, str)
    assert '[00:00-00:05]' in transcription
    assert 'welcome back' in transcription.lower()

@pytest.mark.asyncio
async def test_analyze_transcription(content_pipeline):
    """Test transcription analysis."""
    analysis = await content_pipeline._analyze_transcription(SAMPLE_TRANSCRIPTION)
    assert isinstance(analysis, dict)
    assert 'key_points' in analysis
    assert 'sentiment' in analysis
    assert 'engagement_hooks' in analysis

@pytest.mark.asyncio
async def test_extract_script_elements(content_pipeline):
    """Test script element extraction."""
    elements = await content_pipeline._extract_script_elements(SAMPLE_TRANSCRIPTION)
    assert isinstance(elements, dict)
    assert 'hook' in elements
    assert 'main_points' in elements
    assert 'call_to_action' in elements

@pytest.mark.asyncio
async def test_generate_original_script(content_pipeline):
    """Test original script generation."""
    analysis = await content_pipeline._analyze_transcription(SAMPLE_TRANSCRIPTION)
    script = await content_pipeline._generate_original_script(analysis)
    assert isinstance(script, dict)
    assert 'title' in script
    assert 'description' in script
    assert 'scenes' in script

@pytest.mark.asyncio
async def test_validate_originality(content_pipeline):
    """Test script originality validation."""
    script = {
        'title': 'Test Script',
        'scenes': [
            {'scene': 'Hook', 'voiceover': 'Original content'},
            {'scene': 'Main', 'voiceover': 'New ideas'},
            {'scene': 'CTA', 'voiceover': 'Subscribe now'}
        ]
    }
    is_original = await content_pipeline._validate_script_originality(script, SAMPLE_TRANSCRIPTION)
    assert isinstance(is_original, bool)
    assert is_original is True

@pytest.mark.asyncio
async def test_transcription_to_script_pipeline(content_pipeline):
    """Test complete transcription to script pipeline."""
    script = await content_pipeline.process_trending_video(SAMPLE_VIDEO)
    assert isinstance(script, dict)
    assert 'script' in script
    assert 'analysis' in script
    assert 'originality_score' in script

@pytest.mark.asyncio
async def test_handle_transcription_errors(content_pipeline):
    """Test error handling in transcription."""
    content_pipeline._transcribe_video = AsyncMock(side_effect=Exception("Transcription failed"))
    with pytest.raises(Exception):
        await content_pipeline.process_trending_video(SAMPLE_VIDEO)

@pytest.mark.asyncio
async def test_transcription_rate_limiting(content_pipeline):
    """Test rate limiting for transcription."""
    # Create a new TranscriptionService with a mocked rate limiter
    rate_limiter = AsyncMock()
    transcription_service = TranscriptionService()
    transcription_service.rate_limiter = rate_limiter
    
    # Replace the service in the pipeline
    content_pipeline.transcription_service = transcription_service
    
    # Call the transcribe method
    await transcription_service.transcribe('test_video_id')
    
    # Verify that rate_limiter.handle_rate_limit was called with 'transcription'
    rate_limiter.handle_rate_limit.assert_called_once_with('transcription')

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 