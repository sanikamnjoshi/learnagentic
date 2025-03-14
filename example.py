#!/usr/bin/env python3
"""
Example script demonstrating how to use the research_crew module
to generate a research article on a predefined topic.
"""

from research_crew import generate_research_article

def main():
    # Define the topic for research
    topic = "The impact of AI Coding on Programming Education."
    
    print(f"Generating research article on: {topic}")
    print("This process may take several minutes depending on the complexity of the topic.")
    print("Please wait...\n")
    
    # Generate the research article
    article = generate_research_article(topic)
    
    # Save the article to a file
    filename = f"{topic.replace(' ', '_').lower()}_research_article.md"
    with open(filename, "w") as f:
        f.write(article)
    
    print(f"\nArticle saved to {filename}")
    
    # Print a preview of the article (first 500 characters)
    preview_length = 500
    preview = article[:preview_length] + "..." if len(article) > preview_length else article
    print("\nArticle Preview:")
    print("-" * 80)
    print(preview)
    print("-" * 80)
    print(f"\nFull article saved to {filename}")

if __name__ == "__main__":
    main() 