from typing import Type, List
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import os
import requests
from datetime import datetime


class VideoDetails(BaseModel):

    title: str
    view_count: int
    like_count: int
    comment_count: int
    channel_subscriber_count: int
    video_description: str
    video_tags: List[str]
    upload_date: datetime
    channel_name: str
    total_video_count: int
    current_date: str


class YoutubeVideoDetailsToolInput(BaseModel):
    """Input for YoutubeVideoDetailsTool."""

    video_id: str = Field(..., description="The ID of the YouTube video.")


class YoutubeVideoDetailsTool(BaseTool):
    name: str = "Get YouTube Video Details"
    description: str = "Retrieves details for a specific YouTube video."
    args_schema: Type[BaseModel] = YoutubeVideoDetailsToolInput

    def _run(self, video_id: str) -> VideoDetails:
        try:
            api_key = os.getenv("YOUTUBE_API_KEY")
            video_url = "https://www.googleapis.com/youtube/v3/videos"
            video_params = {
                "part": "snippet,statistics",
                "id": video_id,
                "key": api_key,
            }

            current_date = datetime.now().strftime("%B %d, %Y")
            video_response = requests.get(video_url, params=video_params)
            video_response.raise_for_status()
            video_items = video_response.json().get("items", [])

            if not video_items:
                raise ValueError(
                    f"No video found for the provided video ID: {video_id}"
                )

            video_item = video_items[0]

            title = video_item["snippet"]["title"]
            video_description = video_item["snippet"]["description"]
            video_tags = video_item["snippet"].get("tags", [])
            view_count = int(video_item["statistics"]["viewCount"])
            like_count = int(video_item["statistics"].get("likeCount", 0))
            comment_count = int(video_item["statistics"].get("commentCount", 0))

            channel_id = video_item["snippet"]["channelId"]
            channel_url = "https://www.googleapis.com/youtube/v3/channels"
            channel_params = {
                "part": "statistics,snippet",
                "id": channel_id,
                "key": api_key,
            }
            channel_response = requests.get(channel_url, params=channel_params)
            channel_response.raise_for_status()
            channel_items = channel_response.json().get("items", [])

            if not channel_items:
                raise ValueError(
                    f"No channel found for the provided channel ID: {channel_id}"
                )

            channel_item = channel_items[0]

            channel_subscriber_count = int(
                channel_item["statistics"]["subscriberCount"]
            )
            channel_name = channel_item["snippet"]["title"]
            total_video_count = int(channel_item["statistics"]["videoCount"])

            upload_date_str = video_item["snippet"]["publishedAt"]
            upload_date = datetime.fromisoformat(upload_date_str.replace("Z", "+00:00"))

            # Limit the description length to 200 characters
            max_description_length = 200
            if len(video_description) > max_description_length:
                video_description = video_description[:max_description_length] + "..."

            return VideoDetails(
                title=title,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                channel_subscriber_count=channel_subscriber_count,
                video_description=video_description,
                video_tags=video_tags,
                upload_date=upload_date,
                channel_name=channel_name,
                total_video_count=total_video_count,
                current_date=current_date,
            )
        except Exception as e:
            return f"An error occurred while fetching video details: {str(e)}"
