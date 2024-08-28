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

    def generate_final_report(
        self,
        agent,
        fetch_and_analyze_video_details_task,
        fetch_and_summarize_comment_threads_task,
    ):
        return Task(
            description=dedent(
                """
                Combine the video analysis, comment summary, and video details into a final report.
                Ensure all sections from the example report are included and properly filled out.
                Include any additional insights or recommendations based on the combined data.
                Get the current date for the report.
                After creating the report, use the `text_to_pdf_tool` to convert the report into a PDF format.

                Example Report:
                ## YouTube Video Analysis Report

                ### Channel Overview
                **Channel Name:** Rick Astley  
                **Total Video Count:** 254  
                ### 1. Video Performance Metrics

                **Video Title:** Rick Astley - Never Gonna Give You Up (Official Music Video)  
                **View Count:** 1234567  
                **Like Count:** 45678  
                **Comment Count:** 2345  
                **Channel Subscriber Count:** 1234000  
                **Video Description:** Rick Astley's official music video for “Never Gonna Give You Up”  
                **Video Tags:** [Rick Astley, Never Gonna Give You Up, Music Video, 80s Music]  
                **Upload Date:** 2009-10-25  
                **Date Since Upload:** 14 years, 9 months, 22 days   

                #### Engagement Metrics
                
                **Engagement Ratio:** 3.8%  
                **Subscriber Ratio:** 1.0005  
                **Like-to-View Ratio:** 3.7%  
                **Comment-to-View Ratio:** 0.19%  

                #### Advice

                **1. Likes to Views Ratio:**
                The current likes to views ratio of %3.7 is slightly below the ideal benchmark of 3.75% to 4%. This indicates good engagement, but there is room for improvement. Consider incorporating more direct calls to action in your videos, asking viewers to like if they enjoy the content.

                **2. Engagement and Performance:**
                The engagement ratio of 0.0385 is quite strong, reflecting good viewer interaction. Continue to leverage this engagement by maintaining high-quality content and encouraging viewers to interact more.

                **3. Relative Performance:**
                The subscriber ratio of 1.00 is impressive, suggesting that the video performs exceptionally well relative to the channel's size. Use this positive performance to foster further viewer interaction and encourage likes and shares.

                **4. Content Improvement:**
                The comment-to-view ratio of 0.0019 suggests that while the video attracts a lot of views, the level of interaction in the comments is relatively low. To boost this ratio, engage more actively with the audience through comments and create content that prompts viewers to leave their thoughts and feedback.

                ### 2. Video Comment Thread Summary

                #### Top Comment Thread

                **Top-Level Comment**  
                **Text:** "A timeless classic! This song always brings back great memories."    
                **Author:** ClassicFan123  
                **Like Count:** 1234  
                **Total Reply Count:** 3  

                #### Sentiment and Key Themes:

                **Overall Tone:** Positive  
                **Common Topics:**  

                1.Nostalgia and fond memories associated with the song.
                2.Enduring popularity and timeless appeal of the music video.  
                **Feedback and Suggestions:**
                Viewers express ongoing affection and nostalgia for the song.
                Suggestions for more content that evokes similar nostalgic feelings.

                ### 3. Recommendations for Improvement

                **1. Enhance Likes to Views Ratio:**
                Calls to Action: Use engaging and creative calls to action within your videos to encourage more likes.
                Quality Content: Continue to produce high-quality content that resonates with viewers, as this naturally leads to more likes.
                Promotion: Increase promotion of the video on social media to drive additional traffic and engagement.

                **2. Boost Viewer Engagement:**
                Interactive Content:Create content that invites viewer interaction, such as questions or polls.
                Community Engagement: Respond to comments and build a strong community around the video.

                **3. Content Strategy:**
                Related Content: Produce follow-up or related content that builds on the success of this video.
                Analyze Viewer Preferences: Use YouTube Analytics to refine your content strategy based on viewer behavior and feedback.
    
                **Report Date:** August 16, 2024
                """
            ),
            agent=agent,
            context=[
                fetch_and_analyze_video_details_task,
                fetch_and_summarize_comment_threads_task,
            ],
            expected_output="""
                Generate a comprehensive report formatted exactly like the example report structure provided.
                Ensure all sections are complete and contain relevant information.
                Convert the report into a PDF document and save it.
            """,
        )
