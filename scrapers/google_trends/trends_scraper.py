import requests
from pytrends.request import TrendReq
from openai import OpenAI
import os
from datetime import datetime, timedelta
import time
import pandas as pd

# Initialize the OpenAI client
client = OpenAI()  # This will automatically use OPENAI_API_KEY environment variable

def get_top_trending_topics(max_retries=3):
    """Get top trending topics from Google Trends focusing on viral social media content."""
    for attempt in range(max_retries):
        try:
            # Initialize pytrends
            pytrends = TrendReq(hl='en-US', tz=360)
            
            # Get real-time trending searches
            trending = pytrends.realtime_trending_searches(pn='US')
            
            if not trending.empty:
                # Filter for entertainment and viral content
                entertainment_keywords = ['music', 'song', 'dance', 'tiktok', 'instagram', 'youtube', 
                                       'viral', 'trend', 'challenge', 'movie', 'celebrity', 'star', 
                                       'performance', 'concert', 'video']
                
                # Look through trending topics for entertainment-related content
                for _, row in trending.iterrows():
                    title = row['title'].lower()
                    if any(keyword in title for keyword in entertainment_keywords):
                        return row['title']
                
                # If no entertainment topics found, return the top trending topic
                return trending.iloc[0]['title']
            
            print("No trending topics found, retrying...")
            time.sleep(2)  # Wait 2 seconds before retrying
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                print(f"Error fetching trending topics after {max_retries} attempts: {str(e)}")
                # Fallback to current viral trends
                return "Taylor Swift Eras Tour Movie"
    
    return None

def deep_research(topic):
    """Use OpenAI to research the trending topic with focus on social media virality."""
    try:
        prompt = f"""Analyze the viral trend/topic '{topic}' with a focus on social media impact.
        Provide a concise summary addressing:
        1. What is this trend/topic about?
        2. Why is it going viral on social media?
        3. Which platforms (TikTok/Instagram/YouTube) is it most popular on?
        4. Key elements making it viral (e.g., music, dance, challenge, meme format)
        5. Notable creators or celebrities involved
        6. Cultural impact and engagement levels
        Keep the response focused on social media relevance and viral aspects."""
        
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a social media trends analyst specializing in viral content and internet culture."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in research phase: {str(e)}")
        return None

def generate_film_script(topic, research_summary):
    """Generate a short film script about the viral trend/topic."""
    try:
        prompt = f"""Write a compelling 1-minute social media style video script about '{topic}' based on this context: {research_summary}

Format as a modern social media video script with:
- Quick, engaging scenes (TikTok/Reels style)
- Trendy music suggestions
- Visual effects and transitions
- On-screen text moments
- Viral-worthy hooks and moments
- Keep it dynamic and shareable (60 seconds max)

Focus on creating content that could actually go viral on social media platforms."""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a viral content creator known for producing trending social media videos."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating script: {str(e)}")
        return None

def main():
    """Main execution function."""
    print("🔍 Fetching viral trends from the past week...")
    trending_topic = get_top_trending_topics()
    
    if trending_topic:
        print(f"\n🚀 Viral Trend: {trending_topic}")
        
        print("\n📱 Analyzing social media impact...")
        research_summary = deep_research(trending_topic)
        if research_summary:
            print("\nTrend Analysis:")
            print(research_summary)
            
            print("\n🎥 Generating viral video script...")
            script = generate_film_script(trending_topic, research_summary)
            if script:
                print("\nVideo Script:")
                print(script)
            else:
                print("Failed to generate script.")
        else:
            print("Failed to analyze trend.")
    else:
        print("No viral trends found.")

if __name__ == "__main__":
    main()

