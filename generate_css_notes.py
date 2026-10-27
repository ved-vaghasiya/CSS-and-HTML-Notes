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
    color: #5b21b6;
    line-height: 1;
    letter-spacing: 0.5px;
}

.topic-title {
    font-family: 'Caveat', cursive;
    font-size: 25px;
    font-weight: 700;
    color: #1e1b4b;
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
    background-color: #6d28d9;
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
    color: #3b0764;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 6px;
}

.topic-heading span.dot {
    font-size: 20px;
    color: #7c3aed;
}

.sub-point {
    font-size: 18px;
    line-height: 1.35;
    color: #1e1b4b;
    margin: 1px 0;
    padding-left: 8px;
}

.sub-point .arrow {
    color: #7c3aed;
    font-weight: bold;
    margin-right: 4px;
}

.gujarati-note {
    font-family: 'Noto Sans Gujarati', sans-serif;
    color: #4c1d95;
    font-size: 15px;
    background: #f5f3ff;
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
    border-left: 3px solid #c4b5fd;
    font-style: italic;
}

.code-row {
    background: #f8fafc;
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
    color: #4338ca;
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
    color: #4338ca;
    background: #eef2ff;
    border-left: 3px solid #6366f1;
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

css_pages_data = [
    # Day 1
    {
        "day": "Day 1",
        "title": "Intro to CSS & Selectors",
        "tab": "CSS NOTES",
        "quote": '"Design is not just what it looks like and feels like. Design is how it works"',
        "topics": [
            {
                "heading": "Introduction to CSS",
                "subpoints": [
                    ("→", "Stands for <u>Cascading Style Sheets</u>.", "(વેબસાઇટ નો શણગાર - decoration and styling)"),
                    ("→", "Controls layout, colors, typography, spacing, and animations across web pages."),
                    ("→", "Syntax: <code>selector { property: value; }</code>")
                ],
                "analogy": "🎨 Real-life: HTML is building a bare concrete house; CSS is plaster, colorful paint, and furniture.",
                "code": ("h1 { color: blue; font-size: 24px; }", ":- Makes all &lt;h1&gt; titles blue and 24px"),
                "remember": "Always enclose property-value pairs inside curly braces { } and end lines with semicolons (;).",
                "mistake": "Using '=' instead of ':' (e.g. writing color=red; instead of color: red;)."
            },
            {
                "heading": "Core Selectors: Element, Class & ID",
                "subpoints": [
                    ("→", "<b>Element Selector:</b> Targets all tags of that type (e.g. <code>p { ... }</code>)."),
                    ("→", "<b>Class Selector (.name):</b> Reusable style across multiple elements", "(વર્ગ - ગમે તેટલા તત્વો પર વાપરી શકાય)"),
                    ("→", "<b>ID Selector (#name):</b> Targets exactly ONE unique element per page", "(અનન્ય ઓળખ - એક જ એલિમેન્ટ માટે)")
                ],
                "code": (".btn { padding: 8px; } | #header { top: 0; }", ":- Reusable button | Single unique header"),
                "remember": "Classes start with a dot (.), IDs start with a hash (#).",
                "mistake": "Reusing the same ID on multiple HTML elements; IDs must be strictly unique!"
            }
        ]
    },
    # Day 2
    {
        "day": "Day 2",
        "title": "Comments & Error Handling",
        "tab": "CSS NOTES",
        "quote": '"Clarity of mind means clarity of code"',
        "topics": [
            {
                "heading": "CSS Comments",
                "subpoints": [
                    ("→", "Written using <code>/* comment here */</code> syntax.", "(કોડ સમજવા માટે નોંધ)"),
                    ("→", "Can span single or multiple lines; completely ignored by the browser."),
                    ("→", "Used to organize sections: Header, Navbar, Footer, Media Queries.")
                ],
                "code": ("/* Main Button Style */ .btn { ... }", ":- Explains purpose of the CSS rule"),
                "remember": "CSS does NOT support // single-line comments! Always use /* ... */.",
                "mistake": "Writing HTML comments &lt;!-- --&gt; or JavaScript // inside CSS files."
            },
            {
                "heading": "CSS Error Handling",
                "subpoints": [
                    ("→", "CSS fails silently: it never throws fatal crashes or alerts.", "(ભૂલ હોય તો તે લાઈન છોડી આગળ વધે)"),
                    ("→", "If a browser encounters an unknown property or invalid value, it simply ignores that line and applies the rest."),
                    ("→", "Allows new modern CSS features to be used safely with graceful fallback for older browsers.")
                ],
                "code": ("p { colr: red; font-weight: bold; }", ":- 'colr' typo ignored; bold is still applied!"),
                "remember": "Use browser DevTools (Inspect Element) to spot strikethrough warnings on invalid properties.",
                "mistake": "Assuming silent CSS means code is error-free; always inspect in DevTools!"
            }
        ]
    },
    # Day 3
    {
        "day": "Day 3",
        "title": "Colors & Backgrounds",
        "tab": "CSS NOTES",
        "quote": '"Colors, like features, follow the changes of the emotions"',
        "topics": [
            {
                "heading": "Color Formats in CSS",
                "subpoints": [
                    ("→", "<b>Named Colors:</b> red, blue, coral, darkslateblue (140+ predefined names)."),
                    ("→", "<b>HEX Code:</b> #ff0000 (Red), #ffffff (White), #000000 (Black)."),
                    ("→", "<b>RGB & RGBA:</b> <code>rgb(255, 0, 0)</code> and <code>rgba(0, 0, 0, 0.5)</code>", "(પારદર્શક રંગ - transparency)")
                ],
                "code": ("color: rgba(0, 100, 255, 0.7);", ":- Blue with 70% opacity"),
                "remember": "The 'A' in RGBA stands for Alpha (opacity from 0.0 transparent to 1.0 solid).",
                "mistake": "Confusing color (text color) with background-color (box fill color)."
            },
            {
                "heading": "CSS Background Properties",
                "subpoints": [
                    ("→", "<b>background-color:</b> Fills background with a solid color.", "(પાછળ નો રંગ)"),
                    ("→", "<b>background-image:</b> <code>url('bg.jpg')</code> loads an image.", "(પાછળ નો ફોટો)"),
                    ("→", "<b>background-repeat:</b> <code>no-repeat</code> prevents tiling."),
                    ("→", "<b>background-size:</b> <code>cover</code> scales image to fill the entire container proportionally.")
                ],
                "code": ("background: url('bg.jpg') no-repeat center/cover;", ":- Perfect full-cover background image"),
                "remember": "Always provide a fallback background-color in case the background image fails to load!",
                "mistake": "Forgetting no-repeat; small background images will tile across the whole page by default."
            }
        ]
    },
    # Day 4
    {
        "day": "Day 4",
        "title": "Borders & Rounded Corners",
        "tab": "CSS NOTES",
        "quote": '"Good boundaries create clarity and pleasant aesthetics"',
        "topics": [
            {
                "heading": "CSS Borders",
                "subpoints": [
                    ("→", "Surrounds elements with a line. Has width, style, and color.", "(કિનારી / બોર્ડર)"),
                    ("→", "<b>Styles:</b> solid, dashed, dotted, double, groove, none."),
                    ("→", "<b>Shorthand:</b> <code>border: 2px solid #3b82f6;</code>")
                ],
                "code": ("border-bottom: 3px dashed red;", ":- Dashed red underline below the box"),
                "remember": "If border-style is not specified, border defaults to 'none' and will NOT show!",
                "mistake": "Writing border: 2px red; without specifying 'solid' or 'dashed' (border won't appear!)."
            },
            {
                "heading": "Rounded Corners: border-radius",
                "subpoints": [
                    ("→", "Curves the sharp 90-degree corners of any box or button.", "(ખૂણા ગોળ કરવા)"),
                    ("→", "Small curves: <code>border-radius: 6px;</code>"),
                    ("→", "Pill buttons: <code>border-radius: 9999px;</code>"),
                    ("→", "Perfect circle: <code>width: 100px; height: 100px; border-radius: 50%;</code>")
                ],
                "code": ("border-radius: 50%; width: 80px; height: 80px;", ":- Turns square avatar into a perfect circle"),
                "remember": "For border-radius: 50% to produce a circle, width and height MUST be equal!",
                "mistake": "Setting border-radius: 50% on a rectangular image; it becomes an oval, not a circle."
            }
        ]
    },
    # Day 5
    {
        "day": "Day 5",
        "title": "Margin, Padding & Box Model",
        "tab": "CSS NOTES",
        "quote": '"Space is the breath of art"',
        "topics": [
            {
                "heading": "Margin vs Padding",
                "subpoints": [
                    ("→", "<b>Margin:</b> Space <u>OUTSIDE</u> the border (pushes neighbor elements away).", "(બોર્ડર ની બહાર ની ખાલી જગ્યા)"),
                    ("→", "<b>Padding:</b> Space <u>INSIDE</u> the border (cushions text inside the box).", "(બોર્ડર ની અંદર ની ખાલી જગ્યા)"),
                    ("→", "<b>Shorthand (Clockwise):</b> <code>margin: Top Right Bottom Left;</code> (TRBL)")
                ],
                "code": ("padding: 10px 20px;", ":- 10px Top/Bottom, 20px Left/Right"),
                "remember": "margin: 0 auto; centers a block element horizontally within its parent container!",
                "mistake": "Using margin when you want to increase clickable area of a button; use padding instead."
            },
            {
                "heading": "The CSS Box Model & box-sizing",
                "subpoints": [
                    ("→", "Every element is a rectangular box made of: Content → Padding → Border → Margin."),
                    ("→", "<b>Standard box-sizing: content-box</b> adds padding & border on TOP of width (causes horizontal overflow!)."),
                    ("→", "<b>border-box:</b> Keeps total width fixed; padding and border stay INSIDE the specified width.", "(સાઈઝ બહાર ન નીકળે)")
                ],
                "diagram": "+---------------------------------------+<br>| Margin (Outside Space)                |<br>|   +-------------------------------+   |<br>|   | Border                        |   |<br>|   |   +-----------------------+   |   |<br>|   |   | Padding (Inside Space)|   |   |<br>|   |   |   +---------------+   |   |   |<br>|   |   |   | Content       |   |   |   |<br>+---+---+---+---------------+---+---+---+",
                "remember": "Always put * { box-sizing: border-box; } at the top of every CSS project!",
                "mistake": "Leaving default content-box; adding 20px padding to a 100% wide box creates scrollbars."
            }
        ]
    },
    # Day 6
    {
        "day": "Day 6",
        "title": "Width, Height & Max-Width",
        "tab": "CSS NOTES",
        "quote": '"Flexibility is the key to stability"',
        "topics": [
            {
                "heading": "Width & Height Properties",
                "subpoints": [
                    ("→", "Sets the width and height of block-level and inline-block elements.", "(પહોળાઈ અને ઊંચાઈ)"),
                    ("→", "Can be set in fixed units (<code>px</code>) or relative units (<code>%, vh, vw</code>)."),
                    ("→", "<code>auto</code> lets browser calculate based on content size.")
                ],
                "code": ("div { width: 50%; height: 200px; }", ":- Half width of screen, 200px tall"),
                "remember": "Inline elements (like &lt;span&gt; or &lt;a&gt;) IGNORE width and height properties!",
                "mistake": "Setting hardcoded height in pixels on text cards; content will overflow when text grows."
            },
            {
                "heading": "max-width for Responsive Design",
                "subpoints": [
                    ("→", "<b>max-width:</b> Restricts element from growing beyond a limit, but allows it to shrink on smaller screens.", "(મહત્તમ પહોળાઈ - સ્ક્રીન નાની થાય ત્યારે સંકોચાય)"),
                    ("→", "<b>Responsive images rule:</b> <code>img { max-width: 100%; height: auto; }</code> prevents image from spilling off screen.")
                ],
                "code": (".container { max-width: 1200px; width: 100%; margin: 0 auto; }", ":- Responsive centered website container"),
                "remember": "Prefer max-width over fixed width for main layout wrappers and images!",
                "mistake": "Using width: 1200px on mobile; screen will force a clumsy horizontal scrollbar."
            }
        ]
    },
    # Day 7
    {
        "day": "Day 7",
        "title": "Outline & Text Styling",
        "tab": "CSS NOTES",
        "quote": '"Type is a beautiful group of letters, not a group of beautiful letters"',
        "topics": [
            {
                "heading": "CSS Outline vs Border",
                "subpoints": [
                    ("→", "<b>Outline:</b> Drawn outside the border edge; does NOT take up any layout space.", "(બહાર ની વધારાની લાઈન)"),
                    ("→", "Does not affect document flow or push adjacent elements."),
                    ("→", "Most commonly used for accessibility keyboard focus indicators (<code>:focus-visible</code>).")
                ],
                "code": ("input:focus { outline: 2px solid blue; }", ":- Blue highlight box when user clicks input"),
                "remember": "Never set outline: none without providing an alternative focus indicator for keyboard users!",
                "mistake": "Using outline: none on forms; blind and keyboard users will lose track of where they are."
            },
            {
                "heading": "Text Formatting Properties",
                "subpoints": [
                    ("→", "<b>color:</b> Text color | <b>text-align:</b> left, center, right, justify.", "(લખાણ ની ગોઠવણી)"),
                    ("→", "<b>text-decoration:</b> none (removes link underline), underline, line-through."),
                    ("→", "<b>text-transform:</b> uppercase, lowercase, capitalize.", "(મોટા કે નાના અક્ષરો)"),
                    ("→", "<b>line-height:</b> Distance between lines of text (ideal: 1.5 to 1.6 for readability).")
                ],
                "code": ("a { text-decoration: none; text-transform: uppercase; }", ":- Clean uppercase links without underline"),
                "remember": "Always use line-height: 1.5+ on body text for comfortable reading experience.",
                "mistake": "Using text-align: justify on websites; it creates awkward 'rivers' of empty white gaps."
            }
        ]
    },
    # Day 8
    {
        "day": "Day 8",
        "title": "Fonts & Icons",
        "tab": "CSS NOTES",
        "quote": '"Words have meaning, type has character"',
        "topics": [
            {
                "heading": "Typography & Font Properties",
                "subpoints": [
                    ("→", "<b>font-family:</b> Specifies font face with fallbacks: <code>'Inter', Arial, sans-serif;</code>", "(ફોન્ટ ની શૈલી)"),
                    ("→", "<b>font-size:</b> Text size (e.g. <code>16px, 1.25rem</code>)."),
                    ("→", "<b>font-weight:</b> Thickness from thin (100), regular (400), semi-bold (600), to bold (700)."),
                    ("→", "<b>Google Fonts:</b> Import via <code>@import url('...');</code> in CSS or &lt;link&gt; in HTML.")
                ],
                "code": ("font-family: 'Patrick Hand', cursive, sans-serif;", ":- Applies handwriting font with fallbacks"),
                "remember": "Always include a generic fallback (sans-serif, serif, or monospace) at the end of font-family!",
                "mistake": "Using 5 different font families on one webpage; stick to 1 or 2 fonts maximum."
            },
            {
                "heading": "Web Icons (FontAwesome & SVG)",
                "subpoints": [
                    ("→", "Icons can be added using icon font libraries (Font Awesome) or inline SVGs.", "(આઇકોન્સ - પ્રતીકો)"),
                    ("→", "Icon fonts can be styled just like regular text using <code>font-size</code> and <code>color</code>!"),
                    ("→", "SVGs provide sharp crisp rendering on all retina high-res screens.")
                ],
                "code": (".icon { font-size: 24px; color: #f59e0b; }", ":- Sizes and colors icon like normal text"),
                "remember": "SVG icons are resolution-independent and will never get blurry on zoom!",
                "mistake": "Using low-res PNG files for icons; they look pixelated on mobile phones."
            }
        ]
    },
    # Day 9
    {
        "day": "Day 9",
        "title": "Links & Lists Styling",
        "tab": "CSS NOTES",
        "quote": '"Navigation should be a guide, not a puzzle"',
        "topics": [
            {
                "heading": "Styling Hyperlink States (LVHA Rule)",
                "subpoints": [
                    ("→", "Links have 4 interactive pseudo-classes:", "(લિંક ની અલગ અલગ સ્થિતિ)"),
                    ("→", "<b>:link</b> (normal unvisited) → <b>:visited</b> (already visited page)"),
                    ("→", "<b>:hover</b> (mouse over) → <b>:active</b> (moment link is clicked).")
                ],
                "code": ("a:hover { color: orange; text-decoration: underline; }", ":- Highlights when cursor hovers"),
                "remember": "Follow the LVHA order strictly in CSS: :link → :visited → :hover → :active!",
                "mistake": "Writing :hover before :link in CSS; the hover effect will be overridden and fail!"
            },
            {
                "heading": "Styling HTML Lists",
                "subpoints": [
                    ("→", "<b>list-style-type:</b> none, disc, circle, square, decimal, lower-alpha.", "(લિસ્ટ ના ટપકાં બદલવા)"),
                    ("→", "<b>list-style: none;</b> Removes default black dots and numbers."),
                    ("→", "To reset a list for navbars: <code>list-style: none; padding: 0; margin: 0;</code>")
                ],
                "code": ("ul.nav { list-style: none; display: flex; gap: 15px; }", ":- Turns list into horizontal navigation bar"),
                "remember": "Browser adds default padding-left (40px) to &lt;ul&gt;; remember to zero it out when resetting!",
                "mistake": "Setting list-style: none and wondering why items are indented (forgot to set padding: 0;)."
            }
        ]
    },
    # Day 10
    {
        "day": "Day 10",
        "title": "Tables & Display Property",
        "tab": "CSS NOTES",
        "quote": '"Structure enables freedom of presentation"',
        "topics": [
            {
                "heading": "CSS Table Styling",
                "subpoints": [
                    ("→", "<b>border-collapse: collapse;</b> Merges double border lines into a single clean line.", "(ડબલ લાઈન ભેગી કરી સિંગલ લાઈન બનાવવી)"),
                    ("→", "Zebra striping: <code>tr:nth-child(even) { background: #f1f5f9; }</code>", "(એક પછી એક પટ્ટા વાળો રંગ)"),
                    ("→", "Hover effect: <code>tr:hover { background: #e2e8f0; }</code>")
                ],
                "code": ("table { width: 100%; border-collapse: collapse; }", ":- Clean, full-width single-bordered table"),
                "remember": "Without border-collapse: collapse, HTML tables show an ugly double border around cells!",
                "mistake": "Forgetting to add padding to &lt;th&gt; and &lt;td&gt;; text will touch the border lines."
            },
            {
                "heading": "The CSS display Property",
                "subpoints": [
                    ("→", "Controls how an element is rendered in page flow.", "(એલિમેન્ટ નો પ્રદર્શન પ્રકાર)"),
                    ("→", "<b>block:</b> Full width, starts new line (div, p)."),
                    ("→", "<b>inline:</b> Flow within sentence, ignores width/height (span, a)."),
                    ("→", "<b>inline-block:</b> Flows like inline, BUT respects width, height, and margins!"),
                    ("→", "<b>none:</b> Completely hides element and removes its space from document.")
                ],
                "code": (".btn { display: inline-block; padding: 10px 20px; }", ":- Allows padding & width on link buttons"),
                "remember": "display: none hides element completely; visibility: hidden hides it but reserves empty space!",
                "mistake": "Trying to apply width & top/bottom margin to inline elements without setting inline-block."
            }
        ]
    },
    # Day 11
    {
        "day": "Day 11",
        "title": "CSS Positions",
        "tab": "CSS NOTES",
        "quote": '"Everything has its place, and everything in its place"',
        "topics": [
            {
                "heading": "Static, Relative & Absolute Positioning",
                "subpoints": [
                    ("→", "<b>position: static:</b> Default normal page flow; top/left/right/bottom have no effect.", "(સામાન્ય ગોઠવણી)"),
                    ("→", "<b>position: relative:</b> Shifted relative to its normal position without disturbing others.", "(પોતાની જગ્યા થી ખસવું)"),
                    ("→", "<b>position: absolute:</b> Removed from normal flow; positioned relative to nearest <u>positioned parent</u> (with relative/absolute).", "(પેરેન્ટ ના આધારે ગમે ત્યાં મૂકવું)")
                ],
                "code": (".parent { position: relative; } .badge { position: absolute; top: -5px; right: -5px; }", ":- Notification badge on top corner"),
                "remember": "Always give position: relative to parent before putting position: absolute on children!",
                "mistake": "Setting position: absolute without a relative parent; the child jumps to the top of &lt;body&gt;!"
            },
            {
                "heading": "Fixed & Sticky Positioning",
                "subpoints": [
                    ("→", "<b>position: fixed:</b> Locked to the browser viewport; stays in exact place even when scrolling.", "(સ્ક્રીન પર ચોંટી રહેવું - e.g. floating chat/navbar)"),
                    ("→", "<b>position: sticky:</b> Scrolls normally until reaching offset (e.g. <code>top: 0</code>), then sticks like fixed!", "(સ્ક્રોલ થતા ટોપ પર ચોંટી જવું)")
                ],
                "code": ("nav { position: sticky; top: 0; z-index: 100; }", ":- Header that sticks to top when user scrolls down"),
                "remember": "position: sticky requires at least one direction offset (top, bottom, left, or right) to work!",
                "mistake": "Using position: sticky inside an ancestor that has overflow: hidden (sticky will NOT work!)."
            }
        ]
    },
    # Day 12
    {
        "day": "Day 12",
        "title": "Z-Index & Overflow",
        "tab": "CSS NOTES",
        "quote": '"Layers of depth create a world of perspective"',
        "topics": [
            {
                "heading": "Layer Stacking with z-index",
                "subpoints": [
                    ("→", "Controls vertical stacking order of overlapping elements (3rd dimension Z-axis).", "(કયું એલિમેન્ટ ઉપર દેખાશે - stacking order)"),
                    ("→", "Higher number appears on top of lower numbers (e.g. <code>z-index: 10</code> beats <code>z-index: 1</code>)."),
                    ("→", "Can be negative (<code>z-index: -1</code> places background behind content).")
                ],
                "code": (".modal { position: fixed; z-index: 1000; }", ":- Pops up above all regular website elements"),
                "remember": "z-index ONLY works on elements with a position property (relative, absolute, fixed, sticky)!",
                "mistake": "Adding z-index: 9999 to position: static element and wondering why it doesn't come on top."
            },
            {
                "heading": "Handling Spills with overflow",
                "subpoints": [
                    ("→", "Controls what happens when content exceeds its box container's width/height.", "(લખાણ બોક્સ ની બહાર નીકળે ત્યારે)"),
                    ("→", "<b>visible:</b> Default; spills outside the box boundary."),
                    ("→", "<b>hidden:</b> Clips the overflow; extra content becomes invisible."),
                    ("→", "<b>scroll:</b> Always shows scrollbars (even if content fits)."),
                    ("→", "<b>auto:</b> Smart; adds scrollbar ONLY when content actually overflows.")
                ],
                "code": (".card-body { height: 200px; overflow-y: auto; }", ":- Clean vertical scroll when text gets long"),
                "remember": "Use overflow: auto instead of overflow: scroll to avoid empty disabled scrollbars!",
                "mistake": "Setting overflow: hidden on dropdown menus; the dropdown list will be cut off and hidden!"
            }
        ]
    },
    # Day 13
    {
        "day": "Day 13",
        "title": "Floats & Alignment",
        "tab": "CSS NOTES",
        "quote": '"Balance is not something you find, it\'s something you create"',
        "topics": [
            {
                "heading": "Float, Clear & Clearfix",
                "subpoints": [
                    ("→", "<b>float: left / right:</b> Pushes element to side and lets text wrap around it (magazine style).", "(એલિમેન્ટ ને ડાબે કે જમણે તરતું મૂકવું)"),
                    ("→", "<b>clear: both:</b> Prevents following elements from wrapping around floated items."),
                    ("→", "<b>Clearfix Hack:</b> When parent collapses because all children are floated, add <code>overflow: auto;</code> or <code>.clearfix::after</code>.")
                ],
                "code": ("img { float: left; margin-right: 15px; }", ":- Article text wraps neatly around the image"),
                "remember": "Use Flexbox and Grid for modern layouts; reserve float strictly for text-wrapping images!",
                "mistake": "Floating child elements without clearing; parent height collapses to 0px!"
            },
            {
                "heading": "Centering & Alignment Methods",
                "subpoints": [
                    ("→", "<b>Center inline text / images:</b> <code>text-align: center;</code> on parent container.", "(લખાણ વચ્ચે લાવવું)"),
                    ("→", "<b>Center block box:</b> <code>margin: 0 auto; width: 600px;</code> on the block itself.", "(બોક્સ ને વચ્ચે લાવવું)"),
                    ("→", "<b>Center both vertically & horizontally:</b> <code>display: flex; justify-content: center; align-items: center;</code>")
                ],
                "code": (".box { width: 400px; margin: 0 auto; }", ":- Centers a 400px wide card on the screen"),
                "remember": "margin: 0 auto ONLY works if the element has a specified width and is display: block!",
                "mistake": "Putting text-align: center on a div expecting the div box itself to center (it only centers text inside!)."
            }
        ]
    },
    # Day 14
    {
        "day": "Day 14",
        "title": "CSS Combinators",
        "tab": "CSS NOTES",
        "quote": '"Relationships define meaning in systems and code"',
        "topics": [
            {
                "heading": "Descendant & Child Combinators",
                "subpoints": [
                    ("→", "Combinators explain relationship between multiple selectors.", "(સિલેક્ટર્સ વચ્ચે નો સંબંધ)"),
                    ("→", "<b>Descendant Selector (space):</b> Targets ALL matching children, grandchildren, and deeper.", "(અંદર ના તમામ વારસદારો)"),
                    ("→", "<b>Child Selector (>):</b> Targets ONLY direct immediate children (1 level deep).", "(ફક્ત સીધો પુત્ર - direct child)")
                ],
                "code": ("div p { ... } vs div > p { ... }", ":- All paragraphs inside div vs only direct child paragraphs"),
                "remember": "Use child selector (>) when you want to avoid accidentally styling deeply nested elements!",
                "mistake": "Using space selector when styling navbar dropdowns; sub-dropdown items inherit unwanted styles."
            },
            {
                "heading": "Sibling Combinators (+ and ~)",
                "subpoints": [
                    ("→", "<b>Adjacent Sibling (+):</b> Targets the element immediately following another element.", "(તરત પછી નું પડોશી એલિમેન્ટ)"),
                    ("→", "<b>General Sibling (~):</b> Targets all siblings that follow an element at the same level.", "(પછી ના તમામ પડોશી એલિમેન્ટ્સ)")
                ],
                "code": ("h2 + p { font-size: 18px; font-weight: bold; }", ":- Styles only the lead paragraph directly following h2"),
                "remember": "The adjacent sibling (+) is perfect for styling the first paragraph after a heading!",
                "mistake": "Thinking '+' targets preceding elements; combinators only target elements that appear AFTER."
            }
        ]
    },
    # Day 15
    {
        "day": "Day 15",
        "title": "Pseudo-classes & Elements",
        "tab": "CSS NOTES",
        "quote": '"The unseen details create the magic of modern interfaces"',
        "topics": [
            {
                "heading": "CSS Pseudo-Classes (:)",
                "subpoints": [
                    ("→", "Defines a special STATE of an element (single colon <code>:</code>).", "(એલિમેન્ટ ની ખાસ પરિસ્થિતિ)"),
                    ("→", "<b>:hover:</b> Mouse cursor is over the element."),
                    ("→", "<b>:focus:</b> Form input is actively selected."),
                    ("→", "<b>:first-child & :last-child:</b> First / last child of parent."),
                    ("→", "<b>:nth-child(2n):</b> Every even child (used for zebra striping tables).")
                ],
                "code": ("button:hover { transform: translateY(-2px); }", ":- Subtle lift animation on mouse hover"),
                "remember": ":nth-child() is 1-indexed in CSS (first element is 1, not 0)!",
                "mistake": "Using :nth-child(0); it matches nothing because CSS child counting starts at 1."
            },
            {
                "heading": "CSS Pseudo-Elements (::)",
                "subpoints": [
                    ("→", "Styles a specific PART of an element or creates virtual elements (double colon <code>::</code>).", "(વર્ચ્યુઅલ એલિમેન્ટ બનાવવું)"),
                    ("→", "<b>::before & ::after:</b> Injects decorative content before or after element without HTML tags!"),
                    ("→", "<b>::first-letter:</b> Drop-cap initial letter like in storybooks."),
                    ("→", "<b>::selection:</b> Styles highlighted text selection color.")
                ],
                "code": (".star::after { content: ' ★'; color: gold; }", ":- Adds gold star after text via CSS"),
                "remember": "::before and ::after MUST always have <code>content: '';</code> (even if empty) to render!",
                "mistake": "Omitting the content property on ::before/::after; the pseudo-element will not display."
            }
        ]
    },
    # Day 16
    {
        "day": "Day 16",
        "title": "Navbars & Dropdowns",
        "tab": "CSS NOTES",
        "quote": '"Good navigation leads visitors where they want to go with zero friction"',
        "topics": [
            {
                "heading": "Building Clean Navbars",
                "subpoints": [
                    ("→", "Navbars are built using semantic <code>&lt;nav&gt;</code> containing a <code>&lt;ul&gt;</code>.", "(નેવિગેશન મેનુ બાર)"),
                    ("→", "Remove bullet dots: <code>list-style: none;</code>"),
                    ("→", "Horizontal alignment: <code>display: flex; gap: 20px; align-items: center;</code>"),
                    ("→", "Give links generous padding (<code>padding: 8px 16px;</code>) for comfortable tap targets on touchscreens.")
                ],
                "code": ("nav ul { display: flex; list-style: none; gap: 20px; }", ":- Clean modern horizontal menu"),
                "remember": "Make the entire link clickable with padding, rather than making user click tiny text letters!",
                "mistake": "Applying padding to &lt;li&gt; instead of &lt;a&gt;; only the letters will be clickable."
            },
            {
                "heading": "Pure CSS Dropdown Menus",
                "subpoints": [
                    ("→", "Parent list item gets <code>position: relative;</code>.", "(ડ્રોપડાઉન સબ-મેનુ)"),
                    ("→", "Sub-menu gets <code>position: absolute; display: none; top: 100%; left: 0;</code>"),
                    ("→", "On hover: <code>.nav-item:hover .sub-menu { display: block; }</code> reveals menu!")
                ],
                "diagram": "[ Products v ] ← parent (position: relative)<br>&nbsp;&nbsp;|-- [ Laptops ]<br>&nbsp;&nbsp;|-- [ Mobiles ] ← sub-menu (position: absolute; display: none)",
                "remember": "Add a subtle box-shadow (0 4px 12px rgba(0,0,0,0.15)) to dropdowns for depth!",
                "mistake": "Leaving a gap between parent button and dropdown list; mouse hover is lost when moving across gap."
            }
        ]
    },
    # Day 17
    {
        "day": "Day 17",
        "title": "Opacity & Attribute Selectors",
        "tab": "CSS NOTES",
        "quote": '"Precision in selection leads to elegance in design"',
        "topics": [
            {
                "heading": "Opacity vs RGBA Transparency",
                "subpoints": [
                    ("→", "<b>opacity:</b> Sets transparency of the ENTIRE element and all its children (0.0 to 1.0).", "(આખું એલિમેન્ટ અને અંદર નું લખાણ ઝાંખું કરવું)"),
                    ("→", "<b>rgba():</b> Sets transparency of background ONLY; text inside stays 100% solid and crisp!", "(ફક્ત બેકગ્રાઉન્ડ પારદર્શક રાખવું)")
                ],
                "code": ("background: rgba(0, 0, 0, 0.6); color: #fff;", ":- Semi-transparent dark card with crisp white text"),
                "remember": "Use rgba() or hex alpha for translucent backgrounds so text readability isn't ruined!",
                "mistake": "Using opacity: 0.5 on a modal dialog box; text inside becomes washed out and hard to read."
            },
            {
                "heading": "CSS Attribute Selectors",
                "subpoints": [
                    ("→", "Targets elements based on presence or value of HTML attributes.", "(એટ્રિબ્યુટ ના આધારે પસંદગી)"),
                    ("→", "<b>[target]:</b> Elements having target attribute."),
                    ("→", "<b>[type=\"submit\"]:</b> Exact attribute match."),
                    ("→", "<b>[href^=\"https\"]:</b> Starts with 'https' (secure links)."),
                    ("→", "<b>[src$=\".pdf\"]:</b> Ends with '.pdf' (PDF downloads).")
                ],
                "code": ("input[type=\"email\"] { border-color: #3b82f6; }", ":- Styles only email input fields"),
                "remember": "Attribute selectors allow styling form inputs without adding extra class names!",
                "mistake": "Typing attribute selectors without brackets (e.g. type=\"text\" instead of [type=\"text\"])."
            }
        ]
    },
    # Day 18
    {
        "day": "Day 18",
        "title": "Form Styling & CSS Counters",
        "tab": "CSS NOTES",
        "quote": '"Small automated touches make code graceful"',
        "topics": [
            {
                "heading": "Professional Form Styling",
                "subpoints": [
                    ("→", "Reset ugly browser defaults: <code>border: 1.5px solid #cbd5e1; border-radius: 6px; padding: 10px 14px;</code>"),
                    ("→", "Smooth focus transition: <code>input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.2); }</code>", "(ઈનપુટ સિલેક્ટ થાય ત્યારે સુંદર ગ્લો)"),
                    ("→", "Style placeholders: <code>::placeholder { color: #94a3b8; font-style: italic; }</code>")
                ],
                "code": ("input:focus { outline: none; border-color: #2563eb; }", ":- Professional focused glow effect"),
                "remember": "Always provide a visual focus state on inputs so users know where their cursor is!",
                "mistake": "Removing browser default outline with outline: none and providing no replacement border focus."
            },
            {
                "heading": "CSS Counters (Automatic Numbering)",
                "subpoints": [
                    ("→", "CSS variables that automatically count items in a page without manual numbering.", "(આપોઆપ ક્રમ આપવો - 1, 2, 3)"),
                    ("→", "<b>counter-reset: name;</b> Initializes counter to 0 (placed on parent container)."),
                    ("→", "<b>counter-increment: name;</b> Increments counter by 1 on each item."),
                    ("→", "<b>content: counter(name);</b> Displays number inside ::before pseudo-element!")
                ],
                "code": ("ol { counter-reset: c; } li::before { counter-increment: c; content: counter(c) '. '; }", ":- Fully customized list numbering"),
                "remember": "CSS counters are ideal for multi-step wizards (Step 1, Step 2, Step 3)!",
                "mistake": "Placing counter-reset on the list items themselves; the counter will reset to 0 every time!"
            }
        ]
    },
    # Day 19
    {
        "day": "Day 19",
        "title": "Units & Specificity",
        "tab": "CSS NOTES",
        "quote": '"Measure twice, style once"',
        "topics": [
            {
                "heading": "CSS Units: Absolute vs Relative",
                "subpoints": [
                    ("→", "<b>px (Pixels):</b> Absolute fixed unit; does not scale with user browser zoom settings.", "(ફિક્સ પિક્સેલ્સ)"),
                    ("→", "<b>rem (Root EM):</b> Relative to root <code>&lt;html&gt;</code> font size (1rem = 16px default). Best for accessible typography!", "(રૂટ ફોન્ટ સાઈઝ ના આધારે - શ્રેષ્ઠ પદ્ધતિ)"),
                    ("→", "<b>em:</b> Relative to parent element font size (can compound unintentionally)."),
                    ("→", "<b>vw / vh:</b> 1% of Viewport Width / Viewport Height (100vh = full screen height).", "(સ્ક્રીન ની ટકાવારી)")
                ],
                "code": ("h1 { font-size: 2rem; } /* 32px */ body { min-height: 100vh; }", ":- Scalable heading & full-height page"),
                "remember": "Use rem for fonts and spacing; use % or vh/vw for responsive layouts!",
                "mistake": "Nesting em units deeply; font size multiplies and becomes unexpectedly huge or tiny."
            },
            {
                "heading": "CSS Specificity Hierarchy",
                "subpoints": [
                    ("→", "Determines which rule wins when multiple CSS rules target the same element.", "(કયો નિયમ જીતશે - priority order)"),
                    ("→", "<b>1. !important:</b> Overrides everything (use sparingly!)."),
                    ("→", "<b>2. Inline styles:</b> <code>style=\"...\"</code> (Weight: 1000)"),
                    ("→", "<b>3. ID selector:</b> <code>#header</code> (Weight: 100)"),
                    ("→", "<b>4. Classes / Attributes:</b> <code>.btn, [type]</code> (Weight: 10)"),
                    ("→", "<b>5. Elements:</b> <code>p, div</code> (Weight: 1)")
                ],
                "diagram": "!important > Inline (1000) > #id (100) > .class (10) > tag (1)",
                "remember": "Higher specificity wins; if specificity is equal, the rule written LATER in the file wins!",
                "mistake": "Overusing !important to patch bugs; it destroys maintainability and cascades into CSS wars."
            }
        ]
    },
    # Day 20
    {
        "day": "Day 20",
        "title": "Performance & Gradients",
        "tab": "CSS NOTES",
        "quote": '"Speed is a feature, and beauty is an asset"',
        "topics": [
            {
                "heading": "CSS Performance Optimization",
                "subpoints": [
                    ("→", "<b>Minimize Reflows & Repaints:</b> Animating <code>transform</code> and <code>opacity</code> uses GPU and is 60fps fast.", "(ઝડપી સ્પીડ - GPU એનિમેશન)"),
                    ("→", "Avoid animating layout properties: <code>top, left, width, height, margin</code> cause slow CPU recalculations."),
                    ("→", "Keep selectors shallow (avoid <code>div body #main ul li a span</code>)."),
                    ("→", "Minify CSS files in production to eliminate whitespace and comments.")
                ],
                "code": ("/* Fast */ transform: translateX(100px); /* Slow */ left: 100px;", ":- Hardware accelerated smooth movement"),
                "remember": "Always animate transform and opacity for buttery-smooth 60fps animations!",
                "mistake": "Animating margin-left or top; mobile phones will stutter and lag."
            },
            {
                "heading": "CSS Gradients (Linear & Radial)",
                "subpoints": [
                    ("→", "Smooth transitions between two or more colors without downloading heavy images.", "(રંગો નું મિશ્રણ - ઢાળવાળા રંગો)"),
                    ("→", "<b>linear-gradient(direction, color1, color2):</b> <code>to right, #4facfe, #00f2fe;</code>"),
                    ("→", "<b>radial-gradient(circle, color1, color2):</b> Radiates outward from center.")
                ],
                "code": ("background: linear-gradient(135deg, #667eea, #764ba2);", ":- Elegant modern purple gradient"),
                "remember": "Gradients are treated as background-image, not background-color!",
                "mistake": "Writing background-color: linear-gradient(...); (it will be ignored; use background:)."
            }
        ]
    },
    # Day 21
    {
        "day": "Day 21",
        "title": "Shadows & Text Effects",
        "tab": "CSS NOTES",
        "quote": '"Light and shadow give shape and dimension to flat screens"',
        "topics": [
            {
                "heading": "box-shadow & text-shadow",
                "subpoints": [
                    ("→", "<b>box-shadow:</b> Adds elevation and 3D depth to cards and buttons.", "(કાર્ડ નો પડછાયો - 3D elevation)"),
                    ("→", "Syntax: <code>box-shadow: X Y Blur Spread Color;</code>"),
                    ("→", "<b>text-shadow:</b> Adds shadow behind letters for contrast on photo backgrounds.")
                ],
                "code": ("box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);", ":- Soft modern card drop-shadow"),
                "remember": "Use multiple subtle shadows with soft blur for realistic, premium lighting!",
                "mistake": "Using harsh black shadows (like box-shadow: 5px 5px 0 #000); looks 90s and dated."
            },
            {
                "heading": "Text Truncation & Ellipsis (...)",
                "subpoints": [
                    ("→", "When text is too long for a single line, cut it cleanly with three dots (...).", "(લાંબુ લખાણ કાપીને ... બતાવવું)"),
                    ("→", "<b>Must combine 3 properties:</b>"),
                    ("→", "1. <code>white-space: nowrap;</code> (prevents wrapping)"),
                    ("→", "2. <code>overflow: hidden;</code> (clips overflow)"),
                    ("→", "3. <code>text-overflow: ellipsis;</code> (appends ...)")
                ],
                "code": ("white-space: nowrap; overflow: hidden; text-overflow: ellipsis;", ":- Shows: 'Very long product title...'"),
                "remember": "All 3 properties are required together; if you miss one, ellipsis will NOT appear!",
                "mistake": "Expecting text-overflow: ellipsis to work without overflow: hidden."
            }
        ]
    },
    # Day 22
    {
        "day": "Day 22",
        "title": "2D & 3D Transforms",
        "tab": "CSS NOTES",
        "quote": '"Transformations turn static graphics into lively experiences"',
        "topics": [
            {
                "heading": "2D Transforms: translate, rotate, scale",
                "subpoints": [
                    ("→", "Modifies element shape, size, and position without disrupting document flow.", "(આકાર અને સ્થિતિ બદલવી)"),
                    ("→", "<b>translate(X, Y):</b> Moves element (e.g. <code>translateY(-5px)</code> lifts up)."),
                    ("→", "<b>rotate(deg):</b> Spins element (e.g. <code>rotate(45deg)</code>)."),
                    ("→", "<b>scale(N):</b> Enlarges or shrinks (e.g. <code>scale(1.05)</code> zooms 5%).")
                ],
                "code": ("button:hover { transform: scale(1.05); }", ":- Micro-zoom button effect on hover"),
                "remember": "Combine multiple transforms in one rule: transform: translate(-50%, -50%) rotate(45deg);",
                "mistake": "Writing two separate transform lines; the second line completely overrides the first!"
            },
            {
                "heading": "3D Transforms & Perspective",
                "subpoints": [
                    ("→", "Simulates real-world 3D depth along the Z-axis.", "(3D પરિમાણ - ઊંડાણ)"),
                    ("→", "<b>perspective: 1000px;</b> Defines how far the viewer is from the 3D plane (placed on parent)."),
                    ("→", "<b>rotateX(), rotateY():</b> Flips card along horizontal and vertical axes."),
                    ("→", "<b>transform-style: preserve-3d;</b> Keeps children in 3D space (for 3D card flips).")
                ],
                "code": (".card:hover { transform: rotateY(180deg); }", ":- 3D card flip showing backside"),
                "remember": "Always add perspective to parent container to enable realistic 3D foreshortening!",
                "mistake": "Forgetting perspective; rotateY will look like a flat shrinking box rather than 3D rotation."
            }
        ]
    },
    # Day 23
    {
        "day": "Day 23",
        "title": "Transitions & Animations",
        "tab": "CSS NOTES",
        "quote": '"Animation is not the art of drawings that move, but the art of movements that are drawn"',
        "topics": [
            {
                "heading": "CSS Transitions (Smooth State Changes)",
                "subpoints": [
                    ("→", "Smoothly animates property changes over time (like on :hover).", "(સરળ ફેરફાર - smooth change)"),
                    ("→", "<b>Shorthand:</b> <code>transition: property duration timing-function delay;</code>"),
                    ("→", "<b>ease-in-out:</b> Starts slow, speeds up in middle, ends slow for natural feel.")
                ],
                "code": ("transition: all 0.3s ease-in-out;", ":- Smooth 0.3 second hover animation"),
                "remember": "Put transition on the BASE class (e.g. .btn), not on :hover, so it animates both ways!",
                "mistake": "Putting transition on :hover only; the hover-in is smooth, but hover-out snaps abruptly."
            },
            {
                "heading": "Keyframe Animations (@keyframes)",
                "subpoints": [
                    ("→", "Creates continuous, multi-step animations without requiring user interaction.", "(આપોઆપ ચાલતી એનિમેશન)"),
                    ("→", "<b>@keyframes name:</b> Defines checkpoints (0%, 50%, 100%)."),
                    ("→", "<b>animation:</b> <code>name duration timing iteration-count;</code>")
                ],
                "code": ("@keyframes spin { 100% { transform: rotate(360deg); } }<br>.loader { animation: spin 1s linear infinite; }", ":- Infinite spinning loading spinner"),
                "remember": "Use iteration-count: infinite for continuous animations like loading spinners!",
                "mistake": "Forgetting to bind animation-name to the element class after defining @keyframes."
            }
        ]
    },
    # Day 24
    {
        "day": "Day 24",
        "title": "Tooltips & Image Styling",
        "tab": "CSS NOTES",
        "quote": '"Helpful hints make complex interfaces intuitive"',
        "topics": [
            {
                "heading": "Pure CSS Tooltips",
                "subpoints": [
                    ("→", "Small popup bubble explaining an icon or button when hovered.", "(માઉસ લઈ જતાં નાની મદદગાર માહિતી બતાવવી)"),
                    ("→", "Built with <code>data-tooltip</code> attribute and <code>::after</code> pseudo-element."),
                    ("→", "Positioned with <code>position: absolute; bottom: 125%; left: 50%; transform: translateX(-50%);</code>")
                ],
                "code": (".tip:hover::after { content: attr(data-tooltip); opacity: 1; }", ":- Fades in tooltip text on hover"),
                "remember": "Use attr(data-tooltip) in CSS content so HTML controls the tooltip text dynamically!",
                "mistake": "Setting z-index too low on tooltip; it ends up hidden behind neighboring cards."
            },
            {
                "heading": "Image Styling: object-fit",
                "subpoints": [
                    ("→", "Controls how an image or video fits inside a container with fixed width/height.", "(ફોટો ખેંચાયા વગર બોક્સમાં ફીટ કરવો)"),
                    ("→", "<b>fill:</b> Default; stretches and distorts image aspect ratio."),
                    ("→", "<b>cover:</b> Crops edges to fill the container without distorting proportions! (Best for avatars & cards)", "(પ્રમાણસર કવર કરવું)"),
                    ("→", "<b>contain:</b> Letterboxes image so the whole photo is visible without cropping.")
                ],
                "code": ("img { width: 100%; height: 250px; object-fit: cover; }", ":- Perfectly cropped card image without distortion"),
                "remember": "Always pair fixed height with object-fit: cover on image cards!",
                "mistake": "Squishing images by forcing width & height without object-fit; people look fat or skinny."
            }
        ]
    },
    # Day 25
    {
        "day": "Day 25",
        "title": "Filters, Clip-path & Multi-columns",
        "tab": "CSS NOTES",
        "quote": '"Artistic filters and geometric shapes elevate standard layouts into editorial art"',
        "topics": [
            {
                "heading": "CSS Image Filters & clip-path",
                "subpoints": [
                    ("→", "<b>filter:</b> Visual effects: <code>blur(5px), grayscale(100%), brightness(1.2), drop-shadow()</code>.", "(ઈમેજ ઈફેક્ટ્સ - બ્લેક એન્ડ વ્હાઈટ, બ્લર)"),
                    ("→", "<b>clip-path:</b> Cuts elements into geometric custom shapes (polygons, circles, triangles).", "(ખાસ આકારમાં કાપવું - polygon/circle)"),
                    ("→", "Example: Slanted hero sections via <code>clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);</code>")
                ],
                "code": ("img:hover { filter: grayscale(0%); } img { filter: grayscale(100%); }", ":- Black & white photo turns vibrant on hover"),
                "remember": "drop-shadow() filter conforms to transparent PNG edges, unlike standard box-shadow!",
                "mistake": "Using box-shadow on a transparent PNG; it casts a shadow around the rectangular box, not the icon."
            },
            {
                "heading": "CSS Multi-column Layout",
                "subpoints": [
                    ("→", "Splits text into newspaper-style multi-column layout.", "(અખબાર જેવા સ્તંભો - newspaper columns)"),
                    ("→", "<b>column-count: 3;</b> Divides text into 3 equal columns."),
                    ("→", "<b>column-gap: 30px;</b> Space between adjacent columns."),
                    ("→", "<b>column-rule: 1px solid #ccc;</b> Draws vertical dividing line between columns.")
                ],
                "code": (".article { column-count: 2; column-gap: 24px; }", ":- 2-column newspaper layout for article text"),
                "remember": "Use column-width instead of column-count for responsive auto-adjusting column counts!",
                "mistake": "Using hardcoded column-count: 3 on mobile screens; text columns become unreadably narrow."
            }
        ]
    },
    # Day 26
    {
        "day": "Day 26",
        "title": "CSS Variables (Custom Properties)",
        "tab": "CSS NOTES",
        "quote": '"Don\'t repeat yourself. Centralize your design tokens"',
        "topics": [
            {
                "heading": "Declaring & Using CSS Variables",
                "subpoints": [
                    ("→", "Allows defining reusable design values (colors, spacing, font sizes) in one place.", "(વેરીએબલ - એક જગ્યાએ ફેરફાર કરવાથી આખી સાઈટ બદલાય)"),
                    ("→", "Declared with two dashes (<code>--name</code>) inside <code>:root</code> for global scope."),
                    ("→", "Accessed using <code>var(--name, fallback)</code>.")
                ],
                "code": (":root { --primary: #3b82f6; }<br>button { background: var(--primary); }", ":- Uses centralized primary blue variable"),
                "remember": "Variables cascade! You can override --primary inside a specific card for thematic coloring.",
                "mistake": "Forgetting the two dashes '--' prefix when defining CSS custom properties."
            },
            {
                "heading": "Dark Mode with CSS Variables",
                "subpoints": [
                    ("→", "Variables make instant Dark Mode implementation effortless.", "(ડાર્ક મોડ - રાત્રિ મોડ)"),
                    ("→", "Define base theme on <code>:root</code>, then redefine color variables inside <code>[data-theme='dark']</code> or <code>@media (prefers-color-scheme: dark)</code>.")
                ],
                "diagram": ":root {<br>&nbsp;&nbsp;--bg: #ffffff; --text: #1e293b;<br>}<br>[data-theme='dark'] {<br>&nbsp;&nbsp;--bg: #0f172a; --text: #f8fafc;<br>}",
                "remember": "All elements using var(--bg) and var(--text) will swap themes instantaneously!",
                "mistake": "Hardcoding hex codes on child elements; they will refuse to change in dark mode."
            }
        ]
    },
    # Day 27
    {
        "day": "Day 27",
        "title": "Flexbox Layout",
        "tab": "CSS NOTES",
        "quote": '"Flexibility is the greatest strength in a world of varying screen sizes"',
        "topics": [
            {
                "heading": "Flex Container: Direction & Spacing",
                "subpoints": [
                    ("→", "<b>display: flex;</b> Activates 1-dimensional layout along main and cross axes.", "(એક પરિમાણીય લવચીક ગોઠવણી)"),
                    ("→", "<b>flex-direction:</b> row (horizontal default) or column (vertical stack).", "(આડી કે ઊભી દિશા)"),
                    ("→", "<b>justify-content:</b> Aligns items along main axis (flex-start, center, flex-end, space-between, space-around)."),
                    ("→", "<b>align-items:</b> Aligns items along cross axis (stretch, center, flex-start)."),
                    ("→", "<b>gap:</b> Simple space between items (e.g. <code>gap: 16px;</code>).")
                ],
                "code": ("display: flex; justify-content: space-between; align-items: center;", ":- Items pushed to opposite ends and centered vertically"),
                "remember": "justify-content aligns along main axis; align-items aligns along perpendicular cross axis!",
                "mistake": "Using space-between and then adding margins on items; spacing becomes uneven."
            },
            {
                "heading": "Flex Items: grow, shrink, wrap",
                "subpoints": [
                    ("→", "<b>flex-wrap: wrap;</b> Allows items to wrap onto the next line if space runs out.", "(જગ્યા ન હોય તો બીજી લાઈનમાં જવું)"),
                    ("→", "<b>flex-grow: 1;</b> Tells item to expand and take up all remaining available space."),
                    ("→", "<b>flex-shrink: 0;</b> Prevents item from being squished when space is tight.")
                ],
                "code": (".input { flex: 1; } .btn { flex-shrink: 0; }", ":- Search input stretches; search button stays fixed size"),
                "remember": "flex: 1 is shorthand for flex-grow: 1, flex-shrink: 1, flex-basis: 0%!",
                "mistake": "Items overflowing off screen because flex-wrap: wrap was omitted on responsive rows."
            }
        ]
    },
    # Day 28
    {
        "day": "Day 28",
        "title": "Media Queries & CSS Grid",
        "tab": "CSS NOTES",
        "quote": '"Responsive design is not about designing for devices, but designing for people"',
        "topics": [
            {
                "heading": "Media Queries for Responsive Design",
                "subpoints": [
                    ("→", "Applies CSS rules conditionally based on screen width, height, or orientation.", "(મોબાઈલ અને ડેસ્કટોપ માટે અલગ નિયમ)"),
                    ("→", "<b>Mobile First approach:</b> Write default styles for mobile, then add <code>@media (min-width: 768px)</code> for tablets and <code>(min-width: 1024px)</code> for desktop laptops.")
                ],
                "code": ("@media (max-width: 768px) {<br>&nbsp;&nbsp;.nav { flex-direction: column; }<br>}", ":- Stacks navbar vertically on mobile phones"),
                "remember": "Always include &lt;meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"&gt; in HTML!",
                "mistake": "Using fixed pixel widths inside media query blocks; use percentages or fr units."
            },
            {
                "heading": "CSS Grid (2D Grid Layout)",
                "subpoints": [
                    ("→", "<b>display: grid;</b> Powerful 2-dimensional system handling rows AND columns simultaneously.", "(દ્વિ-પરિમાણીય ગ્રીડ - રો અને કોલમ બંને)"),
                    ("→", "<b>grid-template-columns:</b> <code>repeat(3, 1fr);</code> (3 equal flexible fractional columns)."),
                    ("→", "<b>grid-column: 1 / 3;</b> Item spans across 2 columns.", "(બે કોલમ રોકી લેવી)"),
                    ("→", "<b>Auto-responsive magic:</b> <code>grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));</code> (no media queries needed!)")
                ],
                "code": ("display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;", ":- Responsive auto-wrapping grid cards"),
                "remember": "Use Flexbox for 1D navigation bars and rows; use CSS Grid for 2D page layouts and card galleries!",
                "mistake": "Trying to build complex 2D dashboard grids using nested flexboxes; CSS Grid does it with 3 lines."
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

with open('css_notes.html', 'w', encoding='utf-8') as f:
    f.write(generate_pages_html(css_pages_data, "CSS"))

print("Generated css_notes.html successfully with", len(css_pages_data), "pages!")
