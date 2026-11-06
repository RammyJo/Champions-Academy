"""School copy and links. See HANDOVER.md for provenance and review gates."""
NAME = "Champions Academy"
ADDRESS = "F. Ortega Highway, Santiago Norte, City of San Fernando, La Union, Philippines"
EMAIL = "enroll@champions.edu.ph"
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSckgefkFs3NMyp8YYy8rGlWFUny6dtpokpARlEOSFFk2Y8Jcg/viewform"
FACEBOOK = "https://www.facebook.com/sfchampionsacademy"
INSTAGRAM = "https://www.instagram.com/championsacademy.ph"
MAP = "https://www.google.com/maps?cid=10628483174156427098"
VISION = "An excellent school of influence producing champions in life. A cutting-edge learning hub for global champions."
MISSION = "To honor God and deliver all His benefits by building a solid foundation for children and equip them with life skills to become champions in life."

PROGRAMS = {
    "/preschool/": {
        "name": "Preschool", "stage": "Nursery & Kindergarten", "image": "preschool",
        "intro": "Young children learn by asking questions, trying things for themselves, and discovering what they can do together.",
        "areas": [
            ("Explore and create", "Children make sense of their world through hands-on discovery, movement, and creative expression."),
            ("Build early skills", "Language, literacy, and numeracy grow through activities that connect ideas to everyday experiences."),
            ("Learn alongside others", "Children practice expressing feelings, listening to others, and becoming more confident in a group."),
        ],
        "guidance": "Published guidance lists Nursery at age 4 and Kindergarten at age 5. Ask Admissions to confirm cut-off dates and placement for your child.",
    },
    "/grade-school/": {
        "name": "Grade School", "stage": "Grades 1–6", "image": "student-performance",
        "intro": "Children build strong academic foundations and practice applying Christian values in their relationships and everyday choices.",
        "areas": [
            ("Read, reason, and communicate", "Learners develop comprehension and numeracy, explain what they think, and work through problems with others."),
            ("Practice faith in daily life", "Bible study supports the development of humility, discipline, and a Christ-like attitude."),
            ("Keep families involved", "Parents and teachers communicate about learning and help children develop habits they can use at school and at home."),
        ],
        "guidance": "Contact Admissions for grade placement and the current document checklist.",
    },
    "/junior-high-school/": {
        "name": "Junior High School", "stage": "Grades 7–10", "image": "junior-high",
        "intro": "Students deepen their faith, learn to think critically, and take greater responsibility for their work as they prepare for further education.",
        "areas": [
            ("Academic development", "Students apply foundational skills to more complex questions and practice explaining and evaluating ideas."),
            ("Christian character and leadership", "Students explore how their faith shapes choices, relationships, and responsibility to others."),
            ("Digital competencies", "Students build computer literacy and practice using digital tools in support of their learning."),
        ],
        "guidance": "Ask Admissions about current grade availability and the records needed for placement.",
    },
}

PHOTOS = {
    "classroom-activity": ("Students in uniform working on activity sheets", 940/788),
    "classroom-together": ("Students in uniform seated together in a Champions Academy classroom", 940/788),
    "celebration": ("Champions Academy students in uniform gathered on stage", 3/2),
    "student-performance": ("Students lined up on stage during a school presentation", 3/2),
    "school-event": ("A group of students on stage at a Champions Academy event", 3/2),
    "junior-high": ("Students and an adult in a Champions Academy classroom", 1024/879),
    "campus": ("Champions Academy sign above the school entrance", 4/3),
    "preschool": ("Young learners gathered around a yellow classroom table", 4/3),
}

REQUIREMENTS = [
    ("Online registration form", "Complete the school’s Google Form using the pre-registration page."),
    ("PSA birth certificate", "Prepare a photocopy."),
    ("Form 138 or report card", "Ask Admissions which school records are needed for your child’s entry level."),
    ("Medical certificate", "The published list specifies a photocopy for face-to-face learning. Confirm whether it applies."),
    ("Long white folder", "Prepare a folder with a fastener."),
    ("Two 2 × 2 ID photos", "Confirm the current photo specifications with Admissions."),
]

# Publish dated announcements after the school approves their copy.
# Each entry needs date (YYYY-MM-DD), title and summary.
ANNOUNCEMENTS = []

# Confirm active staff, roles and portrait permission before adding public profiles.
# Each entry needs group, name and role, and can include a local portrait filename.
FACULTY = []

ARCHIVE = [
    ("2017-12-28", "learning-spaces-converted-space-for-learning", "Learning spaces", "The school described how it arranged preschool learning spaces to encourage exploration, hands-on work, and collaborative play."),
    ("2017-12-07", "champion-families-in-champions-academy-a-special-united-nations-celebration", "A United Nations celebration", "Families supported a school celebration with costumes, student presentations, and food representing different countries."),
    ("2017-10-18", "benchmarking-trip-to-make-things-better", "A school learning visit", "School leaders visited Life College in Palawan and reflected on staff collaboration, teacher development, and parent communication."),
]

PHOTO_WIDTHS = {
    "classroom-activity": (480, 940),
    "classroom-together": (480, 940),
}
