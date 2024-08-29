from typing import Type, List
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import os
import requests


class CommentDetails(BaseModel):
    text: str
    author: str
    like_count: int


class YoutubeCommentThreadsToolInput(BaseModel):
    """Input for YoutubeCommentThreadsTool."""

    video_id: str = Field(..., description="The ID of the YouTube video.")
    max_results: int = Field(30, description="The maximum number of results to return.")


class YoutubeCommentThreadsTool(BaseTool):
    name: str = "Get YouTube Comment Threads"
    description: str = "Retrieves comment threads for a specific YouTube video."
    args_schema: Type[BaseModel] = YoutubeCommentThreadsToolInput

    def _run(self, video_id: str, max_results: int = 30) -> List[CommentDetails]:
        try:
            api_key = os.getenv("YOUTUBE_API_KEY")
            url = "https://www.googleapis.com/youtube/v3/commentThreads"
            params = {
                "part": "snippet,replies",
                "maxResults": max_results,
                "videoId": video_id,
                "key": api_key,
                "order": "relevance",
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            items = response.json().get("items", [])

            comment_threads = []

            for item in items:
                top_level_comment = item["snippet"]["topLevelComment"]["snippet"]
                comment_details = CommentDetails(
                    text=top_level_comment["textDisplay"],
                    author=top_level_comment["authorDisplayName"],
                    like_count=int(top_level_comment.get("likeCount", 0)),
                )
                comment_threads.append(comment_details)

            # Sort comments by like count in descending order and get the top 3
            sorted_comments = sorted(
                comment_threads, key=lambda x: x.like_count, reverse=True
            )
            top_comments = sorted_comments[:10]

            return top_comments
        except Exception as e:
            return f"An error occurred while fetching comment threads: {str(e)}"
