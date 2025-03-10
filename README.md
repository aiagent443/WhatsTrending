# WhatsTrending - Cross-Platform Content Analysis & Generation System

## Overview
WhatsTrending is a sophisticated Python-based system that analyzes trends and automates content generation across multiple platforms. The system leverages both TikTok and YouTube Shorts APIs along with web scraping capabilities to identify trending content, analyze patterns, and generate optimized cross-platform content.

## Current Status
- ✅ TikTok Integration: All tests passing (16/16 tests successful)
- 🔄 TikTok API integration ready (pending API key approval)
- 🚀 Mock data implementation available for development
- 💡 YouTube Shorts integration maintained and functional

## Features

### Cross-Platform Analysis
- 🔄 **Unified Content Strategy**
  - Cross-platform trend correlation
  - Platform-specific optimization
  - Engagement comparison
  - Content adaptation

### Platform-Specific Features

#### TikTok
- 🔍 **Trend Analysis**
  - Hashtag tracking and analysis
  - Sound trend identification
  - Engagement metrics calculation
  - Content pattern recognition

- 🎥 **Content Generation**
  - Script generation based on trends
  - Content structure optimization
  - Engagement prediction
  - Originality scoring

#### YouTube Shorts
- 📊 **Analytics Integration**
  - View count tracking
  - Audience retention analysis
  - Engagement metrics
  - Monetization tracking

- 🎬 **Content Optimization**
  - SEO optimization
  - Thumbnail generation
  - Description optimization
  - Tag recommendations

### Shared Features
- 🤖 **Automation**
  - Rate limiting and request management
  - Asynchronous operations
  - Error handling and logging
  - Session management

## System Architecture

### Core Components
1. **Platform Clients**
   - TikTokAPIClient
   - YouTubeShortsClient
   - Authentication management
   - Rate limiting implementation

2. **Web Scrapers**
   - Platform-specific data extraction
   - Intelligent scraping patterns
   - Rate limiting handling

3. **ContentPipeline**
   - Cross-platform content processing
   - Multi-platform optimization
   - Engagement analysis
   - Transcription services

4. **Analysis Tools**
   - Sound/Audio analysis
   - Hashtag/Tag analysis
   - Cross-platform trend correlation
   - Unified metrics calculation

## Setup

### Prerequisites
- Python 3.8+
- Chrome/Chromium (for web scraping)
- Poetry (recommended for dependency management)

### Environment Variables
```env
# TikTok Configuration
TIKTOK_API_KEY=your_tiktok_key  # Currently pending approval
VADOO_API_KEY=your_vadoo_key    # For transcription services

# YouTube Configuration
YOUTUBE_API_KEY=your_youtube_key
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/WhatsTrending.git

# Install dependencies
poetry install

# Or using pip
pip install -r requirements.txt
```

## Testing
The system includes comprehensive test coverage for all platforms:
- Unit tests for all core components
- Integration tests for the pipeline
- Mock data tests for API-dependent features

To run tests:
```bash
PYTHONPATH=$PYTHONPATH:. python -m pytest tests/ -v
```

Current test status:
- ✅ TikTok Analysis Tests (8/8 passed)
- ✅ Transcription Tests (8/8 passed)
- ✅ YouTube Shorts Tests (maintained)
- 🔄 All async/await patterns properly implemented
- 🔄 Rate limiting correctly handled

## Demo
A demo script is provided to showcase the system's capabilities:
```python
python demo.py
```

The demo demonstrates:
1. Cross-platform trend analysis
2. Content generation for both platforms
3. Video processing and optimization
4. Engagement metrics calculation

## Development Status

### Completed Features
- ✅ Async/await implementation
- ✅ Rate limiting system
- ✅ Mock data integration
- ✅ Test suite
- ✅ Content pipeline
- ✅ Cross-platform trend analysis

### Pending
- 🔄 TikTok API key approval
- 🔄 Production data integration
- 🔄 Advanced analytics dashboard

## Best Practices
- Async operations for optimal performance
- Rate limiting for API compliance
- Comprehensive error handling
- Extensive logging
- Mock data for development
- Cross-platform optimization

## Notes for Development
- TikTok: Using mock data while awaiting API approval
- YouTube: Full API integration available
- All tests passing with current implementation
- System ready for production data integration
- Scalable architecture in place

## Future Enhancements
1. Real-time trend monitoring across platforms
2. AI-powered content optimization
3. Advanced analytics dashboard
4. Batch processing capabilities
5. Content performance prediction
6. Cross-platform content scheduling

## Contributing
Contributions are welcome! Please read our contributing guidelines and submit pull requests for any enhancements.

## License
[Your License Type] - See LICENSE file for details 