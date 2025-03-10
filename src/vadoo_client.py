"""
Mock Vadoo AI client for testing.
"""

class VadooAIClient:
    """Mock client for Vadoo AI video generation service."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    async def create_video(self, content: dict) -> str:
        """
        Mock video creation.
        
        Args:
            content (dict): Video content specification
            
        Returns:
            str: Mock video URL
        """
        return "https://vadoo.ai/videos/mock-video-123" 