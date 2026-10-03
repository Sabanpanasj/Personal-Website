"""Edit this file with your own details, then run: python build.py"""

NAME = "Steve Jesus P. Sabanpan"
ROLE = "Frontend Developer"     # shows in amber above your name
AVAILABLE = True                # shows the green "Available for work" badge

EMAIL = "Sjsabanpan@gmail.com"
PHONE = "09917731731"
SCHOOL = "USTP - Balubal Campus"
LOCATION = "Libona, Bukidnon, Philippines"

SUMMARY = (
    "I am a frontend developer who enjoys building clean, responsive websites. "
    "I am currently studying at the University of Science and Technology of "
    "Southern Philippines and looking for opportunities to grow my skills."
)

# Contact form email.
# "" = use Netlify Forms (default). To use the free Web3Forms service instead, get your
# access key at https://web3forms.com (it is emailed to you) and paste it between the quotes.
WEB3FORMS_KEY = "51efe6d6-f636-45e1-87fc-cb44b86e027d"

# Put these files in the assets/ folder (both optional):
PHOTO = "assets/profile.jpg"       # your photo (JPG or PNG; a transparent PNG cut-out looks best)
RESUME_FILE = "assets/resume.pdf"  # shows the "Download Resume" button

# Usernames only (no @ and no link). Leave "" to hide an icon.
SOCIALS = {
    "facebook": "sabanpan2004",
    "instagram": "sabanpansteve",
    "tiktok": "sjsab2004",
}

# Education & certificates: title (white) and detail (amber).
# Optional "link" + "link_text" adds a clickable link under the entry.
EDUCATION = [
    {"title": "Primary School", "detail": "Graduated: 2017"},
    {"title": "Junior High School", "detail": "Graduated: 2021"},
    {"title": "Senior High School", "detail": "Graduated: 2023"},
    {"title": "Capitol University", "detail": "Enrolled: 2023 - 2025"},
    {
        "title": "CS50x Certificate, Harvard University",
        "detail": "Certified: 2026",
        "link": "https://cs50.harvard.edu/certificates/7bbb3703-3738-48cf-a002-48996f0b662e",
        "link_text": "View certificate",
    },
    {
        "title": "University of Science and Technology of Southern Philippines (Balubal Campus)",
        "detail": "Currently studying: 2026 - Present",
    },
]

# Optional: leave as [] to hide
EXPERIENCE = []

# The amber bullet list in Skills & Tools
ROLES = ["Frontend Web Developer", "Responsive Web Designer"]

# Tool tiles: (label, devicon name). Browse names at https://devicon.dev
TOOLS = [
    ("HTML", "html5"),
    ("CSS", "css3"),
    ("PHP", "php"),
    ("JavaScript", "javascript"),
    ("C", "c"),
    ("Python", "python"),
    ("MySQL", "mysql"),
    ("GitHub", "github"),
    ("Git", "git"),
    ("Figma", "figma"),
]

# image is optional (e.g. "assets/project1.png"); link is optional.
# Leave as [] to hide the Projects section and its menu button.
PROJECTS = [
    {
        "title": "Inventory Manager",
        "desc": "Desktop app to track products, stock and sales with live charts. Works offline.",
        "image": "assets/inventory-manager.jpg",
        "link": "https://sabanpanasj.github.io/Inventory-Management/",
    },
]
