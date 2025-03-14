# Research Crew

This project uses CrewAI to create a crew of AI agents that collaborate to research a topic, write a comprehensive article, and ensure its quality through an iterative feedback loop.

## Overview

The crew consists of three specialized agents:

1. **Research Specialist**: Searches the web to find information about a topic and creates a list of relevant resources and an outline for a research article.

2. **Content Writer**: Uses the research provided by the Research Specialist to write a comprehensive, well-structured research article in Markdown format with proper citations.

3. **Quality Assurance Specialist**: Reviews the article for comprehensiveness, accuracy, structure, clarity, citations, and engagement. Provides feedback for improvement if needed.

The agents work in a sequential process with a feedback loop:

1. The Research Specialist gathers information and creates an outline
2. The Content Writer creates an initial draft based on the research
3. The Quality Assurance Specialist reviews the article
4. If the article needs improvement, the QA Specialist provides specific feedback
5. The Content Writer revises the article based on the feedback
6. Steps 3-5 repeat until the QA Specialist approves the article or a maximum number of revisions is reached

## Features

- **Web Search Integration**: Uses Serper API for real-time web search to gather the most up-to-date information
- **Feedback Loop**: Implements an iterative improvement process between the writer and QA specialist
- **Markdown Formatting**: Produces well-formatted research articles in Markdown
- **Citation Management**: Ensures all information is properly cited with sources

## Setup

### Prerequisites

- Python 3.8 or higher
- API keys for OpenAI and Serper (for web search)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   OPENAI_MODEL_NAME=gpt-4-turbo  # Optional, defaults to gpt-3.5-turbo if not specified
   ```

   You can get a Serper API key from [Serper.dev](https://serper.dev/).

## Usage

Run the script and enter a topic when prompted:

```
python research_crew.py
```

The script will:
1. Prompt you to enter a topic for research
2. The Research Specialist will search the web for information on the topic
3. The Content Writer will create a research article based on the research
4. The Quality Assurance Specialist will review the article and provide feedback
5. If necessary, the Content Writer will revise the article based on the feedback
6. Steps 4-5 will repeat until the article is approved or reaches the maximum revision limit (3 revisions)
7. The final article will be printed to the console and saved as a Markdown file

## Example

```
Enter a topic for research: Quantum Computing

🔍 Researching topic: Quantum Computing...

✍️ Writing initial article draft...

🔍 Quality assurance review (iteration 1)...

✍️ Revising article based on feedback (iteration 1)...

✅ Article approved by QA Specialist!

=== FINAL RESEARCH ARTICLE ===

# Quantum Computing: The Future of Computation

[Article content will appear here]

Article saved to quantum_computing_research_article.md
```

## Customization

You can modify the following aspects of the script:

- **Agent Roles and Backstories**: Customize the agents' personalities and expertise
- **Task Descriptions**: Change what each agent is asked to do
- **Feedback Loop Parameters**: Adjust the maximum number of revisions
- **OpenAI Model**: Change the model used by setting the OPENAI_MODEL_NAME environment variable

## License

This project is licensed under the MIT License - see the LICENSE file for details.