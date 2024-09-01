from crewai import Agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()


class LLMChoice(Enum):
    LLAMA_3_1_70B = "llama-3.1-70b-versatile"
    LLAMA3_70B = "llama3-70b-8192"
    MIXTRAL_8X7B = "mixtral-8x7b-32768"


class YoutubeAnalysisAgents:
    def __init__(self, llm_choice=LLMChoice.LLAMA_3_1_70B):
        self.llm, self.max_rpm = self._get_llm(llm_choice)

    def _get_llm(self, llm_choice):
        llm_configs = {
            LLMChoice.LLAMA_3_1_70B: ("llama-3.1-70b-versatile", 100),
            LLMChoice.LLAMA3_70B: ("llama3-70b-8192", 30),
            LLMChoice.MIXTRAL_8X7B: ("mixtral-8x7b-32768", 30),
        }

        model, max_rpm = llm_configs[llm_choice]
        return ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model=model), max_rpm

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
            max_rpm=self.max_rpm,
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
            max_rpm=self.max_rpm,
        )

    def summary_agent(self, text_to_pdf_tool):
        return Agent(
            role="YouTube Content Strategist",
            goal="""Synthesize critical information from video metrics and audience feedback to craft a comprehensive, 
                data-driven summary that guides content creators in refining their strategy and maximizing the impact of their videos.""",
            backstory="""As the top YouTube content strategist, you specialize in blending data from various sources 
                     into clear, actionable insights. Your expertise helps content creators make informed decisions 
                     that elevate their content's reach and effectiveness.""",
            verbose=True,
            allow_delegation=False,
            tools=[text_to_pdf_tool],
            llm=self.llm,
            max_rpm=self.max_rpm,
            max_iter=50,
        )
