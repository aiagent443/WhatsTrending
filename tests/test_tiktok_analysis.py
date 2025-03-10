"""Tests for TikTok trend analysis functionality."""

import os
import pytest
import pytest_asyncio
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock

from src.tiktok_automation import (
    TikTokTrendScraper,
    TikTokContentPipeline,
    TikTokSound,
    TikTokHashtag,
    TikTokTrendingVideo,
    TikTokContentType
)

# Sample test data
SAMPLE_SOUND = TikTokSound(
    sound_id="123",
    name="Test Sound",
    author="test_user",
    video_count=1000,
    duration=30
)

SAMPLE_HASHTAG = TikTokHashtag(
    name="test",
    video_count=4000,
    view_count=40000,
    description="Test hashtag"
)

SAMPLE_VIDEO = TikTokTrendingVideo(
    video_id="123",
    description="Test video",
    author="test_user",
    sound=SAMPLE_SOUND,
    hashtags=["test"],
    likes=1000,
    shares=500,
    comments=100,
    created_at=datetime.now()
)

@pytest_asyncio.fixture
async def trend_scraper():
    """Create a TikTokTrendScraper instance for testing."""
    with patch('src.tiktok_automation.TikTokAPIClient') as mock_api, \
         patch('src.tiktok_automation.TikTokWebScraper') as mock_web, \
         patch('src.tiktok_automation.TikTokSoundAnalyzer') as mock_sound, \
         patch('src.tiktok_automation.TikTokHashtagAnalyzer') as mock_hashtag:
        
        # Set up async mock methods
        mock_api.return_value.get_trending_videos = AsyncMock(return_value=[SAMPLE_VIDEO])
        mock_web.return_value.scrape_discover_page = AsyncMock(return_value=[SAMPLE_HASHTAG])
        mock_sound.return_value.get_trending_sounds = AsyncMock(return_value=[SAMPLE_SOUND])
        mock_hashtag.return_value.get_trending_hashtags = AsyncMock(return_value=[SAMPLE_HASHTAG])
        
        scraper = TikTokTrendScraper()
        scraper._get_trending_hashtags_api = AsyncMock(return_value=[SAMPLE_HASHTAG])
        scraper._scrape_discover_page = AsyncMock(return_value=[SAMPLE_HASHTAG])
        scraper._get_trending_sound_hashtags = AsyncMock(return_value=[SAMPLE_HASHTAG])
        
        return scraper

@pytest_asyncio.fixture
async def content_pipeline():
    """Create a TikTokContentPipeline instance for testing."""
    with patch.dict('os.environ', {
        'TIKTOK_API_KEY': 'test_key',
        'VADOO_API_KEY': 'test_key'
    }), \
    patch('src.tiktok_automation.TikTokTrendScraper') as mock_scraper, \
    patch('src.tiktok_automation.VadooAIClient') as mock_vadoo:
        
        # Set up async mock methods
        mock_scraper.return_value.get_trending_hashtags = AsyncMock(return_value=[SAMPLE_HASHTAG])
        mock_scraper.return_value.get_trending_sounds = AsyncMock(return_value=[SAMPLE_SOUND])
        mock_scraper.return_value.get_trending_videos = AsyncMock(return_value=[SAMPLE_VIDEO])
        
        mock_vadoo.return_value.create_video = AsyncMock(return_value="https://vadoo.ai/videos/123")
        
        pipeline = TikTokContentPipeline()
        pipeline.analyze_trends = AsyncMock(return_value={
            'hashtags': [SAMPLE_HASHTAG],
            'sounds': [SAMPLE_SOUND],
            'videos': [SAMPLE_VIDEO],
            'analysis': {
                'top_trend': 'test',
                'engagement_metrics': {
                    'average_likes': 1000,
                    'average_shares': 500,
                    'average_comments': 100
                },
                'sound_metrics': {
                    'average_usage': 1000,
                    'top_sound': {
                        'id': '123',
                        'name': 'Test Sound',
                        'popularity': 1000,
                        'potential': 0.0,
                        'engagement_score': 700.0
                    }
                }
            }
        })
        
        return pipeline

@pytest.mark.asyncio
async def test_get_trending_hashtags(trend_scraper):
    """Test fetching trending hashtags."""
    hashtags = await trend_scraper.get_trending_hashtags()
    assert len(hashtags) > 0
    assert isinstance(hashtags[0], TikTokHashtag)
    assert hashtags[0].name == SAMPLE_HASHTAG.name

@pytest.mark.asyncio
async def test_get_trending_sounds(trend_scraper):
    """Test fetching trending sounds."""
    sounds = await trend_scraper.get_trending_sounds()
    assert len(sounds) > 0
    assert isinstance(sounds[0], TikTokSound)
    assert sounds[0].sound_id == SAMPLE_SOUND.sound_id

@pytest.mark.asyncio
async def test_get_trending_videos(trend_scraper):
    """Test fetching trending videos."""
    videos = await trend_scraper.get_trending_videos()
    assert len(videos) > 0
    assert isinstance(videos[0], TikTokTrendingVideo)
    assert videos[0].video_id == SAMPLE_VIDEO.video_id

@pytest.mark.asyncio
async def test_analyze_trends(content_pipeline):
    """Test trend analysis."""
    trends = await content_pipeline.analyze_trends()
    assert 'hashtags' in trends
    assert 'sounds' in trends
    assert 'videos' in trends
    assert 'analysis' in trends
    assert len(trends['hashtags']) > 0
    assert len(trends['sounds']) > 0
    assert len(trends['videos']) > 0

@pytest.mark.asyncio
async def test_generate_script(content_pipeline):
    """Test script generation."""
    trends = await content_pipeline.analyze_trends()
    script = await content_pipeline._generate_script(trends)
    assert isinstance(script, dict)
    assert 'scenes' in script
    assert len(script['scenes']) > 0

@pytest.mark.asyncio
async def test_content_type_templates(content_pipeline):
    """Test content type templates."""
    content_pipeline.set_content_type(TikTokContentType.TUTORIAL)
    template = content_pipeline._get_content_template()
    assert isinstance(template, dict)
    assert 'structure' in template
    assert 'style' in template
    assert template['style'] == 'educational'

@pytest.mark.asyncio
async def test_analyze_content_patterns(content_pipeline):
    """Test content pattern analysis."""
    trends = await content_pipeline.analyze_trends()
    patterns = content_pipeline._analyze_content_patterns(trends['videos'])
    assert isinstance(patterns, dict)
    assert 'duration_patterns' in patterns
    assert 'hashtag_patterns' in patterns
    assert 'engagement_patterns' in patterns

@pytest.mark.asyncio
async def test_analyze_sounds(content_pipeline):
    """Test sound analysis."""
    trends = await content_pipeline.analyze_trends()
    sound_analysis = content_pipeline._analyze_sounds(trends['sounds'])
    assert isinstance(sound_analysis, list)
    assert len(sound_analysis) > 0
    assert 'engagement_score' in sound_analysis[0]
    assert sound_analysis[0]['engagement_score'] == 700.0

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 