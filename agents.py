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

    def comment_analysis_agent(self, yt_commend_thread_tool):
        return Agent(
            role="Audience Engagement Analyst",
            goal="""Extract, analyze, and interpret detailed information from a YouTube video to deliver actionable insights 
                on its performance, audience reach, and engagement patterns, aimed at enhancing content strategy.""",
            backstory="""A seasoned video insights specialist with an exceptional track record in dissecting video metrics. 
                     You have a deep understanding of what makes content resonate with audiences and how to leverage data 
                     to optimize video performance for creators and marketers.""",
            verbose=True,
            allow_delegation=False,
            tools=[yt_commend_thread_tool],
            llm=self.llm,
        )
