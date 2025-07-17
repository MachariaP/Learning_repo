from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, 
                                Preformatted, HRFlowable, Table, ListFlowable, 
                                PageBreak, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import logging
import textwrap

# Set up logging for debugging
logging.basicConfig(filename='pdf_generation.log', level=logging.ERROR)

# Initialize the document
doc = SimpleDocTemplate("car_sales_tutorial.pdf", pagesize=letter, 
                        title="Car Sales System Tutorial", 
                        author="Phines Macharia", 
                        creator="Grok 3",
                        leftMargin=0.75*inch, rightMargin=0.75*inch, 
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Define styles
styles = getSampleStyleSheet()

# Enhanced color scheme
NAVY = HexColor('#1B263B')
FOREST_GREEN = HexColor('#2E7D32')
SOFT_GRAY = HexColor('#4A4A4A')
LIGHT_BLUE = HexColor('#E6F3FA')
DARK_GRAY = HexColor('#E8ECEF')

# Define new styles
new_styles = {
    'BookTitle': ParagraphStyle(
        name='BookTitle',
        fontName='Times-Bold',
        fontSize=36,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=24,
        leading=40,
        letterSpacing=0.3
    ),
    'BookSubtitle': ParagraphStyle(
        name='BookSubtitle',
        fontName='Times-Italic',
        fontSize=18,
        textColor=SOFT_GRAY,
        alignment=TA_CENTER,
        spaceAfter=16,
        leading=22
    ),
    'ChapterTitle': ParagraphStyle(
        name='ChapterTitle',
        fontName='Times-Bold',
        fontSize=20,
        textColor=NAVY,
        spaceAfter=16,
        leading=24,
        letterSpacing=0.2
    ),
    'SectionHeading': ParagraphStyle(
        name='SectionHeading',
        fontName='Times-Bold',
        fontSize=16,
        textColor=FOREST_GREEN,
        spaceAfter=12,
        leading=20
    ),
    'BodyText': ParagraphStyle(
        name='BodyText',
        fontName='Times-Roman',
        fontSize=12,
        textColor=SOFT_GRAY,
        spaceAfter=10,
        leading=18,
        alignment=TA_JUSTIFY
    ),
    'CodeBlock': ParagraphStyle(
        name='CodeBlock',
        fontName='Courier-Bold',
        fontSize=11,
        textColor=black,
        backColor=DARK_GRAY,
        spaceAfter=10,
        leading=13,
        leftIndent=10,
        rightIndent=10,
        borderPadding=10
    ),
    'CodeLabel': ParagraphStyle(
        name='CodeLabel',
        fontName='Times-Italic',
        fontSize=10,
        textColor=SOFT_GRAY,
        spaceAfter=4,
        leading=12,
        alignment=TA_LEFT
    ),
    'Callout': ParagraphStyle(
        name='Callout',
        fontName='Times-Roman',
        fontSize=12,
        textColor=SOFT_GRAY,
        backColor=LIGHT_BLUE,
        spaceAfter=10,
        leading=18,
        leftIndent=10,
        rightIndent=10,
        borderWidth=1,
        borderColor=NAVY,
        borderPadding=8,
        alignment=TA_JUSTIFY
    ),
    'TOCEntry': ParagraphStyle(
        name='TOCEntry',
        fontName='Times-Roman',
        fontSize=12,
        textColor=SOFT_GRAY,
        spaceAfter=6,
        leading=14
    ),
    'Header': ParagraphStyle(
        name='Header',
        fontName='Times-Italic',
        fontSize=10,
        textColor=SOFT_GRAY,
        alignment=TA_LEFT
    ),
    'Footer': ParagraphStyle(
        name='Footer',
        fontName='Times-Roman',
        fontSize=10,
        textColor=SOFT_GRAY,
        alignment=TA_CENTER
    ),
    'IntroText': ParagraphStyle(
        name='IntroText',
        fontName='Times-Italic',
        fontSize=12,
        textColor=SOFT_GRAY,
        backColor=LIGHT_BLUE,
        spaceAfter=10,
        leading=18,
        borderPadding=8,
        alignment=TA_JUSTIFY
    ),
    'KeyTakeaway': ParagraphStyle(
        name='KeyTakeaway',
        fontName='Times-Roman',
        fontSize=12,
        textColor=SOFT_GRAY,
        spaceAfter=8,
        leading=16,
        leftIndent=10
    )
}

# Add new styles
for style_name, style in new_styles.items():
    if style_name not in styles:
        styles.add(style)

# Track chapter number for headers
chapter_number = 0

# Define page template with header and footer
def on_page(canvas, doc):
    global chapter_number
    canvas.saveState()
    canvas.setFont('Times-Italic', 10)
    canvas.drawString(0.75*inch, 10.5*inch, "Car Sales System Tutorial")
    if doc.page > 2:  # Start chapter numbering after cover and TOC
        canvas.drawString(0.75*inch, 10.3*inch, f"Chapter {chapter_number}")
    canvas.setFont('Times-Roman', 10)
    canvas.drawCentredString(4.25*inch, 0.5*inch, f"Page {doc.page}")
    canvas.restoreState()

main_frame = Frame(0.75*inch, 0.75*inch, 6.5*inch, 9.5*inch, id='main')
page_templates = [PageTemplate(id='standard', frames=main_frame, onPage=on_page)]
doc.addPageTemplates(page_templates)

# Helper function for code blocks
def create_code_block(code):
    try:
        return KeepTogether(
            Table(
                [
                    [Paragraph("Code Example", styles['CodeLabel'])],
                    [Preformatted(code, styles['CodeBlock'], maxWidth=6.15*inch)]
                ],
                colWidths=[6.25*inch],
                style=[
                    ('BOX', (0,0), (-1,-1), 2, black),
                    ('BACKGROUND', (0,0), (-1,-1), DARK_GRAY),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 10),
                    ('RIGHTPADDING', (0,0), (-1,-1), 10),
                    ('TOPPADDING', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#D3D3D3')),
                ],
                splitByRow=True
            )
        )
    except Exception as e:
        logging.error(f"Failed to create code block: {str(e)}")
        return Paragraph(f"Error rendering code block: {str(e)}", styles['BodyText'])

# Cover page
def cover_page():
    return [
        Spacer(1, 2.5*inch),
        Paragraph("Car Sales System Tutorial", styles['BookTitle']),
        Paragraph("A Beginner’s Guide to Building a Python Project", styles['BookSubtitle']),
        Spacer(1, 0.75*inch),
        Paragraph("By Phines Macharia", styles['BodyText']),
        Spacer(1, 1.25*inch),
        HRFlowable(width=4*inch, thickness=2, color=NAVY, spaceAfter=0.75*inch),
        Spacer(1, 2.5*inch),
        PageBreak()
    ]

# Preface
def preface():
    return [
        Paragraph("Preface", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "Welcome to the <b>Car Sales System Tutorial</b>! This book guides beginners through building a Python-based car sales system. Each chapter offers clear explanations, analogies, and tips to ensure success. Whether you’re new to coding or brushing up, you’ll create a secure, functional program. Let’s dive in!",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("Who This Book is For", styles['SectionHeading']),
        Paragraph(
            "This book targets absolute beginners with little programming experience. If you know basic Python (e.g., variables), great! If not, we explain everything step-by-step to make learning fun and accessible.",
            styles['BodyText']
        ),
        Spacer(1, 12),
        Paragraph("What You’ll Learn", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("How to store data in a <b>database</b>.", styles['BodyText']),
                Paragraph("Creating <b>classes</b> to organize code.", styles['BodyText']),
                Paragraph("Building a terminal interface with menus.", styles['BodyText']),
                Paragraph("Adding security with logins.", styles['BodyText']),
                Paragraph("Testing and optimizing your program.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 12),
        PageBreak()
    ]

# Table of Contents
def table_of_contents():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name='TOCLevel1',
            fontName='Times-Roman',
            fontSize=12,
            textColor=SOFT_GRAY,
            leftIndent=0,
            firstLineIndent=0,
            spaceAfter=6
        )
    ]
    return [
        Paragraph("Table of Contents", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        toc,
        PageBreak()
    ]

# Chapter 1
def chapter1():
    global chapter_number
    chapter_number = 1  # Set chapter number for header
    return [
        Paragraph("Chapter 1: Your First Step into the Car Sales Adventure", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: Welcome to your programming journey! This chapter introduces you to the car sales system you’ll build using Python. We’ll explain what the system does, why it’s exciting, and what you need to get started. Whether you’ve never written code or are brushing up, this chapter will spark your enthusiasm for creating a real-world project!",
            styles['IntroText']
        ),
        Spacer(1, 12),

        # 1.1 Welcome to Your Programming Journey!
        Paragraph("1.1 Welcome to Your Programming Journey!", styles['SectionHeading']),
        Paragraph(
            "Imagine owning a car dealership where you manage cars, customers, and sales—all through a computer program you build yourself! In this book, you’ll create a <b>car sales system</b> using <b>Python</b>, a beginner-friendly programming language. This system will act like a digital assistant for a car lot, helping you store car details, track customers, and even suggest cars to buyers. The best part? You don’t need any coding experience—we’ll guide you step-by-step, explaining every piece as if you’re learning for the first time.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "Programming is like giving instructions to a super-smart robot (your computer) to do tasks for you. For example, you’ll tell your program to save a car’s details (like ‘Toyota Camry, 2020, $20,000’) or show a list of cars to a customer. By the end of this book, you’ll have a working program you can show off, and you’ll feel like a coding superhero!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Building this project teaches you skills used in real jobs, like organizing data, creating secure logins, and making user-friendly interfaces. Plus, it’s incredibly fun to see your code come to life as a working system!",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.2 Why Python?
        Paragraph("1.2 Why Python?", styles['SectionHeading']),
        Paragraph(
            "Python is one of the easiest programming languages to learn, making it perfect for beginners. It’s like writing instructions in plain English, so your computer understands exactly what you want. Python is also super popular—companies like Google, Netflix, and even car companies use it to build apps, analyze data, and more.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "Here’s why Python is great for this project:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        ListFlowable(
            [
                Paragraph("<b>Easy to Read</b>: Python code looks clean and simple, like a recipe.", styles['BodyText']),
                Paragraph("<b>Powerful Tools</b>: Python has libraries (pre-built code) to handle databases, APIs, and interfaces.", styles['BodyText']),
                Paragraph("<b>Beginner-Friendly</b>: You’ll write short, clear code that does big things.", styles['BodyText']),
                Paragraph("<b>Fun!</b>: Python makes it easy to focus on building cool features without getting stuck on complex rules.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Think of Python as a friendly guide who helps you talk to your computer. You say, ‘Save this car,’ and Python makes it happen!",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.3 What You’ll Build: Your Digital Car Dealership
        Paragraph("1.3 What You’ll Build: Your Digital Car Dealership", styles['SectionHeading']),
        Paragraph(
            "Your car sales system will be like a digital version of a car dealership, complete with a virtual lot, customer records, and a cashier’s desk. You’ll build a program that runs in your computer’s terminal (a text-based window) and lets users interact with menus to buy, sell, or browse cars. Here’s a detailed look at what your system will do:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        ListFlowable(
            [
                Paragraph("<b>Store Car Details</b>: Save information like make (e.g., Toyota), model (e.g., Camry), year, price, and more in a <b>database</b>, like a digital filing cabinet.", styles['BodyText']),
                Paragraph("<b>Manage Cars</b>: Let admins add, update, or remove cars, like stocking a car lot.", styles['BodyText']),
                Paragraph("<b>Track Customers</b>: Store customer names and contact info to keep track of buyers.", styles['BodyText']),
                Paragraph("<b>Search Cars</b>: Allow customers to search for cars by make or model, like browsing an online store.", styles['BodyText']),
                Paragraph("<b>Fetch Real Data</b>: Use <b>APIs</b> (internet services) to get car details or market prices, like checking a car’s value online.", styles['BodyText']),
                Paragraph("<b>Smart Suggestions</b>: Add <b>AI</b> to recommend cars based on what customers like, like a salesperson suggesting similar models.", styles['BodyText']),
                Paragraph("<b>Secure Logins</b>: Protect the system with usernames and passwords, so only authorized users can access it.", styles['BodyText']),
                Paragraph("<b>Easy Menus</b>: Create a text-based interface with menus, so users can choose options by pressing numbers, like a video game menu.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Analogy</b>: Your system is like a LEGO car dealership. Each chapter adds a new piece—cars, customers, menus—until you have a complete, working model. We’ll explain how every piece fits, so you’re never lost!",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.4 A Sneak Peek at the Code
        Paragraph("1.4 A Sneak Peek at the Code", styles['SectionHeading']),
        Paragraph(
            "Wondering what your project will look like? Let’s preview some real code you’ll write in later chapters. Don’t worry if it looks unfamiliar now—we’ll explain every line when you get there. These examples show the exciting things you’ll create!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Example 1: Setting Up the Database", styles['BodyText']),
        Paragraph(
            "You’ll create a database to store car details, like a digital notebook. This code sets up a table for cars:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import sqlite3

def init_db():
    conn = sqlite3.connect('car_sales.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                 (vin TEXT PRIMARY KEY,
                  make TEXT,
                  model TEXT,
                  year INTEGER,
                  color TEXT,
                  mileage INTEGER,
                  price REAL,
                  status TEXT)''')
    conn.commit()
    conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("This code creates a file called <b>car_sales.db</b> to store data.", styles['BodyText']),
                Paragraph("The <b>cars</b> table holds details like VIN (unique car ID), make, and price.", styles['BodyText']),
                Paragraph("You’ll use this to save and retrieve cars, like adding a Toyota Camry to your lot.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("Example 2: Defining a Car", styles['BodyText']),
        Paragraph(
            "You’ll create a <b>Car</b> class to represent each car, like a blueprint for a vehicle. Here’s how it looks:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """class Car:
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status

    def save(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
        conn.commit()
        conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("The <b>Car</b> class stores details for one car, like a digital car file.", styles['BodyText']),
                Paragraph("The <b>save</b> method puts the car’s info into the database.", styles['BodyText']),
                Paragraph("You’ll use this to add cars like ‘VIN001, Toyota, Camry, 2020’ to your system.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("Example 3: Creating a Menu", styles['BodyText']),
        Paragraph(
            "Your system will have a text-based menu, like a game menu. Here’s a simple welcome screen:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses

def main_ui(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Car Sales System!")
    stdscr.addstr(2, 0, "Press any key to continue...")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("This code displays a welcome message in the terminal.", styles['BodyText']),
                Paragraph("Users press a key to continue, like starting a game.", styles['BodyText']),
                Paragraph("You’ll expand this into menus for viewing cars or adding customers.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: These snippets are like puzzle pieces. You’ll learn to build each one, and by the end, they’ll fit together into a complete system!",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.5 What You Need to Start
        Paragraph("1.5 What You Need to Start", styles['SectionHeading']),
        Paragraph(
            "You don’t need fancy equipment or prior knowledge to begin. Here’s a simple checklist to get ready:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        ListFlowable(
            [
                Paragraph("<b>Python 3</b>: A free program you download from <b>python.org</b>. It’s like the toolbox for your project.", styles['BodyText']),
                Paragraph("<b>A Computer</b>: Any computer with Windows, macOS, or Linux will work.", styles['BodyText']),
                Paragraph("<b>A Terminal</b>: A text window to run your code. Windows has Command Prompt or PowerShell; macOS and Linux have Terminal.", styles['BodyText']),
                Paragraph("<b>Curiosity</b>: No coding experience needed—just a willingness to learn!", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "To check if Python is installed, open your terminal and type:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 --version"),
        Paragraph(
            "If you see a version number (e.g., ‘Python 3.10.0’), you’re ready! If not, visit <b>python.org</b>, download Python 3, and follow the installation instructions. It’s as easy as installing a game!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If <b>python3 --version</b> doesn’t work, try <b>python --version</b>. If both fail, download Python from <b>python.org</b> and ensure it’s added to your system’s PATH (the installer has an option for this).",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.6 How to Approach This Book
        Paragraph("1.6 How to Approach This Book", styles['SectionHeading']),
        Paragraph(
            "This book is designed for absolute beginners, so we’ll take things slowly and clearly. Here’s how to make the most of it:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        ListFlowable(
            [
                Paragraph("<b>Follow Along</b>: Type the code examples as you read. It’s like practicing a recipe by cooking it yourself.", styles['BodyText']),
                Paragraph("<b>Make Mistakes</b>: Errors are part of learning. If code doesn’t work, we’ll show you how to fix it.", styles['BodyText']),
                Paragraph("<b>Read the Analogies</b>: We use examples like LEGO or car dealerships to make ideas clear.", styles['BodyText']),
                Paragraph("<b>Use the Troubleshooting Tips</b>: Each chapter has tips to solve common problems.", styles['BodyText']),
                Paragraph("<b>Have Fun</b>: Treat this like a game—each chapter unlocks a new feature for your system!", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "Each chapter builds on the previous one, starting with setting up your tools (Chapter 2) and ending with sharing your project (Chapter 15). By the end, you’ll have a complete car sales system and the confidence to code more projects!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Don’t worry if terms like ‘database’ or ‘API’ sound scary now. We’ll explain them like teaching a friend, and you’ll be using them like a pro!",
            styles['Callout']
        ),
        Spacer(1, 10),

        # 1.7 Key Takeaways
        Paragraph("1.7 Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("You’re building a car sales system with Python, a beginner-friendly language.", styles['KeyTakeaway']),
                Paragraph("The system includes real-world features like databases, APIs, and secure logins.", styles['KeyTakeaway']),
                Paragraph("You need Python 3, a computer, and a terminal—no prior coding experience required.", styles['KeyTakeaway']),
                Paragraph("This book guides you step-by-step with analogies and troubleshooting tips.", styles['KeyTakeaway']),
                Paragraph("You’ll see real code examples, like saving cars and creating menus, that bring your system to life.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 2
def chapter2():
    return [
        Paragraph("Chapter 2: Setting Up Your Coding Workspace", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter helps you set up your project folder, virtual environment, and tools. It’s like preparing a workbench for your car sales system.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("2.1 Creating Your Project Folder", styles['SectionHeading']),
        Paragraph(
            "Your project needs a dedicated folder. This keeps everything organized.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Open your terminal and type:", styles['BodyText']),
        create_code_block("mkdir car_sales_system\ncd car_sales_system"),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>mkdir car_sales_system</b>: Creates a folder.", styles['BodyText']),
                Paragraph("<b>cd car_sales_system</b>: Enters the folder.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: A clean folder is like a tidy desk for coding.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Type <b>ls</b> (or <b>dir</b> on Windows) to confirm the folder exists. Check spelling if it’s missing.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("2.2 Setting Up a Virtual Environment", styles['SectionHeading']),
        Paragraph(
            "A <b>virtual environment</b> isolates your project’s tools, avoiding conflicts.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 -m venv venv\nsource venv/bin/activate  # On Windows: venv\\Scripts\\activate"),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>python3 -m venv venv</b>: Creates a virtual environment.", styles['BodyText']),
                Paragraph("<b>source venv/bin/activate</b>: Activates it (shows ‘(venv)’).", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like a private toolbox for your project’s tools.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If activation fails, ensure Python 3 is installed (<b>python3 --version</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("2.3 Installing Libraries", styles['SectionHeading']),
        Paragraph(
            "Libraries are pre-built tools for your project. We need a few.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("pip install reportlab requests bcrypt pytest"),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>pip</b>: Installs libraries.", styles['BodyText']),
                Paragraph("<b>reportlab</b>: Creates PDFs.", styles['BodyText']),
                Paragraph("<b>requests</b>: Fetches internet data.", styles['BodyText']),
                Paragraph("<b>bcrypt</b>: Secures passwords.", styles['BodyText']),
                Paragraph("<b>pytest</b>: Tests code.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Libraries save time by providing ready-made features.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure ‘(venv)’ is active. Reactivate with <b>source venv/bin/activate</b> if needed.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("2.4 Testing Your Setup", styles['SectionHeading']),
        Paragraph(
            "Let’s confirm everything works with a simple test.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("print('Setup is working!')"),
        Paragraph("Save as <b>test_setup.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_setup.py"),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>print</b>: Displays text.", styles['BodyText']),
                Paragraph("Seeing ‘Setup is working!’ means you’re ready.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If nothing runs, check your folder (<b>pwd</b>) and virtual environment.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Organize with a project folder.", styles['KeyTakeaway']),
                Paragraph("Use a virtual environment for tools.", styles['KeyTakeaway']),
                Paragraph("Install libraries with pip.", styles['KeyTakeaway']),
                Paragraph("Test your setup.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 3
def chapter3():
    return [
        Paragraph("Chapter 3: Building Your Data Storage (Database)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter teaches you to create a <b>database</b> using <b>SQLite</b> to store cars, customers, and sales data. You’ll learn what databases are and how to set them up.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("3.1 What’s a Database?", styles['SectionHeading']),
        Paragraph(
            "A <b>database</b> is a digital filing cabinet for organized data. <b>SQLite</b> is a simple database stored in a file, perfect for this project.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Think of a database as a super-organized notebook that never loses data.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Databases ensure your system remembers everything reliably.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("3.2 Designing the Database", styles['SectionHeading']),
        Paragraph(
            "Databases use <b>tables</b> (like spreadsheets) with <b>columns</b> (headings) and <b>rows</b> (entries). We’ll create tables for cars, customers, sales, users, and favorites.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import sqlite3

def init_db():
    conn = sqlite3.connect('car_sales.db')
    c = conn.cursor()
    
    # Cars table
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                 (vin TEXT PRIMARY KEY,
                  make TEXT,
                  model TEXT,
                  year INTEGER,
                  color TEXT,
                  mileage INTEGER,
                  price REAL,
                  status TEXT)''')
    
    # Customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  contact TEXT)''')
    
    # Sales table
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  customer_id INTEGER,
                  vin TEXT,
                  sale_date TEXT,
                  sale_price REAL,
                  payment_method TEXT,
                  FOREIGN KEY(customer_id) REFERENCES customers(id),
                  FOREIGN KEY(vin) REFERENCES cars(vin))''')
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT)''')
    
    # Favorites table
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  vin TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id),
                  FOREIGN KEY(vin) REFERENCES cars(vin))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('car_sales.db')"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>import sqlite3</b>: Imports the database tool.", styles['BodyText']),
                Paragraph("2. <b>conn = sqlite3.connect(...)</b>: Creates a database file.", styles['BodyText']),
                Paragraph("3. <b>c.execute(...)</b>: Defines tables and columns.", styles['BodyText']),
                Paragraph("4. <b>PRIMARY KEY</b>: Ensures unique entries.", styles['BodyText']),
                Paragraph("5. <b>FOREIGN KEY</b>: Links tables (e.g., sales to cars).", styles['BodyText']),
                Paragraph("6. <b>conn.commit()</b>: Saves changes.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Tables are like spreadsheets. Each car is a row, with columns for details like price.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("3.3 Starting the Database", styles['SectionHeading']),
        Paragraph(
            "Create a <b>main.py</b> file to initialize the database.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("from database import init_db\n\ninit_db()"),
        Paragraph("Run it:", styles['BodyText']),
        create_code_block("python3 main.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If errors occur, check <b>database.py</b> for typos or ensure you’re in the project folder (<b>pwd</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("3.4 Testing the Database", styles['SectionHeading']),
        Paragraph(
            "Verify the tables were created.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("import sqlite3\n\nconn = sqlite3.connect('car_sales.db')\nc = conn.cursor()\nc.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')\ntables = c.fetchall()\nprint(tables)\nconn.close()"),
        Paragraph("Save as <b>test_database.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_database.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If tables are missing, re-run <b>python3 main.py</b>.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Databases organize data in tables.", styles['KeyTakeaway']),
                Paragraph("<b>SQLite</b> is simple and file-based.", styles['KeyTakeaway']),
                Paragraph("Test your database setup.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 4
def chapter4():
    return [
        Paragraph("Chapter 4: Creating Your First Class (The Car)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter introduces <b>classes</b> by building a <b>Car</b> class to represent cars. You’ll learn how classes organize code.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("4.1 What is a Class?", styles['SectionHeading']),
        Paragraph(
            "A <b>class</b> is a blueprint for objects. The <b>Car</b> class defines car attributes like VIN or price. Each car you create is an <b>object</b>.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: A class is like a cookie cutter. Each cookie (object) has the same shape but different flavors (details).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Classes keep code organized, reusing the same blueprint for all cars.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("4.2 Building the Car Class", styles['SectionHeading']),
        Paragraph("Step 1: Start the Class", styles['BodyText']),
        create_code_block("class Car:\n    pass"),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>class Car:</b> Defines the blueprint.", styles['BodyText']),
                Paragraph("<b>pass</b>: Placeholder for code.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("Step 2: Add Attributes", styles['BodyText']),
        create_code_block("""class Car:
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>def __init__(...):</b> Initializes car attributes.", styles['BodyText']),
                Paragraph("2. <b>self</b>: Refers to the car object.", styles['BodyText']),
                Paragraph("3. <b>self.vin = vin</b>: Stores the VIN.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: <b>__init__</b> is like filling out a car’s registration form. <b>self</b> is the car holding the details.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Step 3: Connect to the Database", styles['SectionHeading']),
        Paragraph(
            "Add methods to save and load cars in <b>models.py</b>.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from database import get_db_connection

class Car:
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
        conn.commit()
        conn.close()
    
    @staticmethod
    def load_all():
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM cars")
        rows = c.fetchall()
        conn.close()
        return [Car(*row) for row in rows]"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>save(self):</b> Saves the car to the database.", styles['BodyText']),
                Paragraph("2. <b>load_all()</b>: Retrieves all cars.", styles['BodyText']),
                Paragraph("3. <b>@staticmethod</b>: No <b>self</b> needed for <b>load_all</b>.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If saving fails, ensure the <b>cars</b> table exists (<b>python3 main.py</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("4.3 Testing the Car Class", styles['SectionHeading']),
        Paragraph(
            "Test saving and loading a car.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("from models import Car\n\ncar = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')\ncar.save()\ncars = Car.load_all()\nassert len(cars) == 1\nassert cars[0].vin == 'VIN001'\nprint('Car test passed!')"),
        Paragraph("Save as <b>test_car.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_car.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If tests fail, check <b>models.py</b> and <b>database.py</b>.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("<b>Classes</b> are blueprints for objects.", styles['KeyTakeaway']),
                Paragraph("The <b>Car</b> class manages car data.", styles['KeyTakeaway']),
                Paragraph("Test classes to ensure they work.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 5
def chapter5():
    return [
        Paragraph("Chapter 5: More Classes (Customer and User)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter builds <b>Customer</b> and <b>User</b> classes for buyers and logins. You’ll learn to create classes for different purposes.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("5.1 The Customer Class", styles['SectionHeading']),
        Paragraph(
            "The <b>Customer</b> class stores buyer details like name and contact info.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from database import get_db_connection

class Customer:
    def __init__(self, id, name, contact):
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        conn = get_db_connection()
        c = conn.cursor()
        if self.id is None:
            c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
            self.id = c.lastrowid
        else:
            c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def load_all():
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM customers")
        rows = c.fetchall()
        conn.close()
        return [Customer(*row) for row in rows]"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>__init__</b>: Sets customer details.", styles['BodyText']),
                Paragraph("2. <b>save</b>: Adds or updates a customer.", styles['BodyText']),
                Paragraph("3. <b>load_all</b>: Retrieves all customers.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The <b>Customer</b> class is like a contact card for buyers, stored digitally.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("5.2 The User Class", styles['SectionHeading']),
        Paragraph(
            "The <b>User</b> class handles secure logins with usernames and passwords.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import bcrypt
from database import get_db_connection

class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        conn = get_db_connection()
        c = conn.cursor()
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        if self.id is None:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (self.username, hashed, self.role))
            self.id = c.lastrowid
        else:
            c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (self.username, hashed, self.role, self.id))
        conn.commit()
        conn.close()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>bcrypt</b>: Hashes passwords for security.", styles['BodyText']),
                Paragraph("2. <b>save</b>: Saves a user with a hashed password.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The <b>User</b> class is like a secure key card. <b>bcrypt</b> locks the password safely.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("5.3 Testing the Classes", styles['SectionHeading']),
        Paragraph(
            "Test both classes to ensure they save correctly.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("from models import Customer, User\n\ncustomer = Customer(None, 'John Doe', 'john@example.com')\ncustomer.save()\nuser = User(None, 'admin', 'adminpass', 'admin')\nuser.save()\nprint('Tests passed!')"),
        Paragraph("Save as <b>test_classes.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_classes.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>bcrypt</b> is installed (<b>pip install bcrypt</b>) and the database is initialized.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("<b>Customer</b> class tracks buyers.", styles['KeyTakeaway']),
                Paragraph("<b>User</b> class secures logins.", styles['KeyTakeaway']),
                Paragraph("Test classes for reliability.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 6
def chapter6():
    return [
        Paragraph("Chapter 6: Creating a Simple Terminal Interface", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter uses the <b>curses</b> library to build a text-based interface, starting with a welcome screen.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("6.1 What is a Terminal Interface?", styles['SectionHeading']),
        Paragraph(
            "A <b>terminal interface</b> is a text-based menu system where users press keys to choose options, like a simple video game.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like a restaurant menu in your terminal—press ‘1’ to pick an option!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: A terminal interface makes your system user-friendly without needing a graphical app.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("6.2 Building a Welcome Screen", styles['SectionHeading']),
        Paragraph(
            "Create <b>ui.py</b> to display a welcome message.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import curses

def main_ui(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Car Sales System!")
    stdscr.addstr(2, 0, "Press any key to continue...")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_ui)"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>curses.curs_set(0)</b>: Hides the cursor.", styles['BodyText']),
                Paragraph("2. <b>stdscr.addstr(...)</b>: Displays text.", styles['BodyText']),
                Paragraph("3. <b>stdscr.getch()</b>: Waits for a key press.", styles['BodyText']),
                Paragraph("4. <b>curses.wrapper</b>: Sets up the terminal.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If <b>curses</b> fails, install <b>ncurses</b> (<b>sudo apt-get install libncurses5-dev</b>) on Linux.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("6.3 Testing the Interface", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: See a welcome message and press any key to exit.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>ui.py</b> has no typos and you’re in the virtual environment.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Terminal interfaces are interactive.", styles['KeyTakeaway']),
                Paragraph("<b>curses</b> controls the terminal.", styles['KeyTakeaway']),
                Paragraph("Start with a welcome screen.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 7
def chapter7():
    return [
        Paragraph("Chapter 7: Building Advanced Menus", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds interactive menus for admins and customers, making the system easier to navigate.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("7.1 Why Add Menus?", styles['SectionHeading']),
        Paragraph(
            "Menus let users pick options (e.g., ‘View Cars’) without typing complex commands, improving usability.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Menus are like a game controller—press a number to act!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Good menus make your system intuitive for users.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("7.2 Creating Menus", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to add admin and customer menus.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import curses
from models import Car

def admin_menu(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Admin Menu")
        stdscr.addstr(2, 0, "1. View All Cars")
        stdscr.addstr(3, 0, "2. Add New Car")
        stdscr.addstr(4, 0, "3. Manage Customers")
        stdscr.addstr(5, 0, "4. Logout")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('1'):
            view_all_cars(stdscr)
        elif key == ord('4'):
            break

def customer_menu(stdscr, user_id):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Customer Menu")
        stdscr.addstr(2, 0, "1. View All Cars")
        stdscr.addstr(3, 0, "2. Search Cars")
        stdscr.addstr(4, 0, "3. Logout")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('1'):
            view_all_cars(stdscr)
        elif key == ord('3'):
            break

def view_all_cars(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "All Cars")
    cars = Car.load_all()
    for i, car in enumerate(cars):
        stdscr.addstr(i+1, 0, f"{car.vin}: {car.make} {car.model}")
    stdscr.addstr(len(cars)+1, 0, "Press any key to return")
    stdscr.getch()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>admin_menu</b>: Shows admin options.", styles['BodyText']),
                Paragraph("2. <b>customer_menu</b>: Shows customer options.", styles['BodyText']),
                Paragraph("3. <b>view_all_cars</b>: Lists all cars.", styles['BodyText']),
                Paragraph("4. <b>while True</b>: Keeps menus active until logout.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If menus don’t work, check <b>ui.py</b> imports and <b>Car</b> class.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("7.3 Testing Menus", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: Run the program, see the welcome screen, and test menu options (e.g., ‘1’ to view cars).",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Add cars via a test script if none appear.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Menus improve usability.", styles['KeyTakeaway']),
                Paragraph("Separate menus for admins and customers.", styles['KeyTakeaway']),
                Paragraph("Test menus thoroughly.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 8
def chapter8():
    return [
        Paragraph("Chapter 8: Adding Search Functionality", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds a search feature so customers can find cars by make, model, or other criteria.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("8.1 Why Search is Important", styles['SectionHeading']),
        Paragraph(
            "Search lets customers find specific cars, like typing ‘Toyota’ to see only Toyota models.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like searching a library for books by one author—fast and focused.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Search makes your system more user-friendly and efficient.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.2 Creating the Search Function", styles['SectionHeading']),
        Paragraph(
            "Create <b>search.py</b> to handle car searches.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from database import get_db_connection
from models import Car

def search_cars(make=None):
    conn = get_db_connection()
    c = conn.cursor()
    query = "SELECT * FROM cars WHERE 1=1"
    params = []
    if make:
        query += " AND make = ?"
        params.append(make)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [Car(*row) for row in rows]"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>search_cars</b>: Builds a dynamic query.", styles['BodyText']),
                Paragraph("2. <b>params</b>: Safely passes search criteria.", styles['BodyText']),
                Paragraph("3. <b>return</b>: Converts rows to <b>Car</b> objects.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: This is like asking a clerk to find all Toyota cars in the lot.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.3 Adding Search to the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to include a search option.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from search import search_cars

def search_cars_ui(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Search Cars")
    stdscr.addstr(1, 0, "Enter make (or leave blank):")
    make = stdscr.getstr(2, 0).decode()
    results = search_cars(make=make if make else None)
    stdscr.addstr(4, 0, "Search Results:")
    for i, car in enumerate(results):
        stdscr.addstr(5+i, 0, f"{car.vin}: {car.make} {car.model}")
    stdscr.addstr(5+len(results), 0, "Press any key to return")
    stdscr.getch()

# In customer_menu, add:
# if key == ord('2'):
#     search_cars_ui(stdscr)"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>search_cars_ui</b>: Prompts for a make and shows results.", styles['BodyText']),
                Paragraph("2. Integrated into the customer menu.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If search fails, check <b>search.py</b> and ensure cars exist.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.4 Testing Search", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: In the customer menu, press ‘2,’ search for ‘Toyota,’ and see Toyota cars.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Add cars via the admin menu if none appear.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Search enhances usability.", styles['KeyTakeaway']),
                Paragraph("Safe queries prevent errors.", styles['KeyTakeaway']),
                Paragraph("Test search functionality.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 9
def chapter9():
    return [
        Paragraph("Chapter 9: Managing Customers", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds features for admins to view and add customers, enhancing system management.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("9.1 Why Manage Customers?", styles['SectionHeading']),
        Paragraph(
            "Admins need to track customers to manage sales, like keeping a guest list for your shop. This ensures smooth transactions.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s a digital notebook for customer details, easy to update and search.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Customer management is key for sales tracking and relationships.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("9.2 Adding Customer Management", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to include customer management options.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from models import Customer

def manage_customers_ui(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Manage Customers")
        stdscr.addstr(2, 0, "1. View All Customers")
        stdscr.addstr(3, 0, "2. Add New Customer")
        stdscr.addstr(4, 0, "3. Back")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('1'):
            view_customers(stdscr)
        elif key == ord('2'):
            add_customer_ui(stdscr)
        elif key == ord('3'):
            break

def view_customers(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "All Customers")
    customers = Customer.load_all()
    for i, customer in enumerate(customers):
        stdscr.addstr(i+1, 0, f"{customer.id}: {customer.name} - {customer.contact}")
    stdscr.addstr(len(customers)+1, 0, "Press any key to return")
    stdscr.getch()

def add_customer_ui(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Add New Customer")
    stdscr.addstr(1, 0, "Enter Name:")
    name = stdscr.getstr(2, 0).decode()
    stdscr.addstr(3, 0, "Enter Contact:")
    contact = stdscr.getstr(4, 0).decode()
    new_customer = Customer(None, name, contact)
    new_customer.save()
    stdscr.addstr(5, 0, "Customer added successfully.")
    stdscr.getch()

# In admin_menu, add:
# if key == ord('3'):
#     manage_customers_ui(stdscr)"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>manage_customers_ui</b>: Creates a customer menu.", styles['BodyText']),
                Paragraph("2. <b>view_customers</b>: Lists all customers.", styles['BodyText']),
                Paragraph("3. <b>add_customer_ui</b>: Adds a new customer.", styles['BodyText']),
                Paragraph("4. Integrated into admin menu.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If customers don’t save, ensure the <b>customers</b> table exists (<b>python3 main.py</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("9.3 Testing Customer Management", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: In the admin menu, press ‘3,’ then ‘2’ to add a customer, and ‘1’ to see the list.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Check <b>ui.py</b> and <b>models.py</b> for errors.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Customer management tracks buyers.", styles['KeyTakeaway']),
                Paragraph("Menus simplify admin tasks.", styles['KeyTakeaway']),
                Paragraph("Test to ensure functionality.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 10
def chapter10():
    return [
        Paragraph("Chapter 10: Connecting to the Internet (APIs)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter introduces <b>APIs</b> to fetch car details, enhancing your system with external data.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("10.1 What’s an API?", styles['SectionHeading']),
        Paragraph(
            "An <b>API</b> (Application Programming Interface) is like a messenger fetching data from another system, such as car specs online.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like asking a librarian to grab car info for you!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: APIs make your system dynamic and informative.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.2 Creating an API Function", styles['SectionHeading']),
        Paragraph(
            "Create <b>api.py</b> with a placeholder API function.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import requests

def get_car_details(make, model, year):
    # Placeholder: Use a real API like Edmunds
    return {'engine_type': 'V6', 'transmission': 'Automatic'}"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>requests</b>: Fetches internet data.", styles['BodyText']),
                Paragraph("2. <b>get_car_details</b>: Returns fake data for testing.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Install <b>requests</b> (<b>pip install requests</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.3 Adding API to the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to show API data when adding cars.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from api import get_car_details

def add_new_car_ui(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Add New Car")
    stdscr.addstr(1, 0, "Enter VIN:")
    vin = stdscr.getstr(2, 0).decode()
    stdscr.addstr(3, 0, "Enter Make:")
    make = stdscr.getstr(4, 0).decode()
    stdscr.addstr(5, 0, "Enter Model:")
    model = stdscr.getstr(6, 0).decode()
    stdscr.addstr(7, 0, "Enter Year:")
    year = int(stdscr.getstr(8, 0).decode())
    stdscr.addstr(9, 0, "Enter Color:")
    color = stdscr.getstr(10, 0).decode()
    stdscr.addstr(11, 0, "Enter Mileage:")
    mileage = int(stdscr.getstr(12, 0).decode())
    stdscr.addstr(13, 0, "Enter Price:")
    price = float(stdscr.getstr(14, 0).decode())
    stdscr.addstr(15, 0, "Enter Status:")
    status = stdscr.getstr(16, 0).decode()
    new_car = Car(vin, make, model, year, color, mileage, price, status)
    new_car.save()
    details = get_car_details(make, model, year)
    stdscr.addstr(17, 0, f"Engine: {details['engine_type']}, Transmission: {details['transmission']}")
    stdscr.addstr(18, 0, "Car added. Press any key.")
    stdscr.getch()

# In admin_menu, add:
# if key == ord('2'):
#     add_new_car_ui(stdscr)"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>get_car_details</b>: Fetches API data.", styles['BodyText']),
                Paragraph("2. <b>add_new_car_ui</b>: Saves car and shows details.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If API data fails, check <b>api.py</b> imports.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.4 Testing the API", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: Add a car (admin menu, ‘2’) and see fake API data (e.g., ‘Engine: V6’).",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>Car</b> class and database are set up.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("APIs add external data.", styles['KeyTakeaway']),
                Paragraph("Placeholders help test.", styles['KeyTakeaway']),
                Paragraph("Test API integration.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 11
def chapter11():
    return [
        Paragraph("Chapter 11: More API Fun (Market Value)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds market value data to show fair car prices, using another API function to enhance transparency.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("11.1 Why Market Value Matters", styles['SectionHeading']),
        Paragraph(
            "Market value shows if a car’s price is competitive, like checking similar cars online. It builds trust with customers by ensuring fair pricing.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like looking up a car’s worth on a website to ensure you’re not overpaying.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Transparency through market value helps customers make informed decisions.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("11.2 Updating api.py", styles['SectionHeading']),
        Paragraph(
            "Add a placeholder function to <b>api.py</b> to fetch market values.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""def get_market_value(vin):
    # Placeholder: Use a real API like CarsXE (carsxe.com)
    return 20000"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>get_market_value</b>: Returns a fake market value ($20,000) for testing.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>api.py</b> is in your project folder and imported correctly.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("11.3 Showing Market Value in the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>view_all_cars</b> in <b>ui.py</b> to display market value next to each car’s price.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from api import get_market_value

def view_all_cars(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "All Cars")
    cars = Car.load_all()
    for i, car in enumerate(cars):
        market_value = get_market_value(car.vin)
        stdscr.addstr(i+1, 0, f"{car.vin}: {car.make} {car.model} - ${car.price} (Market: ${market_value})")
    stdscr.addstr(len(cars)+1, 0, "Press any key to return")
    stdscr.getch()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>from api import get_market_value</b>: Imports the market value function.", styles['BodyText']),
                Paragraph("2. <b>market_value = get_market_value(...)</b>: Fetches the value for each car.", styles['BodyText']),
                Paragraph("3. Displays price and market value together for clarity.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If market values don’t appear, check <b>ui.py</b> imports and ensure cars exist in the database.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("11.4 Testing Market Value", styles['SectionHeading']),
        Paragraph(
            "Test the updated <b>view_all_cars</b> function.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: In the admin or customer menu, press ‘1’ to view cars and see prices with market values (e.g., ‘Market: $20000’).",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Add test cars via the admin menu if none appear.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Market value enhances pricing transparency.", styles['KeyTakeaway']),
                Paragraph("APIs integrate external data seamlessly.", styles['KeyTakeaway']),
                Paragraph("Test UI changes to ensure functionality.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 12
def chapter12():
    return [
        Paragraph("Chapter 12: Adding Smart Features (AI)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter introduces a basic AI feature to recommend cars based on user searches, making the system smarter.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("12.1 What’s AI in This Context?", styles['SectionHeading']),
        Paragraph(
            "Here, <b>AI</b> means simple logic to suggest cars, like recommending similar models based on a customer’s search. It mimics intelligent behavior.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like a shop assistant saying, ‘You like Toyota? Check out these other Toyotas!’",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Recommendations improve user experience by suggesting relevant cars.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("12.2 Adding Recommendations", styles['SectionHeading']),
        Paragraph(
            "Update <b>search.py</b> to include a recommendation function.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""def recommend_cars(make):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM cars WHERE make = ? AND status = 'Available'", (make,))
    rows = c.fetchall()
    conn.close()
    return [Car(*row) for row in rows]"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>recommend_cars</b>: Finds available cars of the same make.", styles['BodyText']),
                Paragraph("2. Returns a list of <b>Car</b> objects.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("12.3 Showing Recommendations", styles['SectionHeading']),
        Paragraph(
            "Update <b>search_cars_ui</b> in <b>ui.py</b> to show recommendations.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from search import recommend_cars

def search_cars_ui(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Search Cars")
    stdscr.addstr(1, 0, "Enter make (or leave blank):")
    make = stdscr.getstr(2, 0).decode()
    results = search_cars(make=make if make else None)
    stdscr.addstr(4, 0, "Search Results:")
    for i, car in enumerate(results):
        stdscr.addstr(5+i, 0, f"{car.vin}: {car.make} {car.model}")
    if make:
        recommendations = recommend_cars(make)
        stdscr.addstr(6+len(results), 0, "Recommended Cars:")
        for i, car in enumerate(recommendations):
            stdscr.addstr(7+len(results)+i, 0, f"{car.vin}: {car.make} {car.model}")
    stdscr.addstr(8+len(results)+len(recommendations), 0, "Press any key to return")
    stdscr.getch()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. Imports <b>recommend_cars</b>.", styles['BodyText']),
                Paragraph("2. Shows recommendations if a make is searched.", styles['BodyText']),
                Paragraph("3. Displays recommendations below search results.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If recommendations don’t appear, ensure cars with the searched make exist.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("12.4 Testing Recommendations", styles['SectionHeading']),
        Paragraph(
            "Test the search with recommendations.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: In the customer menu, press ‘2,’ search for ‘Toyota,’ and see search results plus recommended Toyota cars.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Add Toyota cars via the admin menu if none appear.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Simple AI improves user experience.", styles['KeyTakeaway']),
                Paragraph("Recommendations use database queries.", styles['KeyTakeaway']),
                Paragraph("Test features for accuracy.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 13
def chapter13():
    return [
        Paragraph("Chapter 13: Locking Down Your System (Security)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds a secure login system to protect your system, using <b>bcrypt</b> for password hashing.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("13.1 Why Security Matters", styles['SectionHeading']),
        Paragraph(
            "A login system ensures only authorized users access the system, protecting sensitive data like customer info or car prices.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: It’s like a key card that only lets the right people into a secure building.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Security prevents unauthorized access and builds trust.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("13.2 Creating the Login System", styles['SectionHeading']),
        Paragraph(
            "Create <b>auth.py</b> to handle logins.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import bcrypt
from database import get_db_connection

def create_user(username, password, role='customer'):
    conn = get_db_connection()
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
        return user[0], user[2]
    return None, None"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>create_user</b>: Saves a user with a hashed password.", styles['BodyText']),
                Paragraph("2. <b>login</b>: Verifies username and password, returns user ID and role.", styles['BodyText']),
                Paragraph("3. <b>bcrypt</b>: Secures passwords.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("13.3 Adding Default Users", styles['SectionHeading']),
        Paragraph(
            "Update <b>init_db</b> in <b>database.py</b> to add default users for testing.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from auth import create_user

def init_db():
    # Existing table creation code...
    conn = sqlite3.connect('car_sales.db')
    conn.close()
    create_user('admin', 'adminpass', 'admin')
    create_user('customer1', 'custpass')"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("Adds an admin and a customer user.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("13.4 Requiring Login", styles['SectionHeading']),
        Paragraph(
            "Update <b>main_ui</b> in <b>ui.py</b> to require login.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""from auth import login

def main_ui(stdscr):
    curses.curs_set(0)
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Car Sales System - Login")
        stdscr.addstr(2, 0, "Username:")
        username = stdscr.getstr(3, 0).decode()
        stdscr.addstr(4, 0, "Password:")
        password = stdscr.getstr(5, 0).decode()
        user_id, role = login(username, password)
        if user_id:
            if role == 'admin':
                admin_menu(stdscr)
            else:
                customer_menu(stdscr, user_id)
            break
        else:
            stdscr.addstr(6, 0, "Login failed. Press any key.")
            stdscr.getch()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. Prompts for username and password.", styles['BodyText']),
                Paragraph("2. Directs to admin or customer menu based on role.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If login fails, ensure the <b>users</b> table exists and default users are added.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("13.5 Testing Login", styles['SectionHeading']),
        Paragraph(
            "Test with default credentials.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: Log in with ‘admin’/‘adminpass’ for admin menu or ‘customer1’/‘custpass’ for customer menu.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Re-run <b>init_db</b> if users are missing.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Secure logins protect the system.", styles['KeyTakeaway']),
                Paragraph("<b>bcrypt</b> ensures safe passwords.", styles['KeyTakeaway']),
                Paragraph("Test logins with default users.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 14
def chapter14():
    return [
        Paragraph("Chapter 14: Making Your System Fast and Reliable", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter optimizes the system with database indexes and adds <b>pytest</b> tests for reliability.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("14.1 Speeding Up Searches", styles['SectionHeading']),
        Paragraph(
            "Adding an <b>index</b> to the database makes searches faster, like adding a table of contents to a book.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: An index is like a shortcut that helps the database find data quickly.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Faster searches improve user experience.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("14.2 Adding an Index", styles['SectionHeading']),
        Paragraph(
            "Update <b>init_db</b> in <b>database.py</b> to add an index on the <b>make</b> column.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""def init_db():
    conn = sqlite3.connect('car_sales.db')
    c = conn.cursor()
    # Existing table creation...
    c.execute("CREATE INDEX IF NOT EXISTS idx_make ON cars(make)")
    conn.commit()
    conn.close()"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>CREATE INDEX</b>: Speeds up searches by <b>make</b>.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("14.3 Writing Tests", styles['SectionHeading']),
        Paragraph(
            "Create <b>test_models.py</b> to test the <b>Car</b> and <b>Customer</b> classes.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("""import pytest
from models import Car, Customer
from database import init_db

@pytest.fixture
def setup_db():
    init_db()

def test_car(setup_db):
    car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
    car.save()
    cars = Car.load_all()
    assert len(cars) == 1
    assert cars[0].vin == 'VIN001'

def test_customer(setup_db):
    customer = Customer(None, 'John Doe', 'john@example.com')
    customer.save()
    customers = Customer.load_all()
    assert len(customers) == 1
    assert customers[0].name == 'John Doe'"""),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("1. <b>pytest.fixture</b>: Sets up the database.", styles['BodyText']),
                Paragraph("2. Tests saving and loading cars and customers.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("14.4 Running Tests", styles['SectionHeading']),
        create_code_block("pytest test_models.py"),
        Paragraph(
            "<b>What Should Happen</b>: Tests pass, confirming classes work correctly.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Install <b>pytest</b> (<b>pip install pytest</b>) if not found.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("14.5 Testing the System", styles['SectionHeading']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>What Should Happen</b>: Log in, test menus, searches, and recommendations to ensure everything works smoothly.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Check logs in <b>pdf_generation.log</b> for errors.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Indexes improve database performance.", styles['KeyTakeaway']),
                Paragraph("<b>pytest</b> ensures reliability.", styles['KeyTakeaway']),
                Paragraph("Test the entire system.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 15
def chapter15():
    return [
        Paragraph("Chapter 15: Sharing Your Awesome System", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter shows how to share your car sales system with others and explores ideas for future enhancements, celebrating your achievement.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("15.1 Why Share Your Project?", styles['SectionHeading']),
        Paragraph(
            "Sharing your system allows others to use or learn from it, like passing on a well-crafted recipe. It’s a way to showcase your skills and contribute to the community.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Think of it as giving someone a LEGO kit with clear instructions to build the same model you did.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: Sharing spreads knowledge and opens opportunities for collaboration or feedback.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("15.2 Deployment Steps", styles['SectionHeading']),
        Paragraph(
            "To share your system, include a <b>README.md</b> file with setup instructions. This file guides others to run your project.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(textwrap.dedent(r"""# Car Sales System

## Setup Instructions
1. Install Python 3 from python.org.
2. Clone or download the project folder.
3. Open a terminal in the project folder.
4. Create a virtual environment:
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
5. Install required libraries:
    pip install reportlab requests bcrypt pytest
6. Run the system:
    python3 ui.py

## Usage
- Log in with default credentials:
  - Admin: username=admin, password=adminpass
  - Customer: username=customer1, password=custpass
- Use the menus to manage cars, customers, or search inventory.""").strip()),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("The <b>README.md</b> provides step-by-step instructions for setup and usage.", styles['BodyText']),
                Paragraph("Includes default login credentials for immediate access.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure recipients have Python 3 installed and follow the <b>README</b> exactly. Check the virtual environment is activated.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("15.3 Ideas for Future Enhancements", styles['SectionHeading']),
        Paragraph(
            "Your system is complete, but there’s room to grow! Here are some ideas to take it further:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        ListFlowable(
            [
                Paragraph("Build a <b>web app</b> using Flask or Django for online access.", styles['BodyText']),
                Paragraph("Develop a <b>mobile app</b> for customers on the go.", styles['BodyText']),
                Paragraph("Integrate advanced <b>AI</b> for price predictions or customer preferences.", styles['BodyText']),
                Paragraph("Connect to a real car data <b>API</b> for live market values.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: These ideas are like adding new features to your LEGO model, making it even cooler!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("15.4 Congratulations on Your Achievement!", styles['SectionHeading']),
        Paragraph(
            "You’ve built a fully functional car sales system from scratch! You’ve mastered databases, classes, APIs, AI, and security. Take a moment to celebrate your hard work!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: These skills are used in real-world programming jobs, and you’ve proven you can do it!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Share your project with clear, concise instructions.", styles['KeyTakeaway']),
                Paragraph("Consider future enhancements to keep growing.", styles['KeyTakeaway']),
                Paragraph("Be proud of your programming journey!", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Combine all elements into a single list
elements = []
elements.extend(cover_page())
elements.extend(preface())
elements.extend(table_of_contents())
elements.extend(chapter1())
elements.extend(chapter2())
elements.extend(chapter3())
elements.extend(chapter4())
elements.extend(chapter5())
elements.extend(chapter6())
elements.extend(chapter7())
elements.extend(chapter8())
elements.extend(chapter9())
elements.extend(chapter10())
elements.extend(chapter11())
elements.extend(chapter12())
elements.extend(chapter13())
elements.extend(chapter14())
elements.extend(chapter15())

# Build the PDF
try:
    doc.build(elements)
    print("PDF generated successfully!")
except Exception as e:
    logging.error(f"Failed to generate PDF: {str(e)}")
    print(f"Error: {str(e)}")