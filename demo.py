"""
Demo script to showcase the TikTok trend analysis and content generation system.
"""

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from src.tiktok_automation import (
    TikTokContentPipeline,
    TikTokContentType,
    TikTokSound,
    TikTokHashtag,
    TikTokTrendingVideo
)

async def main():
    """Run a demonstration of the TikTok automation system."""
    # Load environment variables
    load_dotenv()
    
    # Initialize the pipeline
    pipeline = TikTokContentPipeline()
    
    # Set content type to tutorial
    pipeline.set_content_type(TikTokContentType.TUTORIAL)
    
    try:
        # Step 1: Analyze current trends
        print("\n🔍 Analyzing TikTok trends...")
        trends = await pipeline.analyze_trends()
        
        print("\n📊 Trend Analysis Results:")
        print(f"Top Trending Hashtag: {trends['analysis']['top_trend']}")
        print("\nEngagement Metrics:")
        print(f"- Average Likes: {trends['analysis']['engagement_metrics']['average_likes']:.0f}")
        print(f"- Average Shares: {trends['analysis']['engagement_metrics']['average_shares']:.0f}")
        print(f"- Average Comments: {trends['analysis']['engagement_metrics']['average_comments']:.0f}")
        
        # Step 2: Generate content based on trends
        print("\n✍️ Generating content...")
        content = await pipeline.generate_content()
        
        print("\n🎥 Generated Video Details:")
        print(f"Video URL: {content['video_url']}")
        print("\nMetadata:")
        print(f"- Title: {content['metadata']['title']}")
        print(f"- Description: {content['metadata']['description']}")
        print(f"- Hashtags: {', '.join(content['metadata']['hashtags'])}")
        
        # Step 3: Process a trending video for inspiration
        print("\n🎬 Processing trending video for inspiration...")
        sample_video = TikTokTrendingVideo(
            video_id="test123",
            description="Amazing life hack that will change your morning routine!",
            author="trending_creator",
            sound=TikTokSound(
                sound_id="sound123",
                name="Original Sound",
                author="trending_creator",
                video_count=50000,
                duration=45
            ),
            hashtags=["lifehack", "morningroutine", "productivity"],
            likes=100000,
            shares=25000,
            comments=5000,
            created_at=datetime.now()
        )
        
        analysis = await pipeline.process_trending_video(sample_video)
        
        print("\n📝 Video Analysis Results:")
        print("Script Structure:")
        for scene in analysis['script']['scenes']:
            print(f"- {scene['scene']} ({scene['duration']}s): {scene['voiceover']}")
        
        print(f"\nOriginality Score: {analysis['originality_score']:.2f}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 