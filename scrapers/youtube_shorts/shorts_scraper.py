import os
from googleapiclient.discovery import build
from openai import OpenAI
import json
from datetime import datetime, timedelta
import isodate

# Initialize the OpenAI client
client = OpenAI()  # This will automatically use OPENAI_API_KEY environment variable

class YouTubeShortsAnalyzer:
    def __init__(self, api_key):
        """Initialize with YouTube API key."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def get_trending_shorts(self, max_results=10):
        """Get trending YouTube Shorts."""
        try:
            # Search for trending shorts
            request = self.youtube.search().list(
                part="snippet",
                maxResults=max_results,
                q="#shorts",
                type="video",
                videoDuration="short",  # Only short videos
                order="viewCount",  # Sort by view count
                publishedAfter=(datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'  # Last 7 days
            )
            response = request.execute()
            
            # Get detailed video information
            video_ids = [item['id']['videoId'] for item in response['items']]
            videos_request = self.youtube.videos().list(
                part="snippet,statistics",
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()
            
            # Process and return the results
            trending_shorts = []
            for video in videos_response['items']:
                short_info = {
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'channel': video['snippet']['channelTitle'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'published_at': video['snippet']['publishedAt'],
                    'video_id': video['id'],
                    'url': f"https://www.youtube.com/shorts/{video['id']}"
                }
                trending_shorts.append(short_info)
            
            # Sort by views
            trending_shorts.sort(key=lambda x: x['views'], reverse=True)
            return trending_shorts
            
        except Exception as e:
            print(f"Error fetching trending shorts: {str(e)}")
            return None

def analyze_short(short_info):
    """Use OpenAI to analyze the YouTube Short."""
    try:
        # Create a detailed prompt about the short
        prompt = f"""Analyze this trending YouTube Short:
Title: {short_info['title']}
Channel: {short_info['channel']}
Views: {short_info['views']:,}
Likes: {short_info['likes']:,}
Comments: {short_info['comments']:,}
Description: {short_info['description']}

Provide a concise analysis addressing:
1. What makes this short engaging and viral-worthy?
2. Key elements of its success (e.g., humor, music, editing style)
3. Target audience and appeal
4. Potential trends or challenges it's part of
5. Tips for creating similar successful content
Keep the analysis focused on what makes it work as a Short."""
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a YouTube Shorts content strategist who understands viral video trends and audience engagement."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in analysis phase: {str(e)}")
        return None

def generate_short_script(short_info, analysis):
    """Generate a script for a similar YouTube Short."""
    try:
        prompt = f"""Based on this successful YouTube Short and its analysis:

Original Short:
{json.dumps(short_info, indent=2)}

Analysis:
{analysis}

Create a script for a new YouTube Short that could achieve similar success. Include:
1. Visual sequence descriptions
2. Music/sound suggestions
3. Text overlays and effects
4. Transitions and hooks
5. Call-to-action

Format it specifically for YouTube Shorts (vertical, under 60 seconds).
Make it engaging and shareable while maintaining originality."""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional YouTube Shorts creator known for viral, engaging content."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating script: {str(e)}")
        return None

def main():
    """Main execution function."""
    # Get API key from environment variable
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Please set the YOUTUBE_API_KEY environment variable")
        return
    
    print("🎥 Fetching trending YouTube Shorts...")
    analyzer = YouTubeShortsAnalyzer(api_key)
    trending_shorts = analyzer.get_trending_shorts(max_results=5)  # Start with 5 shorts
    
    if trending_shorts:
        # Analyze each trending short
        for i, short in enumerate(trending_shorts, 1):
            print(f"\n{'='*50}")
            print(f"📱 Trending Short #{i}")
            print(f"Title: {short['title']}")
            print(f"Channel: {short['channel']}")
            print(f"Views: {short['views']:,}")
            print(f"URL: {short['url']}")
            
            print("\n📊 Analyzing engagement factors...")
            analysis = analyze_short(short)
            if analysis:
                print("\nAnalysis:")
                print(analysis)
                
                print("\n✍️ Generating similar short script...")
                script = generate_short_script(short, analysis)
                if script:
                    print("\nScript Concept:")
                    print(script)
                else:
                    print("Failed to generate script.")
            else:
                print("Failed to analyze short.")
            
            # Add a break between shorts
            if i < len(trending_shorts):
                print("\nPress Enter to continue to next short...")
                input()
    else:
        print("No trending shorts found.")

if __name__ == "__main__":
    main() 