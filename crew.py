from crewai import Crew
from agents import YoutubeAnalysisAgents
from tasks import YoutubeAnalysisTasks

from tools.yt_video_details_tool import YoutubeVideoDetailsTool
from tools.yt_video_analysis_tool import VideoAnalysisTool
from tools.yt_video_comment_tool import YoutubeCommentThreadsTool
from tools.pdf_converter_tool import TextToPDFTool
from crewai.process import Process
import re


class YoutubeAnalysisCrew:
    def __init__(
        self,
        video_url,
    ):
        self.video_url = video_url
        self.video_id = self.extract_video_id(video_url)
        if self.video_id is None:
            raise ValueError("Invalid YouTube URL provided.")

    def extract_video_id(self, url: str) -> str:
        # Regular expression to match YouTube video ID from various URL formats
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Invalid YouTube URL. Please provide a valid URL.")

    def run(self):
        agents = YoutubeAnalysisAgents()
        tasks = YoutubeAnalysisTasks()
        # tools
        youtube_video_details_tool = YoutubeVideoDetailsTool()
        video_analysis_tool = VideoAnalysisTool()
        youtube_commend_thread_tool = YoutubeCommentThreadsTool()
        text_to_pdf_tool = TextToPDFTool()

        # Define agents
        video_details_agent = agents.video_details_agent(
            youtube_video_details_tool=youtube_video_details_tool,
            video_analysis_tool=video_analysis_tool,
        )
        comment_analysis_agent = agents.comment_analysis_agent(
            youtube_commend_thread_tool=youtube_commend_thread_tool
        )
        summary_agent = agents.summary_agent(text_to_pdf_tool=text_to_pdf_tool)

        # Define tasks
        fetch_and_analyze_video_details_task = tasks.fetch_and_analyze_video_details(
            video_details_agent,
            video_id=self.video_id,
        )

        fetch_and_summarize_comment_threads_task = (
            tasks.fetch_and_summarize_comment_threads(
                comment_analysis_agent,
                video_id=self.video_id,
            )
        )

        generate_final_report_task = tasks.generate_final_report(
            summary_agent,
            fetch_and_analyze_video_details_task,
            fetch_and_summarize_comment_threads_task,
        )

        # Create and run the crew
        crew = Crew(
            agents=[video_details_agent, comment_analysis_agent, summary_agent],
            tasks=[
                fetch_and_analyze_video_details_task,
                fetch_and_summarize_comment_threads_task,
                generate_final_report_task,
            ],
            verbose=True,
            process=Process.sequential,
        )

        result = crew.kickoff()
        return result
