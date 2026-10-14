#!/usr/bin/env python3
"""
Test Suite for Day 60: Grand Finale Showcase Engine
===================================================
Tests presentation slide count, metrics integrity, HTML exporter,
best-project data structure, struggles, and evolution timeline.
"""

import unittest
import os
import sys

# Add Day 60 to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from day60 import (
    ShowcasePresentationEngine,
    PRESENTATION_SLIDES,
    BEST_PROJECT_DEEPDIVE,
    ENGINEERING_STRUGGLES,
    ENGINEERING_LESSONS,
    EVOLUTION_TIMELINE
)

class TestDay60Showcase(unittest.TestCase):
    """Test cases verifying Day 60 presentation data and engine functionality."""

    def setUp(self):
        self.engine = ShowcasePresentationEngine()

    def test_slide_deck_completeness(self):
        """Verifies slide deck contains all 7 core thematic slides."""
        self.assertGreaterEqual(len(self.engine.slides), 7)
        for slide in self.engine.slides:
            self.assertIn("id", slide)
            self.assertIn("title", slide)
            self.assertIn("subtitle", slide)
            self.assertIn("bullets", slide)
            self.assertIn("metrics", slide)
            self.assertGreaterEqual(len(slide["bullets"]), 2)

    def test_best_project_structure(self):
        """Ensures best project deep dive contains architecture, trade-offs, and metrics."""
        bp = self.engine.best_project
        self.assertIn("name", bp)
        self.assertIn("AI Spam Guard", bp["name"])
        self.assertGreaterEqual(len(bp["architecture"]), 4)
        self.assertGreaterEqual(len(bp["decisions_and_tradeoffs"]), 3)
        self.assertIn("Test Classification Accuracy", bp["metrics"])
        self.assertIn("Repeated Query Latency", bp["metrics"])

    def test_struggles_completeness(self):
        """Ensures all 4 major engineering struggles and breakthroughs are documented."""
        struggles = self.engine.struggles
        self.assertEqual(len(struggles), 4)
        for st in struggles:
            self.assertIn("problem", st)
            self.assertIn("solution", st)
            self.assertIn("lesson", st)

    def test_lessons_completeness(self):
        """Verifies 6 foundational engineering lessons exist."""
        lessons = self.engine.lessons
        self.assertEqual(len(lessons), 6)
        for l in lessons:
            self.assertIn("number", l)
            self.assertIn("title", l)
            self.assertIn("description", l)

    def test_evolution_timeline(self):
        """Verifies evolution timeline spans from Phase 1 (Day 1) to Phase 6 (Day 60)."""
        evo = self.engine.evolution
        self.assertGreaterEqual(len(evo), 5)
        first_phase = evo[0]
        last_phase = evo[-1]
        self.assertIn("Days 1", first_phase["phase"])
        self.assertIn("Days 58", last_phase["phase"])

    def test_html_export(self):
        """Tests that HTML presentation exports correctly and contains required markers."""
        output_path = os.path.join(os.path.dirname(__file__), "test_output.html")
        try:
            generated_path = self.engine.export_html(output_path)
            self.assertTrue(os.path.exists(generated_path))
            
            with open(generated_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Grand Finale Engineering Showcase", content)
            self.assertIn("AI Spam Guard: Enterprise Edition", content)
            self.assertIn("The 60-Day Evolution", content)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

if __name__ == "__main__":
    unittest.main()
