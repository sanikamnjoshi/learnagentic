#!/usr/bin/env python3
"""
Test script for the research_crew module.
This script tests the basic functionality of the research crew
without actually making API calls.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from research_crew import (
    researcher, writer, quality_assurance,
    research_task, writing_task, qa_review_task, revision_task
)

class TestResearchCrew(unittest.TestCase):
    """Test cases for the research_crew module."""
    
    def setUp(self):
        """Set up test environment."""
        # Ensure environment variables are set for testing
        os.environ["OPENAI_API_KEY"] = "test_openai_key"
        os.environ["SERPER_API_KEY"] = "test_serper_key"
    
    def test_agent_initialization(self):
        """Test that agents are initialized correctly."""
        self.assertEqual(researcher.role, "Research Specialist")
        self.assertEqual(writer.role, "Content Writer")
        self.assertEqual(quality_assurance.role, "Quality Assurance Specialist")
        
        # Check that the researcher has tools
        self.assertTrue(len(researcher.tools) > 0)
        
        # Check delegation settings
        self.assertFalse(researcher.allow_delegation)
        self.assertFalse(writer.allow_delegation)
        self.assertTrue(quality_assurance.allow_delegation)
    
    def test_task_initialization(self):
        """Test that tasks are initialized correctly."""
        self.assertEqual(research_task.agent, researcher)
        self.assertEqual(writing_task.agent, writer)
        self.assertEqual(qa_review_task.agent, quality_assurance)
        self.assertEqual(revision_task.agent, writer)
        
        # Check task contexts
        self.assertEqual(len(writing_task.context), 1)
        self.assertEqual(writing_task.context[0], research_task)
        
        self.assertEqual(len(qa_review_task.context), 1)
        self.assertEqual(qa_review_task.context[0], writing_task)
        
        self.assertEqual(len(revision_task.context), 2)
        self.assertEqual(revision_task.context[0], writing_task)
        self.assertEqual(revision_task.context[1], qa_review_task)

if __name__ == "__main__":
    unittest.main() 