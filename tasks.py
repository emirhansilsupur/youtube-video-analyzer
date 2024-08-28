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
