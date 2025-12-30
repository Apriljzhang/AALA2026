from jinja2 import Environment
import os

# --- Step 1: Define Your Content Data ---
# Note: I changed image paths to relative ones (e.g., 'logo.png')
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
                'content': """The Asian Association for Language Assessment (AALA) 2026 Conference will be held from September 18-20, 2026, at the City University of Macau. This year's theme is the <b>'Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability'.</b> We invite you to contribute to this important conversation. You can find more information on our <a href='call-for-papers.html'>Call for Papers</a> page.
                <p><h3> Why Attend? </h3>
                <ul>
                    <li> Learn from leading scholars in plenary sessions and workshops </li>
                    <li> Exchange ideas with peers from across Asia and the world </li>
                    <li> Explore Macau, a UNESCO World Heritage city with rich cultural heritage and world-class facilities </li>
                </ul></p>"""
            },
            {
                'id': 'about-aala',
                'heading': 'Asian Association for Language Assessment',
                'content': """
                <div style="margin-bottom: 20px;">
                    <img src="images/aala-logo.png" alt="AALA Logo" style="height: 80px; width: auto;">
                </div>
                <p>The Asian Association for Language Assessment (AALA) is a professional organization dedicated to promoting best practices in language assessment throughout Asia and beyond. Learn more about our mission and history on the <a href='https://www.aalawebsite.com/' target='_blank'>official AALA website</a>.</p>"""
            },
            {
                'id': 'about-macau',
                'heading': 'Macao Overview',
                'content': "Macao offers a unique cultural blend and is a UNESCO World Heritage Site. It has a compact city layout with easy transport connectivity. <br><br><b><a href='https://www.macaotourism.gov.mo/en/dining' target='_blank'>Dining:</a></b> Diverse options from local eateries to Michelin stars.<br><br><b><a href='https://www.macaotourism.gov.mo/en/shows-and-entertainment/nightlife' target='_blank'>Nightlife:</a></b> Vibrant mix of casinos, rooftop bars, and pubs."
            },
            {
                'id': 'sponsors',
                'heading': 'Sponsors',
                'content': 'Sponsor logos will be displayed here. (to be confirmed)'
            }
        ]
    },
    'call-for-papers': {
        'page_title': 'Call For Papers - AALA 2026',
        'sections': [
            {
                'id': 'call',
                'heading': 'Call for Papers',
                'content': """<p>Asian Association for Language Assessment (AALA) 2026 Conference</p><p>📍 <b>City University of Macau</b> | 18–20 September 2026</p>"""
            }
        ]
    },
    'registration': {
        'page_title': 'Registration & Payment- AALA 2026',
        'sections': [{'id': 'reg', 'heading': 'Registration', 'content': 'Opening soon.'}]
    },
    'program': {
        'page_title': 'Program & Schedule - AALA 2026',
        'sections': [{'id': 'prog', 'heading': 'Program', 'content': 'To be announced.'}]
    },
    'venue': {
        'page_title': 'Venue & Transport - AALA 2026',
        'sections': [{'id': 'ven', 'heading': 'Venue', 'content': 'City University of Macau.'}]
    }
}

# --- Step 2: Define Your HTML Template ---
html_template = """
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
    <div class="logo-container">
        <img src="images/aala2026-logo.png" alt="AALA 2026 Logo" class="aala-logo">
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
        {% for section in sections %}
        <section id="{{ section.id }}" class="content-section">
            <h2>{{ section.heading }}</h2>
            <div class="section-text">
                {{ section.content | safe }}
            </div>
        </section>
        {% endfor %}
    </main>

    <footer class="footer">
        <p>&copy; 2026 AALA. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# --- Step 3: Run the generation process ---
def build():
    try:
        env = Environment()
        # Create an 'images' folder if it doesn't exist to encourage good structure
        if not os.path.exists('images'):
            os.makedirs('images')
            print("📁 Created 'images' folder. Please move your logos there!")

        for page_name, data in site_data.items():
            template = env.from_string(html_template)
            rendered_html = template.render(data)

            file_name = 'index.html' if page_name == 'home' else f'{page_name}.html'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(rendered_html)

        print("✨ Website updated! Open index.html to see the changes.")
        print("💡 Remember: Place your images in the 'images' folder and name them 'aala-logo.png' and 'aala2026-logo.png'.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    build()
