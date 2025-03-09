# WhatsTrending - Social Media Trend Analyzer

A powerful tool suite for analyzing and generating content based on trending social media topics. Currently supports YouTube Shorts analysis and Google Trends tracking.

## 🚀 Features

### YouTube Shorts Analyzer
- Fetches trending YouTube Shorts from the past week
- Provides detailed engagement analytics (views, likes, comments)
- Uses AI to analyze viral elements and success factors
- Generates custom short-form video scripts based on trending content
- Includes engagement metrics and content strategy insights

### Google Trends Analyzer (Archive)
- Tracks trending topics from Google Trends
- Analyzes social media impact and virality
- Generates creative content ideas based on trends

## 📋 Requirements

- Python 3.8+
- YouTube Data API v3 key
- OpenAI API key
- Required Python packages (see requirements.txt)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WhatsTrending.git
cd WhatsTrending
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your API keys:
```bash
export YOUTUBE_API_KEY='your_youtube_api_key'
export OPENAI_API_KEY='your_openai_api_key'
```

## 📊 Usage

### YouTube Shorts Analysis
```bash
python scrapers/youtube_shorts/shorts_scraper.py
```

This will:
- Fetch top trending YouTube Shorts
- Analyze engagement factors
- Generate similar content ideas
- Provide detailed analytics reports

## 📁 Repository Structure

```
WhatsTrending/
├── scrapers/
│   ├── youtube_shorts/
│   │   ├── shorts_scraper.py
│   │   └── README.md
│   └── google_trends/
│       └── trends_scraper.py
├── docs/
│   ├── YOUTUBE_ANALYSIS.md
│   └── CONTENT_STRATEGY.md
├── requirements.txt
└── README.md
```

## 📈 Analysis Documentation

- See [YOUTUBE_ANALYSIS.md](docs/YOUTUBE_ANALYSIS.md) for detailed YouTube Shorts analysis methodology
- See [CONTENT_STRATEGY.md](docs/CONTENT_STRATEGY.md) for content creation strategies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Data API
- OpenAI GPT-4
- Google Trends API 