"""
Master Compiler for the Comprehensive Major Project Phase-I Report (B12 Format).
"""
import sys
import os

sys.path.insert(0, "/home/goliar/Documents/LLM/media/report_builders")
sys.path.insert(0, "/home/goliar/Documents/LLM")

from build_comprehensive_b12 import ReportBuilder
from report_sections.front_matter import add_front_matter
from report_sections.chapter_1 import add_chapter_1
from report_sections.chapter_2 import add_chapter_2
from report_sections.chapter_3 import add_chapter_3
from report_sections.chapter_4 import add_chapter_4
from report_sections.chapter_5_6 import add_chapter_5_and_6

def main():
    print("Beginning compilation of comprehensive B12 report...")
    builder = ReportBuilder()

    print("Adding Front Matter (Covers, Certificate, Ack, Dec, TOC, LOF, LOT, Abstract)...")
    add_front_matter(builder)

    print("Adding Chapter 1: Introduction...")
    add_chapter_1(builder)

    print("Adding Chapter 2: Literature Survey...")
    add_chapter_2(builder)

    print("Adding Chapter 3: System Requirements Specification...")
    add_chapter_3(builder)

    print("Adding Chapter 4: Methodology...")
    add_chapter_4(builder)

    print("Adding Chapter 5: Conclusion & Future Scope and Chapter 6: References...")
    add_chapter_5_and_6(builder)

    print("Compilation complete! Report generated successfully.")

if __name__ == "__main__":
    main()
