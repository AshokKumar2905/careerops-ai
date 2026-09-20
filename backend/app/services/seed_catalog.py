from __future__ import annotations

from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.career import Career
from backend.app.models.career_skill import CareerSkill
from backend.app.models.industry import Industry
from backend.app.models.skill import Skill


INDUSTRIES = {
    "Technology": "Software, cloud, cybersecurity, data, AI and digital technology careers.",
    "Business": "Management, operations, consulting, marketing and business strategy careers.",
    "Finance & Analytics": "Finance, accounting, analytics, investment and business intelligence careers.",
    "Healthcare & Life Sciences": "Healthcare, biotechnology, research and life science careers.",
    "Design & Creative": "UI/UX, graphic design, product design and creative careers.",
    "Engineering & Infrastructure": "Engineering, infrastructure, automation, manufacturing and technical operations.",
    "Education & Research": "Teaching, academic, training and research-oriented careers.",
    "Media & Communication": "Content, journalism, communications, media and public relations careers.",
    "Law & Public Service": "Law, policy, government and public-service careers.",
    "Hospitality & Travel": "Hospitality, tourism, travel and customer-experience careers.",
    "Skilled Trades": "Hands-on technical, maintenance, construction and skilled-trade careers.",
}


SKILLS = {
    # Technology
    "Python": ("Technology", "Programming and automation using Python."),
    "Java": ("Technology", "Object-oriented programming using Java."),
    "JavaScript": ("Technology", "Programming for web applications."),
    "SQL": ("Technology", "Querying and managing relational databases."),
    "Git": ("Technology", "Source control and collaborative software development."),
    "Linux": ("Technology", "Linux operating systems and administration."),
    "Cloud Computing": ("Technology", "Cloud platforms and infrastructure concepts."),
    "Docker": ("Technology", "Containerization and application packaging."),
    "Kubernetes": ("Technology", "Container orchestration and platform engineering."),
    "Cybersecurity": ("Technology", "Security principles, controls and threat awareness."),
    "Data Analysis": ("Technology", "Analysis and interpretation of structured data."),
    "Machine Learning": ("Technology", "Machine learning concepts and model development."),
    "Communication": ("Technology", "Clear written and verbal communication."),
    "Problem Solving": ("Technology", "Structured reasoning and practical problem solving."),

    # Business
    "Business Analysis": ("Business", "Analyzing business needs and translating them into requirements."),
    "Project Management": ("Business", "Planning, coordinating and delivering projects."),
    "Leadership": ("Business", "Leading teams and coordinating organizational activities."),
    "Marketing": ("Business", "Marketing strategy, campaigns and customer engagement."),
    "Sales": ("Business", "Customer relationship building and sales execution."),
    "Operations": ("Business", "Process improvement and operational coordination."),

    # Finance
    "Accounting": ("Finance & Analytics", "Financial accounting and reporting."),
    "Financial Analysis": ("Finance & Analytics", "Analyzing financial performance and trends."),
    "Excel": ("Finance & Analytics", "Spreadsheet analysis and business modeling."),
    "Statistics": ("Finance & Analytics", "Statistical methods for analysis and decision making."),
    "Financial Modeling": ("Finance & Analytics", "Building financial models for planning and analysis."),

    # Healthcare
    "Healthcare Knowledge": ("Healthcare & Life Sciences", "Understanding healthcare systems and practices."),
    "Biology": ("Healthcare & Life Sciences", "Core biological sciences knowledge."),
    "Research": ("Healthcare & Life Sciences", "Structured investigation and evidence-based research."),
    "Clinical Documentation": ("Healthcare & Life Sciences", "Accurate healthcare record and documentation practices."),

    # Design
    "UI/UX Design": ("Design & Creative", "Designing useful and intuitive digital experiences."),
    "Figma": ("Design & Creative", "Interface design and prototyping with Figma."),
    "Graphic Design": ("Design & Creative", "Visual design, composition and branding."),
    "Creativity": ("Design & Creative", "Generating and developing original ideas."),
    "User Research": ("Design & Creative", "Understanding user needs through research."),

    # Engineering & Infrastructure
    "Engineering Fundamentals": ("Engineering & Infrastructure", "Core engineering principles and technical reasoning."),
    "AutoCAD": ("Engineering & Infrastructure", "Computer-aided technical drawing and design."),
    "Mechanical Design": ("Engineering & Infrastructure", "Mechanical component and system design."),
    "Networking": ("Engineering & Infrastructure", "Computer networking and infrastructure fundamentals."),
    "Automation": ("Engineering & Infrastructure", "Automating repeatable technical processes."),
    "Electrical Systems": ("Engineering & Infrastructure", "Electrical systems and circuit fundamentals."),

    # Education & Research
    "Teaching": ("Education & Research", "Instructional methods and learner support."),
    "Curriculum Development": ("Education & Research", "Designing structured educational programs."),
    "Public Speaking": ("Education & Research", "Presenting information clearly to an audience."),

    # Media & Communication
    "Content Writing": ("Media & Communication", "Writing useful and engaging content."),
    "Journalism": ("Media & Communication", "News research, reporting and editorial practices."),
    "Video Editing": ("Media & Communication", "Editing video content for digital platforms."),
    "Social Media": ("Media & Communication", "Creating and managing social media content."),
    "Public Relations": ("Media & Communication", "Managing communications and public image."),

    # Law & Public Service
    "Legal Research": ("Law & Public Service", "Researching laws, regulations and legal sources."),
    "Legal Writing": ("Law & Public Service", "Drafting structured legal documents."),
    "Policy Analysis": ("Law & Public Service", "Analyzing public policy and regulatory issues."),
    "Civic Knowledge": ("Law & Public Service", "Understanding public institutions and civic systems."),

    # Hospitality & Travel
    "Customer Service": ("Hospitality & Travel", "Supporting customers and handling service needs."),
    "Hospitality Operations": ("Hospitality & Travel", "Managing hotel, restaurant and hospitality operations."),
    "Travel Planning": ("Hospitality & Travel", "Planning travel experiences and itineraries."),
    "Event Management": ("Hospitality & Travel", "Planning and coordinating events."),

    # Skilled Trades
    "Electrical Maintenance": ("Skilled Trades", "Electrical installation, maintenance and troubleshooting."),
    "Mechanical Maintenance": ("Skilled Trades", "Mechanical maintenance and equipment troubleshooting."),
    "Welding": ("Skilled Trades", "Welding techniques and fabrication."),
    "Plumbing": ("Skilled Trades", "Plumbing installation and maintenance."),
    "Construction": ("Skilled Trades", "Construction methods, materials and site practices."),
}


CAREERS = [
    {
        "industry": "Technology",
        "title": "Software Developer",
        "description": "Build, test and maintain software applications and digital products.",
        "experience_level": "Entry Level",
        "skills": ["Programming", "Problem Solving", "Git", "Communication"],
    },
    {
        "industry": "Technology",
        "title": "Data Analyst",
        "description": "Use data, statistics and visualization to support business decisions.",
        "experience_level": "Entry Level",
        "skills": ["SQL", "Data Analysis", "Statistics", "Excel", "Communication"],
    },
    {
        "industry": "Technology",
        "title": "Data Engineer",
        "description": "Build reliable data pipelines and systems for analytics and applications.",
        "experience_level": "Entry Level",
        "skills": ["Python", "SQL", "Data Analysis", "Cloud Computing", "Problem Solving"],
    },
    {
        "industry": "Technology",
        "title": "AI / Machine Learning Engineer",
        "description": "Develop intelligent systems and machine learning solutions.",
        "experience_level": "Entry Level",
        "skills": ["Python", "Machine Learning", "Statistics", "Data Analysis", "Problem Solving"],
    },
    {
        "industry": "Technology",
        "title": "Cybersecurity Analyst",
        "description": "Monitor systems, investigate threats and improve security controls.",
        "experience_level": "Entry Level",
        "skills": ["Cybersecurity", "Linux", "Networking", "Problem Solving", "Communication"],
    },
    {
        "industry": "Technology",
        "title": "Cloud Engineer",
        "description": "Design and maintain scalable applications and cloud infrastructure.",
        "experience_level": "Entry Level",
        "skills": ["Cloud Computing", "Linux", "Networking", "Automation", "Problem Solving"],
    },
    {
        "industry": "Technology",
        "title": "DevOps Engineer",
        "description": "Automate software delivery and improve infrastructure reliability.",
        "experience_level": "Entry Level",
        "skills": ["Linux", "Git", "Cloud Computing", "Docker", "Kubernetes", "Automation"],
    },
    {
        "industry": "Business",
        "title": "Business Analyst",
        "description": "Translate business needs into requirements, insights and process improvements.",
        "experience_level": "Entry Level",
        "skills": ["Business Analysis", "Problem Solving", "Communication", "Excel", "Project Management"],
    },
    {
        "industry": "Business",
        "title": "Project Coordinator",
        "description": "Coordinate project activities, timelines, communication and documentation.",
        "experience_level": "Entry Level",
        "skills": ["Project Management", "Communication", "Excel", "Operations", "Leadership"],
    },
    {
        "industry": "Business",
        "title": "Marketing Specialist",
        "description": "Plan marketing activities and create campaigns that connect products with customers.",
        "experience_level": "Entry Level",
        "skills": ["Marketing", "Communication", "Creativity", "Social Media", "Data Analysis"],
    },
    {
        "industry": "Business",
        "title": "Sales Executive",
        "description": "Build customer relationships and help organizations grow revenue.",
        "experience_level": "Entry Level",
        "skills": ["Sales", "Communication", "Problem Solving", "Customer Service", "Leadership"],
    },
    {
        "industry": "Finance & Analytics",
        "title": "Financial Analyst",
        "description": "Analyze financial information and help organizations make informed decisions.",
        "experience_level": "Entry Level",
        "skills": ["Financial Analysis", "Excel", "Statistics", "Financial Modeling", "Communication"],
    },
    {
        "industry": "Finance & Analytics",
        "title": "Accountant",
        "description": "Maintain financial records, prepare reports and support accounting operations.",
        "experience_level": "Entry Level",
        "skills": ["Accounting", "Excel", "Financial Analysis", "Communication"],
    },
    {
        "industry": "Finance & Analytics",
        "title": "Business Intelligence Analyst",
        "description": "Turn organizational data into dashboards, insights and business recommendations.",
        "experience_level": "Entry Level",
        "skills": ["SQL", "Data Analysis", "Statistics", "Excel", "Business Analysis"],
    },
    {
        "industry": "Healthcare & Life Sciences",
        "title": "Healthcare Administrator",
        "description": "Support healthcare operations, coordination and service delivery.",
        "experience_level": "Entry Level",
        "skills": ["Healthcare Knowledge", "Communication", "Operations", "Customer Service"],
    },
    {
        "industry": "Healthcare & Life Sciences",
        "title": "Clinical Research Assistant",
        "description": "Support research activities, documentation and evidence collection.",
        "experience_level": "Entry Level",
        "skills": ["Research", "Biology", "Clinical Documentation", "Communication"],
    },
    {
        "industry": "Healthcare & Life Sciences",
        "title": "Biotechnology Researcher",
        "description": "Conduct laboratory and research activities within life science environments.",
        "experience_level": "Entry Level",
        "skills": ["Biology", "Research", "Statistics", "Problem Solving"],
    },
    {
        "industry": "Design & Creative",
        "title": "UI/UX Designer",
        "description": "Design intuitive digital experiences based on user needs and behavior.",
        "experience_level": "Entry Level",
        "skills": ["UI/UX Design", "Figma", "User Research", "Creativity", "Communication"],
    },
    {
        "industry": "Design & Creative",
        "title": "Graphic Designer",
        "description": "Create visual assets, branding and communication materials.",
        "experience_level": "Entry Level",
        "skills": ["Graphic Design", "Creativity", "Communication", "Figma"],
    },
    {
        "industry": "Engineering & Infrastructure",
        "title": "Mechanical Engineer",
        "description": "Design, analyze and improve mechanical systems and components.",
        "experience_level": "Entry Level",
        "skills": ["Engineering Fundamentals", "Mechanical Design", "AutoCAD", "Problem Solving"],
    },
    {
        "industry": "Engineering & Infrastructure",
        "title": "Network Engineer",
        "description": "Design, configure and maintain network infrastructure.",
        "experience_level": "Entry Level",
        "skills": ["Networking", "Linux", "Problem Solving", "Communication"],
    },
    {
        "industry": "Engineering & Infrastructure",
        "title": "Automation Engineer",
        "description": "Automate technical processes and improve system efficiency.",
        "experience_level": "Entry Level",
        "skills": ["Automation", "Engineering Fundamentals", "Python", "Problem Solving"],
    },
    {
        "industry": "Education & Research",
        "title": "Teacher / Educator",
        "description": "Help learners develop knowledge, skills and confidence.",
        "experience_level": "Entry Level",
        "skills": ["Teaching", "Communication", "Public Speaking", "Curriculum Development"],
    },
    {
        "industry": "Education & Research",
        "title": "Research Assistant",
        "description": "Support structured research, analysis and documentation.",
        "experience_level": "Entry Level",
        "skills": ["Research", "Statistics", "Communication", "Problem Solving"],
    },
    {
        "industry": "Media & Communication",
        "title": "Content Writer",
        "description": "Create clear and engaging written content for audiences and organizations.",
        "experience_level": "Entry Level",
        "skills": ["Content Writing", "Communication", "Creativity", "Research"],
    },
    {
        "industry": "Media & Communication",
        "title": "Video Editor",
        "description": "Transform raw footage into engaging digital video content.",
        "experience_level": "Entry Level",
        "skills": ["Video Editing", "Creativity", "Communication", "Social Media"],
    },
    {
        "industry": "Media & Communication",
        "title": "Public Relations Specialist",
        "description": "Plan communication strategies and manage relationships with audiences and media.",
        "experience_level": "Entry Level",
        "skills": ["Public Relations", "Communication", "Content Writing", "Social Media"],
    },
    {
        "industry": "Law & Public Service",
        "title": "Legal Researcher",
        "description": "Research legal sources and prepare structured findings.",
        "experience_level": "Entry Level",
        "skills": ["Legal Research", "Legal Writing", "Communication", "Problem Solving"],
    },
    {
        "industry": "Law & Public Service",
        "title": "Policy Analyst",
        "description": "Study policies, regulations and public-sector issues.",
        "experience_level": "Entry Level",
        "skills": ["Policy Analysis", "Research", "Communication", "Civic Knowledge", "Statistics"],
    },
    {
        "industry": "Hospitality & Travel",
        "title": "Hotel Operations Executive",
        "description": "Coordinate hospitality operations and deliver customer experiences.",
        "experience_level": "Entry Level",
        "skills": ["Hospitality Operations", "Customer Service", "Communication", "Operations"],
    },
    {
        "industry": "Hospitality & Travel",
        "title": "Travel Consultant",
        "description": "Plan travel experiences and assist customers with travel arrangements.",
        "experience_level": "Entry Level",
        "skills": ["Travel Planning", "Customer Service", "Communication", "Sales"],
    },
    {
        "industry": "Hospitality & Travel",
        "title": "Event Coordinator",
        "description": "Plan and coordinate events, vendors, schedules and customer requirements.",
        "experience_level": "Entry Level",
        "skills": ["Event Management", "Project Management", "Communication", "Customer Service"],
    },
    {
        "industry": "Skilled Trades",
        "title": "Electrical Technician",
        "description": "Install, maintain and troubleshoot electrical systems and equipment.",
        "experience_level": "Entry Level",
        "skills": ["Electrical Maintenance", "Electrical Systems", "Problem Solving", "Communication"],
    },
    {
        "industry": "Skilled Trades",
        "title": "Mechanical Technician",
        "description": "Maintain and troubleshoot mechanical equipment and systems.",
        "experience_level": "Entry Level",
        "skills": ["Mechanical Maintenance", "Mechanical Design", "Problem Solving", "Engineering Fundamentals"],
    },
    {
        "industry": "Skilled Trades",
        "title": "Construction Technician",
        "description": "Support construction projects, site activities and technical work.",
        "experience_level": "Entry Level",
        "skills": ["Construction", "Engineering Fundamentals", "Problem Solving", "Communication"],
    },
]


def get_or_create_industry(
    db,
    name: str,
    description: str,
) -> Industry:
    industry = db.scalar(
        select(Industry).where(Industry.name == name)
    )

    if industry is None:
        industry = Industry(
            name=name,
            description=description,
        )
        db.add(industry)
        db.flush()

    return industry


def get_or_create_skill(
    db,
    name: str,
    category: str,
    description: str,
) -> Skill:
    skill = db.scalar(
        select(Skill).where(Skill.name == name)
    )

    if skill is None:
        skill = Skill(
            name=name,
            category=category,
            description=description,
        )
        db.add(skill)
        db.flush()

    return skill


def get_or_create_career(
    db,
    industry_id: int,
    title: str,
    description: str,
    experience_level: str,
) -> Career:
    career = db.scalar(
        select(Career).where(Career.title == title)
    )

    if career is None:
        career = Career(
            industry_id=industry_id,
            title=title,
            description=description,
            experience_level=experience_level,
        )
        db.add(career)
        db.flush()
    else:
        career.industry_id = industry_id
        career.description = description
        career.experience_level = experience_level

    return career


def add_career_skill(
    db,
    career_id: int,
    skill_id: int,
    importance: str,
) -> None:
    existing = db.scalar(
        select(CareerSkill).where(
            CareerSkill.career_id == career_id,
            CareerSkill.skill_id == skill_id,
        )
    )

    if existing is None:
        db.add(
            CareerSkill(
                career_id=career_id,
                skill_id=skill_id,
                importance=importance,
            )
        )


def seed_catalog() -> None:
    db = SessionLocal()

    try:
        industry_objects = {}

        for name, description in INDUSTRIES.items():
            industry_objects[name] = get_or_create_industry(
                db,
                name,
                description,
            )

        skill_objects = {}

        for name, (category, description) in SKILLS.items():
            skill_objects[name] = get_or_create_skill(
                db,
                name,
                category,
                description,
            )

        db.flush()

        for career_data in CAREERS:
            industry = industry_objects[career_data["industry"]]

            career = get_or_create_career(
                db,
                industry.id,
                career_data["title"],
                career_data["description"],
                career_data["experience_level"],
            )

            for skill_name in career_data["skills"]:
                if skill_name not in skill_objects:
                    continue

                importance = "high"

                if skill_name in {
                    "Communication",
                    "Excel",
                    "Statistics",
                    "Leadership",
                }:
                    importance = "medium"

                add_career_skill(
                    db,
                    career.id,
                    skill_objects[skill_name].id,
                    importance,
                )

        db.commit()

        print(f"Industries seeded: {len(INDUSTRIES)}")
        print(f"Skills seeded: {len(SKILLS)}")
        print(f"Careers seeded: {len(CAREERS)}")
        print("Career catalog seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_catalog()