import os
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List, Optional

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Set up API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Set OpenAI model if specified in .env
if os.getenv("OPENAI_MODEL_NAME"):
    os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Define Pydantic models for structured output
class Resource(BaseModel):
    title: str = Field(description="Title of the resource")
    url: str = Field(description="URL of the resource")
    description: str = Field(description="Brief description of what information it contains")
    relevance: str = Field(description="Why it's relevant to the research")

class ResearchOutline(BaseModel):
    introduction: str = Field(description="Introduction section of the outline")
    main_sections: List[str] = Field(description="List of main sections in the outline")
    subsections: dict = Field(description="Dictionary mapping main sections to their subsections")
    key_points: dict = Field(description="Dictionary mapping sections to key points to cover")
    conclusion: str = Field(description="Conclusion section of the outline")

class ResearchPackage(BaseModel):
    resources: List[Resource] = Field(description="List of resources with descriptions and relevance")
    outline: ResearchOutline = Field(description="Detailed outline for the research article")
    information_gaps: List[str] = Field(description="Areas needing further research")

class QAFeedback(BaseModel):
    approval: bool = Field(description="Whether the article is approved or needs revision")
    strengths: List[str] = Field(description="Specific strengths of the article")
    areas_for_improvement: Optional[List[str]] = Field(description="Specific areas that need improvement")
    suggestions: Optional[List[str]] = Field(description="Actionable suggestions for addressing each area of improvement")
    overall_assessment: str = Field(description="Overall assessment of the article's quality")

# Define the agents
researcher = Agent(
    role="Research Specialist",
    goal="Find comprehensive and accurate information about {topic} and create a list of relevant resources",
    backstory="""You are an expert researcher with a talent for finding the most relevant and 
    reliable information on any topic. You have a keen eye for detail and can quickly identify 
    credible sources. Your research skills are unmatched, and you take pride in providing 
    thorough and well-organized information. If web search tools are unavailable, you can still 
    provide valuable information based on your own knowledge and expertise.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

writer = Agent(
    role="Content Writer",
    goal="Create a comprehensive, well-structured research article on {topic} based on the provided research",
    backstory="""You are a skilled writer with expertise in creating informative and engaging 
    research articles. You have a talent for synthesizing complex information into clear, 
    coherent prose. You always ensure your writing is well-structured, properly cited, 
    and provides valuable insights to readers.""",
    verbose=True,
    allow_delegation=False
)

quality_assurance = Agent(
    role="Quality Assurance Specialist",
    goal="Ensure the research article is comprehensive, well-structured, accurate, and properly cited",
    backstory="""You are a meticulous editor with an eye for detail and a commitment to quality. 
    You have extensive experience reviewing research articles and can quickly identify areas 
    for improvement in terms of content, structure, flow, and citations. You provide specific, 
    actionable feedback to help writers improve their work.""",
    verbose=True,
    allow_delegation=True
)

# Define the tasks
research_task = Task(
    description="""
    Research the topic: {topic}
    
    1. Conduct a comprehensive search to find the most relevant and reliable information about the topic.
    2. Identify key subtopics, trends, debates, and perspectives related to the main topic.
    3. Compile a list of at least 10 high-quality resources (articles, research papers, websites, etc.) 
       that provide valuable information on the topic.
    4. For each resource, provide:
       - The title and URL
       - A brief description of what information it contains
       - Why it's relevant to the research
    5. Create a detailed outline for a research article on the topic, including:
       - Introduction
       - Main sections and subsections
       - Key points to cover in each section
       - Conclusion
    6. Identify any gaps in the available information or areas that require further research.
    
    Your output should be well-organized and ready to be used by the Content Writer to create 
    a comprehensive research article.
    
    IMPORTANT: If you encounter issues with the web search tools (such as "Not enough credits" errors),
    you should still complete the task to the best of your ability using your own knowledge and expertise.
    In this case, create a detailed outline for the article and suggest potential resources that would be
    valuable for this topic, even if you cannot access them directly.
    """,
    expected_output="""
    A comprehensive research package that includes:
    1. A list of at least 10 high-quality resources with descriptions and relevance
    2. A detailed outline for a research article
    3. Notes on key information, statistics, quotes, and insights from the resources
    4. Identification of any information gaps or areas needing further research
    """,
    agent=researcher
)

writing_task = Task(
    description="""
    Write a comprehensive research article on {topic} based on the research provided.
    
    1. Follow the outline provided by the Research Specialist.
    2. Incorporate information from the resources provided, ensuring all facts are accurate.
    3. Structure the article with clear headings and subheadings.
    4. Write in a clear, engaging, and informative style appropriate for the target audience.
    5. Include proper citations for all information taken from the resources.
    6. Ensure the article has:
       - An engaging introduction that explains the importance of the topic
       - Well-developed main sections that cover all key aspects of the topic
       - A conclusion that summarizes the main points and provides final insights
    7. Format the article in Markdown.
    
    Your article should be comprehensive, well-structured, and properly cited.
    
    If you receive feedback from the Quality Assurance Specialist, carefully review it and revise
    your article accordingly. Address all areas for improvement and implement the suggested changes.
    
    IMPORTANT: If the research provided is limited due to technical issues with web search tools,
    you should still write a comprehensive article based on the outline and your own knowledge of the topic.
    In this case, make it clear in your citations that some information is based on general knowledge
    rather than specific sources.
    """,
    expected_output="""
    A comprehensive research article in Markdown format that:
    1. Follows the provided outline
    2. Incorporates information from the provided resources
    3. Is well-structured with clear headings and subheadings
    4. Is written in a clear, engaging, and informative style
    5. Includes proper citations for all information
    6. Has an engaging introduction, well-developed main sections, and a strong conclusion
    """,
    agent=writer,
    context=[research_task]
)

qa_review_task = Task(
    description="""
    Review the research article on {topic} and provide feedback for improvement.
    
    1. Evaluate the article for:
       - Comprehensiveness: Does it cover all key aspects of the topic?
       - Accuracy: Is all information correct and up-to-date?
       - Structure: Is the article well-organized with a logical flow?
       - Clarity: Is the writing clear and easy to understand?
       - Citations: Are all facts properly cited?
       - Engagement: Is the article interesting and engaging to read?
    
    2. Identify specific areas for improvement, such as:
       - Missing information or perspectives
       - Sections that need more development
       - Unclear explanations or arguments
       - Citation issues
       - Structural problems
    
    3. Provide specific, actionable feedback for the writer to improve the article.
    
    4. If the article meets all quality standards, approve it. If not, provide detailed 
       feedback for revision.
    
    Your feedback should be constructive, specific, and actionable.
    
    IMPORTANT: If the article was written with limited research resources due to technical issues,
    take this into account in your review. Focus on the quality of the writing, structure, and
    logical flow rather than expecting extensive citations from external sources.
    """,
    expected_output="""
    A detailed review of the research article that includes:
    1. An overall assessment of the article's quality
    2. Specific strengths of the article
    3. Specific areas for improvement
    4. Actionable suggestions for addressing each area of improvement
    5. A clear decision: approve the article or request revisions
    """,
    agent=quality_assurance,
    context=[writing_task]
)

revision_task = Task(
    description="""
    Revise the research article on {topic} based on the feedback provided by the Quality Assurance Specialist.
    
    1. Carefully review all feedback provided.
    2. Address each area for improvement identified by the QA Specialist.
    3. Implement the suggested changes and improvements.
    4. Ensure that the revised article:
       - Is more comprehensive, covering all key aspects of the topic
       - Has improved structure and flow
       - Is clearer and more engaging
       - Has proper citations for all information
       - Addresses any other issues identified in the feedback
    
    Your revised article should maintain all the strengths identified by the QA Specialist
    while addressing all areas for improvement.
    """,
    expected_output="""
    A revised research article in Markdown format that:
    1. Addresses all feedback from the QA Specialist
    2. Maintains all the strengths of the original article
    3. Is more comprehensive, well-structured, clear, and engaging
    4. Has proper citations for all information
    """,
    agent=writer,
    context=[writing_task, qa_review_task]
)

# Function to run the crew with feedback loop
def generate_research_article(topic):
    """
    Generate a research article on the specified topic with a feedback loop between
    the writer and QA specialist.
    
    Args:
        topic (str): The topic to research and write about
        
    Returns:
        str: The final research article
    """
    print(f"\n🔍 Researching topic: {topic}...\n")
    
    # Step 1: Research the topic
    research_crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=2,
        process=Process.sequential
    )
    research_result = research_crew.kickoff(inputs={"topic": topic})
    
    print(f"\n✍️ Writing initial article draft...\n")
    
    # Step 2: Write the initial article
    writing_crew = Crew(
        agents=[writer],
        tasks=[writing_task],
        verbose=2,
        process=Process.sequential
    )
    article = writing_crew.kickoff(inputs={"topic": topic, "research": research_result})
    
    # Step 3: QA review and revision loop
    max_revisions = 3
    revision_count = 0
    article_approved = False
    
    while not article_approved and revision_count < max_revisions:
        print(f"\n🔍 Quality assurance review (iteration {revision_count + 1})...\n")
        
        # QA review
        qa_crew = Crew(
            agents=[quality_assurance],
            tasks=[qa_review_task],
            verbose=2,
            process=Process.sequential
        )
        qa_feedback = qa_crew.kickoff(inputs={"topic": topic, "article": article})
        
        # Check if the QA feedback indicates approval
        if "approved" in qa_feedback.lower() or "approval" in qa_feedback.lower():
            article_approved = True
            print(f"\n✅ Article approved by QA Specialist!\n")
            break
        
        print(f"\n✍️ Revising article based on feedback (iteration {revision_count + 1})...\n")
        
        # Revise the article
        revision_crew = Crew(
            agents=[writer],
            tasks=[revision_task],
            verbose=2,
            process=Process.sequential
        )
        article = revision_crew.kickoff(inputs={"topic": topic, "article": article, "feedback": qa_feedback})
        
        revision_count += 1
    
    if not article_approved:
        print(f"\n⚠️ Reached maximum revision limit ({max_revisions}). Returning the latest version.\n")
    
    return article

if __name__ == "__main__":
    # Get topic from user
    topic = input("Enter a topic for research: ")
    
    # Generate the research article
    article = generate_research_article(topic)
    
    # Print the result
    print("\n\n=== FINAL RESEARCH ARTICLE ===\n\n")
    print(article)
    
    # Save the article to a file
    filename = f"{topic.replace(' ', '_').lower()}_research_article.md"
    with open(filename, "w") as f:
        f.write(article)
    
    print(f"\nArticle saved to {filename}") 