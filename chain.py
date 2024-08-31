from langchain.schema.runnable import RunnableLambda
from langchain.prompts import ChatPromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import NoTranscriptFound
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI


def get_transcript(youtube_url):
    video_id = youtube_url.split("v=")[-1]
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    try:
        transcript = transcript_list.find_manually_created_transcript(language_codes=['ko', 'en'])
    except NoTranscriptFound:
        try:
            generated_transcripts = [trans for trans in transcript_list if trans.is_generated]
            transcript = generated_transcripts[0]
        except NoTranscriptFound:
            raise Exception("No suitable transcript found.")

    full_transcript = " ".join([part['text'] for part in transcript.fetch()])
    return full_transcript



def create_summary_chain():
    system_template = """Please summarize the YouTube video transcript according to the following guidelines:
[TRANSCRIPT START]
{transcript}
[TRANSCRIPT END]

Summary Guidelines:
1. Summarize in Korean.
2. Include the main topic and key points of the video.
3. Highlight important facts, statistics, and examples.
4. Structure the summary as follows:
   - Introduction of the video topic (1-2 sentences)
   - Main points (use bullet points)
   - Conclusion or key implications (1-2 sentences)
5. If technical terms are used, add brief explanations.

Please provide a clear and informative summary following these guidelines."""
    prompt_template = ChatPromptTemplate.from_template(system_template)
    model = GoogleGenerativeAI(model="gemini-1.5-flash")

    return (
        RunnableLambda(get_transcript)
        | prompt_template
        | model
        | StrOutputParser()
    )

youtube_summary_chain = create_summary_chain()