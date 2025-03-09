# YouTube Shorts Analyzer

A powerful tool for analyzing trending YouTube Shorts and generating content insights.

## 🎥 Features

- Fetches trending YouTube Shorts from the past week
- Provides detailed engagement metrics
- AI-powered content analysis
- Script generation for similar content
- Engagement metrics visualization

## 🛠️ Technical Details

### API Usage
```python
from youtube_shorts.shorts_scraper import YouTubeShortsAnalyzer

# Initialize analyzer
analyzer = YouTubeShortsAnalyzer(api_key='your_api_key')

# Get trending shorts
trending_shorts = analyzer.get_trending_shorts(max_results=5)
```

### Data Structure
```python
short_info = {
    'title': str,          # Video title
    'description': str,    # Video description
    'channel': str,        # Channel name
    'views': int,          # View count
    'likes': int,          # Like count
    'comments': int,       # Comment count
    'published_at': str,   # Publication date
    'video_id': str,      # YouTube video ID
    'url': str            # Full video URL
}
```

## 📊 Analysis Components

### 1. Trend Detection
- Recent uploads (7 days)
- High engagement metrics
- Viral potential indicators

### 2. Content Analysis
- AI-powered topic analysis
- Engagement factor identification
- Success pattern recognition

### 3. Script Generation
- Format-specific scripts
- Trending elements incorporation
- Platform-optimized content

## 🚀 Usage Examples

### Basic Usage
```python
# Get and analyze trending shorts
trending_shorts = analyzer.get_trending_shorts()
for short in trending_shorts:
    analysis = analyze_short(short)
    script = generate_short_script(short, analysis)
```

### Custom Analysis
```python
# Analyze specific video
video_id = "your_video_id"
video_info = analyzer.get_video_details(video_id)
analysis = analyze_short(video_info)
```

## 📈 Output Examples

### Analysis Output
```
Title: "Amazing Life Hack #shorts"
Channel: "Life Hacks Daily"
Views: 1,200,000
Engagement Rate: 8.5%

Analysis:
1. Hook Type: Pattern Interrupt
2. Content Category: Tutorial
3. Viral Elements: Quick Solution, Surprise Factor
4. Target Audience: DIY Enthusiasts
```

### Script Output
```
TITLE: "5 Second Life Hack That Will Blow Your Mind"

[Opening Hook]
Fast-paced reveal of problem
Text Overlay: "Wait for it..."

[Main Content]
Quick demonstration
Visual effects highlight key moment
Sound effect on reveal

[Closing]
Call-to-action
Subscribe prompt
```

## ⚙️ Configuration

### Environment Variables
```bash
YOUTUBE_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_key
```

### Optional Parameters
```python
analyzer = YouTubeShortsAnalyzer(
    api_key='your_api_key',
    region_code='US',
    max_results=10
)
```

## 🔍 Error Handling

The scraper includes robust error handling for:
- API quota limits
- Network issues
- Invalid responses
- Rate limiting

## 📝 Logging

Detailed logging of:
- API requests
- Analysis results
- Error messages
- Performance metrics

## 🤝 Integration

### Supported Platforms
- YouTube Shorts
- TikTok (format compatibility)
- Instagram Reels (format compatibility)

### Export Formats
- JSON
- CSV
- Markdown reports
- Video scripts

## 🔄 Update Frequency

- Trend analysis: Real-time
- Content suggestions: Daily
- Performance metrics: Hourly
- API quota reset: Daily

## 📚 Dependencies

- google-api-python-client
- openai
- pandas
- requests

## 🐛 Troubleshooting

Common issues and solutions:
1. API Quota Exceeded
   - Check daily limits
   - Implement rate limiting
   - Use quota management

2. Analysis Failures
   - Verify API keys
   - Check network connection
   - Validate input data

3. Script Generation Issues
   - Review OpenAI credits
   - Check prompt formatting
   - Verify analysis data

## 🔜 Future Updates

Planned features:
1. Real-time trend monitoring
2. Advanced analytics dashboard
3. Automated content scheduling
4. Multi-platform analysis
5. AI-powered thumbnail generation 