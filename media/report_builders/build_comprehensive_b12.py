"""
Comprehensive Major Project Phase-I Report Generator (B12 Format).
Produces an authoritative, 15,000+ word academic report for
'Automated Failure Attribution for LLM-Based Multi-Agent Systems'.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

OUTPUT_DOCX = "/home/goliar/Documents/LLM/media/reports/Major_Project_Phase1_Report_B12.docx"
LOGO_PATH = "/tmp/b12_media/word/media/image1.jpg"
ACK_IMG_PATH = "/tmp/b12_media/word/media/image3.jpg"
DIAG_DIR = "/home/goliar/Documents/LLM/media/diagrams/docs_diagrams"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

class ReportBuilder:
    def __init__(self):
        self.doc = docx.Document()
        self._setup_page()

    def _setup_page(self):
        for section in self.doc.sections:
            section.page_width = Inches(8.27)
            section.page_height = Inches(11.69)
            section.top_margin = Inches(0.85)
            section.bottom_margin = Inches(0.85)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(0.85)

        normal = self.doc.styles['Normal']
        normal.font.name = 'Times New Roman'
        normal.font.size = Pt(12)
        normal.font.color.rgb = RGBColor(0, 0, 0)
        normal.paragraph_format.line_spacing = 1.15
        normal.paragraph_format.space_after = Pt(6)

    def p(self, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_before=0, space_after=6, color=(0,0,0)):
        par = self.doc.add_paragraph()
        par.alignment = align
        par.paragraph_format.space_before = Pt(space_before)
        par.paragraph_format.space_after = Pt(space_after)
        par.paragraph_format.line_spacing = 1.15
        if text:
            run = par.add_run(text)
            run.bold = bold
            run.italic = italic
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.font.color.rgb = RGBColor(*color)
        return par

    def h1(self, text):
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_before = Pt(18)
        par.paragraph_format.space_after = Pt(8)
        run = par.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return par

    def h2(self, text):
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_before = Pt(14)
        par.paragraph_format.space_after = Pt(6)
        run = par.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return par

    def h3(self, text):
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_before = Pt(11)
        par.paragraph_format.space_after = Pt(4)
        run = par.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return par

    def h4(self, text):
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_before = Pt(9)
        par.paragraph_format.space_after = Pt(3)
        run = par.add_run(text)
        run.bold = True
        run.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(71, 85, 105)
        return par

    def fig(self, img_path, caption):
        if os.path.exists(img_path):
            p_img = self.doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(12)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(6.0))
        p_cap = self.doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(14)
        run = p_cap.add_run(caption)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(30, 41, 59)

    def callout(self, title, paragraphs, border_color="1E3A8A", bg_color="F8FAFC"):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.42)
        
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=100, bottom=100, left=150, right=120)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p0 = cell.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(4)
        run_t = p0.add_run(f"★  {title}")
        run_t.bold = True
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(11.5)
        r_val = int(border_color[0:2], 16)
        g_val = int(border_color[2:4], 16)
        b_val = int(border_color[4:6], 16)
        run_t.font.color.rgb = RGBColor(r_val, g_val, b_val)
        
        if isinstance(paragraphs, str):
            paragraphs = [paragraphs]
            
        for p_text in paragraphs:
            p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(p_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(30, 41, 59)
            
        p_after = self.doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6)

    def code_listing(self, listing_num, listing_title, code_str, language="python"):
        p_cap = self.doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        run_cap = p_cap.add_run(f"Listing {listing_num}: {listing_title}")
        run_cap.bold = True
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(11)
        run_cap.font.color.rgb = RGBColor(15, 23, 42)
        
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.42)
        
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        lines = code_str.strip().split("\n")
        for idx, line in enumerate(lines):
            if idx == 0:
                p = cell.paragraphs[0]
            else:
                p = cell.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(line)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.0)
            run.font.color.rgb = RGBColor(30, 41, 59)
            
        p_after = self.doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(8)

    def styled_table(self, title, headers, rows, col_widths=None):
        if title:
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_cap.paragraph_format.space_before = Pt(10)
            p_cap.paragraph_format.space_after = Pt(3)
            run_cap = p_cap.add_run(title)
            run_cap.bold = True
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(11)
            run_cap.font.color.rgb = RGBColor(15, 23, 42)
            
        total_rows = len(rows) + 1
        total_cols = len(headers)
        tbl = self.doc.add_table(rows=total_rows, cols=total_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        
        hdr_cells = tbl.rows[0].cells
        for c_idx, h_text in enumerate(headers):
            hdr_cells[c_idx].text = str(h_text)
            set_cell_background(hdr_cells[c_idx], "1E293B")
            set_cell_margins(hdr_cells[c_idx], top=35, bottom=35, left=60, right=60)
            p = hdr_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.0)
                r.font.color.rgb = RGBColor(255, 255, 255)
                
        for r_idx, row_data in enumerate(rows):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                set_cell_background(row_cells[c_idx], bg_col)
                set_cell_margins(row_cells[c_idx], top=25, bottom=25, left=50, right=50)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.1
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(30, 41, 59)
                    
        if col_widths:
            for r in tbl.rows:
                for c_idx, w in enumerate(col_widths):
                    r.cells[c_idx].width = Inches(w)
                    
        p_after = self.doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6)
        return tbl

    def page_break(self):
        self.doc.add_page_break()

    def save(self, path=OUTPUT_DOCX):
        self.doc.save(path)
        print(f"Report successfully saved to: {path}")

builder = ReportBuilder()
print("Builder instantiated.")
