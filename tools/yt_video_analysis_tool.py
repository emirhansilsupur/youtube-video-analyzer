from typing import Dict, Any, Type
from pydantic import BaseModel
from crewai_tools import BaseTool


class VideoAnalysisToolInput(BaseModel):
    """Input for VideoAnalysisTool."""

    view_count: int
    like_count: int
    comment_count: int
    channel_subscriber_count: int


class VideoAnalysisTool(BaseTool):
    name: str = "Analyze YouTube Video"
    description: str = "Analyzes the statistics of a YouTube video and provides advice."
    args_schema: Type[BaseModel] = VideoAnalysisToolInput

    def _run(
        self,
        view_count: int,
        like_count: int,
        comment_count: int,
        channel_subscriber_count: int,
    ) -> Dict[str, Any]:

        # Ensure all inputs are the correct type

        if isinstance(view_count, str):
            view_count = int(view_count)
        if isinstance(like_count, str):
            like_count = int(like_count)
        if isinstance(comment_count, str):
            comment_count = int(comment_count)
        if isinstance(channel_subscriber_count, str):
            channel_subscriber_count = int(channel_subscriber_count)

        # Performance metrics
        engagement_ratio = round((like_count + comment_count) / max(1, view_count), 2)
        subscriber_ratio = round(view_count / max(1, channel_subscriber_count), 2)
        like_to_view_ratio = round(like_count / max(1, view_count), 2)
        comment_to_view_ratio = round(comment_count / max(1, view_count), 2)

        advice = []

        # Using the correct metric for assessing likes
        if like_to_view_ratio > 0.9:
            advice.append("This video is very well-received by viewers.")
        elif like_to_view_ratio < 0.7:
            advice.append("Consider improving the content to increase likes.")

        if engagement_ratio > 0.05:
            advice.append("Good engagement from viewers.")
        else:
            advice.append("Try to increase viewer interaction.")

        if subscriber_ratio > 10:
            advice.append("This video performed very well for the channel size.")
        else:
            advice.append("Consider targeting a larger audience to grow your channel.")

        return {
            "advice": " ".join(advice),
            "engagement_ratio": engagement_ratio,
            "subscriber_ratio": subscriber_ratio,
            "like_to_view_ratio": like_to_view_ratio,
            "comment_to_view_ratio": comment_to_view_ratio,
        }
