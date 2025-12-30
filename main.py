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
                'content': """The Asian Association for Language Assessment (AALA) 2026 Conference will be held from September 18-20, 2026, at the City University of Macau. This year's theme is the <b>'Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability'.</b> We invite you to contribute to this important conversation. You can find more information on our <a href='call-for-papers.html'>Call for Papers</a> page."""
                """
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
                # ADDED THE LOGO HERE BEFORE THE TEXT
                'content': """
                <div style="margin-bottom: 20px;">
                    <img src="/Users/ajz/Library/CloudStorage/OneDrive-Personal/Coding/AALA2026/AALA logo.png" alt="AALA Logo" style="height: 100px; width: auto;">
                </div>
                The Asian Association for Language Assessment (AALA) is a professional organization dedicated to promoting best practices in language assessment throughout Asia and beyond. Learn more about our mission and history on the <a href='https://www.aalawebsite.com/' target='_blank'>official AALA website</a>."""
            },
            {
                'id': 'about-macau',
                'heading': 'Macao Overview',
                'content': "Macao offers a unique cultural blend and is a UNESCO World Heritage Site. It has a compact city layout with easy transport connectivity, which is convenient for conference attendees to explore leisure and cultural attractions. Here's a glimpse into the city's key offerings:<br><br><b><a href='https://www.macaotourism.gov.mo/en/dining' target='_blank'>Dining:</a></b> The city has diverse dining options, ranging from authentic local eateries to high-end international restaurants with cuisines like Cantonese, Portuguese, Asian fusion, and Western.<br><br><b><a href='https://www.macaotourism.gov.mo/en/shows-and-entertainment/nightlife' target='_blank'>Nightlife:</a></b> The nightlife is a vibrant mix of world-class casinos, rooftop bars, nightclubs, and local pubs. You can find cozy bars with live music and stunning city views.<br><br><b><a href='https://www.dst.gov.mo/en/home.html' target='_blank'>Tourism Infrastructure:</a></b> There's strong government support for cultural tourism, historic site revitalization, and event hosting."
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
                'content': """
                <p>Asian Association for Language Assessment (AALA) 2026 Conference</p>
                <p>📍 <b>City University of Macau</b> | 18–20 September 2026</p>
                <br>
                <p>🔗 <a href="https://forms.office.com/r/bSxtmKfi8C?origin=lprLink" target="_blank">Submit your abstract and register.</a></p>
                <h3>Theme:</h3>
                <p><b>Humanistic Approach to <span class="highlight-red">A</span>ssessment, <span class="highlight-red">S</span>tandards, <span class="highlight-red">I</span>nnovation, and <span class="highlight-red">A</span>ccountability</b></p>
                <p>The Asian Association for Language Assessment (AALA) invites researchers, educators, practitioners, and policymakers to submit proposals for the 2026 annual conference, hosted by City University of Macau, in collaboration with the University of Macau and Macao Polytechnic University.</p>
                <p>This year’s conference highlights a human-centred vision of language assessment—one that promotes fairness, inclusivity, and learner well-being while engaging with new technologies, evolving standards, and institutional accountability.</p>
                <br>
                <h3>Subthemes</h3>
                <p>We welcome proposals related to (but not limited to):</p>
                <ul>
                    <li>Humanistic and ethical practices in assessment</li>
                    <li>Standards and policy in diverse educational contexts</li>
                    <li>Innovations in assessment (AI, GenAI, multimodal, biometrics)</li>
                    <li>Accountability and stakeholder perspectives</li>
                    <li>Classroom-based assessment and teacher assessment literacy</li>
                    <li>Multilingual assessment in Asian and global contexts</li>
                    <li>Socio-psychological aspects of assessment (affect, motivation, identity)</li>
                    <li>Future directions: sustainability, accessibility, and equity</li>
                </ul>
                <br>
                <h3>Proposal Types</h3>
                <ul>
                    <li><b>Individual Papers:</b> (20 minutes + 10 minutes Q&A)</li>
                    <li><b>Posters:</b> (interactive sessions)</li>
                </ul>
                <br>
                <h3>Key Dates</h3>
                <ul>
                    <li><b>Abstract submission opens:</b> [insert date]</li>
                    <li><b>Submission deadline:</b> [insert date]</li>
                    <li><b>Notification of acceptance:</b> [insert date]</li>
                    <li><b>Early bird registration closes:</b> [insert date]</li>
                </ul>
                <br>
                <h3>Submission Guidelines</h3>
                <ul>
                    <li><b>Abstracts:</b> max. 300 words (excluding references).</li>
                    <li>Indicate presentation type and select a relevant subtheme.</li>
                    <li>All submissions will undergo double-blind peer review.</li>
                </ul>
                <br>
                <p>We look forward to welcoming you to Macau for AALA 2026!</p>
                """
            }
        ]
    },
    'registration': {
        'page_title': 'Registration & Payment- AALA 2026',
        'sections': [
            {
                'id': 'registration',
                'heading': 'Registration and Payment',
                'content': 'Conference registration is now open. The registration process includes easy online sign-up and secure payment. We offer different registration tiers for students and professionals. Click the link to register now!'
            }
        ]
    },
    'program': {
        'page_title': 'Program & Schedule - AALA 2026',
        'sections': [
            {
                'id': 'program',
                'heading': 'Program & Schedule',
                'content': 'The detailed agenda, including session times, speaker profiles, and workshop information, will be released closer to the conference date. The program will feature a wide range of topics related to language assessment in a humanistic light.'
            }
        ]
    },
    'venue': {
        'page_title': 'Venue & Transport - AALA 2026',
        'sections': [
            {
                'id': 'venue',
                'heading': 'Venue Overview',
                'content': 'The conference will be held at the City University of Macau, which offers world-class facilities including a modern theatre and a convention centre.'
            },
            {
                'id': 'accommodation',
                'heading': 'Accommodation Options',
                'content': """A range of accommodation options are available near the university:
<br><br>
<p><a href='https://www.altiramacau.com/en' target='_blank'>Altira Macau</a> (8 mins walk) </p>
<p><a href='http://www.regencyarthotel.com.mo/' target='_blank'>Regency Art Hotel Macau</a> (8 mins walk) </p>
<p><a href='https://www.innhotel.com/index.php' target='_blank'>Inn Hotel Macau</a> (18 mins walk) </p>
<p><a href='http://www.granddragon.com.mo/index_en.php' target='_blank'>Grand Dragon Hotel</a> (17 mins walk) </p>
<p><a href='http://www.grandview-hotel.com/' target='_blank'>Hotel Grandview</a> (18 mins walk)</p>
"""
            },
            {
                'id': 'transport',
                'heading': 'Transportation & Accessibility',
                'content': """<p><b>By Air ✈️</b></p>
                <p>Macau International Airport (MFM), located in Taipa, operates 24 hours a day with direct flights from many major Asian cities. For participants travelling from outside Asia, Hong Kong International Airport (HKG) is a convenient hub with excellent onward connections to Macau. From HKG, you can take either a direct bus across the Hong Kong–Zhuhai–Macau Bridge or a ferry service to Macau.</p>
                <br>
                <p><b>By Sea 🛥️</b></p>
                <p>Macau is well connected by frequent high-speed ferries, offering a comfortable and scenic journey.</p>
                <ul>
                    <li>Outer Harbour Ferry Terminal (外港客運碼頭) in the Macau Peninsula operates around the clock.</li>
                    <li>Inner Harbour Ferry Terminal (內港客運碼頭) serves selected routes during daytime hours (07:00–22:00).</li>
                    <li>Taipa Ferry Terminal (氹仔客運碼頭), close to the airport and Cotai area, also operates 24 hours.</li>
                </ul>
                <p>The ferry from Hong Kong takes approximately 55–60 minutes, with additional links to Shenzhen and Zhuhai.</p>
                <br>
                <p><b>By Land 🚗</b></p>
                <p>The Hong Kong–Zhuhai–Macau Bridge has transformed land travel to Macau. A shuttle bus service known as the “Golden Bus” runs 24 hours a day, connecting Hong Kong and Macau in about 40 minutes.</p>
                <p>Macau also shares several land border checkpoints with mainland China:</p>
                <ul>
                    <li>Border Gate (關閘口岸) – open daily from 06:00 to 01:00, the busiest gateway connecting Zhuhai and Macau.</li>
                    <li>Hengqin Port (橫琴口岸) – a 24-hour crossing directly linking Hengqin and Macau.</li>
                    <li>Qingmao Port (青茂口岸) – a new 24-hour crossing designed for pedestrian travellers.</li>
                </ul>
                <br>
                <p><b>✅ Tip for participants: </b> For convenience, travellers from Hong Kong International Airport are strongly encouraged to take the Hong Kong–Zhuhai–Macau Bridge 
                shuttle bus, which is faster and more cost-effective than the ferry.</p>
                """
            },
        ]
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
</head>
<body>
<header class="navbar">
    <div class="logo-container">
        <!-- UPDATED BANNER LOGO TO AALA 2026 LOGO -->
        <img src="/Users/ajz/Library/CloudStorage/OneDrive-Personal/Coding/AALA2026/AALA2026 logo.png" alt="AALA 2026 Logo" class="aala-logo">
    </div>
    <nav class="nav-links nav-left">
        <a href="index.html">Home</a>
        <a href="call-for-papers.html">Call For Papers</a>
        <a href="registration.html">Registration</a>
        <a href="program.html">Program</a>
        <a href="venue.html">Venue/Transport</a>
    </nav>
</header>
    <main>
        {% if 'home' in page_title.lower() %}
        <section id="home" class="hero-section">
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

        {% for section in sections %}
        <section id="{{ section.id }}" class="content-section">
            <h2>{{ section.heading }}</h2>
            <p>{{ section.content | safe }}</p>
        </section>
        {% endfor %}

        {% if 'home' in page_title.lower() %}
        <section id="important-dates-contact" class="dates-contact-section">
            <div class="dates-container">
                <h2>Important Dates:</h2>
                <ul>
                    <li><strong>Conference Dates:</strong> {{ date }}</li>
                </ul>
            </div>
            <div class="contact-container">
                <h2>Get in Contact</h2>
                <p>For enquiries, please email us directly at: <a href="mailto:{{ contact_email }}">{{ contact_email }}</a></p>
                <form action="#" method="post" class="contact-form">
                    <input type="text" name="name" placeholder="Name" required>
                    <input type="email" name="email" placeholder="Email" required>
                    <input type="text" name="subject" placeholder="Subject" required>
                    <textarea name="message" placeholder="Type your message here..." required></textarea>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </section>
        {% endif %}
    </main>

    <footer class="footer">
        <p>&copy; 2026 AALA. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""

# --- Step 3: Define your CSS stylesheet ---
css_content = """
:root {
    --color-green: #008264;
    --color-red: #FA0202;
    --color-dark-blue: #020266;
    --color-yellow: #f2d72e;
    --color-white: #ffffff;
    --color-light-grey: #f8f9fa;
}

body {
    font-family: 'Montserrat', sans-serif;
    margin: 0;
    line-height: 1.6;
    color: var(--color-dark-blue);
    background-color: var(--color-white);
    scroll-behavior: smooth;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: var(--color-green);
}

.highlight-red {
    color: var(--color-red);
}

.navbar {
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    position: fixed;
    width: 100%;
    top: 0;
    left: 0;
    z-index: 1000;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.aala-logo {
    height: 70px; /* Adjusted height for navigation bar */
    width: auto;
}

.nav-links a {
    color: var(--color-dark-blue);
    text-decoration: none;
    font-weight: 600;
    margin: 0 1.5rem;
    transition: color 0.3s ease;
}

.hero-section {
    background: #020266; /* Fallback color */
    color: var(--color-white);
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding-top: 80px;
}

.heading-large { font-size: 3rem; color: white; }
.theme { font-size: 1.5rem; color: var(--color-yellow); }

.content-section {
    padding: 4rem 2rem;
    max-width: 900px;
    margin: 0 auto;
}

.cta-button {
    background-color: var(--color-red);
    color: white;
    padding: 1rem 2rem;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
}

.dates-contact-section {
    display: flex;
    gap: 20px;
    padding: 40px;
    background: var(--color-light-grey);
}

.footer {
    background: var(--color-green);
    color: white;
    text-align: center;
    padding: 20px;
}
"""

# --- Step 4: Run the generation process ---
try:
    # We use a string loader since we defined the template in the script
    env = Environment()

    for page_name, data in site_data.items():
        template = env.from_string(html_template)
        rendered_html = template.render(data)

        file_name = 'index.html' if page_name == 'home' else f'{page_name}.html'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        print(f"✅ '{file_name}' generated successfully!")

    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✅ 'style.css' generated successfully!")

except Exception as e:
    print(f"❌ An error occurred: {e}")
