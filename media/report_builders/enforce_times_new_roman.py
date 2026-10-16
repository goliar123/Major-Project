"""
Enforce Times New Roman across ALL presentations and documentation:
1. PPT Presentations:
   - media/presentations/Review_3_Automated_Failure_Attribution_B12.pptx
   - media/presentations/D1_Review_3_PW.pptx
   - media/presentations/D1_Review_3_PW_Filled.pptx
   And convert them to fresh PDFs via headless LibreOffice.

2. Documentation Reports:
   - media/reports/Major_Project_Phase1_Report_B12.docx
   - media/reports/Major_Project_Phase1_Report.docx
   And convert Major_Project_Phase1_Report_B12.docx to PDF via headless LibreOffice.
"""
import os
import io
import re
import zipfile
import subprocess
import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE
import docx

FONT_NAME = "Times New Roman"

def set_shape_font(shape):
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            p.font.name = FONT_NAME
            for r in p.runs:
                r.font.name = FONT_NAME
    if shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                for p in cell.text_frame.paragraphs:
                    p.font.name = FONT_NAME
                    for r in p.runs:
                        r.font.name = FONT_NAME
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for sub in shape.shapes:
            set_shape_font(sub)

def process_pptx(pptx_path):
    print(f"--> Processing PPTX: {pptx_path}")
    prs = pptx.Presentation(pptx_path)

    # 1. Slides
    for slide in prs.slides:
        for shape in slide.shapes:
            set_shape_font(shape)
        if slide.has_notes_slide:
            for shape in slide.notes_slide.shapes:
                set_shape_font(shape)

    # 2. Slide Masters & Layouts
    for master in prs.slide_masters:
        for shape in master.shapes:
            set_shape_font(shape)
        for layout in master.slide_layouts:
            for shape in layout.shapes:
                set_shape_font(shape)

    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)

    # 3. Low-level XML clean-up for themes and fallbacks
    zin = zipfile.ZipFile(buf, 'r')
    buf_out = io.BytesIO()
    zout = zipfile.ZipFile(buf_out, 'w', compression=zipfile.ZIP_DEFLATED)

    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith('.xml'):
            text = data.decode('utf-8', errors='ignore')
            # Replace any other font typefaces with Times New Roman
            text = re.sub(r'typeface=\"(?!Times New Roman)[^\"]+\"', f'typeface="{FONT_NAME}"', text)
            data = text.encode('utf-8')
        zout.writestr(item, data)
    zin.close()
    zout.close()

    with open(pptx_path, 'wb') as f:
        f.write(buf_out.getvalue())
    print(f"    Saved {pptx_path} with 100% Times New Roman.")

def process_docx(docx_path):
    print(f"--> Processing DOCX: {docx_path}")
    doc = docx.Document(docx_path)

    # 1. Styles
    for s in doc.styles:
        if hasattr(s, 'font') and s.font:
            s.font.name = FONT_NAME

    # 2. Paragraphs & Runs
    for p in doc.paragraphs:
        for r in p.runs:
            r.font.name = FONT_NAME

    # 3. Tables
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = FONT_NAME

    # 4. Headers & Footers
    for sec in doc.sections:
        for p in sec.header.paragraphs:
            for r in p.runs:
                r.font.name = FONT_NAME
        for t in sec.header.tables:
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.name = FONT_NAME
        for p in sec.footer.paragraphs:
            for r in p.runs:
                r.font.name = FONT_NAME
        for t in sec.footer.tables:
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for r in p.runs:
                            r.font.name = FONT_NAME

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)

    # 5. Low-level XML clean-up for word/theme/theme1.xml & styles.xml
    zin = zipfile.ZipFile(buf, 'r')
    buf_out = io.BytesIO()
    zout = zipfile.ZipFile(buf_out, 'w', compression=zipfile.ZIP_DEFLATED)

    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.endswith('.xml'):
            text = data.decode('utf-8', errors='ignore')
            # Cleanly replace all w:rFonts tags with valid, single-attribute Times New Roman
            text = re.sub(
                r'<w:rFonts\b[^>]*/>',
                f'<w:rFonts w:ascii="{FONT_NAME}" w:hAnsi="{FONT_NAME}" w:cs="{FONT_NAME}" w:eastAsia="{FONT_NAME}"/>',
                text
            )
            # Replace typeface in themes
            text = re.sub(r'typeface=\"(?!Times New Roman)[^\"]+\"', f'typeface="{FONT_NAME}"', text)
            data = text.encode('utf-8')
        zout.writestr(item, data)
    zin.close()
    zout.close()

    with open(docx_path, 'wb') as f:
        f.write(buf_out.getvalue())
    print(f"    Saved {docx_path} with 100% Times New Roman.")

def main():
    # Fix builder script if needed
    builder_script = "media/report_builders/build_comprehensive_b12.py"
    if os.path.exists(builder_script):
        with open(builder_script, "r") as f:
            code = f.read()
        if "run.font.name = 'Consolas'" in code:
            code = code.replace("run.font.name = 'Consolas'", "run.font.name = 'Times New Roman'")
            with open(builder_script, "w") as f:
                f.write(code)
            print("Updated build_comprehensive_b12.py: changed Consolas to Times New Roman.")

    # 1. Process Presentations
    pptx_files = [
        "media/presentations/Review_3_Automated_Failure_Attribution_B12.pptx",
        "media/presentations/D1_Review_3_PW.pptx",
        "media/presentations/D1_Review_3_PW_Filled.pptx",
    ]
    for p in pptx_files:
        if os.path.exists(p):
            process_pptx(p)

    # 2. Process Documentation
    docx_files = [
        "media/reports/Major_Project_Phase1_Report_B12.docx",
        "media/reports/Major_Project_Phase1_Report.docx",
    ]
    for d in docx_files:
        if os.path.exists(d):
            process_docx(d)

    # 3. Convert PPTX to PDF via LibreOffice
    print("--> Converting updated presentations to PDF via LibreOffice...")
    for p in pptx_files:
        if os.path.exists(p):
            cmd = ["libreoffice", "--headless", "--convert-to", "pdf", p, "--outdir", "media/presentations/"]
            subprocess.run(cmd, check=True)
            print(f"    Exported {p[:-5]}.pdf")

    # 4. Convert DOCX Report to PDF via LibreOffice
    print("--> Converting updated documentation report to PDF via LibreOffice...")
    doc_main = "media/reports/Major_Project_Phase1_Report_B12.docx"
    cmd_doc = ["libreoffice", "--headless", "--convert-to", "pdf", doc_main, "--outdir", "media/reports/"]
    subprocess.run(cmd_doc, check=True)
    print("    Exported Major_Project_Phase1_Report_B12.pdf")

    print("\n[SUCCESS] All PPT presentations and documentation reports are now 100% in Times New Roman!")

if __name__ == "__main__":
    main()
