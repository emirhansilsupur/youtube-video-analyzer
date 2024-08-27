from crewai import Agent
from langchain_groq import ChatGroq
import os


class YoutubeAnalysisAgents:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="mixtral-8x7b-32768",
            temperature=0.1,
        )

    def video_details_agent(self, yt_video_details_tool, yt_video_analysis_tool):
        return Agent(
            role="Video Insights Specialist",
            goal="""Retrieve and analyze detailed information about a specific YouTube video 
                    to provide insights into its performance and engagement.""",
            backstory="""An expert YouTube video analyst known for providing comprehensive 
                         insights into video performance metrics and audience engagement.""",
            verbose=True,
            allow_delegation=False,
            tools=[yt_video_details_tool, yt_video_analysis_tool],
            llm=self.llm,
        )
