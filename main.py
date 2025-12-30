import os
from jinja2 import Template

# --- STEP 1: YOUR DATA ---
site_data = {
    'home': {
        'filename': 'index.html',
        'page_title': 'AALA 2026 Macao Conference',
        'show_hero': True, # Keep this True if you want the banner image
        'sections': [
            {
                'heading': 'AALA 2026',
                'content': """
                <p style="text-align: center; font-weight: bold; margin-bottom: 20px;">
                    September 18-20, 2026 | City University of Macau
                </p>

                <p>The Asian Association for Language Assessment (AALA) 2026 Conference will be held from September 18-20, 2026, at the City University of Macau. This year's theme is the <b>'Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability'.</b> We invite you to contribute to this important conversation.</p>
                
                <h3>Why Attend?</h3>
                <ul>
                    <li>Learn from leading scholars in plenary sessions and workshops</li>
                    <li>Exchange ideas with peers from across Asia and the world</li>
                    <li>Explore Macau, a UNESCO World Heritage city</li>
                </ul>"""
            },
        ]
    },
}
    'call-for-papers': {'page_title': 'Call For Papers - AALA 2026', 'sections': []},
    'registration': {'page_title': 'Registration - AALA 2026', 'sections': []},
    'program': {'page_title': 'Program - AALA 2026', 'sections': []},
    'venue': {'page_title': 'Venue - AALA 2026', 'sections': []}
}

# --- STEP 2: THE TEMPLATE ---
html_layout = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="navbar">
        <div class="logo-area">
            <img src="aala2026-logo.png" alt="AALA 2026 Logo" style="height: 60px;">
        </div>
        <nav class="nav-links">
            <a href="index.html">Home</a>
            <a href="call-for-papers.html">Call For Papers</a>
            <a href="registration.html">Registration</a>
            <a href="program.html">Program</a>
            <a href="venue.html">Venue</a>
        </nav>
    </header>

    <main>
        {% if header_title %}
        <section class="hero">
            <div class="hero-overlay">
                <h1>{{ header_title }}</h1>
                <p class="hero-theme">{{ theme }}</p>
                <p class="hero-info"><strong>{{ date }}</strong> | {{ location }}</p>
            </div>
        </section>
        {% endif %}

        <div class="container">
            {% for section in sections %}
            <section id="{{ section.id }}" class="content-block">
                <h2>{{ section.heading }}</h2>
                <div class="text-body">{{ section.content | safe }}</div>
            </section>
            {% endfor %}
        </div>
    </main>

    <footer class="footer">
        <p>&copy; 2026 AALA Conference. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# --- STEP 3: THE STYLE (CSS) ---
css_code = """
body { font-family: 'Montserrat', sans-serif; margin: 0; line-height: 1.6; color: #333; }

.navbar { 
    display: flex; 
    justify-content: space-between; 
    padding: 10px 5%; 
    background: white; 
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
    position: sticky; 
    top: 0; 
    z-index: 1000;
}

.nav-links { display: flex; align-items: center; }
.nav-links a { margin-left: 20px; text-decoration: none; color: #008264; font-weight: bold; }

.container { max-width: 900px; margin: 40px auto; padding: 0 20px; }

/* HERO SECTION WITH BANNER */
.hero { 
    position: relative;
    background: url('aala2026-banner.png') no-repeat center center/cover; 
    height: 450px; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    color: white; 
    text-align: center;
}

.hero-overlay {
    background: rgba(0, 0, 0, 0.5); /* Makes text readable over the banner */
    padding: 40px;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero h1 { font-size: 2.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
.hero-theme { color: #f2d72e; font-size: 1.3rem; margin: 15px 0; font-weight: bold; }
.hero-info { font-size: 1.1rem; }

.content-block { margin-bottom: 40px; padding-bottom: 20px; }
.content-block h2 { color: #008264; border-bottom: 3px solid #008264; display: inline-block; }

.footer { text-align: center; padding: 30px; background: #008264; color: white; margin-top: 50px; }
"""

# --- STEP 4: THE GENERATOR ---
def build_site():
    try:
        # Save CSS
        with open('style.css', 'w', encoding='utf-8') as f:
            f.write(css_code)
        
        # Save HTML Pages
        template = Template(html_layout)
        for page_id, content in site_data.items():
            filename = 'index.html' if page_id == 'home' else f"{page_id}.html"
            rendered_page = template.render(content)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(rendered_page)
        
        print("✨ Site built successfully with new image names!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    build_site()
