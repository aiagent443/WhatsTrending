# WhatsTrending

A comprehensive platform for analyzing, generating, and publishing content across YouTube Shorts and TikTok, powered by AI-driven trend analysis and Vadoo AI video generation.

## Overview

WhatsTrending helps content creators:
- Analyze trending content on YouTube Shorts and TikTok
- Generate platform-optimized content using Vadoo AI
- Automate content publishing and performance tracking
- Maximize engagement through cross-platform strategies

## Features

### Trend Analysis
- Real-time trend detection for both platforms
- Engagement metrics tracking
- Performance prediction
- Cross-platform trend correlation

### Content Generation
- AI-powered script generation
- Vadoo AI video creation
- Platform-specific optimization
- Monetization compliance

### Automation
- Automated content publishing
- Multi-platform management
- Performance tracking
- Trend monitoring

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/aiagent443/WhatsTrending.git
cd WhatsTrending

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Set up environment variables
export YOUTUBE_API_KEY=your_youtube_key
export TIKTOK_API_KEY=your_tiktok_key
export VADOO_API_KEY=your_vadoo_key
```

### 3. Basic Usage
```python
from content_pipeline import ContentPipeline

# Initialize the pipeline
pipeline = ContentPipeline()

# Generate and publish content
async def main():
    # Analyze trends
    trends = await pipeline.analyze_trends()
    
    # Create content plan
    plan = pipeline.create_content_plan(trends)
    
    # Generate and publish content
    content = await pipeline.generate_content(plan)
    await pipeline.publish_content(content)
```

## Documentation

### Content Strategy
Learn how to create engaging content for each platform:
- [YouTube Shorts Strategy](docs/content_strategy/YOUTUBE_SHORTS_STRATEGY.md)
- [TikTok Strategy](docs/content_strategy/TIKTOK_STRATEGY.md)
- [Cross-Platform Strategy](docs/content_strategy/CROSS_PLATFORM_STRATEGY.md)

### Technical Implementation
Understand the technical aspects:
- [YouTube Shorts Analysis](docs/technical/YOUTUBE_SHORTS_ANALYSIS.md)
- [TikTok Analysis](docs/technical/TIKTOK_ANALYSIS.md)
- [Vadoo Integration](docs/technical/VADOO_INTEGRATION.md)

### Platform Guides
Step-by-step implementation guides:
- [YouTube Automation Guide](docs/platform_guides/YOUTUBE_AUTOMATION_GUIDE.md)
- [TikTok Automation Guide](docs/platform_guides/TIKTOK_AUTOMATION_GUIDE.md)

## Repository Structure

```
├── src/
│   ├── youtube_shorts_automation.py   # YouTube Shorts implementation
│   ├── tiktok_automation.py          # TikTok implementation
│   ├── content_pipeline.py           # Unified content pipeline
│   └── scrapers/
│       ├── youtube_shorts/           # YouTube analysis tools
│       └── tiktok/                   # TikTok analysis tools
│
├── docs/
│   ├── content_strategy/
│   │   ├── YOUTUBE_SHORTS_STRATEGY.md
│   │   ├── TIKTOK_STRATEGY.md
│   │   └── CROSS_PLATFORM_STRATEGY.md
│   ├── technical/
│   │   ├── YOUTUBE_SHORTS_ANALYSIS.md
│   │   ├── TIKTOK_ANALYSIS.md
│   │   └── VADOO_INTEGRATION.md
│   └── platform_guides/
│       ├── YOUTUBE_AUTOMATION_GUIDE.md
│       └── TIKTOK_AUTOMATION_GUIDE.md
│
├── tests/                            # Test suite
├── requirements.txt                  # Dependencies
└── README.md                         # This file
```

## Key Components

### Content Pipeline
The unified content pipeline (`src/content_pipeline.py`) manages:
- Cross-platform trend analysis
- Content planning and generation
- Platform-specific optimization
- Publishing and monitoring

### Platform-Specific Modules
1. **YouTube Shorts** (`src/youtube_shorts_automation.py`):
   - Shorts-specific trend analysis
   - Content optimization for YouTube
   - Monetization compliance
   - Performance tracking

2. **TikTok** (`src/tiktok_automation.py`):
   - TikTok trend analysis
   - Creator Rewards optimization
   - Sound and hashtag tracking
   - Engagement monitoring

### Vadoo AI Integration
- Template-based video generation
- Platform-specific formatting
- Automated rendering
- Quality assurance

## Implementation Guide

### 1. Understanding the System
1. Start with [Cross-Platform Strategy](docs/content_strategy/CROSS_PLATFORM_STRATEGY.md)
2. Review platform-specific strategies
3. Explore technical documentation

### 2. Integration Steps
1. Set up API credentials
2. Configure Vadoo AI integration
3. Implement content pipeline
4. Add platform-specific optimizations

### 3. Customization
- Modify content templates
- Adjust trend analysis parameters
- Configure posting schedules
- Set up performance monitoring

## Best Practices

### Content Creation
- Follow platform-specific guidelines
- Maintain consistent branding
- Optimize for each platform
- Track performance metrics

### Technical Implementation
- Regular API quota monitoring
- Error handling and logging
- Performance optimization
- Regular updates and maintenance

## Support

- [Issue Tracker](https://github.com/aiagent443/WhatsTrending/issues)
- [Documentation](docs/)
- [Changelog](CHANGELOG.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Last Updated: 2024* 