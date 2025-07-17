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
import sqlite3

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

# Add custom styles
styles.add(ParagraphStyle(
    name='Subtitle',
    parent=styles['Title'],
    fontSize=14,
    leading=16,
    alignment=TA_CENTER,
    spaceAfter=12,
))

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
    """Add header and footer to each page.

    Args:
        canvas: The ReportLab canvas object.
        doc: The SimpleDocTemplate object.
    """
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
    """Create a styled code block for the PDF.

    Args:
        code (str): The code snippet to display.

    Returns:
        KeepTogether: A styled table containing the code block.
    """
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
    """Generate the cover page for the PDF.

    Returns:
        list: List of ReportLab flowables for the cover page.
    """
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
    """Generate the preface for the PDF.

    Returns:
        list: List of ReportLab flowables for the preface.
    """
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
    """Generate the table of contents for the PDF.

    Returns:
        list: List of ReportLab flowables for the table of contents.
    """
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
    """Generate content for Chapter 1: Your First Step into the Car Sales Adventure.

    Returns:
        list: List of ReportLab flowables for Chapter 1.
    """
    global chapter_number
    chapter_number = 1
    return [
        Paragraph("Chapter 1: Your First Step into the Car Sales Adventure", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: Welcome to your programming journey! This chapter introduces you to the car sales system you’ll build using Python. We’ll explain what the system does, why it’s exciting, and what you need to get started. Whether you’ve never written code or are brushing up, this chapter will spark your enthusiasm for creating a real-world project!",
            styles['IntroText']
        ),
        Spacer(1, 12),
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
    \"\"\"Initialize the SQLite database with required tables.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
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
    \"\"\"Represents a car with attributes and database operations.\"\"\"
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
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
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
    \"\"\"Display the main user interface with a welcome screen.\"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to Car Sales System!")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.getch()
    except curses.error as e:
        logging.error(f"UI rendering failed: {str(e)}")

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
    """Generate content for Chapter 2: Setting Up Your Coding Workspace.

    Returns:
        list: List of ReportLab flowables for Chapter 2.
    """
    global chapter_number
    chapter_number = 2
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
        create_code_block(
            """def test_setup():
    \"\"\"Test if the Python environment is set up correctly.\"\"\"
    print('Setup is working!')
"""
        ),
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
        Paragraph("2.5 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created so far, so you can verify your setup:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_setup.py</b>", styles['BodyText']),
        create_code_block(
            """def test_setup():
    \"\"\"Test if the Python environment is set up correctly.\"\"\"
    print('Setup is working!')
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 test_setup.py</b> to confirm your setup works.", styles['BodyText']),
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
    """Generate content for Chapter 3: Building Your Data Storage (Database).

    Returns:
        list: List of ReportLab flowables for Chapter 3.
    """
    global chapter_number
    chapter_number = 3
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
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.\"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
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
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
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
        create_code_block(
            """import sqlite3

def test_database():
    \"\"\"Test if database tables were created successfully.\"\"\"
    try:
        conn = sqlite3.connect('car_sales.db')
        c = conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = c.fetchall()
        print(tables)
    except sqlite3.Error as e:
        logging.error(f"Database test failed: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_database()
"""
        ),
        Paragraph("Save as <b>test_database.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_database.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If tables are missing, re-run <b>python3 main.py</b>.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("3.5 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far, so you can verify your setup:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.\"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def test_database():
    \"\"\"Test if database tables were created successfully.\"\"\"
    try:
        conn = sqlite3.connect('car_sales.db')
        c = conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = c.fetchall()
        print(tables)
    except sqlite3.Error as e:
        logging.error(f"Database test failed: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_database()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 main.py</b> to initialize the database, then <b>python3 test_database.py</b> to verify.", styles['BodyText']),
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
    """Generate content for Chapter 4: Creating Your First Class (The Car).

    Returns:
        list: List of ReportLab flowables for Chapter 4.
    """
    global chapter_number
    chapter_number = 4
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
        create_code_block(
            """class Car:
    \"\"\"Blueprint for car objects.\"\"\"
    pass
"""
        ),
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
        create_code_block(
            """class Car:
    \"\"\"Blueprint for car objects with attributes.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.\"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
"""
        ),
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
        create_code_block(
            """from database import get_db_connection

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.\"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
"""
        ),
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
        create_code_block(
            """from models import Car

def test_car():
    \"\"\"Test saving and loading a car.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        cars = Car.load_all()
        assert len(cars) == 1
        assert cars[0].vin == 'VIN001'
        print('Car test passed!')
    except Exception as e:
        logging.error(f"Car test failed: {str(e)}")
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_car()
"""
        ),
        Paragraph("Save as <b>test_car.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_car.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If tests fail, check <b>models.py</b> and <b>database.py</b>.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("4.4 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.\"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.\"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_car.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car

def test_car():
    \"\"\"Test saving and loading a car.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        cars = Car.load_all()
        assert len(cars) == 1
        assert cars[0].vin == 'VIN001'
        print('Car test passed!')
    except Exception as e:
        logging.error(f"Car test failed: {str(e)}")
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_car()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 main.py</b> to initialize the database, then <b>python3 test_car.py</b> to verify.", styles['BodyText']),
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
    """Generate content for Chapter 5: More Classes (Customer and User).

    Returns:
        list: List of ReportLab flowables for Chapter 5.
    """
    global chapter_number
    chapter_number = 5
    return [
        Paragraph("Chapter 5: More Classes (Customer and User)", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter builds <b>Customer</b> and <b>User</b> classes for buyers and logins. You’ll learn to create classes for different purposes, including secure password handling.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("5.1 The Customer Class", styles['SectionHeading']),
        Paragraph(
            "The <b>Customer</b> class stores buyer details like name and contact info, enabling customer management in your system.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """from database import get_db_connection

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>__init__</b>: Sets customer attributes like name and contact.", styles['BodyText']),
                Paragraph("<b>save</b>: Adds or updates a customer in the database.", styles['BodyText']),
                Paragraph("<b>load_all</b>: Retrieves all customers as objects.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The <b>Customer</b> class is like a digital contact card for buyers, stored in your database.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("5.2 The User Class", styles['SectionHeading']),
        Paragraph(
            "The <b>User</b> class handles secure logins with usernames and hashed passwords using <b>bcrypt</b>.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import bcrypt
from database import get_db_connection

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>bcrypt.hashpw</b>: Secures the password by hashing it.", styles['BodyText']),
                Paragraph("<b>save</b>: Stores the user with the hashed password.", styles['BodyText']),
                Paragraph("<b>role</b>: Defines user type (e.g., admin or customer).", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The <b>User</b> class is like a secure key card. <b>bcrypt</b> locks the password so it’s safe.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("5.3 Testing the Classes", styles['SectionHeading']),
        Paragraph(
            "Test the <b>Customer</b> and <b>User</b> classes to ensure they save correctly.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """from models import Customer, User

def test_classes():
    \"\"\"Test saving Customer and User classes.\"\"\"
    try:
        customer = Customer(None, 'John Doe', 'john@example.com')
        customer.save()
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        customers = Customer.load_all()
        assert len(customers) >= 1
        print('Tests passed!')
    except Exception as e:
        logging.error(f"Classes test failed: {str(e)}")
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_classes()
"""
        ),
        Paragraph("Save as <b>test_classes.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_classes.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>bcrypt</b> is installed (<b>pip install bcrypt</b>) and the database is initialized (<b>python3 main.py</b>).",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("5.4 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far, so you can verify your setup:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_classes.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Customer, User

def test_classes():
    \"\"\"Test saving Customer and User classes.\"\"\"
    try:
        customer = Customer(None, 'John Doe', 'john@example.com')
        customer.save()
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        customers = Customer.load_all()
        assert len(customers) >= 1
        print('Tests passed!')
    except Exception as e:
        logging.error(f"Classes test failed: {str(e)}")
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_classes()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 main.py</b> to initialize the database, then <b>python3 test_classes.py</b> to verify.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("<b>Customer</b> class manages buyer info.", styles['KeyTakeaway']),
                Paragraph("<b>User</b> class handles secure logins with <b>bcrypt</b>.", styles['KeyTakeaway']),
                Paragraph("Test classes to confirm functionality.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 6
def chapter6():
    """Generate content for Chapter 6: Creating a Simple Terminal Interface.

    Returns:
        list: List of ReportLab flowables for Chapter 6.
    """
    global chapter_number
    chapter_number = 6
    return [
        Paragraph("Chapter 6: Creating a Simple Terminal Interface", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter introduces <b>curses</b> to create a text-based interface with a welcome screen, the foundation for your system’s menus.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("6.1 What is a Terminal Interface?", styles['SectionHeading']),
        Paragraph(
            "A <b>terminal interface</b> lets users interact with your program using text and keyboard inputs. We’ll use <b>curses</b>, a Python library for text-based displays.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Think of it as a text-based video game menu where you press keys to choose options.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Why This Matters</b>: A clear interface makes your system user-friendly, like a dashboard for your car lot.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("6.2 Creating the Welcome Screen", styles['SectionHeading']),
        Paragraph(
            "Create <b>ui.py</b> to display a welcome message using <b>curses</b>.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses

def main_ui(stdscr):
    \"\"\"Display the main user interface with a welcome screen.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to Car Sales System!")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()  # Wait for key press
    except curses.error as e:
        logging.error(f"UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>curses.curs_set(0)</b>: Hides the blinking cursor.", styles['BodyText']),
                Paragraph("<b>stdscr.addstr</b>: Displays text at specified positions.", styles['BodyText']),
                Paragraph("<b>stdscr.getch</b>: Waits for a key press.", styles['BodyText']),
                Paragraph("<b>curses.wrapper</b>: Sets up and tears down the curses environment.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The welcome screen is like the start menu of a game, inviting users to begin.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("6.3 Running the Interface", styles['SectionHeading']),
        Paragraph(
            "Save the code as <b>ui.py</b> and run it:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 ui.py"),
        Paragraph(
            "You should see a welcome message. Press any key to exit.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If <b>curses</b> fails, ensure you’re using a Unix-like terminal (e.g., macOS Terminal, Linux, or Windows Subsystem for Linux). Windows Command Prompt may not support <b>curses</b>.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("6.4 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses

def main_ui(stdscr):
    \"\"\"Display the main user interface with a welcome screen.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to Car Sales System!")
        stdscr.addstr(2, 0, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()  # Wait for key press
    except curses.error as e:
        logging.error(f"UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 ui.py</b> to see the welcome screen.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("<b>curses</b> creates text-based interfaces.", styles['KeyTakeaway']),
                Paragraph("The welcome screen is the start of your UI.", styles['KeyTakeaway']),
                Paragraph("Test in a compatible terminal.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 7
def chapter7():
    """Generate content for Chapter 7: Building Advanced Menus.

    Returns:
        list: List of ReportLab flowables for Chapter 7.
    """
    global chapter_number
    chapter_number = 7
    return [
        Paragraph("Chapter 7: Building Advanced Menus", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter expands the interface with interactive menus for admins and customers, allowing users to view cars and perform actions.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("7.1 Designing the Menus", styles['SectionHeading']),
        Paragraph(
            "Menus let users choose actions by pressing numbers. We’ll create an admin menu (add/remove cars) and a customer menu (view cars).",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Menus are like a restaurant menu—users pick options to interact with the system.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("7.2 Updating ui.py", styles['SectionHeading']),
        Paragraph(
            "Modify <b>ui.py</b> to include admin and customer menus, and a function to view all cars.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses
from models import Car

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with role selection.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Welcome to Car Sales System!")
            stdscr.addstr(2, 0, "1. Admin")
            stdscr.addstr(3, 0, "2. Customer")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                admin_menu(stdscr)
            elif key == ord('2'):
                customer_menu(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>main_ui</b>: Now offers role selection (admin or customer).", styles['BodyText']),
                Paragraph("<b>admin_menu</b>: Allows admins to view cars or exit.", styles['BodyText']),
                Paragraph("<b>customer_menu</b>: Lets customers view cars or exit.", styles['BodyText']),
                Paragraph("<b>view_all_cars</b>: Displays all cars from the database.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The menus are like a choose-your-own-adventure book, guiding users through options.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("7.3 Testing the Menus", styles['SectionHeading']),
        Paragraph(
            "Add a test car to the database to see it in the menu.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """from models import Car

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Paragraph("Save as <b>test_data.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_data.py"),
        Paragraph("Then run the interface:", styles['BodyText']),
        create_code_block("python3 ui.py"),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If no cars appear, ensure the database is initialized (<b>python3 main.py</b>) and the test car was added.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("7.4 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses
from models import Car

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with role selection.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Welcome to Car Sales System!")
            stdscr.addstr(2, 0, "1. Admin")
            stdscr.addstr(3, 0, "2. Customer")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                admin_menu(stdscr)
            elif key == ord('2'):
                customer_menu(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_data.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 test_data.py</b> to add a test car, then <b>python3 ui.py</b> to test the menus.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Menus make the system interactive.", styles['KeyTakeaway']),
                Paragraph("Admins and customers have tailored options.", styles['KeyTakeaway']),
                Paragraph("Test with sample data.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 8
def chapter8():
    """Generate content for Chapter 8: Adding Search Functionality.

    Returns:
        list: List of ReportLab flowables for Chapter 8.
    """
    global chapter_number
    chapter_number = 8
    return [
        Paragraph("Chapter 8: Adding Search Functionality", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds a search feature so users can find cars by make or model, integrating it into the customer menu.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("8.1 Why Add Search?", styles['SectionHeading']),
        Paragraph(
            "Search lets customers quickly find cars, like searching an online store. We’ll create a <b>search.py</b> file to handle queries safely.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Search is like using a library catalog to find a specific book by title.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.2 Creating the Search Function", styles['SectionHeading']),
        Paragraph(
            "Create <b>search.py</b> to search cars by make or model.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """from database import get_db_connection
from models import Car

def search_cars(search_term):
    \"\"\"Search cars by make or model.

    Args:
        search_term (str): Term to search for in make or model.

    Returns:
        list: List of matching Car objects.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        # Use parameterized query to prevent SQL injection
        c.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                 (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()
        return [Car(*row) for row in rows]
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Search failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>LIKE</b>: Matches partial text (e.g., ‘Toy’ finds ‘Toyota’).", styles['BodyText']),
                Paragraph("<b>%{search_term}%</b>: Allows partial matches.", styles['BodyText']),
                Paragraph("Parameterized query: Prevents SQL injection for security.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The search is like a magnifying glass finding cars that match your keyword.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.3 Integrating Search into the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to add a search option in the customer menu.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses
from models import Car
from search import search_cars

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)  # Show cursor
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:  # Enter key
                break
            elif key == 27:  # Escape key
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with role selection.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Welcome to Car Sales System!")
            stdscr.addstr(2, 0, "1. Admin")
            stdscr.addstr(3, 0, "2. Customer")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                admin_menu(stdscr)
            elif key == ord('2'):
                customer_menu(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>search_cars_ui</b>: Prompts for a search term and displays results.", styles['BodyText']),
                Paragraph("Handles keyboard input (Enter, Backspace, Escape).", styles['BodyText']),
                Paragraph("Customer menu now includes a search option.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("8.4 Testing the Search", styles['SectionHeading']),
        Paragraph(
            "Ensure a test car exists, then run the UI to test search.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 test_data.py\npython3 ui.py"),
        Paragraph(
            "Select ‘Customer’, then ‘Search cars’, and type ‘Toyota’ to find the test car.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If search fails, check <b>search.py</b> and ensure the database has cars.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("8.5 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: search.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
from models import Car

def search_cars(search_term):
    \"\"\"Search cars by make or model.

    Args:
        search_term (str): Term to search for in make or model.

    Returns:
        list: List of matching Car objects.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                 (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()
        return [Car(*row) for row in rows]
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Search failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses
from models import Car
from search import search_cars

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)  # Show cursor
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:  # Enter key
                break
            elif key == 27:  # Escape key
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with role selection.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Welcome to Car Sales System!")
            stdscr.addstr(2, 0, "1. Admin")
            stdscr.addstr(3, 0, "2. Customer")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                admin_menu(stdscr)
            elif key == ord('2'):
                customer_menu(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_data.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 test_data.py</b> to add a test car, then <b>python3 ui.py</b> to test the search.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Search makes finding cars easier.", styles['KeyTakeaway']),
                Paragraph("Secure queries prevent errors.", styles['KeyTakeaway']),
                Paragraph("Integrate search into the UI for usability.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 9
def chapter9():
    """Generate content for Chapter 9: Implementing User Authentication.

    Returns:
        list: List of ReportLab flowables for Chapter 9.
    """
    global chapter_number
    chapter_number = 9
    return [
        Paragraph("Chapter 9: Implementing User Authentication", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter adds login functionality to secure the system, ensuring only authorized users access admin or customer menus.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("9.1 Why Authentication?", styles['SectionHeading']),
        Paragraph(
            "Authentication verifies users, like a key to a locked door. We’ll use <b>bcrypt</b> to check passwords securely.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Authentication is like a school ID card—you need it to access certain areas.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("9.2 Creating the Authentication Logic", styles['SectionHeading']),
        Paragraph(
            "Create <b>auth.py</b> to handle login and user verification.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import bcrypt
from database import get_db_connection

def authenticate_user(username, password):
    \"\"\"Authenticate a user by username and password.

    Args:
        username (str): User's login name.
        password (str): User's password.

    Returns:
        dict or None: User data (id, username, role) if authenticated, else None.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        return None
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Authentication failed: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>bcrypt.checkpw</b>: Verifies the password against the stored hash.", styles['BodyText']),
                Paragraph("Returns user data if authenticated, else None.", styles['BodyText']),
                Paragraph("Parameterized query prevents SQL injection.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("9.3 Integrating Authentication into the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to add a login screen before accessing menus.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses
from models import Car
from search import search_cars
from auth import authenticate_user

def login_ui(stdscr):
    \"\"\"Display a login interface.

    Args:
        stdscr: The curses window object.

    Returns:
        dict or None: Authenticated user data or None if login fails.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Login to Car Sales System")
        stdscr.addstr(2, 0, "Username: ")
        stdscr.addstr(4, 0, "Password: ")
        stdscr.refresh()
        
        username = ""
        password = ""
        y, x = 2, 10
        current_field = 'username'
        
        while True:
            key = stdscr.getch()
            if key == 10:  # Enter key
                if current_field == 'username':
                    current_field = 'password'
                    y, x = 4, 10
                    stdscr.move(y, x)
                else:
                    user = authenticate_user(username, password)
                    if user:
                        return user
                    else:
                        stdscr.addstr(6, 0, "Invalid credentials. Press any key to try again...")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Login to Car Sales System")
                        stdscr.addstr(2, 0, "Username: ")
                        stdscr.addstr(4, 0, "Password: ")
                        username = ""
                        password = ""
                        current_field = 'username'
                        y, x = 2, 10
                        stdscr.move(y, x)
                stdscr.refresh()
            elif key == 27:  # Escape key
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 'username' and username:
                    username = username[:-1]
                    stdscr.addstr(y, x + len(username), " ")
                elif current_field == 'password' and password:
                    password = password[:-1]
                    stdscr.addstr(y, x + len(password), " ")
                stdscr.refresh()
            else:
                char = chr(key)
                if current_field == 'username':
                    username += char
                    stdscr.addstr(y, x, username)
                else:
                    password += char
                    stdscr.addstr(y, x, "*" * len(password))
                stdscr.refresh()
    except curses.error as e:
        logging.error(f"Login UI failed: {str(e)}")
        return None

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:
                break
            elif key == 27:
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with login.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        while True:
            user = login_ui(stdscr)
            if not user:
                break
            if user['role'] == 'admin':
                admin_menu(stdscr)
            elif user['role'] == 'customer':
                customer_menu(stdscr)
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>login_ui</b>: Prompts for username and password.", styles['BodyText']),
                Paragraph("Directs users to appropriate menus based on role.", styles['BodyText']),
                Paragraph("Handles invalid credentials with a retry option.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("9.4 Testing Authentication", styles['SectionHeading']),
        Paragraph(
            "Add a test user to the database to test login.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """from models import User

def add_test_user():
    \"\"\"Add a test admin user to the database.\"\"\"
    try:
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        print("Test user added.")
    except Exception as e:
        logging.error(f"Failed to add test user: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    add_test_user()
"""
        ),
        Paragraph("Save as <b>test_user.py</b> and run:", styles['BodyText']),
        create_code_block("python3 test_user.py\npython3 ui.py"),
        Paragraph(
            "Log in with username ‘admin’ and password ‘adminpass’.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: Ensure <b>bcrypt</b> is installed and the database has the users table.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("9.5 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: search.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
from models import Car

def search_cars(search_term):
    \"\"\"Search cars by make or model.

    Args:
        search_term (str): Term to search for in make or model.

    Returns:
        list: List of matching Car objects.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                 (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()
        return [Car(*row) for row in rows]
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Search failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: auth.py</b>", styles['BodyText']),
        create_code_block(
            """import bcrypt
from database import get_db_connection

def authenticate_user(username, password):
    \"\"\"Authenticate a user by username and password.

    Args:
        username (str): User's login name.
        password (str): User's password.

    Returns:
        dict or None: User data (id, username, role) if authenticated, else None.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        return None
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Authentication failed: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses
from models import Car
from search import search_cars
from auth import authenticate_user

def login_ui(stdscr):
    \"\"\"Display a login interface.

    Args:
        stdscr: The curses window object.

    Returns:
        dict or None: Authenticated user data or None if login fails.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Login to Car Sales System")
        stdscr.addstr(2, 0, "Username: ")
        stdscr.addstr(4, 0, "Password: ")
        stdscr.refresh()
        
        username = ""
        password = ""
        y, x = 2, 10
        current_field = 'username'
        
        while True:
            key = stdscr.getch()
            if key == 10:  # Enter key
                if current_field == 'username':
                    current_field = 'password'
                    y, x = 4, 10
                    stdscr.move(y, x)
                else:
                    user = authenticate_user(username, password)
                    if user:
                        return user
                    else:
                        stdscr.addstr(6, 0, "Invalid credentials. Press any key to try again...")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Login to Car Sales System")
                        stdscr.addstr(2, 0, "Username: ")
                        stdscr.addstr(4, 0, "Password: ")
                        username = ""
                        password = ""
                        current_field = 'username'
                        y, x = 2, 10
                        stdscr.move(y, x)
                stdscr.refresh()
            elif key == 27:  # Escape key
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 'username' and username:
                    username = username[:-1]
                    stdscr.addstr(y, x + len(username), " ")
                elif current_field == 'password' and password:
                    password = password[:-1]
                    stdscr.addstr(y, x + len(password), " ")
                stdscr.refresh()
            else:
                char = chr(key)
                if current_field == 'username':
                    username += char
                    stdscr.addstr(y, x, username)
                else:
                    password += char
                    stdscr.addstr(y, x, "*" * len(password))
                stdscr.refresh()
    except curses.error as e:
        logging.error(f"Login UI failed: {str(e)}")
        return None

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:
                break
            elif key == 27:
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with login.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        while True:
            user = login_ui(stdscr)
            if not user:
                break
            if user['role'] == 'admin':
                admin_menu(stdscr)
            elif user['role'] == 'customer':
                customer_menu(stdscr)
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_data.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_user.py</b>", styles['BodyText']),
        create_code_block(
            """from models import User

def add_test_user():
    \"\"\"Add a test admin user to the database.\"\"\"
    try:
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        print("Test user added.")
    except Exception as e:
        logging.error(f"Failed to add test user: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    add_test_user()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 test_user.py</b> to add a test user, then <b>python3 ui.py</b> to test login.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Authentication secures the system.", styles['KeyTakeaway']),
                Paragraph("<b>bcrypt</b> ensures safe password handling.", styles['KeyTakeaway']),
                Paragraph("Login UI directs users to role-based menus.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Continuing from Chapter 10
def chapter10():
    """Generate content for Chapter 10: Connecting to a Real API.

    Returns:
        list: List of ReportLab flowables for Chapter 10.
    """
    global chapter_number
    chapter_number = 10
    flowables = [
        Paragraph("Chapter 10: Connecting to a Real API", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter connects your system to the CarQuery API to fetch real car data, enhancing your database.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("10.1 What is an API?", styles['SectionHeading']),
        Paragraph(
            "An <b>API</b> (Application Programming Interface) lets your program talk to external services, like asking a librarian for book details.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: An API is like a waiter taking your order to the kitchen and bringing back food.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.2 Choosing an API", styles['SectionHeading']),
        Paragraph(
            "We’ll use the <b>CarQuery API</b> (http://www.carqueryapi.com), which provides car makes and models. No API key is required for basic access.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("10.3 Fetching Car Data", styles['SectionHeading']),
        Paragraph(
            "Create <b>api.py</b> to fetch car makes from the CarQuery API.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import requests
import logging

def fetch_car_makes():
    \"\"\"Fetch car makes from the CarQuery API.

    Returns:
        list: List of car makes, or empty list if request fails.
    \"\"\"
    try:
        response = requests.get('http://www.carqueryapi.com/api/0.3/?cmd=getMakes')
        response.raise_for_status()
        data = response.json()
        return [make['make_display'] for make in data['Makes']]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch car makes: {str(e)}")
        return []
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>requests.get</b>: Sends a request to the API.", styles['BodyText']),
                Paragraph("<b>response.json</b>: Parses the JSON response.", styles['BodyText']),
                Paragraph("Extracts car makes from the response.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: The API call is like asking a car catalog for a list of brands.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.4 Displaying API Data in the UI", styles['SectionHeading']),
        Paragraph(
            "Update <b>ui.py</b> to add an option in the admin menu to view API-fetched car makes.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import curses
from models import Car
from search import search_cars
from auth import authenticate_user
from api import fetch_car_makes

def login_ui(stdscr):
    \"\"\"Display a login interface.

    Args:
        stdscr: The curses window object.

    Returns:
        dict or None: Authenticated user data or None if login fails.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Login to Car Sales System")
        stdscr.addstr(2, 0, "Username: ")
        stdscr.addstr(4, 0, "Password: ")
        stdscr.refresh()
        
        username = ""
        password = ""
        y, x = 2, 10
        current_field = 'username'
        
        while True:
            key = stdscr.getch()
            if key == 10:
                if current_field == 'username':
                    current_field = 'password'
                    y, x = 4, 10
                    stdscr.move(y, x)
                else:
                    user = authenticate_user(username, password)
                    if user:
                        return user
                    else:
                        stdscr.addstr(6, 0, "Invalid credentials. Press any key to try again...")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Login to Car Sales System")
                        stdscr.addstr(2, 0, "Username: ")
                        stdscr.addstr(4, 0, "Password: ")
                        username = ""
                        password = ""
                        current_field = 'username'
                        y, x = 2, 10
                        stdscr.move(y, x)
                stdscr.refresh()
            elif key == 27:
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 'username' and username:
                    username = username[:-1]
                    stdscr.addstr(y, x + len(username), " ")
                elif current_field == 'password' and password:
                    password = password[:-1]
                    stdscr.addstr(y, x + len(password), " ")
                stdscr.refresh()
            else:
                char = chr(key)
                if current_field == 'username':
                    username += char
                    stdscr.addstr(y, x, username)
                else:
                    password += char
                    stdscr.addstr(y, x, "*" * len(password))
                stdscr.refresh()
    except curses.error as e:
        logging.error(f"Login UI failed: {str(e)}")
        return None

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:
                break
            elif key == 27:
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def view_car_makes(stdscr):
    \"\"\"Display car makes fetched from the API.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        makes = fetch_car_makes()
        if not makes:
            stdscr.addstr(0, 0, "No car makes available.")
        else:
            for i, make in enumerate(makes):
                stdscr.addstr(i, 0, make)
        stdscr.addstr(len(makes) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View car makes UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. View car makes (API)")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                view_car_makes(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with login.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        while True:
            user = login_ui(stdscr)
            if not user:
                break
            if user['role'] == 'admin':
                admin_menu(stdscr)
            elif user['role'] == 'customer':
                customer_menu(stdscr)
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>view_car_makes</b>: Displays API-fetched car makes.", styles['BodyText']),
                Paragraph("Admin menu now includes an API option.", styles['BodyText']),
                Paragraph("Handles empty or failed API responses.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("10.5 Testing the API Integration", styles['SectionHeading']),
        Paragraph(
            "Ensure an internet connection, then run the UI to test the API.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("python3 test_user.py\npython3 ui.py"),
        Paragraph(
            "Log in as ‘admin’, select ‘View car makes (API)’ to see the list.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If the API fails, check your internet connection or verify the CarQuery API URL.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("10.6 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3
import logging

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt
import logging

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: search.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
from models import Car
import logging

def search_cars(search_term):
    \"\"\"Search cars by make or model.

    Args:
        search_term (str): Term to search for in make or model.

    Returns:
        list: List of matching Car objects.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                 (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()
        return [Car(*row) for row in rows]
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Search failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: auth.py</b>", styles['BodyText']),
        create_code_block(
            """import bcrypt
from database import get_db_connection
import logging

def authenticate_user(username, password):
    \"\"\"Authenticate a user by username and password.

    Args:
        username (str): User's login name.
        password (str): User's password.

    Returns:
        dict or None: User data (id, username, role) if authenticated, else None.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        return None
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Authentication failed: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: api.py</b>", styles['BodyText']),
        create_code_block(
            """import requests
import logging

def fetch_car_makes():
    \"\"\"Fetch car makes from the CarQuery API.

    Returns:
        list: List of car makes, or empty list if request fails.
    \"\"\"
    try:
        response = requests.get('http://www.carqueryapi.com/api/0.3/?cmd=getMakes')
        response.raise_for_status()
        data = response.json()
        return [make['make_display'] for make in data['Makes']]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch car makes: {str(e)}")
        return []
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses
from models import Car
from search import search_cars
from auth import authenticate_user
from api import fetch_car_makes
import logging

def login_ui(stdscr):
    \"\"\"Display a login interface.

    Args:
        stdscr: The curses window object.

    Returns:
        dict or None: Authenticated user data or None if login fails.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Login to Car Sales System")
        stdscr.addstr(2, 0, "Username: ")
        stdscr.addstr(4, 0, "Password: ")
        stdscr.refresh()
        
        username = ""
        password = ""
        y, x = 2, 10
        current_field = 'username'
        
        while True:
            key = stdscr.getch()
            if key == 10:
                if current_field == 'username':
                    current_field = 'password'
                    y, x = 4, 10
                    stdscr.move(y, x)
                else:
                    user = authenticate_user(username, password)
                    if user:
                        return user
                    else:
                        stdscr.addstr(6, 0, "Invalid credentials. Press any key to try again...")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Login to Car Sales System")
                        stdscr.addstr(2, 0, "Username: ")
                        stdscr.addstr(4, 0, "Password: ")
                        username = ""
                        password = ""
                        current_field = 'username'
                        y, x = 2, 10
                        stdscr.move(y, x)
                stdscr.refresh()
            elif key == 27:
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 'username' and username:
                    username = username[:-1]
                    stdscr.addstr(y, x + len(username), " ")
                elif current_field == 'password' and password:
                    password = password[:-1]
                    stdscr.addstr(y, x + len(password), " ")
                stdscr.refresh()
            else:
                char = chr(key)
                if current_field == 'username':
                    username += char
                    stdscr.addstr(y, x, username)
                else:
                    password += char
                    stdscr.addstr(y, x, "*" * len(password))
                stdscr.refresh()
    except curses.error as e:
        logging.error(f"Login UI failed: {str(e)}")
        return None

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:
                break
            elif key == 27:
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def view_car_makes(stdscr):
    \"\"\"Display car makes fetched from the API.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        makes = fetch_car_makes()
        if not makes:
            stdscr.addstr(0, 0, "No car makes available.")
        else:
            for i, make in enumerate(makes):
                stdscr.addstr(i, 0, make)
        stdscr.addstr(len(makes) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View car makes UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. View car makes (API)")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                view_car_makes(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with login.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        while True:
            user = login_ui(stdscr)
            if not user:
                break
            if user['role'] == 'admin':
                admin_menu(stdscr)
            elif user['role'] == 'customer':
                customer_menu(stdscr)
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_data.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car
import logging

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_user.py</b>", styles['BodyText']),
        create_code_block(
            """from models import User
import logging

def add_test_user():
    \"\"\"Add a test admin user to the database.\"\"\"
    try:
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        print("Test user added.")
    except Exception as e:
        logging.error(f"Failed to add test user: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    add_test_user()
"""
        ),
        Spacer(1, 10),
        Paragraph("Run <b>python3 test_user.py</b> to add a test user, then <b>python3 ui.py</b> to test the API integration.", styles['BodyText']),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("APIs connect your app to external data.", styles['KeyTakeaway']),
                Paragraph("<b>requests</b> simplifies API calls.", styles['KeyTakeaway']),
                Paragraph("Handle API errors to keep your app stable.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]
    return flowables

# Chapter 11
def chapter11():
    """Generate content for Chapter 11: Testing Your Application.

    Returns:
        list: List of ReportLab flowables for Chapter 11.
    """
    global chapter_number
    chapter_number = 11
    return [
        Paragraph("Chapter 11: Testing Your Application", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This chapter introduces testing with <b>pytest</b> to ensure your car sales system works as expected.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("11.1 Why Test?", styles['SectionHeading']),
        Paragraph(
            "Testing catches bugs, like checking a car’s engine before a race. Automated tests save time and ensure reliability.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: Testing is like double-checking your homework to avoid mistakes.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("11.2 Setting Up pytest", styles['SectionHeading']),
        Paragraph(
            "Install <b>pytest</b> if you haven’t already:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("pip install pytest"),
        Paragraph(
            "Create a <b>tests</b> directory with a <b>test_car.py</b> file to test the Car class.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("11.3 Writing Tests for the Car Class", styles['SectionHeading']),
        Paragraph(
            "Add tests to verify saving and loading cars.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import pytest
from models import Car
from database import init_db, get_db_connection

@pytest.fixture
def setup_database():
    \"\"\"Set up a test database and clean up after tests.\"\"\"
    init_db()
    yield
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM cars")
    conn.commit()
    conn.close()

def test_save_and_load_car(setup_database):
    \"\"\"Test saving a car and loading it from the database.\"\"\"
    car = Car('VIN002', 'Honda', 'Civic', 2021, 'Blue', 30000, 18000, 'Available')
    car.save()
    
    cars = Car.load_all()
    assert len(cars) == 1
    assert cars[0].vin == 'VIN002'
    assert cars[0].make == 'Honda'
    assert cars[0].model == 'Civic'

def test_load_empty_database(setup_database):
    \"\"\"Test loading cars from an empty database.\"\"\"
    cars = Car.load_all()
    assert len(cars) == 0
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>@pytest.fixture</b>: Sets up a clean database for each test.", styles['BodyText']),
                Paragraph("<b>test_save_and_load_car</b>: Verifies saving and retrieving a car.", styles['BodyText']),
                Paragraph("<b>test_load_empty_database</b>: Ensures an empty database returns no cars.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("11.4 Running Tests", styles['SectionHeading']),
        Paragraph(
            "Run tests from the project directory:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block("pytest tests/test_car.py -v"),
        Paragraph(
            "<b>-v</b> enables verbose output to see test results clearly.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Troubleshooting Tip</b>: If tests fail, ensure the database is accessible and <b>pytest</b> is installed.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("11.5 Testing Authentication", styles['SectionHeading']),
        Paragraph(
            "Create <b>tests/test_auth.py</b> to test user authentication.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        create_code_block(
            """import pytest
from auth import authenticate_user
from models import User
from database import init_db, get_db_connection

@pytest.fixture
def setup_database():
    \"\"\"Set up a test database and clean up after tests.\"\"\"
    init_db()
    yield
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def test_authenticate_user(setup_database):
    \"\"\"Test authenticating a user with correct credentials.\"\"\"
    user = User(None, 'testuser', 'testpass', 'customer')
    user.save()
    
    result = authenticate_user('testuser', 'testpass')
    assert result is not None
    assert result['username'] == 'testuser'
    assert result['role'] == 'customer'

def test_authenticate_invalid_user(setup_database):
    \"\"\"Test authenticating with invalid credentials.\"\"\"
    result = authenticate_user('nonexistent', 'wrongpass')
    assert result is None
"""
        ),
        Paragraph("<b>What’s Happening?</b>", styles['BodyText']),
        ListFlowable(
            [
                Paragraph("<b>test_authenticate_user</b>: Verifies correct login.", styles['BodyText']),
                Paragraph("<b>test_authenticate_invalid_user</b>: Ensures invalid credentials fail.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("Run the authentication tests:", styles['BodyText']),
        create_code_block("pytest tests/test_auth.py -v"),
        Spacer(1, 10),
        Paragraph("11.6 Cumulative Code Files", styles['SectionHeading']),
        Paragraph(
            "Here are all the files created or updated so far, including the new test files:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("<b>File: database.py</b>", styles['BodyText']),
        create_code_block(
            """import sqlite3
import logging

def init_db():
    \"\"\"Initialize the SQLite database with tables for cars, customers, sales, users, and favorites.\"\"\"
    try:
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
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {str(e)}")
    finally:
        conn.close()

def get_db_connection():
    \"\"\"Return a connection to the SQLite database.

    Returns:
        sqlite3.Connection or None: Database connection or None if connection fails.
    \"\"\"
    try:
        return sqlite3.connect('car_sales.db')
    except sqlite3.Error as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        return None
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: main.py</b>", styles['BodyText']),
        create_code_block(
            """from database import init_db

def main():
    \"\"\"Initialize the database.\"\"\"
    init_db()

if __name__ == "__main__":
    main()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: models.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
import bcrypt
import logging

class Car:
    \"\"\"Blueprint for car objects with database operations.\"\"\"
    def __init__(self, vin, make, model, year, color, mileage, price, status):
        \"\"\"Initialize a Car object with given attributes.

        Args:
            vin (str): Vehicle Identification Number.
            make (str): Car manufacturer (e.g., Toyota).
            model (str): Car model (e.g., Camry).
            year (int): Manufacturing year.
            color (str): Car color.
            mileage (int): Car mileage.
            price (float): Car price.
            status (str): Availability status (e.g., Available).
        \"\"\"
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.price = price
        self.status = status
    
    def save(self):
        \"\"\"Save the car to the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO cars (vin, make, model, year, color, mileage, price, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (self.vin, self.make, self.model, self.year, self.color, self.mileage, self.price, self.status))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save car: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all cars from the database.

        Returns:
            list: List of Car objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM cars")
            rows = c.fetchall()
            return [Car(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load cars: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class Customer:
    \"\"\"Blueprint for customer objects with database operations.\"\"\"
    def __init__(self, id, name, contact):
        \"\"\"Initialize a Customer object with given attributes.

        Args:
            id (int or None): Unique customer ID, None for new customers.
            name (str): Customer's name.
            contact (str): Customer's contact information (e.g., email).
        \"\"\"
        self.id = id
        self.name = name
        self.contact = contact
    
    def save(self):
        \"\"\"Save or update the customer in the database.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            if self.id is None:
                c.execute("INSERT INTO customers (name, contact) VALUES (?, ?)", (self.name, self.contact))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE customers SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save customer: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def load_all():
        \"\"\"Load all customers from the database.

        Returns:
            list: List of Customer objects.
        \"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            c.execute("SELECT * FROM customers")
            rows = c.fetchall()
            return [Customer(*row) for row in rows]
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to load customers: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

class User:
    \"\"\"Blueprint for user objects with secure login operations.\"\"\"
    def __init__(self, id, username, password, role):
        \"\"\"Initialize a User object with given attributes.

        Args:
            id (int or None): Unique user ID, None for new users.
            username (str): User's login name.
            password (str): User's password (will be hashed).
            role (str): User's role (e.g., 'admin', 'customer').
        \"\"\"
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def save(self):
        \"\"\"Save or update the user in the database with a hashed password.\"\"\"
        try:
            conn = get_db_connection()
            if conn is None:
                raise ValueError("Database connection failed")
            c = conn.cursor()
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
            if self.id is None:
                c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                         (self.username, hashed, self.role))
                self.id = c.lastrowid
            else:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", 
                         (self.username, hashed, self.role, self.id))
            conn.commit()
        except (sqlite3.Error, ValueError) as e:
            logging.error(f"Failed to save user: {str(e)}")
        finally:
            if conn:
                conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: search.py</b>", styles['BodyText']),
        create_code_block(
            """from database import get_db_connection
from models import Car
import logging

def search_cars(search_term):
    \"\"\"Search cars by make or model.

    Args:
        search_term (str): Term to search for in make or model.

    Returns:
        list: List of matching Car objects.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                 (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()
        return [Car(*row) for row in rows]
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Search failed: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: auth.py</b>", styles['BodyText']),
        create_code_block(
            """import bcrypt
from database import get_db_connection
import logging

def authenticate_user(username, password):
    \"\"\"Authenticate a user by username and password.

    Args:
        username (str): User's login name.
        password (str): User's password.

    Returns:
        dict or None: User data (id, username, role) if authenticated, else None.
    \"\"\"
    try:
        conn = get_db_connection()
        if conn is None:
            raise ValueError("Database connection failed")
        c = conn.cursor()
        c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {'id': user[0], 'username': user[1], 'role': user[3]}
        return None
    except (sqlite3.Error, ValueError) as e:
        logging.error(f"Authentication failed: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: api.py</b>", styles['BodyText']),
        create_code_block(
            """import requests
import logging

def fetch_car_makes():
    \"\"\"Fetch car makes from the CarQuery API.

    Returns:
        list: List of car makes, or empty list if request fails.
    \"\"\"
    try:
        response = requests.get('http://www.carqueryapi.com/api/0.3/?cmd=getMakes')
        response.raise_for_status()
        data = response.json()
        return [make['make_display'] for make in data['Makes']]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch car makes: {str(e)}")
        return []
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: ui.py</b>", styles['BodyText']),
        create_code_block(
            """import curses
from models import Car
from search import search_cars
from auth import authenticate_user
from api import fetch_car_makes
import logging

def login_ui(stdscr):
    \"\"\"Display a login interface.

    Args:
        stdscr: The curses window object.

    Returns:
        dict or None: Authenticated user data or None if login fails.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Login to Car Sales System")
        stdscr.addstr(2, 0, "Username: ")
        stdscr.addstr(4, 0, "Password: ")
        stdscr.refresh()
        
        username = ""
        password = ""
        y, x = 2, 10
        current_field = 'username'
        
        while True:
            key = stdscr.getch()
            if key == 10:
                if current_field == 'username':
                    current_field = 'password'
                    y, x = 4, 10
                    stdscr.move(y, x)
                else:
                    user = authenticate_user(username, password)
                    if user:
                        return user
                    else:
                        stdscr.addstr(6, 0, "Invalid credentials. Press any key to try again...")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Login to Car Sales System")
                        stdscr.addstr(2, 0, "Username: ")
                        stdscr.addstr(4, 0, "Password: ")
                        username = ""
                        password = ""
                        current_field = 'username'
                        y, x = 2, 10
                        stdscr.move(y, x)
                stdscr.refresh()
            elif key == 27:
                return None
            elif key == curses.KEY_BACKSPACE or key == 127:
                if current_field == 'username' and username:
                    username = username[:-1]
                    stdscr.addstr(y, x + len(username), " ")
                elif current_field == 'password' and password:
                    password = password[:-1]
                    stdscr.addstr(y, x + len(password), " ")
                stdscr.refresh()
            else:
                char = chr(key)
                if current_field == 'username':
                    username += char
                    stdscr.addstr(y, x, username)
                else:
                    password += char
                    stdscr.addstr(y, x, "*" * len(password))
                stdscr.refresh()
    except curses.error as e:
        logging.error(f"Login UI failed: {str(e)}")
        return None

def view_all_cars(stdscr):
    \"\"\"Display all cars in the database.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        cars = Car.load_all()
        if not cars:
            stdscr.addstr(0, 0, "No cars available.")
        else:
            for i, car in enumerate(cars):
                stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
        stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View cars UI failed: {str(e)}")

def search_cars_ui(stdscr):
    \"\"\"Display a search interface for cars.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter search term (make or model): ")
        stdscr.refresh()
        search_term = ""
        y, x = 1, 0
        while True:
            key = stdscr.getch()
            if key == 10:
                break
            elif key == 27:
                return
            elif key == curses.KEY_BACKSPACE or key == 127:
                if search_term:
                    search_term = search_term[:-1]
                    stdscr.addstr(y, x + len(search_term), " ")
                    stdscr.refresh()
            else:
                search_term += chr(key)
                stdscr.addstr(y, x, search_term)
                stdscr.refresh()
        if search_term:
            cars = search_cars(search_term)
            stdscr.clear()
            if not cars:
                stdscr.addstr(0, 0, "No cars found.")
            else:
                for i, car in enumerate(cars):
                    stdscr.addstr(i, 0, f"{car.make} {car.model} ({car.year}) - ${car.price}")
            stdscr.addstr(len(cars) + 2, 0, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
    except curses.error as e:
        logging.error(f"Search UI failed: {str(e)}")

def view_car_makes(stdscr):
    \"\"\"Display car makes fetched from the API.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        stdscr.clear()
        makes = fetch_car_makes()
        if not makes:
            stdscr.addstr(0, 0, "No car makes available.")
        else:
            for i, make in enumerate(makes):
                stdscr.addstr(i, 0, make)
        stdscr.addstr(len(makes) + 2, 0, "Press any key to return...")
        stdscr.refresh()
        stdscr.getch()
    except curses.error as e:
        logging.error(f"View car makes UI failed: {str(e)}")

def admin_menu(stdscr):
    \"\"\"Display the admin menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Admin Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. View car makes (API)")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                view_car_makes(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Admin menu UI failed: {str(e)}")

def customer_menu(stdscr):
    \"\"\"Display the customer menu.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        curses.curs_set(0)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Customer Menu")
            stdscr.addstr(2, 0, "1. View all cars")
            stdscr.addstr(3, 0, "2. Search cars")
            stdscr.addstr(4, 0, "3. Exit")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('1'):
                view_all_cars(stdscr)
            elif key == ord('2'):
                search_cars_ui(stdscr)
            elif key == ord('3'):
                break
    except curses.error as e:
        logging.error(f"Customer menu UI failed: {str(e)}")

def main_ui(stdscr):
    \"\"\"Display the main user interface with login.

    Args:
        stdscr: The curses window object.
    \"\"\"
    try:
        while True:
            user = login_ui(stdscr)
            if not user:
                break
            if user['role'] == 'admin':
                admin_menu(stdscr)
            elif user['role'] == 'customer':
                customer_menu(stdscr)
    except curses.error as e:
        logging.error(f"Main UI rendering failed: {str(e)}")

if __name__ == "__main__":
    curses.wrapper(main_ui)
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_data.py</b>", styles['BodyText']),
        create_code_block(
            """from models import Car
import logging

def populate_test_data():
    \"\"\"Add a test car to the database.\"\"\"
    try:
        car = Car('VIN001', 'Toyota', 'Camry', 2020, 'Black', 50000, 20000, 'Available')
        car.save()
        print("Test car added.")
    except Exception as e:
        logging.error(f"Failed to add test car: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    populate_test_data()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: test_user.py</b>", styles['BodyText']),
        create_code_block(
            """from models import User
import logging

def add_test_user():
    \"\"\"Add a test admin user to the database.\"\"\"
    try:
        user = User(None, 'admin', 'adminpass', 'admin')
        user.save()
        print("Test user added.")
    except Exception as e:
        logging.error(f"Failed to add test user: {str(e)}")
        print(f"Failed: {str(e)}")

if __name__ == "__main__":
    add_test_user()
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: tests/test_car.py</b>", styles['BodyText']),
        create_code_block(
            """import pytest
from models import Car
from database import init_db, get_db_connection

@pytest.fixture
def setup_database():
    \"\"\"Set up a test database and clean up after tests.\"\"\"
    init_db()
    yield
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM cars")
    conn.commit()
    conn.close()

def test_save_and_load_car(setup_database):
    \"\"\"Test saving a car and loading it from the database.\"\"\"
    car = Car('VIN002', 'Honda', 'Civic', 2021, 'Blue', 30000, 18000, 'Available')
    car.save()
    
    cars = Car.load_all()
    assert len(cars) == 1
    assert cars[0].vin == 'VIN002'
    assert cars[0].make == 'Honda'
    assert cars[0].model == 'Civic'

def test_load_empty_database(setup_database):
    \"\"\"Test loading cars from an empty database.\"\"\"
    cars = Car.load_all()
    assert len(cars) == 0
"""
        ),
        Spacer(1, 10),
        Paragraph("<b>File: tests/test_auth.py</b>", styles['BodyText']),
        create_code_block(
            """import pytest
from auth import authenticate_user
from models import User
from database import init_db, get_db_connection

@pytest.fixture
def setup_database():
    \"\"\"Set up a test database and clean up after tests.\"\"\"
    init_db()
    yield
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def test_authenticate_user(setup_database):
    \"\"\"Test authenticating a user with correct credentials.\"\"\"
    user = User(None, 'testuser', 'testpass', 'customer')
    user.save()
    
    result = authenticate_user('testuser', 'testpass')
    assert result is not None
    assert result['username'] == 'testuser'
    assert result['role'] == 'customer'

def test_authenticate_invalid_user(setup_database):
    \"\"\"Test authenticating with invalid credentials.\"\"\"
    result = authenticate_user('nonexistent', 'wrongpass')
    assert result is None
"""
        ),
        Spacer(1, 10),
        Paragraph("Run all tests with:", styles['BodyText']),
        create_code_block("pytest -v"),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("Testing ensures your app works correctly.", styles['KeyTakeaway']),
                Paragraph("<b>pytest</b> automates testing.", styles['KeyTakeaway']),
                Paragraph("Fixtures keep tests clean and isolated.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48),
        PageBreak()
    ]

# Chapter 12
def chapter12():
    """Generate content for Chapter 12: Next Steps and Enhancements.

    Returns:
        list: List of ReportLab flowables for Chapter 12.
    """
    global chapter_number
    chapter_number = 12
    return [
        Paragraph("Chapter 12: Next Steps and Enhancements", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph(
            "<b>Chapter Overview</b>: This final chapter reviews what you’ve built and suggests ways to improve and expand your car sales system.",
            styles['IntroText']
        ),
        Spacer(1, 12),
        Paragraph("12.1 What You’ve Built", styles['SectionHeading']),
        Paragraph(
            "You’ve created a functional car sales system with:",
            styles['BodyText']
        ),
        ListFlowable(
            [
                Paragraph("A SQLite database for cars, users, and more.", styles['BodyText']),
                Paragraph("A text-based UI with admin and customer menus.", styles['BodyText']),
                Paragraph("Search, authentication, and API integration.", styles['BodyText']),
                Paragraph("Automated tests to ensure reliability.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: You’ve built a mini car dealership app, like a digital showroom!",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("12.2 Suggested Enhancements", styles['SectionHeading']),
        Paragraph(
            "Here are ideas to take your project further:",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Add Car Management", styles['SubSectionHeading']),
        Paragraph(
            "Let admins add, update, or delete cars via the UI. Example: Create an <b>admin_add_car_ui</b> function in <b>ui.py</b>.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Implement Sales Tracking", styles['SubSectionHeading']),
        Paragraph(
            "Use the <b>sales</b> table to record purchases. Add a customer option to buy a car, updating its status to ‘Sold’.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Upgrade to a Graphical UI", styles['SubSectionHeading']),
        Paragraph(
            "Replace <b>curses</b> with <b>tkinter</b> or <b>PyQt</b> for a modern interface with buttons and forms.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Add More API Features", styles['SubSectionHeading']),
        Paragraph(
            "Fetch car models or details from the CarQuery API and let admins import them into the database.",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("12.3 Sharing Your Project", styles['SectionHeading']),
        Paragraph(
            "Share your code on GitHub to showcase your work. Create a README with:",
            styles['BodyText']
        ),
        ListFlowable(
            [
                Paragraph("Project description.", styles['BodyText']),
                Paragraph("Setup instructions (e.g., <b>pip install -r requirements.txt</b>).", styles['BodyText']),
                Paragraph("Usage examples.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>For Beginners</b>: GitHub is like a portfolio for your code, letting others see and use it.",
            styles['Callout']
        ),
        Spacer(1, 10),
        Paragraph("12.4 Final Code Review", styles['SectionHeading']),
        Paragraph(
            "Your project now includes these files:",
            styles['BodyText']
        ),
        ListFlowable(
            [
                Paragraph("<b>main.py</b>: Initializes the database.", styles['BodyText']),
                Paragraph("<b>database.py</b>: Sets up SQLite tables.", styles['BodyText']),
                Paragraph("<b>models.py</b>: Defines Car, Customer, and User classes.", styles['BodyText']),
                Paragraph("<b>search.py</b>: Handles car search.", styles['BodyText']),
                Paragraph("<b>auth.py</b>: Manages user authentication.", styles['BodyText']),
                Paragraph("<b>api.py</b>: Fetches data from CarQuery API.", styles['BodyText']),
                Paragraph("<b>ui.py</b>: Provides the text-based interface.", styles['BodyText']),
                Paragraph("<b>test_data.py</b>, <b>test_user.py</b>: Add test data.", styles['BodyText']),
                Paragraph("<b>tests/test_car.py</b>, <b>tests/test_auth.py</b>: Automated tests.", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("12.5 Getting Help", styles['SectionHeading']),
        Paragraph(
            "If you’re stuck, try:",
            styles['BodyText']
        ),
        ListFlowable(
            [
                Paragraph("Stack Overflow for coding questions.", styles['BodyText']),
                Paragraph("Python Discord or Reddit for community support.", styles['BodyText']),
                Paragraph("Official Python docs (python.org).", styles['BodyText'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 10),
        Paragraph("12.6 Congratulations!", styles['SectionHeading']),
        Paragraph(
            "You’ve built a complete Python project from scratch. Keep coding, experimenting, and learning!",
            styles['BodyText']
        ),
        Spacer(1, 10),
        Paragraph("Key Takeaways", styles['SectionHeading']),
        ListFlowable(
            [
                Paragraph("You’ve learned Python, databases, APIs, and testing.", styles['KeyTakeaway']),
                Paragraph("Enhancements make your project more powerful.", styles['KeyTakeaway']),
                Paragraph("Sharing and seeking help grows your skills.", styles['KeyTakeaway'])
            ],
            bulletType='bullet', start='•', bulletFontSize=12, leftIndent=20
        ),
        Spacer(1, 48)
    ]

# Assemble all chapters
def generate_pdf():
    """Generate the complete PDF tutorial."""
    doc = SimpleDocTemplate(
        "car_sales_tutorial.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    flowables = []
    
    # Title Page
    flowables.extend([
        Paragraph("Car Sales System Tutorial", styles['Title']),
        Paragraph("A Beginner’s Guide to Building a Python Project", styles['SubTitle']),
        Spacer(1, 24),
        Paragraph("By Grok, Created by xAI", styles['Author']),
        Spacer(1, 48),
        Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Normal']),
        PageBreak()
    ])
    
    # Table of Contents (simplified)
    flowables.extend([
        Paragraph("Table of Contents", styles['ChapterTitle']),
        HRFlowable(width=6*inch, thickness=1, color=NAVY, spaceAfter=12),
        Paragraph("1. Introduction to the Car Sales System", styles['TOCEntry']),
        Paragraph("2. Setting Up Your Development Environment", styles['TOCEntry']),
        Paragraph("3. Designing the Database", styles['TOCEntry']),
        Paragraph("4. Creating the Car Model", styles['TOCEntry']),
        Paragraph("5. Building the Customer Model", styles['TOCEntry']),
        Paragraph("6. Implementing the User Model and Authentication", styles['TOCEntry']),
        Paragraph("7. Designing the Text-Based User Interface", styles['TOCEntry']),
        Paragraph("8. Adding Search Functionality", styles['TOCEntry']),
        Paragraph("9. Implementing User Authentication", styles['TOCEntry']),
        Paragraph("10. Connecting to a Real API", styles['TOCEntry']),
        Paragraph("11. Testing Your Application", styles['TOCEntry']),
        Paragraph("12. Next Steps and Enhancements", styles['TOCEntry']),
        PageBreak()
    ])
    
    # Add all chapters
    flowables.extend(chapter1())
    flowables.extend(chapter2())
    flowables.extend(chapter3())
    flowables.extend(chapter4())
    flowables.extend(chapter5())
    flowables.extend(chapter6())
    flowables.extend(chapter7())
    flowables.extend(chapter8())
    flowables.extend(chapter9())
    flowables.extend(chapter10())
    flowables.extend(chapter11())
    flowables.extend(chapter12())
    
    # Build the PDF
    doc.build(flowables, onFirstPage=add_page_number, onLaterPages=add_page_number)

# Run the script
if __name__ == "__main__":
    generate_pdf()
    print("PDF generated: car_sales_tutorial.pdf")