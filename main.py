from jinja2 import Environment, FileSystemLoader
import os

# --- Step 1: Define Your Content Data ---
site_data = {
    'home': {
        'page_title': 'AALA 2026 Macao Conference',
        'header_title': 'Asian Association for Language Assessment (AALA) 2026',
        'theme': 'Humanistic approach to Assessment, Standards, Innovation, and Accountability',
        'date': 'September 18-20, 2026',
        'location': 'City University of Macau',
        'contact_email': 'aala2026@outlook.com',
        'sections': [
            {
                'id': 'aala2026-intro',
                'heading': 'AALA 2026',
                'content': """The Asian Association for Language Assessment (AALA) 2026 Conference will be held from September 18-20, 2026, at the City University of Macau. This year's theme is the <b>'Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability'.</b> We invite you to contribute to this important conversation.
                <p><h3> Why Attend? </h3>
                <ul>
                    <li> Learn from leading scholars in plenary sessions and workshops </li>
                    <li> Exchange ideas with peers from across Asia and the world </li>
                    <li> Explore Macau, a UNESCO World Heritage city </li>
                </ul></p>"""
            },
            {
                'id': 'about-aala',
                'heading': 'Asian Association for Language Assessment',
                'content': "The Asian Association for Language Assessment (AALA) is dedicated to promoting best practices in language assessment throughout Asia. Learn more on the <a href='https://www.aalawebsite.com/' target='_blank'>official AALA website</a>."
            }
        ]
    },
    'call-for-papers': {
        'page_title': 'Call For Papers - AALA 2026',
        'sections': [
            {
                'id': 'call',
                'heading': 'Call for Papers',
                'content': """<p>📍 <b>City University of Macau</b> | 18–20 September 2026</p>
                <h3>Subthemes</h3>
                <ul>
                    <li>Humanistic and ethical practices in assessment</li>
                    <li>Innovations (AI, GenAI, multimodal)</li>
                    <li>Accountability and stakeholder perspectives</li>
                </ul>"""
            }
        ]
    },
    'registration': {
        'page_title': 'Registration - AALA 2026',
        'sections': [{'id': 'reg', 'heading': 'Registration', 'content': 'Opening soon.'}]
    },
    'program': {
        'page_title': 'Program - AALA 2026',
        'sections': [{'id': 'prog', 'heading': 'Program', 'content': 'To be announced.'}]
    },
    'venue': {
        'page_title': 'Venue - AALA 2026',
        'sections': [{'id': 'ven', 'heading': 'Venue', 'content': 'City University of Macau.'}]
    }
}

# --- Step 2: Define Your HTML Template ---
# FIX: Moved the <header> into the <body> where it belongs!
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="navbar">
        <div class="logo-container">
            <img src="AALA logo.png" alt="AALA 2026 Logo" class="aala-logo">
        </div>
        <nav class="nav-links">
            <a href="index.html">Home</a>
            <a href="call-for-papers.html">Call For Papers</a>
            <a href="registration.html">Registration</a>
            <a href="program.html">Program</a>
            <a href="venue.html">Venue/Transport</a>
        </nav>
    </header>

    <main>
        {% if 'home' in page_title.lower() %}
        <section class="hero-section">
            <div class="hero-content">
                <h1 class="heading-large">{{ header_title }}</h1>
                <p class="theme">{{ theme }}</p>
                <div class="info-container">
                    <p class="date">{{ date }}</p>
                    <p class="location">{{ location }}</p>
                </div>
                <a href="registration.html" class="cta-button">Register Now</a>
            </div>
        </section>
        {% endif %}

        <div class="container">
            {% for section in sections %}
            <section id="{{ section.id }}" class="content-section">
                <h2>{{ section.heading }}</h2>
                <div class="section-text">
                    {{ section.content | safe }}
                </div>
            </section>
            {% endfor %}
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 AALA. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# --- Step 3: Define Your CSS ---
css_content = """
:root {
    --color-green: #008264;
    --color-red: #FA0202;
    --color-dark-blue: #020266;
    --color-white: #ffffff;
    --color-grey: #f4f4f4;
}

body {
    font-family: 'Montserrat', sans-serif;
    margin: 0;
    color: var(--color-dark-blue);
    background-color: var(--color-white);
}

.navbar {
    background: white;
    padding: 10px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.aala-logo { height: 60px; }

.nav-links a {
    text-decoration: none;
    color: var(--color-dark-blue);
    margin-left: 20px;
    font-weight: 600;
}

.hero-section {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('Copilot_20250618_125349.jpg');
    background-size: cover;
    background-position: center;
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-align: center;
}

.heading-large { font-size: 2.5rem; margin-bottom: 10px; }
.theme { color: #f2d72e; font-size: 1.2rem; }

.container { max-width: 900px; margin: auto; padding: 40px 20px; }

.content-section { margin-bottom: 50px; }
.content-section h2 { border-bottom: 3px solid var(--color-green); display: inline-block; }

.highlight-red { color: var(--color-red); font-weight: bold; }

.footer {
    background: var(--color-green);
    color: white;
    text-align: center;
    padding: 20px;
    margin-top: 50px;
}

.cta-button {
    background: var(--color-red);
    color: white;
    padding: 12px 25px;
    border-radius: 5px;
    text-decoration: none;
    display: inline-block;
    margin-top: 20px;
}
"""

# --- Step 4: Generation Logic ---
try:
    env = Environment()
    for page_name, data in site_data.items():
        template = env.from_string(html_template)
        rendered_html = template.render(data)
        
        file_name = 'index.html' if page_name == 'home' else f'{page_name}.html'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"✅ Generated {file_name}")

    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✅ Generated style.css")

except Exception as e:
    print(f"❌ Error: {e}")
