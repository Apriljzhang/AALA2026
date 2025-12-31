import os
from jinja2 import Template

# --- STEP 1: YOUR DATA ---
site_data = {
    'home': {
        'page_title': 'AALA 2026 Macao Conference',
        'header_title': 'AALA 2026 Macao Conference',
        'theme': 'Humanistic approach to Assessment, Standards, Innovation, and Accountability',
        'date': 'September 18-20, 2026',
        'location': 'City University of Macau',
        'sections': [
            {
                'id': 'intro',
                'heading': 'Welcome to AALA 2026',
                'content': """
                <p style="text-align: center; font-weight: bold; margin-bottom: 20px;">
                    September 18-20, 2026 | City University of Macau
                </p>
                <p>The Asian Association for Language Assessment (AALA) 2026 Conference will be held from September 18-20, 2026, at the City University of Macau. This year's theme is the <b>'Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability'.</b></p>
                <h3>Why Attend?</h3>
                <ul>
                    <li>Learn from leading scholars in plenary sessions and workshops</li>
                    <li>Exchange ideas with peers from across Asia and the world</li>
                    <li>Explore Macau, a UNESCO World Heritage city</li>
                </ul>"""
            }
        ]
    },
    'call-for-papers': {
        'page_title': 'Call For Papers - AALA 2026',
        'sections': [
            {
                'id': 'formats',
                'heading': 'Presentation Formats',
                'content': """
                <div class="parallel-container">
                    <div class="category-card">
                        <h3>Paper Presentations</h3>
                        <p>20 minutes + 5 minutes Q&A.</p>
                        <ul class="tight-list">
                            <li><strong>Empirical:</strong> Rationale, theory, methods, findings.</li>
                            <li><strong>Conceptual:</strong> Frameworks, policies, or emerging issues.</li>
                            <li><strong>Title:</strong> Max 20 words. <strong>Abstract:</strong> Max 300 words.</li>
                            <li><em>Accepted papers may be oral or poster format.</em></li>
                        </ul>
                    </div>
                    <div class="category-card">
                        <h3>Poster Presentations</h3>
                        <p>Platform for sharing work-in-progress during scheduled sessions.</p>
                        <ul class="tight-list">
                            <li><strong>Abstract:</strong> Same requirements as paper presentations.</li>
                            <li><strong>Poster size:</strong> A1 (841 x 594 mm).</li>
                        </ul>
                    </div>
                    <div class="category-card">
                        <h3>Symposia</h3>
                        <p>90 minutes for 3-4 papers on a single theme.</p>
                        <ul class="tight-list">
                            <li><strong>Proposal:</strong> Max 800 words, including:
                                <ul class="tight-list" style="list-style-type: circle;">
                                    <li>Overview of theme and goals</li>
                                    <li>Titles and 150-word paper abstracts</li>
                                    <li>Moderator/discussant roles</li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>"""
            }
        ]
    },
    'registration': {'page_title': 'Registration - AALA 2026', 'sections': [{'id':'reg','heading':'Registration','content':'<p>Coming Soon.</p>'}]},
    'program': {'page_title': 'Program - AALA 2026', 'sections': [{'id':'prog','heading':'Program','content':'<p>Coming Soon.</p>'}]},
    'venue': {
        'page_title': 'Venue & Transport - AALA 2026',
        'sections': [
            {
                'id': 'overview',
                'heading': 'Venue Overview',
                'content': """
                <p>The City University of Macau (CityU Macau), formerly known as the University of East Asia founded in 1981 and renamed in 2011, follows a strategic development outline of “Rename, Restructure, Transform, Upgrade” as it advances disciplines in digital humanities, arts, business, finance, emerging engineering, and social sciences to become a fully-fledged metropolitan university. As a leading education provider, the University shoulders the social responsibility of “Serving Macao, Integrating into Greater Bay Area” by nurturing high-caliber professionals aligned with its motto of “Virtue, Knowledge, Practice,” while sparing no effort to provide the intellectual and academic support necessary to promote local and regional development within the integrated Guangdong-Hong Kong-Macao Greater Bay Area.</p>
                
                <div class="video-grid">
                    <div class="media-box">
                        <p><b>YouTube Introduction</b></p>
                        <iframe width="100%" height="250" src="https://www.youtube.com/embed/yFXsRTb1Sbo" frameborder="0" allowfullscreen style="border-radius:8px;"></iframe>
                    </div>
                    <div class="media-box">
                        <p><b>Bilibili (了解城市大學)</b></p>
                        <iframe width="100%" height="250" src="https://player.bilibili.com/player.html?bvid=BV154qEBMERU&page=1&danmaku=0&autoplay=0" frameborder="0" allowfullscreen style="border-radius:8px;"></iframe>
                    </div>
                </div>

                <div style="max-width: 800px; margin: 40px auto; text-align: center;">
                    <h3>Campus Map</h3>
                    <img src="campus-map.jpg" alt="Campus Map" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                </div>"""
            },
            {
                'id': 'transport-international',
                'heading': 'Transportation to Macau',
                'content': """
                <h3>By Air ✈️</h3>
                <p><b>Macau International Airport (MFM):</b> Direct flights from many Asian cities. 
                <br><b>Hong Kong International Airport (HKG):</b> From HKG, use the "SkyPier Terminal" bus/ferry to Macau without clearing HK immigration.</p>

                <h3>By Sea 🛥️</h3>
                <p>Connected by high-speed ferries from Hong Kong and Shenzhen:</p>
                <ul>
                    <li><b>Outer Harbour Ferry Terminal:</b> 24/7 service.</li>
                    <li><b>Taipa Ferry Terminal:</b> 24/7 service. <i>(Closest to CityU Macau)</i></li>
                </ul>

                <h3>By Land 🚗</h3>
                <p><b>HZMB "Golden Bus":</b> Connects HK and Macau Port (40 mins).
                <br><b>Border Checkpoints:</b> Border Gate (06:00-01:00), Hengqin Port (24h), and Qingmao Port (24h).</p>
                """
            },
            {
                'id': 'local-access',
                'heading': 'Getting to CityU Macau (Taipa Campus)',
                'content': """
                <p>Address: <b>Avenida Padre Tomás Pereira, Taipa, Macau</b></p>
                <table class="transport-table">
                    <tr>
                        <th>From Point</th>
                        <th>Taxi (Fastest)</th>
                        <th>Public Bus (MOP 6)</th>
                    </tr>
                    <tr>
                        <td><b>Macau Airport (MFM)</b></td>
                        <td>8 mins (~MOP 40)</td>
                        <td>Bus <b>MT1</b> (Stop: <i>Esparteiro/Lou Lim Ieok</i>)</td>
                    </tr>
                    <tr>
                        <td><b>Taipa Ferry Terminal</b></td>
                        <td>5 mins (~MOP 50)</td>
                        <td>Bus <b>MT1</b> (Stop: <i>Esparteiro/Lou Lim Ieok</i>)</td>
                    </tr>
                    <tr>
                        <td><b>Border Gate</b></td>
                        <td>12 mins (~MOP 70)</td>
                        <td>Bus <b>25</b> or <b>25B</b> (Stop: <i>Esparteiro/Regency</i>)</td>
                    </tr>
                </table>
                <p><i>Note: After the bus stop, walk up the slope to reach the university entrance.</i></p>
                """
            }
        ]
    }
} # Closing bracket for site_data fixed here

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
        <div class="logo-area"><img src="aala2026-logo.png" alt="Logo" style="height: 60px;"></div>
        <nav class="nav-links">
            <a href="index.html">Home</a>
            <a href="call-for-papers.html">Call For Papers</a>
            <a href="registration.html">Registration</a>
            <a href="program.html">Program</a>
            <a href="venue.html">Venue</a>
        </nav>
    </header>
    <main>
        {% if header_title %}<section class="hero"><div class="hero-overlay"><h1>{{ header_title }}</h1><p class="hero-theme">{{ theme }}</p><p class="hero-info">{{ date }} | {{ location }}</p></div></section>{% endif %}
        <div class="container">
            {% for section in sections %}
            <section id="{{ section.id }}" class="content-block">
                <h2>{{ section.heading }}</h2>
                <div class="text-body">{{ section.content | safe }}</div>
            </section>
            {% endfor %}
        </div>
    </main>
    <footer class="footer"><p>&copy; 2026 AALA Conference. All Rights Reserved.</p></footer>
</body>
</html>
"""

# --- STEP 3: THE STYLE (CSS) ---
css_code = """
body { font-family: 'Montserrat', sans-serif; margin: 0; line-height: 1.6; color: #333; }
.navbar { display: flex; justify-content: space-between; padding: 10px 5%; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000; }
.nav-links a { margin-left: 20px; text-decoration: none; color: #008264; font-weight: bold; }
.container { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
.hero { background: url('aala2026-banner.png') no-repeat center center/cover; height: 400px; color: white; text-align: center; }
.hero-overlay { background: rgba(0,0,0,0.5); height: 100%; display: flex; flex-direction: column; justify-content: center; }
.content-block h2 { color: #008264; border-bottom: 3px solid #008264; display: inline-block; }
.highlight-red { color: #FA0202; font-weight: bold; }

.parallel-container { display: flex; gap: 20px; margin-top: 20px; }
.category-card { flex: 1; background: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.video-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
.media-box { text-align: center; }
.tight-list { padding-left: 18px; margin-left: 0; }
.tight-list li { margin-bottom: 5px; }

/* Transport Table Styling */
.transport-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
.transport-table th, .transport-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
.transport-table th { background-color: #008264; color: white; }
.transport-table tr:nth-child(even) { background-color: #f2f2f2; }

.footer { text-align: center; padding: 30px; background: #008264; color: white; margin-top: 50px; }
@media (max-width: 768px) { .parallel-container, .video-grid { flex-direction: column; } }
"""

def build_site():
    with open('style.css', 'w', encoding='utf-8') as f: f.write(css_code)
    template = Template(html_layout)
    for page_id, content in site_data.items():
        filename = 'index.html' if page_id == 'home' else f"{page_id}.html"
        with open(filename, 'w', encoding='utf-8') as f: f.write(template.render(content))
    print("✨ Site built successfully!")

if __name__ == "__main__": build_site()
