import subprocess, os
import pymupdf

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&family=Noto+Sans+Gujarati:wght@500;700&display=swap" rel="stylesheet">
<style>
@page {
    size: A4 portrait;
    margin: 0;
}
body {
    margin: 0;
    padding: 40px;
    background: #fdfcf7;
    font-family: 'Patrick Hand', 'Caveat', 'Noto Sans Gujarati', cursive;
    font-size: 24px;
    color: #1a3263;
}
h1 { font-family: 'Caveat', cursive; font-size: 34px; color: #162a52; margin: 0; }
.gujarati { font-family: 'Noto Sans Gujarati', sans-serif; font-size: 20px; color: #0d47a1; }
</style>
</head>
<body>
<h1>Day 1 • HTML Basics</h1>
<p>• What is HTML? → HyperText Markup Language <span class="gujarati">(વેબસાઇટ નું કંકાલ / હાડપિંજર - Skeleton of a webpage)</span></p>
<p>Real-life: HTML is like the bricks and walls of a house 🏠</p>
<p><code>&lt;h1&gt;Hello World&lt;/h1&gt;</code> :- <b>Hello World</b> (big heading on screen)</p>
<p><u>Remember:</u> Always close tags with &lt;/tagname&gt;!</p>
<p><u>Mistake:</u> Forgetting to close &lt;p&gt; or writing &lt;h1&gt; inside &lt;head&gt;.</p>
</body>
</html>"""

with open('test_font.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

html_abs = os.path.abspath('test_font.html')
pdf_abs = os.path.abspath('test_font.pdf')

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={pdf_abs}",
    "--no-pdf-header-footer",
    f"file:///{html_abs}"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome stderr:", res.stderr)
print("Chrome returncode:", res.returncode)

doc = pymupdf.open('test_font.pdf')
page = doc[0]
pix = page.get_pixmap(dpi=150)
pix.save(r"C:\Users\Ved\.gemini\antigravity-ide\brain\26a704f8-5f8a-40da-953f-8d4a6c9b3903\test_font.png")
print("Successfully generated and saved test_font.png")
