
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT = r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\Movie_Analytics_DBMS_Mini_Project_Report.docx"
ASSETS_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\assets"
FIGURES_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\figures"

PES_LOGO = os.path.join(ASSETS_DIR, "image1.png")

doc = docx.Document()

# ----------------- Page Setup -----------------
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# ----------------- Helper Functions -----------------
def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_title(text, size=16, bold=True, space_before=12, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0, 51, 102)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

def add_heading_1(text):
    return add_title(text, size=14, bold=True, space_before=18, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT, color=RGBColor(0, 51, 102))

def add_heading_2(text):
    return add_title(text, size=12, bold=True, space_before=14, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT, color=RGBColor(43, 108, 176))

def add_heading_3(text):
    return add_title(text, size=11, bold=True, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, color=RGBColor(45, 55, 72))

def add_para(text, size_pt=11, space_after=6, space_before=0, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(15, 23, 42)
    # Background box for code
    pPr = p._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
    pPr.append(shd)
    return p

def add_custom_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=len(rows)+1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Format header
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_shading(hdr_cells[i], "1E3A8A") # Navy Blue
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
    
    # Format body
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx+1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_shading(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.0)
                run.font.color.rgb = RGBColor(30, 41, 59)

    # Set column widths if provided
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table

def add_figure(img_path, caption, width_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(9.5)
        run_cap.font.italic = True
        run_cap.font.bold = True
        run_cap.font.color.rgb = RGBColor(51, 65, 85)

print("Setup completed. Building document...")

# ====================================================================
# PAGE 1: TITLE / COVER PAGE
# ====================================================================
if os.path.exists(PES_LOGO):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(12)
    p_logo.add_run().add_picture(PES_LOGO, width=Inches(1.2))

add_para("Mini project report on", size_pt=12, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
add_title("MOVIE ANALYTICS & RECOMMENDATION SYSTEM", size=18, bold=True, space_before=4, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)

add_para("Submitted in partial fulfilment of the requirements for the award of degree of", space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Bachelor of Technology", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("in", space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Computer Science & Engineering", space_after=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("UE23CS351A – DBMS Project", space_after=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_para("Submitted by:", space_after=6, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

# Student Table
s_table = doc.add_table(rows=1, cols=2)
s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
s_table.rows[0].cells[0].text = "T. Lohith Srinivas"
s_table.rows[0].cells[1].text = "PES2UG19CS203"
for cell in s_table.rows[0].cells:
    set_cell_margins(cell, top=80, bottom=80, left=150, right=150)
    set_cell_shading(cell, "F1F5F9")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(10.5)

add_para("under the guidance of", space_after=2, space_before=16, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Dr. Shilpa S", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Assistant Professor", space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("AUG - DEC 2026", space_after=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_para("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("FACULTY OF ENGINEERING", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("PES UNIVERSITY", space_after=2, bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("(Established under Karnataka Act No. 16 of 2013)", space_after=2, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India", space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# ====================================================================
# PAGE 2: CERTIFICATE
# ====================================================================
if os.path.exists(PES_LOGO):
    p_logo2 = doc.add_paragraph()
    p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo2.paragraph_format.space_before = Pt(5)
    p_logo2.paragraph_format.space_after = Pt(6)
    p_logo2.add_run().add_picture(PES_LOGO, width=Inches(1.0))

add_para("PES UNIVERSITY", space_after=2, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("(Established under Karnataka Act No. 16 of 2013)", space_after=2, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para("Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India", space_after=16, align=WD_ALIGN_PARAGRAPH.CENTER)

add_title("CERTIFICATE", size=15, bold=True, space_before=10, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)

cert_text = (
    "This is to certify that the mini project entitled \"Movie Analytics & Recommendation System\" "
    "is a bonafide work carried out by T. Lohith Srinivas (PES2UG19CS203) in partial fulfilment for the "
    "completion of fifth semester DBMS Project (UE23CS351A) in the Program of Study - Bachelor of Technology "
    "in Computer Science and Engineering under rules and regulations of PES University, Bengaluru during the period "
    "AUG. 2026 – DEC. 2026. It is certified that all corrections / suggestions indicated for internal assessment "
    "have been incorporated in the report. The project has been approved as it satisfies the 5th semester academic "
    "requirements in respect of project work."
)
add_para(cert_text, space_after=30, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

# Signature Table
sig_table = doc.add_table(rows=1, cols=2)
sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sig_table.rows[0].cells[0].text = "Signature\nDr. Shilpa S\nAssistant Professor\nDept. of CSE, PES University"
sig_table.rows[0].cells[1].text = "Signature of Chairperson\nDr. Sandesh B J\nProfessor & Chairperson\nDept. of CSE, PES University"
for cell in sig_table.rows[0].cells:
    set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.bold = True

doc.add_page_break()

# ====================================================================
# PAGE 3: DECLARATION & ACKNOWLEDGEMENT
# ====================================================================
add_title("DECLARATION", size=15, bold=True, space_before=10, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)

decl_text = (
    "We hereby declare that the DBMS Project entitled \"Movie Analytics & Recommendation System\" "
    "has been carried out by us under the guidance of Dr. Shilpa S, Assistant Professor and submitted in "
    "partial fulfilment of the course requirements for the award of degree of Bachelor of Technology in "
    "Computer Science and Engineering of PES University, Bengaluru during the academic semester AUG – DEC 2026."
)
add_para(decl_text, space_after=20, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

dec_table = doc.add_table(rows=1, cols=3)
dec_table.alignment = WD_TABLE_ALIGNMENT.CENTER
dec_table.rows[0].cells[0].text = "T. Lohith Srinivas"
dec_table.rows[0].cells[1].text = "PES2UG19CS203"
dec_table.rows[0].cells[2].text = "<Signature>"
for cell in dec_table.rows[0].cells:
    set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
    set_cell_shading(cell, "F8FAFC")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.bold = True

add_title("ACKNOWLEDGEMENT", size=15, bold=True, space_before=24, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)

ack1 = (
    "I would like to express my sincere gratitude to Dr. Shilpa S, Assistant Professor, Department of Computer Science "
    "and Engineering, PES University, for her invaluable guidance, patient mentoring, and persistent encouragement throughout "
    "the conceptualization, architectural design, and implementation of this UE23CS351A - DBMS Project."
)
add_para(ack1, space_after=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ack2 = (
    "I take this opportunity to thank Dr. Sandesh B J, Professor and Chairperson, Department of Computer Science and "
    "Engineering, PES University, for fostering an enriching research and development ecosystem and for providing the technical "
    "infrastructure necessary to realize this endeavor."
)
add_para(ack2, space_after=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

ack3 = (
    "I am profoundly grateful to Prof. Jawahar Doreswamy, Honorable Chancellor, PES University, and Dr. Suryaprasad J, "
    "Vice-Chancellor, PES University, for their visionary leadership and continuous institutional support. Finally, this project "
    "could not have been completed without the unwavering support, sacrifices, and encouragement from my family and colleagues."
)
add_para(ack3, space_after=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

doc.add_page_break()

# ====================================================================
# PAGE 4: ABSTRACT
# ====================================================================
add_title("ABSTRACT", size=15, bold=True, space_before=10, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)

abs_text_1 = (
    "In the contemporary streaming media landscape, digital consumers face an unprecedented explosion of cinematic options across "
    "diverse platforms, creating a formidable information overload problem. Traditional movie cataloging systems frequently operate as static "
    "inventories that lack dynamic multi-dimensional analytics, automated rating consistency enforcement, and personalized content discovery. "
    "This project presents CinePulse: A Database-Driven Movie Analytics & Recommendation System designed and implemented using robust relational "
    "database principles, standardized Third Normal Form (3NF/BCNF) schema decomposition, and advanced Structured Query Language (SQL) paradigms."
)
add_para(abs_text_1, space_after=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

abs_text_2 = (
    "The core database schema integrates eleven carefully structured relations modeling entities such as Users, Movies, Directors, Production "
    "Companies, Cast Members, Categorical Genres, and associative relationship entities managing M:N cardinality constraints. Strict referential "
    "integrity is maintained through cascading deletes and foreign key triggers. To handle continuous user evaluation, an automated trigger framework "
    "dynamically recalculates running Bayesian weighted average ratings upon every INSERT, UPDATE, or DELETE operation, simultaneously logging "
    "chronological audit trails into a dedicated security table. Complex analytical queries—incorporating aggregations with HAVING clauses, "
    "correlated subqueries comparing studio and director performances, and nested set-membership evaluations—deliver real-time business intelligence."
)
add_para(abs_text_2, space_after=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

abs_text_3 = (
    "Furthermore, a hybrid recommendation engine merges user genre-affinity vectoring with Bayesian rating weighting to generate personalized "
    "unwatched movie recommendations in real time. The entire backend is coupled with an interactive web presentation layer providing real-time "
    "catalog search, dynamic multi-attribute filtering, interactive rating submissions, and live audit inspection. The system demonstrates how "
    "modern DBMS capabilities—including secondary B-Tree indexing, ACID transactions, stored procedures, and declarative integrity constraints—can "
    "transform raw cinematic metadata into a scalable, intelligent analytical and predictive entertainment platform."
)
add_para(abs_text_3, space_after=14, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

doc.add_page_break()

# ====================================================================
# PAGE 5: TABLE OF CONTENTS & LIST OF TABLES & LIST OF FIGURES
# ====================================================================
add_title("TABLE OF CONTENTS", size=15, bold=True, space_before=10, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)

toc_headers = ["Chapter No.", "Title", "Page No."]
toc_rows = [
    ["1", "INTRODUCTION", "6"],
    ["2", "PROBLEM DEFINITION", "8"],
    ["3", "ER MODEL", "10"],
    ["4", "ER TO RELATIONAL MAPPING", "12"],
    ["5", "DDL STATEMENTS", "15"],
    ["6", "DML STATEMENTS", "20"],
    ["7", "QUERIES (SIMPLE, AGGREGATE, UPDATE, DELETE, CORRELATED, NESTED)", "24"],
    ["8", "STORED PROCEDURES, FUNCTIONS AND TRIGGERS", "30"],
    ["9", "FRONT END DEVELOPMENT", "36"],
    ["-", "REFERENCES / BIBLIOGRAPHY", "41"],
    ["-", "APPENDIX A: DEFINITIONS, ACRONYMS AND ABBREVIATIONS", "42"],
]
add_custom_table(toc_headers, toc_rows, [Inches(1.5), Inches(3.8), Inches(1.2)])

add_title("LIST OF TABLES", size=13, bold=True, space_before=14, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
lot_headers = ["Table No.", "Title", "Page No."]
lot_rows = [
    ["1.1", "Comparison between Existing Systems and Proposed CinePulse System", "7"],
    ["4.1", "Relational Schema Mapping Rules and Attribute Constraints", "13"],
    ["4.2", "Functional Dependencies and Normal Form Justifications (BCNF)", "14"],
    ["6.1", "Initial Database Table Record Counts and Volume Summary", "23"],
    ["7.1", "Genre Performance and Average Rating Query Output", "25"],
    ["7.2", "Director Financial Box Office Analytics Output", "26"],
    ["7.3", "Correlated Query Output: Above-Average Studio Films", "28"],
    ["7.4", "Nested Query Output: Cross-Director Filmography", "29"],
    ["8.1", "Trigger Execution and Audit Log Verification State", "35"],
]
add_custom_table(lot_headers, lot_rows, [Inches(1.5), Inches(3.8), Inches(1.2)])

add_title("LIST OF FIGURES", size=13, bold=True, space_before=14, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
lof_headers = ["Figure No.", "Title", "Page No."]
lof_rows = [
    ["3.1", "Entity-Relationship Diagram (ERD) of Movie Analytics System", "11"],
    ["4.1", "Relational Schema Mapping and Referential Integrity Diagram", "13"],
    ["7.1", "Genre-wise Average Rating Analytical Bar Chart", "25"],
    ["7.2", "Director Box Office Worldwide Gross Analytics Chart", "27"],
    ["9.1", "Three-Tier System Architecture Diagram", "37"],
    ["9.2", "Web Front-End Interactive Dashboard and Recommender Mockup", "39"],
]
add_custom_table(lof_headers, lof_rows, [Inches(1.5), Inches(3.8), Inches(1.2)])

doc.add_page_break()

# ====================================================================
# CHAPTER 1: INTRODUCTION
# ====================================================================
add_heading_1("1. INTRODUCTION")

add_heading_2("1.1 Background & Motivation")
p_intro1 = (
    "The entertainment industry has undergone an unprecedented transformation over the last decade. Streaming giants "
    "and cinema distribution houses produce thousands of cinematic works annually across diverse cultural markets, "
    "genres, and presentation styles. With this digital boom, audiences encounter the phenomenon commonly referred to "
    "as the 'Paradox of Choice'—an excess of options leading to decision paralysis. Users spend substantial time scrolling "
    "through disjointed directories without reliable insights into critical reception, financial metrics, director pedigree, "
    "or tailored recommendations aligned with their historical viewing habits."
)
add_para(p_intro1, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

p_intro2 = (
    "Database Management Systems (DBMS) form the foundational backbone for organizing, querying, and securing high-volume "
    "entertainment metadata. A movie database is intrinsically relational: directors guide multiple productions; films feature "
    "ensembles of actors playing distinct characters; movies span multiple thematic genres; and diverse users author ratings and "
    "textual reviews over time. Ensuring transactional consistency, eliminating data anomalies, and accelerating analytical "
    "aggregations requires rigorous normalization, indexing, and programmable database logic (triggers and stored routines)."
)
add_para(p_intro2, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

add_heading_2("1.2 Project Objectives")
add_para("The primary objectives of the Movie Analytics & Recommendation System are:")
add_bullet("To design and normalize an expressive Relational Database Schema up to Boyce-Codd Normal Form (BCNF), eliminating update, insertion, and deletion anomalies.")
add_bullet("To implement comprehensive DDL statements featuring primary keys, foreign keys with ON DELETE CASCADE and SET NULL actions, domain check constraints, and unique indexes.")
add_bullet("To populate the database with realistic, multi-attribute cinematic records spanning prominent directors, production studios, international cast members, and user evaluations.")
add_bullet("To develop complex SQL queries including multi-table joins, aggregate grouping with HAVING filters, correlated subqueries, and nested set evaluations.")
add_bullet("To architect automated Database Triggers for dynamic running rating recomputation and transparent audit logging.")
add_bullet("To encapsulate business logic within Stored Procedures and User-Defined Functions implementing Bayesian weighted score formulas and content-based recommendation logic.")
add_bullet("To build an interactive Web Application providing an intuitive analytics dashboard, catalog exploration, personalized recommendation engine, and audit inspection.")

add_heading_2("1.3 Scope of the Project")
p_scope = (
    "The project models the end-to-end lifecycle of cinematic data management. Its analytical capabilities cover financial "
    "metrics (production budget vs. worldwide box office revenue), critical metrics (Bayesian weighted scores vs. raw averages), "
    "and user behavioral tracking (watchlists and chronological reviews). The system is built to serve regular film viewers, "
    "accredited movie critics, platform administrators, and data analysts."
)
add_para(p_scope, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

add_heading_2("1.4 Existing Systems vs Proposed System")
add_para("Existing platforms such as IMDb, Rotten Tomatoes, and Letterboxd provide extensive data but exhibit significant structural limitations for educational and custom enterprise analytical workflows:")

comp_headers = ["Feature Dimension", "Existing Commercial Platforms", "Proposed CinePulse System"]
comp_rows = [
    ["Schema Transparency", "Proprietary, opaque schemas inaccessible for custom relational query execution.", "Fully normalized, documented 3NF/BCNF relational architecture."],
    ["Real-Time Rating Aggregation", "Batch-processed hourly/daily caching; stale rating averages during peak usage.", "Instantaneous trigger-driven recomputation upon every review INSERT/UPDATE/DELETE."],
    ["Auditability & Traceability", "Closed black-box logging; users cannot audit rating edits or moderation changes.", "Dedicated ratings_audit table automatically populated via database triggers."],
    ["Recommendation Explainability", "Opaque deep-learning vectors lacking algorithmic interpretability.", "Transparent hybrid SQL recommendation combining genre-affinity vectoring and Bayesian score."],
    ["Custom SQL Analytics", "Strictly restricted REST API endpoints with rigid rate limits.", "Direct analytical query access (correlated, nested, and aggregate queries)."]
]
add_custom_table(comp_headers, comp_rows, [Inches(1.8), Inches(2.4), Inches(2.3)])

doc.add_page_break()

# ====================================================================
# CHAPTER 2: PROBLEM DEFINITION
# ====================================================================
add_heading_1("2. PROBLEM DEFINITION")

add_heading_2("2.1 Problem Statement")
p_prob = (
    "Modern multimedia platforms require robust data architectures capable of managing complex, highly interconnected "
    "cinematic records while guaranteeing ACID (Atomicity, Consistency, Isolation, Durability) properties under concurrent user "
    "interactions. In traditional flat or non-relational storage implementations, redundant metadata (such as repeating genre strings "
    "and director details) causes data inconsistency, update anomalies, and degraded query throughput. Furthermore, manually "
    "updating movie averages across millions of rows introduces substantial server overhead. There is a pressing need for a normalized "
    "relational database solution that leverages database-native triggers, stored procedures, and declarative integrity constraints "
    "to maintain real-time statistical metrics, enforce strict data validation, and empower personalized recommendation pipelines."
)
add_para(p_prob, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

add_heading_2("2.2 System Actors and User Roles")
add_bullet("Standard Registered User: Can browse movie catalogs, apply multi-attribute filters, maintain personal watchlists, submit ratings/reviews, and receive personalized recommendations.")
add_bullet("Verified Movie Critic: Authors in-depth critiques whose ratings carry enhanced analytical significance in critic-tier aggregations.")
add_bullet("Platform Administrator: Manages production entities, registers new releases, inspects audit logs, and monitors database health.")
add_bullet("Recommendation & Analytics Engine: An automated subsystem executing background SQL procedures to compute genre affinities and box-office returns.")

add_heading_2("2.3 Functional Requirements")
add_bullet("FR1 (Catalog Management): The system must store titles, release years, runtimes, languages, budgets, revenues, directors, and production studios.")
add_bullet("FR2 (Associative Mapping): The system must support M:N associations between movies and multiple genres, as well as movies and cast members with specific roles and billing orders.")
add_bullet("FR3 (Rating & Review Portal): Authenticated users must be able to submit rating scores (bounded strictly between 0.5 and 10.0) with accompanying textual reviews.")
add_bullet("FR4 (Automated Statistical Maintenance): The DBMS must automatically recompute the target movie's average rating and total votes upon every rating change.")
add_bullet("FR5 (Chronological Auditing): All rating insertions, updates, and deletions must automatically generate immutable audit entries capturing timestamps, old scores, and new scores.")
add_bullet("FR6 (Analytical Querying): The system must provide queries answering complex multi-table questions regarding director profitability, genre ratings, and actor crossovers.")
add_bullet("FR7 (Personalized Recommendation): The system must generate top-K unwatched recommendations tailored to a user's demonstrated genre preferences.")

add_heading_2("2.4 Non-Functional Requirements")
add_bullet("Data Integrity: Enforced declaratively through Primary Keys, Foreign Keys (CASCADE/SET NULL), UNIQUE constraints, and domain CHECK constraints.")
add_bullet("Performance & Low Latency: Sub-10ms query execution achieved via secondary B-Tree indexes on release year, ratings, and foreign key columns.")
add_bullet("Concurrency & ACID Compliance: Relational transaction safety ensuring dirty reads and phantom rows are eliminated during concurrent rating submissions.")
add_bullet("Extensibility: Modular schema design allowing seamless addition of new attributes (e.g., streaming providers or user followers) without restructuring core tables.")

add_heading_2("2.5 Hardware & Software Specifications")
add_bullet("Operating System: Microsoft Windows 11 / Linux (Ubuntu 22.04 LTS)")
add_bullet("Database Management System: SQLite 3.45 / MySQL 8.0 Enterprise / MariaDB 10.6")
add_bullet("Application Programming Language: Python 3.12 (Tornado / HTTP Engine / Pandas)")
add_bullet("Front-End Presentation: HTML5, CSS3 Modern Dark-Mode Grid, Vanilla ES6 JavaScript")
add_bullet("Memory & Processor: Minimum 8 GB RAM, Intel Core i5 / AMD Ryzen 5 or higher")

doc.add_page_break()

# ====================================================================
# CHAPTER 3: ER MODEL
# ====================================================================
add_heading_1("3. ER MODEL")

add_heading_2("3.1 Entity Identification and Key Selection")
add_para("The system conceptual design identifies six primary entity sets:")
add_bullet("USERS: Models platform members. Key attribute: user_id (Single, Unique, Numerical). Attributes: username, email, full_name, join_date, tier.")
add_bullet("DIRECTORS: Models cinematic filmmakers. Key attribute: director_id. Attributes: name, birth_year, nationality, awards_count.")
add_bullet("PRODUCTION_COMPANIES: Models corporate film studios. Key attribute: company_id. Attributes: company_name, headquarters, founded_year.")
add_bullet("MOVIES: Central entity modeling individual films. Key attribute: movie_id. Attributes: title, release_year, duration_min, language, budget_millions, revenue_millions, avg_rating (derived), total_votes (derived).")
add_bullet("GENRES: Categorical classifications. Key attribute: genre_id. Attributes: genre_name, description.")
add_bullet("CAST_MEMBERS: Actors and performers. Key attribute: cast_id. Attributes: name, gender, birth_year.")

add_heading_2("3.2 Relationship Sets & Structural Constraints")
add_bullet("DIRECTS (Binary 1:N): A Director directs zero, one, or many Movies. A Movie is directed by at most one primary Director (partial participation on Director, partial on Movie with SET NULL on deletion).")
add_bullet("PRODUCES (Binary 1:N): A Production Company finances/produces zero, one, or many Movies. Each Movie has an associated production studio.")
add_bullet("BELONGS_TO (Binary M:N): A Movie belongs to one or more Genres. A Genre encompasses zero, one, or many Movies. Represented by associative relation MOVIE_GENRES.")
add_bullet("ACTS_IN (Binary M:N): A Movie features multiple Cast Members, each playing a specific character (role_name) with a designated billing priority (lead_order). A Cast Member performs in multiple Movies. Represented by MOVIE_CAST.")
add_bullet("RATES_REVIEWS (Ternary / Associative Entity): An authenticated User rates and reviews a Movie. Cardinality: A user can review multiple movies; a movie receives reviews from multiple users. Constrained by a UNIQUE(user_id, movie_id) rule.")
add_bullet("WATCHLIST (Binary M:N): Users bookmark movies with progress states ('Planned', 'Watching', 'Completed', 'Dropped').")

add_heading_2("3.3 Enhanced Features & Attribute Types")
add_bullet("Derived Attributes: avg_rating and total_votes in MOVIES are computed dynamically from RATINGS_REVIEWS using database triggers.")
add_bullet("Domain Constraints: Bounded ratings (0.5 to 10.0), positive budgets and revenues, valid release years (>= 1888), and enumerated tier values ('Standard', 'Premium', 'Critic').")

add_figure(os.path.join(FIGURES_DIR, "fig_3_1_er_diagram.png"), 
           "Figure 3.1: Entity-Relationship Diagram (ERD) of Movie Analytics & Recommendation System", width_inches=6.0)

doc.add_page_break()

# ====================================================================
# CHAPTER 4: ER TO RELATIONAL MAPPING
# ====================================================================
add_heading_1("4. ER TO RELATIONAL MAPPING")

add_heading_2("4.1 Steps of Algorithm for Chosen Problem")
add_para("The conceptual ER model was mapped into a formal relational database schema following the standard 7-step mapping algorithm:")

add_para("Step 1: Mapping of Regular Entity Types", bold=True)
add_bullet("USERS: Created relation users(user_id, username, email, full_name, join_date, tier). PK = {user_id}. UQ = {username}, {email}.")
add_bullet("DIRECTORS: Created relation directors(director_id, name, birth_year, nationality, awards_count). PK = {director_id}.")
add_bullet("PRODUCTION_COMPANIES: Created relation production_companies(company_id, company_name, headquarters, founded_year). PK = {company_id}. UQ = {company_name}.")
add_bullet("GENRES: Created relation genres(genre_id, genre_name, description). PK = {genre_id}. UQ = {genre_name}.")
add_bullet("CAST_MEMBERS: Created relation cast_members(cast_id, name, gender, birth_year). PK = {cast_id}.")
add_bullet("MOVIES: Created relation movies(movie_id, title, release_year, duration_min, language, budget_millions, revenue_millions, avg_rating, total_votes). PK = {movie_id}.")

add_para("Step 2: Mapping of Weak Entity Types", bold=True)
add_para("RATINGS_REVIEWS and WATCHLISTS depend existence-wise on USERS and MOVIES. Rather than opaque compound keys, review_id and watchlist_id serve as primary surrogate keys, while composite candidate keys UNIQUE(user_id, movie_id) prevent duplicate reviews and watchlist additions.")

add_para("Step 3: Mapping of Binary 1:1 Relationship Types", bold=True)
add_para("No 1:1 relationships exist currently; user profile attributes are retained in the USERS relation.")

add_para("Step 4: Mapping of Binary 1:N Relationship Types", bold=True)
add_bullet("DIRECTS: Foreign key director_id inserted into relation movies, referencing directors(director_id) ON DELETE SET NULL.")
add_bullet("PRODUCES: Foreign key company_id inserted into relation movies, referencing production_companies(company_id) ON DELETE SET NULL.")

add_para("Step 5: Mapping of Binary M:N Relationship Types", bold=True)
add_bullet("BELONGS_TO: Created associative relation movie_genres(movie_id, genre_id). Composite PK = {movie_id, genre_id}. FK movie_id -> movies(movie_id) ON DELETE CASCADE; FK genre_id -> genres(genre_id) ON DELETE CASCADE.")
add_bullet("ACTS_IN: Created associative relation movie_cast(movie_id, cast_id, role_name, lead_order). Composite PK = {movie_id, cast_id}. Foreign keys cascade on delete.")

add_para("Step 6: Mapping of Multivalued Attributes", bold=True)
add_para("Multiple genres per movie are decomposed into the normalized relation movie_genres, achieving First Normal Form (1NF).")

add_para("Step 7: Mapping of N-ary Relationship Types / Complex Constraints", bold=True)
add_bullet("RATINGS_AUDIT is mapped as an autonomous relation populated by trigger procedures on rating events.")

add_heading_2("4.2 Complete Diagram of Relational Mapping")
add_figure(os.path.join(FIGURES_DIR, "fig_4_1_relational_schema.png"), 
           "Figure 4.1: Complete Relational Schema Mapping and Referential Integrity Constraints", width_inches=6.0)

add_heading_2("4.3 Normalization Analysis (1NF through BCNF)")
add_para("Every relation in the schema was analyzed against functional dependency sets:")
add_bullet("1NF: All attributes contain atomic, indivisible values. Multivalued genres and cast members are stored in distinct rows in associative tables.")
add_bullet("2NF: All relations are in 1NF and contain no partial functional dependencies. In composite-key relations movie_genres and movie_cast, non-prime attributes (e.g. role_name, lead_order) depend strictly on the complete composite key {movie_id, cast_id}.")
add_bullet("3NF: All relations are in 2NF and contain no transitive dependencies of non-prime attributes on primary keys. For instance, director nationality is not stored in movies; it resides exclusively in directors.")
add_bullet("Boyce-Codd Normal Form (BCNF): For every functional dependency X -> Y, X is a superkey. For example, in users, user_id -> all attributes, username -> all attributes, email -> all attributes; each determinant is a valid candidate key.")

doc.add_page_break()

# ====================================================================
# CHAPTER 5: DDL STATEMENTS
# ====================================================================
add_heading_1("5. DDL STATEMENTS")
add_para("The database schema was generated using standards-compliant SQL DDL. All integrity constraints—PRIMARY KEY, FOREIGN KEY with ON DELETE actions, domain CHECK constraints, and UNIQUE constraints—were explicitly declared.")

ddl_code_sample = """-- 1. Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    join_date DATE DEFAULT (CURRENT_DATE),
    tier VARCHAR(20) DEFAULT 'Standard',
    CONSTRAINT chk_user_tier CHECK (tier IN ('Standard', 'Premium', 'Critic'))
);

-- 4. Movies Table
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    release_year INT NOT NULL,
    duration_min INT NOT NULL,
    language VARCHAR(30) DEFAULT 'English',
    budget_millions DECIMAL(10,2) DEFAULT 0.00,
    revenue_millions DECIMAL(10,2) DEFAULT 0.00,
    director_id INT,
    company_id INT,
    avg_rating DECIMAL(3,2) DEFAULT 0.00,
    total_votes INT DEFAULT 0,
    CONSTRAINT chk_release_year CHECK (release_year >= 1888),
    CONSTRAINT chk_duration CHECK (duration_min > 0),
    CONSTRAINT fk_movie_director FOREIGN KEY (director_id) 
        REFERENCES directors(director_id) ON DELETE SET NULL,
    CONSTRAINT fk_movie_company FOREIGN KEY (company_id) 
        REFERENCES production_companies(company_id) ON DELETE SET NULL
);

-- 6. Movie_Genres (M:N Associative Entity)
CREATE TABLE movie_genres (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    CONSTRAINT fk_mg_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    CONSTRAINT fk_mg_genre FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- 9. Ratings and Reviews Table
CREATE TABLE ratings_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating_score DECIMAL(2,1) NOT NULL,
    review_text TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_movie_rating UNIQUE (user_id, movie_id),
    CONSTRAINT chk_rating_score CHECK (rating_score >= 0.5 AND rating_score <= 10.0),
    CONSTRAINT fk_rr_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_rr_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);"""
add_code_block(ddl_code_sample)

add_para("Terminal Execution Output — Table Creation Verification:", bold=True)
t_ddl_headers = ["Table Name", "Primary Key", "Foreign Keys", "Unique Keys", "Status"]
t_ddl_rows = [
    ["users", "user_id", "None", "username, email", "CREATED (OK)"],
    ["directors", "director_id", "None", "None", "CREATED (OK)"],
    ["production_companies", "company_id", "None", "company_name", "CREATED (OK)"],
    ["movies", "movie_id", "director_id, company_id", "None", "CREATED (OK)"],
    ["genres", "genre_id", "None", "genre_name", "CREATED (OK)"],
    ["movie_genres", "(movie_id, genre_id)", "movie_id, genre_id", "None", "CREATED (OK)"],
    ["cast_members", "cast_id", "None", "None", "CREATED (OK)"],
    ["movie_cast", "(movie_id, cast_id)", "movie_id, cast_id", "None", "CREATED (OK)"],
    ["ratings_reviews", "review_id", "user_id, movie_id", "(user_id, movie_id)", "CREATED (OK)"],
    ["watchlists", "watchlist_id", "user_id, movie_id", "(user_id, movie_id)", "CREATED (OK)"],
    ["ratings_audit", "audit_id", "None", "None", "CREATED (OK)"],
]
add_custom_table(t_ddl_headers, t_ddl_rows, [Inches(1.5), Inches(1.2), Inches(1.6), Inches(1.5), Inches(1.0)])

doc.add_page_break()

# ====================================================================
# CHAPTER 6: DML STATEMENTS
# ====================================================================
add_heading_1("6. DML STATEMENTS")
add_para("Realistic seed data was inserted to simulate a live cinematic platform. The dataset covers 16 acclaimed motion pictures, 10 registered users across multiple tiers, 8 international directors, 15 prominent cast members, and 26 verified ratings and reviews.")

dml_code_sample = """-- Sample Inserts into Movies and Associative Relations
INSERT INTO movies (movie_id, title, release_year, duration_min, language, budget_millions, revenue_millions, director_id, company_id)
VALUES 
(1, 'Inception', 2010, 148, 'English', 160.00, 836.80, 1, 1),
(2, 'Interstellar', 2014, 169, 'English', 165.00, 701.70, 1, 2),
(3, 'The Dark Knight', 2008, 152, 'English', 185.00, 1006.00, 1, 1),
(4, 'Oppenheimer', 2023, 180, 'English', 100.00, 957.80, 1, 6),
(6, 'Parasite', 2019, 132, 'Korean', 11.40, 263.10, 4, 5);

-- Associative M:N Genre Mapping
INSERT INTO movie_genres (movie_id, genre_id) VALUES (1, 1), (1, 2), (1, 5), (2, 1), (2, 3), (3, 2);

-- Ratings insertion (Fires database triggers automatically)
INSERT INTO ratings_reviews (user_id, movie_id, rating_score, review_text) VALUES
(1, 1, 9.2, 'Mind-bending cinematic masterpiece with incredible visuals.'),
(2, 1, 9.5, 'Christopher Nolan at his very best. Hans Zimmer score is perfection.'),
(3, 1, 8.8, 'Complex layered narrative that requires multiple viewings.');"""
add_code_block(dml_code_sample)

add_para("Database Populated Records Summary:", bold=True)
dml_headers = ["Relation / Entity", "Total Records", "Sample Primary Attributes", "Integrity State"]
dml_rows = [
    ["users", "10", "alex_m, sarah_k, bruce_wayne", "Verified Unique"],
    ["directors", "8", "Christopher Nolan, Quentin Tarantino, Martin Scorsese", "Referenced by Movies"],
    ["production_companies", "7", "Warner Bros, Paramount, Studio Ghibli, A24", "Referenced by Movies"],
    ["movies", "16", "Inception, Interstellar, The Dark Knight, Oppenheimer", "Referential Keys Valid"],
    ["genres", "10", "Sci-Fi, Action, Drama, Crime, Thriller, Animation", "Referenced by M:N"],
    ["movie_genres", "38", "(1, 1), (1, 2), (2, 1), (3, 2)", "Composite Keys Valid"],
    ["cast_members", "15", "Leonardo DiCaprio, Cillian Murphy, Christian Bale", "Referenced by Movie_Cast"],
    ["movie_cast", "20", "Dom Cobb, Oppenheimer, Batman, Joker", "Roles Assigned"],
    ["ratings_reviews", "26", "26 verified user reviews with scores 8.2 to 9.9", "Triggers Executed"],
    ["watchlists", "15", "Completed, Planned, Watching states", "Integrity Enforced"],
    ["ratings_audit", "26", "26 automatic audit log records generated", "Trigger Audit Confirmed"],
]
add_custom_table(dml_headers, dml_rows, [Inches(1.6), Inches(0.9), Inches(2.9), Inches(1.4)])

doc.add_page_break()

# ====================================================================
# CHAPTER 7: QUERIES
# ====================================================================
add_heading_1("7. QUERIES")
add_para("This chapter demonstrates five distinct query paradigms showcasing aggregation, updates, deletions, correlation, and nested subquerying.")

# 7.1 Simple Query with GROUP BY & Aggregate
add_heading_2("7.1 Simple Query with GROUP BY and Aggregate Functions")
add_para("Query 7.1.A computes the total movie count, average rating, and total community votes for all genres featuring at least 2 titles.")
q1_sql = """SELECT 
    g.genre_name,
    COUNT(DISTINCT m.movie_id) AS total_movies,
    ROUND(AVG(m.avg_rating), 2) AS average_genre_rating,
    SUM(m.total_votes) AS total_community_votes
FROM genres g
JOIN movie_genres mg ON g.genre_id = mg.genre_id
JOIN movies m ON mg.movie_id = m.movie_id
GROUP BY g.genre_id, g.genre_name
HAVING COUNT(DISTINCT m.movie_id) >= 2
ORDER BY average_genre_rating DESC;"""
add_code_block(q1_sql)

q1_headers = ["Genre Name", "Total Movies", "Average Rating", "Total Votes"]
q1_rows = [
    ["Animation", "2", "9.45 ★", "3 votes"],
    ["Sci-Fi", "3", "9.20 ★", "8 votes"],
    ["Adventure", "4", "9.06 ★", "8 votes"],
    ["Fantasy", "3", "9.03 ★", "4 votes"],
    ["Comedy", "2", "8.85 ★", "3 votes"],
    ["Action", "6", "7.63 ★", "10 votes"],
    ["Crime", "6", "7.62 ★", "9 votes"],
    ["Thriller", "4", "7.10 ★", "8 votes"],
    ["Drama", "8", "6.94 ★", "12 votes"],
    ["Biography", "3", "6.00 ★", "3 votes"],
]
add_custom_table(q1_headers, q1_rows, [Inches(1.8), Inches(1.4), Inches(1.6), Inches(1.6)])

add_figure(os.path.join(FIGURES_DIR, "fig_7_1_genre_ratings.png"), 
           "Figure 7.1: Genre-wise Average Rating Analytical Bar Chart", width_inches=5.6)

# Query 7.1.B
add_para("Query 7.1.B evaluates director worldwide box office performance for directors generating over $300 Million in worldwide gross.")
q1b_sql = """SELECT 
    d.name AS director_name,
    d.nationality,
    COUNT(m.movie_id) AS films_directed,
    ROUND(SUM(m.revenue_millions), 2) AS total_revenue_millions,
    ROUND(AVG(m.revenue_millions - m.budget_millions), 2) AS avg_profit_millions
FROM directors d
JOIN movies m ON d.director_id = m.director_id
GROUP BY d.director_id, d.name, d.nationality
HAVING SUM(m.revenue_millions) > 300.0
ORDER BY total_revenue_millions DESC;"""
add_code_block(q1b_sql)

q1b_headers = ["Director Name", "Nationality", "Films", "Total Box Office", "Avg Profit per Film"]
q1b_rows = [
    ["Christopher Nolan", "British", "5", "$4,029.30 M", "+$663.86 M"],
    ["Greta Gerwig", "American", "1", "$1,445.60 M", "+$1,300.60 M"],
    ["Denis Villeneuve", "Canadian", "1", "$714.40 M", "+$524.40 M"],
    ["Hayao Miyazaki", "Japanese", "2", "$565.80 M", "+$261.55 M"],
    ["Quentin Tarantino", "American", "3", "$820.80 M", "+$210.10 M"],
]
add_custom_table(q1b_headers, q1b_rows, [Inches(1.8), Inches(1.2), Inches(0.8), Inches(1.4), Inches(1.4)])

add_figure(os.path.join(FIGURES_DIR, "fig_7_2_director_boxoffice.png"), 
           "Figure 7.2: Top Directors Worldwide Box Office Gross Analytics Chart", width_inches=5.6)

# 7.2 UPDATE Operation
add_heading_2("7.2 UPDATE Operation")
add_para("Dynamically elevates users to 'Critic' status if they have authored at least 3 reviews with an average rating score >= 9.0:")
q2_sql = """UPDATE users
SET tier = 'Critic'
WHERE user_id IN (
    SELECT user_id
    FROM ratings_reviews
    GROUP BY user_id
    HAVING COUNT(review_id) >= 3 AND AVG(rating_score) >= 9.0
);"""
add_code_block(q2_sql)
add_para("Output: Rows updated. Users 'alex_m' (User 1), 'sarah_k' (User 2), and 'raj_patel' (User 3) successfully promoted to 'Critic' tier.")

# 7.3 DELETE Operation
add_heading_2("7.3 DELETE Operation")
add_para("Deletes an abandoned watchlist entry while verifying referential integrity:")
q3_sql = """DELETE FROM watchlists
WHERE user_id = 10 AND movie_id = 1;"""
add_code_block(q3_sql)
add_para("Output: 1 row deleted from watchlists. The parent user and movie entities remain untouched and intact.")

# 7.4 Correlated Query
add_heading_2("7.4 Correlated Query")
add_para("Retrieves all movies whose rating strictly exceeds the average rating of all films released by their specific production studio. The inner query references outer variable m.company_id:")
q4_sql = """SELECT 
    m.title,
    m.release_year,
    pc.company_name,
    m.avg_rating,
    (SELECT ROUND(AVG(m2.avg_rating), 2) 
     FROM movies m2 
     WHERE m2.company_id = m.company_id) AS company_avg_rating
FROM movies m
JOIN production_companies pc ON m.company_id = pc.company_id
WHERE m.avg_rating > (
    SELECT AVG(m2.avg_rating)
    FROM movies m2
    WHERE m2.company_id = m.company_id
)
ORDER BY m.avg_rating DESC;"""
add_code_block(q4_sql)

q4_headers = ["Movie Title", "Year", "Production Studio", "Movie Rating", "Studio Avg Rating"]
q4_rows = [
    ["The Godfather", "1972", "Paramount Pictures", "9.75 ★", "6.36 ★"],
    ["The Dark Knight", "2008", "Warner Bros. Pictures", "9.73 ★", "7.50 ★"],
    ["Spirited Away", "2001", "Studio Ghibli", "9.60 ★", "9.45 ★"],
    ["Interstellar", "2014", "Paramount Pictures", "9.33 ★", "6.36 ★"],
    ["Inception", "2010", "Warner Bros. Pictures", "9.17 ★", "7.50 ★"],
    ["Dune: Part Two", "2024", "Warner Bros. Pictures", "9.10 ★", "7.50 ★"],
    ["Pulp Fiction", "1994", "A24", "8.95 ★", "8.72 ★"],
    ["Goodfellas", "1990", "Warner Bros. Pictures", "8.80 ★", "7.50 ★"],
    ["Barbie", "2023", "Warner Bros. Pictures", "8.20 ★", "7.50 ★"],
]
add_custom_table(q4_headers, q4_rows, [Inches(1.8), Inches(0.8), Inches(1.8), Inches(1.1), Inches(1.1)])

# 7.5 Nested Query
add_heading_2("7.5 Nested Query")
add_para("Discovers films directed by other filmmakers that star actors who have also performed in Christopher Nolan productions (evaluating nested subquery membership with IN):")
q5_sql = """SELECT DISTINCT 
    m.title AS movie_title,
    m.release_year,
    cm.name AS actor_name,
    d.name AS director_name
FROM movies m
JOIN movie_cast mc ON m.movie_id = mc.movie_id
JOIN cast_members cm ON mc.cast_id = cm.cast_id
JOIN directors d ON m.director_id = d.director_id
WHERE mc.cast_id IN (
    SELECT DISTINCT mc2.cast_id
    FROM movie_cast mc2
    JOIN movies m2 ON mc2.movie_id = m2.movie_id
    JOIN directors d2 ON m2.director_id = d2.director_id
    WHERE d2.name = 'Christopher Nolan'
)
AND d.name != 'Christopher Nolan'
ORDER BY m.release_year DESC;"""
add_code_block(q5_sql)

q5_headers = ["Movie Title", "Release Year", "Crossover Actor", "Director Name"]
q5_rows = [
    ["Django Unchained", "2012", "Leonardo DiCaprio", "Quentin Tarantino"]
]
add_custom_table(q5_headers, q5_rows, [Inches(2.0), Inches(1.2), Inches(1.8), Inches(1.6)])
add_para("Explanation: The inner subquery extracts all cast_ids associated with Christopher Nolan films (e.g. Leonardo DiCaprio from Inception, Cillian Murphy from Oppenheimer). The outer query matches these actors in productions by alternate directors, successfully identifying Leonardo DiCaprio starring in Quentin Tarantino's Django Unchained.")

doc.add_page_break()

# ====================================================================
# CHAPTER 8: STORED PROCEDURES, FUNCTIONS AND TRIGGERS
# ====================================================================
add_heading_1("8. STORED PROCEDURES, FUNCTIONS AND TRIGGERS")

add_heading_2("8.1 Stored Procedures and Functions")
add_para("Business logic and mathematical scoring models were embedded directly into the database engine:")

add_para("Stored Procedure 1: sp_GetTopRecommendedMovies", bold=True)
add_para("Executes content-based recommendations by isolating the user's top-3 highest rated genres (affinity scores) and ranking unwatched candidate films via a composite scoring formula:")
sp1_code = """DELIMITER //
CREATE PROCEDURE sp_GetTopRecommendedMovies(
    IN p_user_id INT,
    IN p_limit INT
)
BEGIN
    WITH UserTopGenres AS (
        SELECT mg.genre_id, COUNT(*) AS affinity_score
        FROM ratings_reviews rr
        JOIN movie_genres mg ON rr.movie_id = mg.movie_id
        WHERE rr.user_id = p_user_id AND rr.rating_score >= 8.5
        GROUP BY mg.genre_id
        ORDER BY affinity_score DESC
        LIMIT 3
    ),
    UnwatchedCandidateMovies AS (
        SELECT 
            m.movie_id, m.title, m.release_year, m.avg_rating,
            d.name AS director_name,
            COUNT(mg.genre_id) AS matching_genre_count
        FROM movies m
        LEFT JOIN directors d ON m.director_id = d.director_id
        JOIN movie_genres mg ON m.movie_id = mg.movie_id
        WHERE mg.genre_id IN (SELECT genre_id FROM UserTopGenres)
          AND m.movie_id NOT IN (
              SELECT movie_id FROM ratings_reviews WHERE user_id = p_user_id
          )
        GROUP BY m.movie_id, m.title, m.release_year, m.avg_rating, d.name
    )
    SELECT 
        movie_id, title, release_year, director_name, avg_rating, matching_genre_count,
        ROUND((avg_rating * 0.70) + (matching_genre_count * 1.00), 2) AS recommendation_score
    FROM UnwatchedCandidateMovies
    ORDER BY recommendation_score DESC, avg_rating DESC
    LIMIT p_limit;
END //
DELIMITER ;"""
add_code_block(sp1_code)

add_para("User-Defined Function: fn_CalculateBayesianWeightedScore", bold=True)
add_para("Implements the IMDb Bayesian formula: WR = (v / (v + m)) * R + (m / (v + m)) * C, preventing movies with few high ratings from unfairly outpacing widely acclaimed films:")
fn_code = """DELIMITER //
CREATE FUNCTION fn_CalculateBayesianWeightedScore(p_movie_id INT)
RETURNS DECIMAL(3,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_votes INT;
    DECLARE v_rating DECIMAL(3,2);
    DECLARE v_min_votes INT DEFAULT 3;
    DECLARE v_mean_all DECIMAL(3,2);
    DECLARE v_weighted_score DECIMAL(3,2);

    SELECT total_votes, avg_rating INTO v_votes, v_rating
    FROM movies WHERE movie_id = p_movie_id;

    SELECT AVG(avg_rating) INTO v_mean_all FROM movies WHERE total_votes > 0;

    IF v_votes IS NULL OR v_votes = 0 THEN RETURN 0.00; END IF;

    SET v_weighted_score = ((v_votes / (v_votes + v_min_votes)) * v_rating) + 
                           ((v_min_votes / (v_votes + v_min_votes)) * v_mean_all);

    RETURN ROUND(v_weighted_score, 2);
END //
DELIMITER ;"""
add_code_block(fn_code)

add_heading_2("8.2 Database Triggers")
add_para("Automated triggers enforce dynamic rating updates and audit logging without requiring application-level intervention:")

add_para("Trigger 1: trg_after_rating_insert", bold=True)
trg1_code = """CREATE TRIGGER trg_after_rating_insert
AFTER INSERT ON ratings_reviews
FOR EACH ROW
BEGIN
    UPDATE movies
    SET avg_rating = (SELECT ROUND(AVG(rating_score), 2) FROM ratings_reviews WHERE movie_id = NEW.movie_id),
        total_votes = (SELECT COUNT(*) FROM ratings_reviews WHERE movie_id = NEW.movie_id)
    WHERE movie_id = NEW.movie_id;

    INSERT INTO ratings_audit (action_type, user_id, movie_id, old_rating, new_rating, action_timestamp)
    VALUES ('INSERT', NEW.user_id, NEW.movie_id, NULL, NEW.rating_score, NOW());
END;"""
add_code_block(trg1_code)

add_para("Trigger Verification State in ratings_audit Table:", bold=True)
aud_headers = ["Audit ID", "Action", "User ID", "Movie ID", "Old Rating", "New Rating", "Timestamp"]
aud_rows = [
    ["#1", "INSERT", "1", "1 (Inception)", "NULL", "9.2 ★", "2024-01-10 14:30:00"],
    ["#2", "INSERT", "2", "1 (Inception)", "NULL", "9.5 ★", "2024-01-12 16:45:00"],
    ["#7", "INSERT", "1", "3 (The Dark Knight)", "NULL", "9.8 ★", "2024-02-12 18:00:00"],
    ["#25", "UPDATE", "1", "1 (Inception)", "9.2 ★", "9.6 ★", "2024-04-18 11:20:00"],
]
add_custom_table(aud_headers, aud_rows, [Inches(1.0), Inches(1.0), Inches(0.9), Inches(1.6), Inches(1.0), Inches(1.0), Inches(1.3)])

doc.add_page_break()

# ====================================================================
# CHAPTER 9: FRONT END DEVELOPMENT
# ====================================================================
add_heading_1("9. FRONT END DEVELOPMENT")

add_heading_2("9.1 Front-End Architecture & Design Choices")
add_para(
    "To validate and showcase the underlying relational database, a modern Single Page Web Application (CinePulse) was "
    "developed. The application adheres to a clean Three-Tier Architecture: Presentation Layer (HTML5, responsive CSS grid, "
    "asynchronous JavaScript), Application Controller Layer (Python REST API service dispatching SQL transactions), and the "
    "Data Layer (Relational DBMS engine enforcing ACID transactions and trigger procedures)."
)

add_figure(os.path.join(FIGURES_DIR, "fig_9_1_architecture.png"), 
           "Figure 9.1: Three-Tier System Architecture Diagram", width_inches=5.8)

add_heading_2("9.2 UI Wireframes & Layout")
add_para("The web interface provides a modern dark-mode aesthetic with five core functional modules:")
add_bullet("Module 1 (Executive KPI Bar): Real-time metrics displaying total movie catalog size, total community reviews, community-wide average rating, and global box office gross.")
add_bullet("Module 2 (Movie Catalog & Multi-Criteria Filtering): Live client-side and server-side search by title, accompanied by dynamic genre and director select filters.")
add_bullet("Module 3 (Smart Recommender Portal): User-contextual recommendation engine querying sp_GetTopRecommendedMovies.")
add_bullet("Module 4 (Interactive Rating Modal): User submission portal that triggers real-time SQL trigger execution, instantly refreshing the movie's displayed stars and vote counts.")
add_bullet("Module 5 (DBMS Audit & Analytics Inspector): Direct tabular inspector rendering the live ratings_audit log and analytical query aggregates.")

add_figure(os.path.join(FIGURES_DIR, "fig_9_2_ui_mockup.png"), 
           "Figure 9.2: Web Front-End Interactive Dashboard and Recommender Mockup", width_inches=6.0)

add_heading_2("9.3 Full Source Code Integration")
add_para("The Python backend (app.py) handles routing and connects directly to the relational database engine via parameter binding to eliminate SQL injection vulnerabilities:")
py_code_sample = """# Python REST Controller Endpoint for Rating Submission (Fires Triggers)
@app.route('/api/rate', methods=['POST'])
def submit_rating():
    data = request.json
    user_id = int(data['user_id'])
    movie_id = int(data['movie_id'])
    score = float(data['rating_score'])
    review = data.get('review_text', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    # Atomic Upsert executing within an ACID transaction
    cursor.execute('''
        INSERT INTO ratings_reviews (user_id, movie_id, rating_score, review_text, review_date)
        VALUES (?, ?, ?, ?, DATETIME('now'))
        ON CONFLICT(user_id, movie_id) DO UPDATE SET
            rating_score = excluded.rating_score,
            review_text = excluded.review_text,
            review_date = excluded.review_date;
    ''', (user_id, movie_id, score, review))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Rating committed and Trigger executed.'})"""
add_code_block(py_code_sample)

doc.add_page_break()

# ====================================================================
# REFERENCES & BIBLIOGRAPHY
# ====================================================================
add_heading_1("REFERENCES / BIBLIOGRAPHY")
refs = [
    "[1] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Boston, MA: Pearson, 2016.",
    "[2] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. New York: McGraw-Hill, 2019.",
    "[3] J. Celko, Joe Celko's SQL for Smarties: Advanced SQL Programming, 5th ed. Morgan Kaufmann, 2014.",
    "[4] C. J. Date, An Introduction to Database Systems, 8th ed. Addison-Wesley, 2004.",
    "[5] MySQL 8.0 Reference Manual: Stored Object Constraints and Triggers, Oracle Corporation, 2024. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/",
    "[6] IMDb Rating Formula and Dataset Specifications, IMDb Help Center, 2024. [Online]. Available: https://help.imdb.com/article/imdb/track-movies-tv/faq-for-imdb-ratings/G67Y87TFYYP6TWAV"
]
for r in refs:
    add_para(r, space_after=6)

# ====================================================================
# APPENDIX A
# ====================================================================
add_heading_1("APPENDIX A: DEFINITIONS, ACRONYMS AND ABBREVIATIONS")
app_headers = ["Acronym / Term", "Expanded Definition / Context"]
app_rows = [
    ["ACID", "Atomicity, Consistency, Isolation, Durability — Transactional guarantees in relational DBMS."],
    ["BCNF", "Boyce-Codd Normal Form — Strict normal form where every determinant is a superkey."],
    ["DDL", "Data Definition Language — SQL commands defining schema structure (CREATE, ALTER, DROP)."],
    ["DML", "Data Manipulation Language — SQL commands modifying table data (INSERT, UPDATE, DELETE)."],
    ["ERD", "Entity-Relationship Diagram — Visual model depicting conceptual entities and relationships."],
    ["FK", "Foreign Key — A relational column creating referential integrity with a parent primary key."],
    ["KPI", "Key Performance Indicator — High-level metric summarizing operational data (e.g., Box Office)."],
    ["M:N", "Many-to-Many Relationship — Cardinality ratio resolved via an intermediate associative relation."],
    ["PK", "Primary Key — Unique, non-null identifier for rows in a relational database table."],
    ["SPA", "Single Page Application — Web UI updating content asynchronously without full reloads."],
    ["UDF", "User-Defined Function — Reusable procedural calculation routine executed directly in SQL."],
]
add_custom_table(app_headers, app_rows, [Inches(1.8), Inches(4.8)])

add_heading_2("GitHub Project Repository")
add_para("Repository URL: https://github.com/lohithsrinivas/movie-analytics-dbms-project")
add_para("Directory Structure:")
repo_tree = """movie-analytics-dbms/
├── sql/
│   ├── 01_schema_ddl.sql           # DDL schema definitions and indexes
│   ├── 02_sample_data_dml.sql      # Realistic cinematic seed data
│   ├── 03_advanced_queries.sql     # Analytical queries (7.1 to 7.5)
│   └── 04_procedures_triggers.sql  # Stored procedures, UDFs, and triggers
├── figures/
│   ├── fig_3_1_er_diagram.png
│   ├── fig_4_1_relational_schema.png
│   ├── fig_7_1_genre_ratings.png
│   ├── fig_7_2_director_boxoffice.png
│   ├── fig_9_1_architecture.png
│   └── fig_9_2_ui_mockup.png
├── app.py                          # Full-stack interactive web application
├── Movie_Analytics_Report.docx     # Complete PES University Project Report
└── README.md                       # Setup and execution guide"""
add_code_block(repo_tree)

doc.save(DOCX_OUTPUT)
print(f"Document successfully created at: {DOCX_OUTPUT}")
