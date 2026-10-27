import os, subprocess, pymupdf

CSS_TEMPLATE = """
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Patrick+Hand&family=Noto+Sans+Gujarati:wght@500;700&display=swap');

@page {
    size: 210mm 297mm; /* A4 */
    margin: 0;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    background-color: #2b2b2b;
    font-family: 'Patrick Hand', 'Noto Sans Gujarati', cursive, sans-serif;
    color: #173366;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

.diary-page {
    width: 210mm;
    height: 297mm;
    position: relative;
    background-color: #fcfbf6;
    background-image: 
        radial-gradient(#ede8db 15%, transparent 16%),
        radial-gradient(#ede8db 15%, transparent 16%);
    background-size: 60px 60px;
    background-position: 0 0, 30px 30px;
    padding: 14mm 16mm 14mm 26mm;
    overflow: hidden;
    page-break-after: always;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    margin: 15px auto;
}

@media print {
    body {
        background: transparent;
    }
    .diary-page {
        margin: 0;
        box-shadow: none;
    }
}

/* Notebook Ruled Lines */
.ruled-lines-layer {
    position: absolute;
    top: 34mm;
    left: 0;
    right: 0;
    bottom: 18mm;
    pointer-events: none;
    background: repeating-linear-gradient(
        transparent,
        transparent 31px,
        #cbd5e1 31px,
        #cbd5e1 32px
    );
    z-index: 1;
}

/* Vertical Pink/Red Margin Line */
.margin-line {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 22mm;
    width: 2px;
    background-color: #f87171;
    z-index: 2;
}

.margin-line-secondary {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 23.5mm;
    width: 1px;
    background-color: #fca5a5;
    opacity: 0.5;
    z-index: 2;
}

/* Diary Header */
.diary-header {
    position: relative;
    z-index: 5;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2.5px solid #d1d5db;
    padding-bottom: 4px;
    margin-bottom: 5mm;
    margin-left: 2mm;
}

.header-left {
    display: flex;
    align-items: baseline;
    gap: 12px;
}

.day-badge {
    font-family: 'Caveat', cursive;
    font-size: 36px;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1;
    letter-spacing: 0.5px;
}

.topic-title {
    font-family: 'Caveat', cursive;
    font-size: 25px;
    font-weight: 700;
    color: #1e3a8a;
    line-height: 1;
}

.header-right {
    text-align: right;
    font-family: 'Caveat', cursive;
    font-size: 15px;
    color: #64748b;
    line-height: 1.2;
}

.header-right .year {
    font-size: 19px;
    font-weight: 700;
    color: #334155;
}

/* Thumb Tab on right edge */
.diary-tab {
    position: absolute;
    right: 0;
    top: 42mm;
    background-color: #1e3a8a;
    color: #ffffff;
    font-family: sans-serif;
    font-size: 11px;
    font-weight: bold;
    padding: 10px 4px;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    border-radius: 6px 0 0 6px;
    box-shadow: -2px 2px 4px rgba(0,0,0,0.15);
    letter-spacing: 1.5px;
    z-index: 10;
}

/* Content Area */
.page-content {
    position: relative;
    z-index: 5;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-left: 3mm;
}

.topic-block {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.topic-heading {
    font-family: 'Caveat', cursive;
    font-size: 23px;
    font-weight: 700;
    color: #162f65;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

.topic-heading span.dot {
    font-size: 20px;
    color: #1d4ed8;
}

.sub-point {
    font-size: 18px;
    line-height: 1.35;
    color: #1a3263;
    margin: 1px 0;
    padding-left: 8px;
}

.sub-point .arrow {
    color: #2563eb;
    font-weight: bold;
    margin-right: 4px;
}

.gujarati-note {
    font-family: 'Noto Sans Gujarati', sans-serif;
    color: #0d47a1;
    font-size: 15px;
    background: #eef2ff;
    padding: 1px 6px;
    border-radius: 4px;
    display: inline-block;
    margin-left: 4px;
}

.real-life-box {
    font-size: 17.5px;
    color: #475569;
    padding: 2px 10px;
    margin: 2px 0 2px 8px;
    border-left: 3px solid #93c5fd;
    font-style: italic;
}

.code-row {
    background: #f1f5f9;
    border: 1px dashed #94a3b8;
    border-radius: 5px;
    padding: 3px 10px;
    margin: 2px 0 2px 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Patrick Hand', monospace;
    font-size: 17.5px;
    color: #0f172a;
}

.code-snippet {
    color: #1e3a8a;
    font-weight: 600;
}

.code-output {
    color: #15803d;
    font-weight: 600;
    background: #dcfce7;
    padding: 1px 8px;
    border-radius: 4px;
    font-family: 'Patrick Hand', cursive;
    font-size: 17px;
}

.remember-line {
    font-size: 17px;
    color: #1e3a8a;
    background: #eff6ff;
    border-left: 3px solid #3b82f6;
    padding: 2px 8px;
    margin: 1px 0 1px 8px;
    border-radius: 0 4px 4px 0;
}

.mistake-line {
    font-size: 17px;
    color: #991b1b;
    background: #fef2f2;
    border-left: 3px solid #ef4444;
    padding: 2px 8px;
    margin: 1px 0 1px 8px;
    border-radius: 0 4px 4px 0;
}

.diagram-box {
    margin: 3px 0 3px 10px;
    padding: 4px 10px;
    border: 1.5px solid #64748b;
    border-radius: 5px;
    background: #ffffff;
    display: inline-block;
    font-size: 15.5px;
    color: #1e293b;
    line-height: 1.25;
}

.diary-footer {
    position: absolute;
    bottom: 7mm;
    left: 26mm;
    right: 16mm;
    text-align: center;
    font-family: 'Patrick Hand', cursive;
    font-size: 15.5px;
    color: #64748b;
    border-top: 1px dashed #cbd5e1;
    padding-top: 4px;
    z-index: 5;
    font-style: italic;
}
"""

html_pages_data = [
    # Page 1
    {
        "day": "Day 1",
        "title": "HTML Intro & Structure",
        "tab": "HTML NOTES",
        "quote": '"Strengthening our identity is one way of reinforcing people\'s confidence"',
        "topics": [
            {
                "heading": "What is HTML?",
                "subpoints": [
                    ("→", "Stands for <u>HyperText Markup Language</u>."),
                    ("→", "Gives skeleton structure to a webpage", "(વેબસાઇટ નું કંકાલ / હાડપિંજર - Skeleton of a website)")
                ],
                "analogy": "🏠 Real-life: HTML is like the bricks and walls of a house, CSS is paint and interior.",
                "code": ("&lt;p&gt;My first web page&lt;/p&gt;", ":- My first web page (shown on screen)"),
                "remember": "HTML is not a programming language; it has no logic or loops, only tags!",
                "mistake": "Thinking HTML alone can make a beautiful website. It only makes the raw skeleton!"
            },
            {
                "heading": "Basic HTML Document Structure",
                "subpoints": [
                    ("→", "Every HTML file must follow this exact hierarchy:"),
                ],
                "diagram": "<b>&lt;!DOCTYPE html&gt;</b> → Tells browser it's HTML5<br><b>&lt;html&gt;</b> → Root element of page<br>&nbsp;&nbsp;├── <b>&lt;head&gt;</b> → Metadata, title, fonts (invisible to user)<br>&nbsp;&nbsp;└── <b>&lt;body&gt;</b> → Visible content (headings, paragraphs, images)<br><b>&lt;/html&gt;</b>",
                "subpoints2": [
                    ("→", "&lt;head&gt; = મગજ (brain - settings), &lt;body&gt; = શરીર (visible body)", "(મગજ અને શરીર)")
                ],
                "code": ("&lt;title&gt;My Site&lt;/title&gt;", ":- Shows on browser tab at top"),
                "remember": "Only things inside &lt;body&gt; are shown on the screen!",
                "mistake": "Putting &lt;h1&gt; or &lt;p&gt; inside &lt;head&gt;. Head is ONLY for metadata and title!"
            }
        ]
    },
    # Page 2
    {
        "day": "Day 2",
        "title": "Headings & Paragraphs",
        "tab": "HTML NOTES",
        "quote": '"Small disciplines repeated with consistency every day lead to great achievements"',
        "topics": [
            {
                "heading": "HTML Headings (&lt;h1&gt; to &lt;h6&gt;)",
                "subpoints": [
                    ("→", "Six levels of headings from most important (&lt;h1&gt;) to least (&lt;h6&gt;)."),
                    ("→", "Search engines like Google use &lt;h1&gt; to understand the main topic", "(મુખ્ય શીર્ષક - Main Heading)")
                ],
                "analogy": "📰 Real-life: &lt;h1&gt; is newspaper headline, &lt;h2&gt; is sub-section, &lt;h6&gt; is small footnote.",
                "code": ("&lt;h1&gt;Main News&lt;/h1&gt; ... &lt;h6&gt;Fine Print&lt;/h6&gt;", ":- <h1>Main News</h1> ... <h6>Fine Print</h6>"),
                "remember": "Use only ONE &lt;h1&gt; per page for best SEO! Never skip heading levels.",
                "mistake": "Using &lt;h1&gt; just to make text bold or big. Use CSS for font size, not heading tags!"
            },
            {
                "heading": "Paragraphs (&lt;p&gt;), &lt;br&gt; & &lt;hr&gt;",
                "subpoints": [
                    ("→", "<b>&lt;p&gt;</b> defines a paragraph of text. Browser adds empty space before and after it."),
                    ("→", "<b>&lt;br&gt;</b> breaks line without extra gap", "(નવી લીટી - single line break)"),
                    ("→", "<b>&lt;hr&gt;</b> draws a horizontal dividing line", "(આડી લીટી - thematic divider)")
                ],
                "code": ("&lt;p&gt;Line 1&lt;br&gt;Line 2&lt;/p&gt;&lt;hr&gt;", ":- Line 1<br>Line 2<hr style='margin:2px 0'>"),
                "remember": "&lt;br&gt; and &lt;hr&gt; are self-closing void tags (no &lt;/br&gt; needed).",
                "mistake": "Using multiple &lt;br&gt;&lt;br&gt;&lt;br&gt; tags to push items down instead of CSS margin!"
            }
        ]
    },
    # Page 3
    {
        "day": "Day 3",
        "title": "Formatting Elements",
        "tab": "HTML NOTES",
        "quote": '"Details make perfection, and perfection is not a detail"',
        "topics": [
            {
                "heading": "Text Formatting Tags",
                "subpoints": [
                    ("→", "<b>&lt;b&gt;</b> vs <b>&lt;strong&gt;</b>: Both look bold, but &lt;strong&gt; adds semantic importance for screen readers", "(મહત્વપૂર્ણ અક્ષરો)"),
                    ("→", "<b>&lt;i&gt;</b> vs <b>&lt;em&gt;</b>: Both look italic, but &lt;em&gt; adds verbal stress/emphasis", "(ત્રાંસા અક્ષરો)")
                ],
                "code": ("&lt;b&gt;Bold&lt;/b&gt; &amp; &lt;i&gt;Italic&lt;/i&gt;", ":- <b>Bold</b> & <i>Italic</i>"),
                "remember": "Prefer &lt;strong&gt; and &lt;em&gt; over &lt;b&gt; and &lt;i&gt; for accessibility & SEO.",
                "mistake": "Overusing formatting tags on whole paragraphs instead of specific keywords."
            },
            {
                "heading": "Special Markups: &lt;mark&gt;, &lt;del&gt;, &lt;ins&gt;, &lt;sub&gt;, &lt;sup&gt;",
                "subpoints": [
                    ("→", "<b>&lt;mark&gt;</b>: Yellow highlighter effect", "(હાઈલાઈટ કરવું)"),
                    ("→", "<b>&lt;del&gt;</b> and <b>&lt;ins&gt;</b>: Strikethrough & underline for price discounts/edits", "(જૂનો ભાવ અને નવો ભાવ)"),
                    ("→", "<b>&lt;sub&gt;</b> (H<sub>2</sub>O) & <b>&lt;sup&gt;</b> (x<sup>2</sup>): Subscript & Superscript" , "(નીચે અને ઉપર લખાણ)")
                ],
                "code": ("&lt;del&gt;500&lt;/del&gt; &lt;ins&gt;399&lt;/ins&gt; | H&lt;sub&gt;2&lt;/sub&gt;O", ":- <del>500</del> <ins>399</ins> | H<sub>2</sub>O"),
                "remember": "Use &lt;del&gt; and &lt;ins&gt; together for showing discounted prices in e-commerce.",
                "mistake": "Confusing &lt;sub&gt; (submarine = goes down) with &lt;sup&gt; (superman = flies up)."
            }
        ]
    },
    # Page 4
    {
        "day": "Day 4",
        "title": "Style Attribute & CSS Methods",
        "tab": "HTML NOTES",
        "quote": '"Simplicity is the soul of efficiency"',
        "topics": [
            {
                "heading": "The style Attribute (Inline CSS)",
                "subpoints": [
                    ("→", "Used to style a single specific HTML element directly inside opening tag."),
                    ("→", "Syntax: <code>style=\"property: value;\"</code>", "(ટેગ ની અંદર જ સ્ટાઈલ આપવી)")
                ],
                "analogy": "👕 Real-life: Wearing custom badge on one shirt vs uniform for whole school.",
                "code": ("&lt;p style=\"color: red; font-size: 20px;\"&gt;Alert&lt;/p&gt;", ":- <span style='color:red;'>Alert</span> (in red color)"),
                "remember": "Always end each CSS property inside style with a semicolon (;)!",
                "mistake": "Writing huge styles in HTML tags. It makes code messy and hard to maintain."
            },
            {
                "heading": "3 Ways to Connect CSS to HTML",
                "subpoints": [
                    ("→", "1. <b>Inline CSS:</b> inside tag via <code>style=\"...\"</code>"),
                    ("→", "2. <b>Internal CSS:</b> inside <code>&lt;style&gt;</code> tag within &lt;head&gt;", "(પેજ ના માથામાં)"),
                    ("→", "3. <b>External CSS:</b> separate <code>.css</code> file connected via <code>&lt;link&gt;</code> in &lt;head&gt;", "(અલગ ફાઈલ જોડીને)")
                ],
                "code": ("&lt;link rel=\"stylesheet\" href=\"style.css\"&gt;", ":- Connects external styling file"),
                "remember": "External CSS is best practice for professional production websites!",
                "mistake": "Placing &lt;link&gt; tag inside &lt;body&gt;. It MUST always be inside &lt;head&gt;!"
            }
        ]
    },
    # Page 5
    {
        "day": "Day 5",
        "title": "HTML Linking (&lt;a&gt; tag)",
        "tab": "HTML NOTES",
        "quote": '"Connection is the energy that exists between people when they feel seen and heard"',
        "topics": [
            {
                "heading": "Hyperlinks & href Attribute",
                "subpoints": [
                    ("→", "<b>&lt;a&gt;</b> (Anchor tag) creates clickable links to other pages or websites."),
                    ("→", "<b>href:</b> Hypertext Reference (the target URL)", "(લિંક નું સરનામું - Destination URL)"),
                    ("→", "<b>target=\"_blank\":</b> Opens link in a brand new browser tab", "(નવા ટેબમાં ખોલવું)")
                ],
                "code": ("&lt;a href=\"https://google.com\" target=\"_blank\"&gt;Google&lt;/a&gt;", ":- Clickable link opening Google"),
                "remember": "When using target=\"_blank\", always add rel=\"noopener noreferrer\" for security!",
                "mistake": "Leaving href empty or writing &lt;a&gt; without href attribute (it won't be clickable)."
            },
            {
                "heading": "Special Links: Email, Phone & Bookmarks",
                "subpoints": [
                    ("→", "<b>mailto:</b> Opens default email client", "(ઈમેલ મોકલવા)"),
                    ("→", "<b>tel:</b> Prompts phone dialer on mobile devices", "(ફોન કોલ કરવા)"),
                    ("→", "<b>#id:</b> Jumps to specific section on the same page", "(પેજ ની અંદર કૂદકો મારવો)")
                ],
                "code": ("&lt;a href=\"mailto:a@b.com\"&gt;Mail&lt;/a&gt; | &lt;a href=\"#sec1\"&gt;Jump&lt;/a&gt;", ":- Opens email app | Jumps to #sec1"),
                "remember": "Bookmark links match the <code>id</code> of the target tag (e.g. href=\"#top\").",
                "mistake": "Forgetting the '#' symbol in internal bookmark link hrefs!"
            }
        ]
    },
    # Page 6
    {
        "day": "Day 6",
        "title": "Images (&lt;img&gt; tag)",
        "tab": "HTML NOTES",
        "quote": '"A picture is a poem without words"',
        "topics": [
            {
                "heading": "Image Embedding & Attributes",
                "subpoints": [
                    ("→", "<b>&lt;img&gt;</b> is an empty self-closing tag used to display images on webpage."),
                    ("→", "<b>src:</b> Source path (URL or local folder path) of image", "(ફોટા નું સરનામું)"),
                    ("→", "<b>alt:</b> Alternative text displayed if image fails to load", "(ફોટો ન દેખાય તો લખાણ)")
                ],
                "code": ("&lt;img src=\"logo.png\" alt=\"College Logo\" width=\"120\"&gt;", ":- Displays 120px wide image"),
                "remember": "Never omit the <code>alt</code> attribute! It is critical for blind users & Google SEO.",
                "mistake": "Writing wrong folder path (like missing images/ or typo in image extension .png vs .jpg)."
            },
            {
                "heading": "Responsive Images & loading=\"lazy\"",
                "subpoints": [
                    ("→", "<b>width & height:</b> Reserve layout space to prevent page jumping during load."),
                    ("→", "<b>loading=\"lazy\":</b> Defers loading image until user scrolls near it", "(પેજ ઝડપી બનાવવું - speed up page)"),
                    ("→", "Always scale proportionally using CSS <code>max-width: 100%; height: auto;</code>" )
                ],
                "code": ("&lt;img src=\"banner.jpg\" loading=\"lazy\" alt=\"Banner\"&gt;", ":- Loads only when scrolled into view"),
                "remember": "Use loading=\"lazy\" on all images below the fold to save user bandwidth!",
                "mistake": "Distorting image aspect ratio by setting both fixed width and fixed height in px."
            }
        ]
    },
    # Page 7
    {
        "day": "Day 7",
        "title": "HTML Tables",
        "tab": "HTML NOTES",
        "quote": '"Order and structure are the foundations of all good work"',
        "topics": [
            {
                "heading": "Table Basics: &lt;table&gt;, &lt;tr&gt;, &lt;th&gt;, &lt;td&gt;",
                "subpoints": [
                    ("→", "<b>&lt;table&gt;:</b> Container for tabular data (rows & columns)."),
                    ("→", "<b>&lt;tr&gt;:</b> Table Row", "(ટેબલ ની આડી હરોળ)"),
                    ("→", "<b>&lt;th&gt;:</b> Table Header (bold & centered by default)", "(કોલમ નું હેડિંગ)"),
                    ("→", "<b>&lt;td&gt;:</b> Table Data cell (regular content)", "(ટેબલ નો ડેટા ખાનું)")
                ],
                "diagram": "&lt;table border='1'&gt;<br>&nbsp;&nbsp;&lt;tr&gt;&lt;th&gt;Name&lt;/th&gt;&lt;th&gt;Roll&lt;/th&gt;&lt;/tr&gt;<br>&nbsp;&nbsp;&lt;tr&gt;&lt;td&gt;Ved&lt;/td&gt;&lt;td&gt;101&lt;/td&gt;&lt;/tr&gt;<br>&lt;/table&gt;",
                "remember": "A table is constructed strictly ROW BY ROW! Every row starts with &lt;tr&gt;.",
                "mistake": "Putting text directly inside &lt;table&gt; without wrapping in &lt;tr&gt; and &lt;td&gt;."
            },
            {
                "heading": "Merging Cells: colspan & rowspan",
                "subpoints": [
                    ("→", "<b>colspan=\"N\":</b> Merges N columns horizontally into one cell", "(આડા ખાના ભેગા કરવા)"),
                    ("→", "<b>rowspan=\"N\":</b> Merges N rows vertically into one cell", "(ઊભા ખાના ભેગા કરવા)"),
                    ("→", "Semantic tags: <code>&lt;thead&gt;</code>, <code>&lt;tbody&gt;</code>, <code>&lt;tfoot&gt;</code> group header, body, footer.")
                ],
                "code": ("&lt;td colspan=\"2\"&gt;Full Address&lt;/td&gt;", ":- One cell spanning 2 columns"),
                "remember": "When you merge cells using colspan=2, delete the adjacent &lt;td&gt; in that row!",
                "mistake": "Using tables for overall website layouts! Tables are ONLY for tabular data."
            }
        ]
    },
    # Page 8
    {
        "day": "Day 8",
        "title": "Lists in HTML",
        "tab": "HTML NOTES",
        "quote": '"Organization isn\'t about perfection. It is about efficiency and peace of mind"',
        "topics": [
            {
                "heading": "Unordered (&lt;ul&gt;) & Ordered (&lt;ol&gt;) Lists",
                "subpoints": [
                    ("→", "<b>&lt;ul&gt;:</b> Bulleted list (dots, circles, squares)", "(બુલેટ લિસ્ટ - ક્રમ વગર)"),
                    ("→", "<b>&lt;ol&gt;:</b> Numbered list (1, A, a, I, i via <code>type</code> attribute)", "(નંબર વાળું લિસ્ટ)"),
                    ("→", "<b>&lt;li&gt;:</b> List Item (must be inside &lt;ul&gt; or &lt;ol&gt;)", "(દરેક આઈટમ)")
                ],
                "code": ("&lt;ol type=\"A\" start=\"3\"&gt;&lt;li&gt;Item&lt;/li&gt;&lt;/ol&gt;", ":- C. Item (starts numbering from C)"),
                "remember": "Only &lt;li&gt; elements can be direct children of &lt;ul&gt; and &lt;ol&gt;!",
                "mistake": "Putting &lt;p&gt; or &lt;div&gt; directly inside &lt;ul&gt; instead of inside &lt;li&gt;."
            },
            {
                "heading": "Description Lists (&lt;dl&gt;) & Nested Lists",
                "subpoints": [
                    ("→", "<b>&lt;dl&gt;:</b> Description list for terms & definitions (like a glossary)."),
                    ("→", "<b>&lt;dt&gt;:</b> Definition Term", "(શબ્દ / ટર્મ)"),
                    ("→", "<b>&lt;dd&gt;:</b> Definition Description (automatically indented)", "(શબ્દ નો અર્થ / સમજૂતી)"),
                    ("→", "<b>Nested lists:</b> Placing a new &lt;ul&gt; inside an existing &lt;li&gt; creates sub-menus.")
                ],
                "code": ("&lt;dl&gt;&lt;dt&gt;HTML&lt;/dt&gt;&lt;dd&gt;Markup Lang&lt;/dd&gt;&lt;/dl&gt;", ":- HTML<br>&nbsp;&nbsp;&nbsp;&nbsp;Markup Lang"),
                "remember": "Nested lists are the foundation of all website navigation dropdown menus!",
                "mistake": "Placing the sub-list between &lt;/li&gt; and &lt;li&gt; instead of INSIDE the parent &lt;li&gt;."
            }
        ]
    },
    # Page 9
    {
        "day": "Day 9",
        "title": "Block vs Inline Elements",
        "tab": "HTML NOTES",
        "quote": '"Good design is obvious. Great design is transparent"',
        "topics": [
            {
                "heading": "Block-level Elements (&lt;div&gt;, &lt;p&gt;, &lt;h1&gt;)",
                "subpoints": [
                    ("→", "Always starts on a <u>new line</u> and takes up the full width available (100%)."),
                    ("→", "Can have margin, padding, width, and height set in CSS.", "(આખી લાઈન રોકી લે)"),
                    ("→", "Examples: <code>&lt;div&gt;, &lt;p&gt;, &lt;h1&gt;-&lt;h6&gt;, &lt;ul&gt;, &lt;li&gt;, &lt;section&gt;, &lt;form&gt;</code>")
                ],
                "diagram": "[------- Block Element takes 100% width of parent row -------]",
                "remember": "&lt;div&gt; is the universal generic block container for grouping elements.",
                "mistake": "Wrapping block elements inside inline elements (like &lt;h1&gt; inside &lt;span&gt;)."
            },
            {
                "heading": "Inline Elements (&lt;span&gt;, &lt;a&gt;, &lt;b&gt;)",
                "subpoints": [
                    ("→", "Does <u>NOT</u> start on a new line; takes only as much width as its content.", "(જેટલી જરૂર હોય તેટલી જ જગ્યા)"),
                    ("→", "Top & bottom margin/padding do NOT push adjacent lines away!"),
                    ("→", "Examples: <code>&lt;span&gt;, &lt;a&gt;, &lt;b&gt;, &lt;i&gt;, &lt;img&gt;, &lt;code&gt;, &lt;strong&gt;</code>"),
                    ("→", "<b>&lt;span&gt;:</b> Generic inline container for styling specific words in a sentence.")
                ],
                "code": ("Price: &lt;span style=\"color:green;\"&gt;$99&lt;/span&gt;", ":- Price: <span style='color:green;'>$99</span> (stays in same line)"),
                "remember": "Use &lt;div&gt; for building boxes/sections; use &lt;span&gt; for coloring words inside text.",
                "mistake": "Trying to apply CSS width and height to inline elements (they will be ignored!)."
            }
        ]
    },
    # Page 10
    {
        "day": "Day 10",
        "title": "Iframes & Computer Code Tags",
        "tab": "HTML NOTES",
        "quote": '"Programs must be written for people to read, and only incidentally for machines to execute"',
        "topics": [
            {
                "heading": "HTML &lt;iframe&gt; (Inline Frame)",
                "subpoints": [
                    ("→", "Used to embed another document or website inside the current page.", "(બીજી સાઈટ અંદર બતાવવી)"),
                    ("→", "Commonly used for Google Maps, YouTube video players, and widgets."),
                    ("→", "Key attributes: <code>src</code>, <code>width</code>, <code>height</code>, <code>loading=\"lazy\"</code>, <code>sandbox</code>")
                ],
                "analogy": "🪟 Real-life: An iframe is like a glass window inside your room looking into another room.",
                "code": ("&lt;iframe src=\"map.html\" width=\"300\" height=\"200\"&gt;&lt;/iframe&gt;", ":- Embeds 300x200 window"),
                "remember": "Always use the <code>sandbox</code> attribute to prevent malicious scripts from external iframes!",
                "mistake": "Many modern sites (like Google, Facebook) block being embedded in iframes using X-Frame-Options."
            },
            {
                "heading": "Computer Code Tags: &lt;code&gt;, &lt;pre&gt;, &lt;kbd&gt;, &lt;samp&gt;",
                "subpoints": [
                    ("→", "<b>&lt;code&gt;:</b> Displays code in monospace font", "(કોડ લખાણ)"),
                    ("→", "<b>&lt;pre&gt;:</b> Preserves exact spaces and line breaks as typed", "(જગ્યા અને લાઈન સાચવી રાખે)"),
                    ("→", "<b>&lt;kbd&gt;:</b> Represents keyboard keys", "(કીબોર્ડ ની કી - e.g. Ctrl + C)"),
                    ("→", "<b>&lt;samp&gt;:</b> Represents sample computer terminal output")
                ],
                "code": ("Press &lt;kbd&gt;Ctrl&lt;/kbd&gt; + &lt;kbd&gt;C&lt;/kbd&gt; to copy", ":- Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to copy"),
                "remember": "Always wrap multi-line code inside &lt;pre&gt;&lt;code&gt; ... &lt;/code&gt;&lt;/pre&gt;.",
                "mistake": "Expecting &lt;code&gt; alone to preserve spaces; without &lt;pre&gt;, spaces get collapsed into one!"
            }
        ]
    },
    # Page 11
    {
        "day": "Day 11",
        "title": "Semantic HTML Elements",
        "tab": "HTML NOTES",
        "quote": '"Meaningful code makes accessible experiences for everyone"',
        "topics": [
            {
                "heading": "What is Semantic HTML?",
                "subpoints": [
                    ("→", "Semantic elements clearly describe their meaning to browser and developer.", "(અર્થપૂર્ણ ટેગ્સ - tags with meaning)"),
                    ("→", "Non-semantic: <code>&lt;div&gt;</code>, <code>&lt;span&gt;</code> (tells nothing about content)."),
                    ("→", "Semantic: <code>&lt;header&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;footer&gt;</code>")
                ],
                "diagram": "+---------------------------------------+<br>| &lt;header&gt; Logo & Site Title           |<br>| &lt;nav&gt; Home | About | Contact         |<br>+-------------------+-------------------+<br>| &lt;main&gt;            | &lt;aside&gt; Sidebar  |<br>|   &lt;section&gt;       |   Trending links  |<br>|   &lt;article&gt;       |                   |<br>+-------------------+-------------------+<br>| &lt;footer&gt; Copyright &copy; 2026       |<br>+---------------------------------------+",
                "remember": "Semantic tags boost SEO ranking and allow screen readers to navigate effortlessly.",
                "mistake": "Building an entire website using 100 &lt;div&gt; tags ('div soup') instead of semantic tags!"
            },
            {
                "heading": "&lt;section&gt;, &lt;article&gt; & &lt;figure&gt;",
                "subpoints": [
                    ("→", "<b>&lt;section&gt;:</b> Thematic grouping of content, usually with a heading."),
                    ("→", "<b>&lt;article&gt;:</b> Self-contained, independently distributable post/card", "(સ્વતંત્ર લેખ - blog post/news)"),
                    ("→", "<b>&lt;aside&gt;:</b> Sidebar content tangentially related to main content."),
                    ("→", "<b>&lt;figure&gt; & &lt;figcaption&gt;:</b> Self-contained photo with caption underneath.")
                ],
                "code": ("&lt;figure&gt;&lt;img src=\"cat.jpg\"&gt;&lt;figcaption&gt;My Cat&lt;/figcaption&gt;&lt;/figure&gt;", ":- Image paired with caption"),
                "remember": "An &lt;article&gt; should make sense on its own if sent via RSS feed or newsletter.",
                "mistake": "Using &lt;section&gt; as a plain styling wrapper; use &lt;div&gt; for purely visual styling."
            }
        ]
    },
    # Page 12
    {
        "day": "Day 12",
        "title": "Entities & Symbols",
        "tab": "HTML NOTES",
        "quote": '"Every symbol carries a story, every character has a place"',
        "topics": [
            {
                "heading": "HTML Reserved Character Entities",
                "subpoints": [
                    ("→", "Some characters are reserved in HTML (like &lt; and &gt;) because browsers treat them as tags.", "(ખાસ ચિન્હો - reserved characters)"),
                    ("→", "To display these characters on screen, use <u>entity names</u> starting with & and ending with ;"),
                    ("→", "<b>&amp;lt;</b> = &lt; (less than) | <b>&amp;gt;</b> = &gt; (greater than)"),
                    ("→", "<b>&amp;amp;</b> = &amp; (ampersand) | <b>&amp;quot;</b> = \" (double quote)")
                ],
                "code": ("To write &lt;p&gt;, code: &amp;lt;p&amp;gt;", ":- Shows &lt;p&gt; literally on screen"),
                "remember": "Always use &amp;nbsp; when you need a non-breaking space between two words!",
                "mistake": "Typing literal '<' in paragraph text; older browsers may interpret it as an unclosed tag!"
            },
            {
                "heading": "Symbols & Emoji Codes",
                "subpoints": [
                    ("→", "<b>Copyright:</b> <code>&amp;copy;</code> :- &copy; | <b>Registered:</b> <code>&amp;reg;</code> :- &reg;"),
                    ("→", "<b>Trademark:</b> <code>&amp;trade;</code> :- &trade; | <b>Euro / Pound:</b> <code>&amp;euro; &amp;pound;</code> :- &euro; &pound;"),
                    ("→", "<b>Emojis:</b> Encoded via UTF-8 decimal code (e.g. <code>&amp;#128512;</code> = &#128512;)", "(ઈમોજી કોડ)")
                ],
                "code": ("&amp;copy; 2026 Coding Gita &amp;#10084;", ":- &copy; 2026 Coding Gita &#10084;"),
                "remember": "Ensure &lt;meta charset=\"UTF-8\"&gt; is present in &lt;head&gt; so all symbols and emojis render!",
                "mistake": "Forgetting the trailing semicolon (;) on entities like typing &amp;copy without ';'!"
            }
        ]
    },
    # Page 13
    {
        "day": "Day 13",
        "title": "Forms Part 1: Basics & Inputs",
        "tab": "HTML NOTES",
        "quote": '"Listening to user input is the starting point of every interactive system"',
        "topics": [
            {
                "heading": "The &lt;form&gt; Element & HTTP Methods",
                "subpoints": [
                    ("→", "Used to collect user data and send it to server for processing.", "(યુઝર ડેટા ફોર્મ - collecting user data)"),
                    ("→", "<b>action:</b> URL where form data is submitted to."),
                    ("→", "<b>method:</b> HTTP method: <u>GET</u> (shows in URL) vs <u>POST</u> (secure, hidden body)")
                ],
                "analogy": "📮 Real-life: GET is like a public postcard; POST is like a sealed, private envelope.",
                "code": ("&lt;form action=\"/login\" method=\"POST\"&gt; ... &lt;/form&gt;", ":- Submits private payload securely"),
                "remember": "Use POST for passwords, credit cards, or large data; use GET for search forms!",
                "mistake": "Using method=\"GET\" for login passwords (it exposes password directly in URL history!)."
            },
            {
                "heading": "Core Input Types (&lt;input&gt;)",
                "subpoints": [
                    ("→", "<b>type=\"text\":</b> Single line text field", "(ટેક્સ્ટ બોક્સ)"),
                    ("→", "<b>type=\"password\":</b> Masks characters as dots/asterisks", "(પાસવર્ડ બોક્સ - ગુપ્ત અક્ષરો)"),
                    ("→", "<b>type=\"email\":</b> Automatically validates email format (@ symbol)"),
                    ("→", "<b>type=\"number\":</b> Numbers only with min, max, and step controls")
                ],
                "code": ("&lt;input type=\"email\" name=\"user_email\" required&gt;", ":- Input field with email validation"),
                "remember": "Every input MUST have a <code>name</code> attribute, or its value will NOT be sent to server!",
                "mistake": "Using type=\"text\" for phone/passwords instead of specialized type=\"tel\" or \"password\"."
            }
        ]
    },
    # Page 14
    {
        "day": "Day 14",
        "title": "Forms Part 2: Controls & Options",
        "tab": "HTML NOTES",
        "quote": '"User experience is about making interactions effortless and self-evident"',
        "topics": [
            {
                "heading": "Radio, Checkbox & Dropdown",
                "subpoints": [
                    ("→", "<b>type=\"radio\":</b> Select ONLY ONE option from a group (must share same <code>name</code>).", "(એક જ પસંદગી - Gender/Option)"),
                    ("→", "<b>type=\"checkbox\":</b> Select MULTIPLE options independently", "(એકથી વધુ પસંદગી)"),
                    ("→", "<b>&lt;select&gt; &amp; &lt;option&gt;:</b> Dropdown selection menu", "(ડ્રોપડાઉન લિસ્ટ)")
                ],
                "code": ("&lt;input type=\"radio\" name=\"g\" value=\"m\"&gt; Male", ":- ( ) Male (radio selection dot)"),
                "remember": "Radio buttons must share the exact same <code>name</code> to make them mutually exclusive!",
                "mistake": "Giving different name attributes to related radio buttons (user will be able to select all!)."
            },
            {
                "heading": "&lt;label&gt;, &lt;textarea&gt; & Attributes",
                "subpoints": [
                    ("→", "<b>&lt;label for=\"id\"&gt;:</b> Clicking text focuses the corresponding input box.", "(ટેક્સ્ટ પર ક્લિક કરવાથી બોક્સ સિલેક્ટ થાય)"),
                    ("→", "<b>&lt;textarea rows=\"4\"&gt;:</b> Multi-line text input for comments/messages."),
                    ("→", "<b>Attributes:</b> <code>placeholder</code> (hint), <code>required</code> (mandatory), <code>disabled</code>, <code>value</code>")
                ],
                "code": ("&lt;label for=\"n\"&gt;Name&lt;/label&gt;&lt;input id=\"n\" required&gt;", ":- Accessible label bound to input"),
                "remember": "Always pair every input with a &lt;label&gt; using <code>for</code> and <code>id</code> for accessibility!",
                "mistake": "Using placeholder as a replacement for label. Placeholders disappear when user types."
            }
        ]
    },
    # Page 15
    {
        "day": "Day 15",
        "title": "Audio & Video Media",
        "tab": "HTML NOTES",
        "quote": '"Multimedia brings the web alive, connecting sight and sound"',
        "topics": [
            {
                "heading": "Embedding Audio (&lt;audio&gt;)",
                "subpoints": [
                    ("→", "Used to play sound files (mp3, wav, ogg) on webpage without external plugins.", "(ઓડિયો / ગીત વગાડવું)"),
                    ("→", "<b>controls:</b> Displays play, pause, and volume bar."),
                    ("→", "<b>&lt;source src=\"...\" type=\"audio/mpeg\"&gt;:</b> Provides fallback audio formats.")
                ],
                "code": ("&lt;audio controls&gt;&lt;source src=\"a.mp3\"&gt;&lt;/audio&gt;", ":- Audio player with play button"),
                "remember": "Always include the <code>controls</code> attribute, otherwise the audio player is completely invisible!",
                "mistake": "Using <code>autoplay</code> with sound; modern browsers block audio autoplay to protect users."
            },
            {
                "heading": "Embedding Video (&lt;video&gt;)",
                "subpoints": [
                    ("→", "Used to embed video clips (mp4, webm).", "(વિડીયો પ્લેયર - video on page)"),
                    ("→", "<b>poster=\"img.jpg\":</b> Thumbnail image displayed before video plays.", "(વિડીયો શરૂ થતા પહેલા નો ફોટો)"),
                    ("→", "<b>attributes:</b> <code>controls</code>, <code>autoplay muted</code>, <code>loop</code>, <code>width=\"640\"</code>")
                ],
                "code": ("&lt;video controls poster=\"thumb.jpg\" width=\"400\"&gt;&lt;/video&gt;", ":- Video box with thumbnail"),
                "remember": "If you want video to autoplay on page load, you MUST add <code>muted</code>!",
                "mistake": "Uploading huge raw 4K video files directly; compress to WebM or stream via YouTube/Vimeo."
            }
        ]
    },
    # Page 16
    {
        "day": "Day 16",
        "title": "Meta Tags & SEO Head",
        "tab": "HTML NOTES",
        "quote": '"What is unseen often provides the power for everything that is seen"',
        "topics": [
            {
                "heading": "Essential Meta Tags in &lt;head&gt;",
                "subpoints": [
                    ("→", "Meta tags live inside <code>&lt;head&gt;</code> and supply metadata to browsers & search engines.", "(પેજ ની છુપી માહિતી - metadata)"),
                    ("→", "<b>charset=\"UTF-8\":</b> Supports all languages (English, Gujarati, Hindi, Emoji)."),
                    ("→", "<b>viewport:</b> <code>content=\"width=device-width, initial-scale=1.0\"</code> enables mobile responsiveness!", "(મોબાઈલ સ્ક્રીન સાઈઝ સેટિંગ)")
                ],
                "diagram": "&lt;meta charset=\"UTF-8\"&gt;<br>&lt;meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"&gt;<br>&lt;meta name=\"description\" content=\"Best HTML Study Notes\"&gt;",
                "remember": "Without the viewport meta tag, mobile phones will display desktop sites tiny and zoomed-out!",
                "mistake": "Forgetting charset=\"UTF-8\" leads to Gujarati or Hindi characters turning into garbage symbols ()."
            },
            {
                "heading": "SEO & Social Sharing Meta Tags",
                "subpoints": [
                    ("→", "<b>meta description:</b> The 1-2 sentence snippet displayed in Google search results.", "(ગૂગલ સર્ચ રિઝલ્ટ લખાણ)"),
                    ("→", "<b>Open Graph (og:title, og:image):</b> Controls title & preview card when shared on WhatsApp/Twitter.", "(વોટ્સએપ શેરિંગ કાર્ડ)"),
                    ("→", "<b>&lt;link rel=\"icon\" href=\"favicon.ico\"&gt;:</b> Displays small logo on browser tab.")
                ],
                "code": ("&lt;meta name=\"description\" content=\"Free CSE Web Dev Notes\"&gt;", ":- Sets Google search snippet"),
                "remember": "Keep meta description between 150-160 characters so Google does not cut it off!",
                "mistake": "Stuffing 50 repetitive keywords in meta keywords tag; Google ignores keyword tags today."
            }
        ]
    }
]

def generate_pages_html(pages_data, subject_name):
    pages_html = []
    for p in pages_data:
        topic_blocks_html = []
        for t in p["topics"]:
            subpoints_html = []
            for sp in t.get("subpoints", []):
                arrow = sp[0]
                text = sp[1]
                guj = sp[2] if len(sp) > 2 else ""
                guj_html = f'<span class="gujarati-note">{guj}</span>' if guj else ""
                subpoints_html.append(f'<div class="sub-point"><span class="arrow">{arrow}</span> {text} {guj_html}</div>')
            
            diagram_html = f'<div class="diagram-box">{t["diagram"]}</div>' if "diagram" in t else ""
            
            subpoints2_html = []
            for sp in t.get("subpoints2", []):
                arrow = sp[0]
                text = sp[1]
                guj = sp[2] if len(sp) > 2 else ""
                guj_html = f'<span class="gujarati-note">{guj}</span>' if guj else ""
                subpoints2_html.append(f'<div class="sub-point"><span class="arrow">{arrow}</span> {text} {guj_html}</div>')
            
            analogy_html = f'<div class="real-life-box">{t["analogy"]}</div>' if "analogy" in t else ""
            
            code_html = ""
            if "code" in t:
                code_html = f'''<div class="code-row">
                    <span class="code-snippet">{t["code"][0]}</span>
                    <span class="code-output">{t["code"][1]}</span>
                </div>'''
            
            remember_html = f'<div class="remember-line"><b>Remember:</b> {t["remember"]}</div>' if "remember" in t else ""
            mistake_html = f'<div class="mistake-line"><b>Mistake:</b> {t["mistake"]}</div>' if "mistake" in t else ""
            
            block = f'''<div class="topic-block">
                <div class="topic-heading"><span class="dot">•</span> {t["heading"]}</div>
                {''.join(subpoints_html)}
                {analogy_html}
                {diagram_html}
                {''.join(subpoints2_html)}
                {code_html}
                {remember_html}
                {mistake_html}
            </div>'''
            topic_blocks_html.append(block)
        
        page_html = f'''<div class="diary-page" id="{p['day'].lower().replace(' ', '-')}">
            <div class="margin-line"></div>
            <div class="margin-line-secondary"></div>
            <div class="ruled-lines-layer"></div>
            <div class="diary-tab">{p["tab"]}</div>

            <div class="diary-header">
                <div class="header-left">
                    <span class="day-badge">{p["day"]}</span>
                    <span class="topic-title">• {p["title"]}</span>
                </div>
                <div class="header-right">
                    <div class="year">2026 • CSE (AI)</div>
                    <div>SEMESTER 1 • DIARY NOTES</div>
                </div>
            </div>

            <div class="page-content">
                {''.join(topic_blocks_html)}
            </div>

            <div class="diary-footer">
                {p["quote"]}
            </div>
        </div>'''
        pages_html.append(page_html)

    full_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{subject_name} Handwritten Diary Study Notes</title>
<style>
{CSS_TEMPLATE}
</style>
</head>
<body>
{''.join(pages_html)}
</body>
</html>'''
    return full_doc

with open('html_notes.html', 'w', encoding='utf-8') as f:
    f.write(generate_pages_html(html_pages_data, "HTML"))

print("Generated html_notes.html successfully with", len(html_pages_data), "pages!")
