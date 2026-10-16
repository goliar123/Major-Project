"""
Syncs Major_Project_Phase1_Report_B12.docx into Major_Project_Phase1_Report.md
preserving headings, markdown tables, callout blocks, and code listings.
"""
import docx

def sync():
    doc = docx.Document('Major_Project_Phase1_Report_B12.docx')
    lines = []

    for element in doc.element.body:
        tag = element.tag.split('}')[-1]
        if tag == 'p':
            p = docx.text.paragraph.Paragraph(element, doc)
            text = p.text.strip()
            if not text:
                continue
            bold = any(r.bold for r in p.runs)
            if text.startswith('CHAPTER ') or text.startswith('APPENDIX:'):
                lines.append(f'\n# {text}\n')
            elif text.startswith(('1.', '2.', '3.', '4.', '5.', '6.', 'I.', 'II.', 'III.', 'IV.', 'V.')) and bold:
                if text.count('.') == 1 or text.startswith(('I.', 'II.', 'III.', 'IV.', 'V.')):
                    lines.append(f'\n## {text}\n')
                elif text.count('.') == 2:
                    lines.append(f'\n### {text}\n')
                else:
                    lines.append(f'\n#### {text}\n')
            elif text.startswith('Figure '):
                lines.append(f'\n**{text}**\n')
            elif text.startswith('Listing '):
                lines.append(f'\n**{text}**\n')
            elif text.startswith('Table '):
                lines.append(f'\n**{text}**\n')
            else:
                lines.append(text + '\n')
        elif tag == 'tbl':
            tbl = docx.table.Table(element, doc)
            if len(tbl.rows) == 1 and len(tbl.columns) == 1:
                cell = tbl.rows[0].cells[0]
                cell_text = cell.text.strip()
                if cell_text.startswith('★'):
                    callout_lines = cell_text.split('\n')
                    lines.append('\n> [!NOTE]\n> ' + '\n> '.join(callout_lines) + '\n')
                else:
                    lines.append(f'\n```python\n{cell_text}\n```\n')
            else:
                headers = [c.text.strip().replace('\n', ' ').replace('|', '\\|') for c in tbl.rows[0].cells]
                lines.append('\n| ' + ' | '.join(headers) + ' |')
                lines.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
                for row in tbl.rows[1:]:
                    row_vals = [c.text.strip().replace('\n', ' ').replace('|', '\\|') for c in row.cells]
                    lines.append('| ' + ' | '.join(row_vals) + ' |')
                lines.append('\n')

    with open('Major_Project_Phase1_Report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print('Markdown report synced successfully.')

if __name__ == '__main__':
    sync()
