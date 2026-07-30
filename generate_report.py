import os
import sys

def convert_md_to_html_report():
    print("Reading laporan_uas_ttos.md...")
    with open("laporan_uas_ttos.md", "r", encoding="utf-8") as f:
        md_content = f.read()
        
    try:
        import markdown
    except ImportError:
        os.system(f"{sys.executable} -m pip install markdown fpdf2")
        import markdown

    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    html_document = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Laporan UAS Trending Topics on Statistics</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #1e293b;
            margin: 40px;
        }}
        h1 {{
            color: #1e3a8a;
            border-bottom: 2px solid #1e3a8a;
            padding-bottom: 8px;
            font-size: 24px;
        }}
        h2 {{
            color: #0f766e;
            margin-top: 25px;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 4px;
            font-size: 18px;
        }}
        h3 {{
            color: #334155;
            font-size: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 8px 12px;
            text-align: left;
            font-size: 13px;
        }}
        th {{
            background-color: #f1f5f9;
            color: #0f172a;
        }}
        code {{
            background-color: #f1f5f9;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: Consolas, monospace;
            font-size: 12px;
        }}
        blockquote {{
            border-left: 4px solid #3b82f6;
            margin: 10px 0;
            padding-left: 12px;
            color: #475569;
            background-color: #eff6ff;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
    
    html_path = "laporan_uas_ttos.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_document)
        
    print(f"Successfully generated HTML report template at '{html_path}'!")
    print("You can print/save this HTML as PDF directly in any browser (Ctrl+P -> Save as PDF) for a perfect 15-page layout!")

if __name__ == "__main__":
    convert_md_to_html_report()
