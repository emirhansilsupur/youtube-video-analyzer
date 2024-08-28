from crewai import Task
from textwrap import dedent


class YoutubeAnalysisTasks:

    def fetch_and_analyze_video_details(self, agent, video_id):

        return Task(
            description=dedent(
                f"""
                Fetch the following information about the video:{video_id}
                - Video title
                - View count
                - Like count
                - Comment count
                - Channel subscriber count
                - Video description
                - Video tags
                - Upload date
                - Current_date

                Ensure that all information is accurate and up-to-date.

                Next, analyze the video statistics based on the fetched details:
                - Engagement ratio
                - Subscriber ratio
                - Like-to-view ratio
                - Comment-to-view ratio

                Return a comprehensive report that includes both the video details and the statistical analysis.
                Use the video_analysis_tool to perform the statistical analysis.
                """
            ),
            agent=agent,
            expected_output="A detailed report with video details,and metrics.",
        )

    def fetch_and_summarize_comment_threads(self, agent, video_id):
        return Task(
            description=dedent(
                f"""

            Retrieve and analyze comment threads for the YouTube video:{video_id}
            Use the 'YouTubeCommentThreadsTool' tool to fetch the top 3 comment threads for this video

            After retrieving the comment threads, summarize and analyze them as follows:

            First, retrieve the following details for up to the top 3 comment threads:
            - Top-level comment text and author
            - Number of replies
            - Like count for each comment
            - Whether the comment thread is public

            If there are replies, include the text, author, and like count for each reply.

            Next, summarize the sentiment and key themes from the retrieved comment threads. Consider the following:
            - Overall tone (positive, negative, neutral)
            - Common topics or concerns raised by viewers
            - Any recurring feedback or suggestions

            Provide a structured summary of the comment threads and a concise report that highlights viewer sentiment and key themes.
            """
            ),
            agent=agent,
            expected_output="A comprehensive report including a list of CommentThreadDetails objects and a summarized analysis of viewer sentiment and key themes.",
        )
