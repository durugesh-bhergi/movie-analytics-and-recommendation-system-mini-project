"""
Generate visual diagrams and analytical charts for the DBMS Mini Project Report.
Uses matplotlib to generate clean, high-resolution figures.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. ER Diagram Visualization
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#ffffff')

    # Title
    ax.text(50, 96, "Figure 3.1: Entity-Relationship Diagram (ERD)\nMovie Analytics & Recommendation System", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1A365D')

    # Entity box styling
    entity_color = '#EBF8FF'
    entity_border = '#2B6CB0'
    rel_color = '#FEFCBF'
    rel_border = '#B7791F'

    # Entities
    entities = {
        'USERS': (15, 75, 18, 10, ['user_id (PK)', 'username (U)', 'email (U)', 'full_name', 'join_date', 'tier']),
        'MOVIES': (50, 50, 20, 14, ['movie_id (PK)', 'title', 'release_year', 'duration_min', 'avg_rating', 'budget_millions', 'revenue_millions', 'director_id (FK)', 'company_id (FK)']),
        'DIRECTORS': (85, 75, 18, 10, ['director_id (PK)', 'name', 'birth_year', 'nationality', 'awards_count']),
        'COMPANIES': (85, 30, 18, 10, ['company_id (PK)', 'company_name (U)', 'headquarters', 'founded_year']),
        'GENRES': (15, 25, 18, 8, ['genre_id (PK)', 'genre_name (U)', 'description']),
        'CAST_MEMBERS': (50, 10, 20, 8, ['cast_id (PK)', 'name', 'gender', 'birth_year']),
    }

    # Draw entities
    for name, (x, y, w, h, attrs) in entities.items():
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.5",
                                      facecolor=entity_color, edgecolor=entity_border, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 1.8, name, ha='center', va='center', fontsize=10, fontweight='bold', color='#1A365D')
        
        # Attributes
        attr_text = "\n".join(attrs)
        ax.text(x, y - 0.5, attr_text, ha='center', va='center', fontsize=7.5, color='#2D3748', family='monospace')

    # Relationships (Diamonds)
    relationships = [
        ('RATES / REVIEWS', 32, 63, '1:N', 'ratings_reviews\n(rating_score, review_text)'),
        ('WATCHLIST', 28, 78, 'M:N', 'status, added_date'),
        ('DIRECTS', 68, 63, '1:N', '1 director -> N movies'),
        ('PRODUCES', 68, 40, '1:N', '1 company -> N movies'),
        ('BELONGS_TO', 32, 38, 'M:N', 'movie_genres'),
        ('ACTS_IN', 50, 30, 'M:N', 'movie_cast\n(role_name, lead_order)'),
    ]

    for name, rx, ry, card, desc in relationships:
        # Diamond
        diamond = patches.RegularPolygon((rx, ry), numVertices=4, radius=4.5,
                                         facecolor=rel_color, edgecolor=rel_border, linewidth=1.5)
        ax.add_patch(diamond)
        ax.text(rx, ry + 0.3, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#744210')
        ax.text(rx, ry - 3.2, f"[{card}]", ha='center', va='center', fontsize=7, color='#975A16', fontweight='bold')

    # Draw Connections
    ax.annotate("", xy=(24, 73), xytext=(28, 66), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))
    ax.annotate("", xy=(40, 56), xytext=(36, 60), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))

    ax.annotate("", xy=(76, 73), xytext=(72, 66), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))
    ax.annotate("", xy=(60, 56), xytext=(64, 60), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))

    ax.annotate("", xy=(76, 32), xytext=(72, 38), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))
    ax.annotate("", xy=(60, 44), xytext=(64, 42), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))

    ax.annotate("", xy=(24, 28), xytext=(28, 35), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))
    ax.annotate("", xy=(40, 44), xytext=(36, 41), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))

    ax.annotate("", xy=(50, 43), xytext=(50, 35), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))
    ax.annotate("", xy=(50, 25), xytext=(50, 14), arrowprops=dict(arrowstyle="-", color='#4A5568', lw=1.5))

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_3_1_er_diagram.png"), bbox_inches='tight')
    plt.close()
    print("ER Diagram generated.")

# 2. Relational Mapping Diagram
def generate_relational_schema_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(50, 95, "Figure 4.1: Relational Schema Mapping & Foreign Key References", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1A365D')

    tables = [
        ("USERS", 18, 80, ["user_id (PK)", "username", "email", "full_name", "join_date", "tier"]),
        ("DIRECTORS", 50, 80, ["director_id (PK)", "name", "birth_year", "nationality", "awards_count"]),
        ("COMPANIES", 82, 80, ["company_id (PK)", "company_name", "headquarters", "founded_year"]),
        ("MOVIES", 50, 50, ["movie_id (PK)", "title", "release_year", "duration_min", "director_id (FK)", "company_id (FK)", "avg_rating", "budget", "revenue"]),
        ("GENRES", 18, 20, ["genre_id (PK)", "genre_name", "description"]),
        ("MOVIE_GENRES", 35, 33, ["movie_id (PK, FK)", "genre_id (PK, FK)"]),
        ("MOVIE_CAST", 65, 33, ["movie_id (PK, FK)", "cast_id (PK, FK)", "role_name", "lead_order"]),
        ("CAST_MEMBERS", 82, 20, ["cast_id (PK)", "name", "gender", "birth_year"]),
        ("RATINGS_REVIEWS", 18, 50, ["review_id (PK)", "user_id (FK)", "movie_id (FK)", "rating_score", "review_text", "review_date"]),
        ("WATCHLISTS", 82, 50, ["watchlist_id (PK)", "user_id (FK)", "movie_id (FK)", "status", "added_date"]),
    ]

    for name, x, y, cols in tables:
        w = 17
        h = 2.0 + len(cols)*1.6
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="square,pad=0.2",
                                      facecolor='#EDF2F7', edgecolor='#4A5568', linewidth=1.2)
        ax.add_patch(rect)
        # Header banner
        header_rect = patches.Rectangle((x - w/2, y + h/2 - 2.2), w, 2.2, facecolor='#2B6CB0', edgecolor='#2B6CB0')
        ax.add_patch(header_rect)
        ax.text(x, y + h/2 - 1.1, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')

        # Columns
        col_y = y + h/2 - 3.2
        for c in cols:
            is_pk = "(PK)" in c
            is_fk = "(FK)" in c
            color = '#C53030' if is_pk else ('#2B6CB0' if is_fk else '#2D3748')
            weight = 'bold' if (is_pk or is_fk) else 'normal'
            ax.text(x - w/2 + 0.8, col_y, c, ha='left', va='center', fontsize=6.8, color=color, fontweight=weight, family='monospace')
            col_y -= 1.6

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_4_1_relational_schema.png"), bbox_inches='tight')
    plt.close()
    print("Relational schema diagram generated.")

# 3. Analytical Charts
def generate_analytical_charts():
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect(r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\movie_analytics.db")

    # Chart 1: Genre Avg Rating
    q1 = """
    SELECT g.genre_name, ROUND(AVG(m.avg_rating), 2) AS avg_rating
    FROM genres g
    JOIN movie_genres mg ON g.genre_id = mg.genre_id
    JOIN movies m ON mg.movie_id = m.movie_id
    GROUP BY g.genre_name
    ORDER BY avg_rating ASC;
    """
    df1 = pd.read_sql_query(q1, conn)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    bars = ax.barh(df1['genre_name'], df1['avg_rating'], color='#3182CE', edgecolor='#2B6CB0')
    ax.set_xlabel('Average Community Rating (Scale 0-10)', fontsize=10, fontweight='bold')
    ax.set_title('Figure 7.1: Average Movie Rating Across Genres', fontsize=12, fontweight='bold', color='#1A365D')
    ax.set_xlim(0, 10.5)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.1, bar.get_y() + bar.get_height()/2, f'{w:.2f}', va='center', fontsize=8.5, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_7_1_genre_ratings.png"), bbox_inches='tight')
    plt.close()

    # Chart 2: Director Box Office
    q2 = """
    SELECT d.name, ROUND(SUM(m.revenue_millions), 2) AS total_revenue
    FROM directors d
    JOIN movies m ON d.director_id = m.director_id
    GROUP BY d.name
    ORDER BY total_revenue DESC
    LIMIT 5;
    """
    df2 = pd.read_sql_query(q2, conn)
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    bars = ax.bar(df2['name'], df2['total_revenue'], color='#38A169', edgecolor='#276749')
    ax.set_ylabel('Total Box Office Gross ($ Millions)', fontsize=10, fontweight='bold')
    ax.set_title('Figure 7.2: Top 5 Directors by Worldwide Box Office Revenue', fontsize=12, fontweight='bold', color='#1A365D')
    plt.xticks(rotation=20, ha='right', fontsize=9)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 30, f'${h:.1f}M', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    ax.set_ylim(0, max(df2['total_revenue']) * 1.15)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_7_2_director_boxoffice.png"), bbox_inches='tight')
    plt.close()

    conn.close()
    print("Analytical charts generated.")

# 4. Three-Tier System Architecture
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    ax.text(50, 46, "Figure 9.1: Three-Tier System Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    tiers = [
        ("Presentation Layer (Client)", 18, 25, 24, 26, 
         ["Web Browser UI", "HTML5 / CSS3 / JavaScript", "Dashboard & Search Views", "Rating Submission Portal"], '#EBF8FF', '#3182CE'),
        ("Application Layer (Server)", 50, 25, 24, 26, 
         ["Python Web Controller", "Recommendation Engine", "Business Logic & Auth", "Query Builder & Dispatcher"], '#FEFCBF', '#D69E2E'),
        ("Data Layer (DBMS)", 82, 25, 24, 26, 
         ["Relational DBMS (MySQL/SQLite)", "ACID Engine & B-Tree Indexes", "Stored Procedures & UDFs", "Trigger Auditing & Integrity"], '#F0FFF4', '#38A169'),
    ]

    for name, x, y, w, h, items, bg, border in tiers:
        rect = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.5",
                                      facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 2.5, name, ha='center', va='center', fontsize=9, fontweight='bold', color='#1A202C')
        
        iy = y + h/2 - 6.5
        for item in items:
            ax.text(x, iy, f"• {item}", ha='center', va='center', fontsize=7.5, color='#4A5568')
            iy -= 4.2

    # Communication Arrows
    ax.annotate("HTTP / JSON\nRequests", xy=(38, 28), xytext=(30, 28),
                arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2),
                ha='center', va='center', fontsize=7.5, fontweight='bold')
    ax.annotate("Rendered UI /\nResponses", xy=(30, 22), xytext=(38, 22),
                arrowprops=dict(arrowstyle="->", color='#2B6CB0', lw=2),
                ha='center', va='center', fontsize=7.5, fontweight='bold')

    ax.annotate("SQL Queries /\nProcedures", xy=(70, 28), xytext=(62, 28),
                arrowprops=dict(arrowstyle="->", color='#38A169', lw=2),
                ha='center', va='center', fontsize=7.5, fontweight='bold')
    ax.annotate("Result Sets /\nRecord Data", xy=(62, 22), xytext=(70, 22),
                arrowprops=dict(arrowstyle="->", color='#38A169', lw=2),
                ha='center', va='center', fontsize=7.5, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_9_1_architecture.png"), bbox_inches='tight')
    plt.close()
    print("Architecture diagram generated.")

if __name__ == '__main__':
    generate_er_diagram()
    generate_relational_schema_diagram()
    generate_analytical_charts()
    generate_architecture_diagram()
    print("All diagrams generated successfully!")
