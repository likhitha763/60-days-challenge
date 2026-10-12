"""
Unit Tests for Day 59: Portfolio Engineering Engine
===================================================
Tests data integrity, recruiter briefing generators, HTML exports, 
and source repository verification.
"""

import os
from pathlib import Path
import tempfile
import unittest

# Import portfolio engine modules
from day59 import PortfolioData, PortfolioGenerator, Project, verify_portfolio_integrity


class TestPortfolioEngineering(unittest.TestCase):

    def setUp(self):
        self.projects = PortfolioData.get_flagship_projects()

    def test_portfolio_data_structure(self):
        """Verify candidate information and core skills structure."""
        self.assertEqual(PortfolioData.CANDIDATE_NAME, "Likhitha")
        self.assertIn("Python (Advanced)", PortfolioData.CORE_SKILLS["Languages"])
        self.assertIn("Scikit-Learn", PortfolioData.CORE_SKILLS["Machine Learning & Data"])
        self.assertIn("REST APIs", PortfolioData.CORE_SKILLS["Backend & Systems"])

    def test_flagship_projects_completeness(self):
        """Verify all flagship projects contain complete metadata and resume bullets."""
        self.assertGreaterEqual(len(self.projects), 5)
        for p in self.projects:
            self.assertIsInstance(p, Project)
            self.assertTrue(p.title)
            self.assertTrue(p.category)
            self.assertTrue(p.phase)
            self.assertGreaterEqual(len(p.tech_stack), 3)
            self.assertGreaterEqual(len(p.key_metrics), 2)
            self.assertGreaterEqual(len(p.resume_bullets), 2)
            self.assertTrue(p.github_path)

            # Test dictionary conversion
            d = p.to_dict()
            self.assertEqual(d["id"], p.id)
            self.assertEqual(d["title"], p.title)

    def test_recruiter_summary_format(self):
        """Verify 60-second recruiter brief contains key sections and formatting."""
        summary = PortfolioGenerator.get_recruiter_summary()
        self.assertIn("60-SECOND RECRUITER BRIEFING", summary)
        self.assertIn("LIKHITHA", summary)
        self.assertIn("TECHNICAL PROFICIENCY:", summary)
        self.assertIn("FLAGSHIP ENGINEERING PROJECTS:", summary)
        for p in self.projects:
            self.assertIn(p.title, summary)

    def test_resume_descriptions_format(self):
        """Verify ATS-friendly resume descriptions follow Google X-Y-Z formula."""
        resume = PortfolioGenerator.get_resume_descriptions()
        self.assertIn("Resume Project Descriptions", resume)
        self.assertIn("Accomplished", resume)
        self.assertIn("as measured by", resume)
        self.assertIn("by doing", resume)
        for p in self.projects:
            self.assertIn(p.title, resume)

    def test_linkedin_reflection_content(self):
        """Verify LinkedIn reflection text contains the Day 59 milestone narrative."""
        reflection = PortfolioGenerator.get_linkedin_reflection()
        self.assertIn("Day 59", reflection)
        self.assertIn("Portfolio Engineering", reflection)
        self.assertIn("#60DaysOfCode", reflection)
        self.assertIn("AI Spam Guard", reflection)

    def test_html_portfolio_generation(self):
        """Verify HTML portfolio generation produces valid, styled HTML5."""
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            generated = PortfolioGenerator.generate_html_portfolio(tmp_path)
            self.assertTrue(generated.exists())
            content = generated.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("<title>Likhitha", content)
            self.assertIn("60-Second TL;DR", content)
            self.assertIn("Flagship Engineering Projects", content)
            for p in self.projects:
                self.assertIn(p.title, content)
                self.assertIn(p.id, content)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_verify_portfolio_integrity(self):
        """Verify that all referenced repository project files exist on disk."""
        result = verify_portfolio_integrity()
        self.assertTrue(result, "All referenced project files must exist in the workspace")


if __name__ == "__main__":
    unittest.main()
