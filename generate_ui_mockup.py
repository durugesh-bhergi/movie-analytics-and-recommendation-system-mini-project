"""
Generate Figure 9.2: Front-End UI Mockup image using matplotlib
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUTPUT_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\movie_analytics_dbms\figures"

def generate_ui_mockup():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0B0F19')

    # Browser frame
    frame = patches.FancyBboxPatch((2, 2), 96, 94, boxstyle="round,pad=0.5",
                                   facecolor='#131B2E', edgecolor='#2D3748', linewidth=2)
    ax.add_patch(frame)

    # Browser header bar
    header_bar = patches.Rectangle((2, 90), 96, 6, facecolor='#0F172A', edgecolor='#2D3748')
    ax.add_patch(header_bar)
    # Circle buttons
    for i, c in enumerate(['#EF4444', '#F59E0B', '#10B981']):
        circle = patches.Circle((5 + i*2.5, 93), 0.8, facecolor=c)
        ax.add_patch(circle)

    ax.text(50, 93, "CinePulse | Movie Analytics & Recommendation System — http://localhost:8080", 
            ha='center', va='center', fontsize=9, color='#94A3B8', family='monospace')

    # App Navbar
    nav = patches.Rectangle((2, 82), 96, 8, facecolor='#1E293B', edgecolor='#2D3748')
    ax.add_patch(nav)
    ax.text(6, 86, "CP  CinePulse Analytics", ha='left', va='center', fontsize=11, fontweight='bold', color='#38BDF8')
    ax.text(94, 86, "[Movie Catalog]   [Smart Recommender]   [SQL Analytics]   [Audit Logs]", 
            ha='right', va='center', fontsize=8, color='#E2E8F0', fontweight='bold')

    # KPI row
    kpis = [
        ("TOTAL TITLES", "16 Movies", 14),
        ("COMMUNITY REVIEWS", "26 Reviews", 38),
        ("AVERAGE RATING", "9.18 ★", 62),
        ("BOX OFFICE GROSS", "$8,383.0M", 86)
    ]
    for lbl, val, kx in kpis:
        kbox = patches.FancyBboxPatch((kx - 10, 70), 20, 8, boxstyle="round,pad=0.3",
                                      facecolor='#1C2640', edgecolor='#3B82F6', linewidth=1.2)
        ax.add_patch(kbox)
        ax.text(kx, 75, lbl, ha='center', va='center', fontsize=6.5, color='#94A3B8', fontweight='bold')
        ax.text(kx, 72, val, ha='center', va='center', fontsize=9.5, color='#F8FAFC', fontweight='bold')

    # Search bar
    sbar = patches.FancyBboxPatch((5, 62), 90, 5, boxstyle="round,pad=0.2",
                                  facecolor='#1C2640', edgecolor='#2D3748')
    ax.add_patch(sbar)
    ax.text(8, 64.5, "🔍 Search movie titles...                 | Filter by Genre: [All Genres ▾]  | Filter by Director: [All Directors ▾]", 
            ha='left', va='center', fontsize=7.5, color='#94A3B8')

    # Movie cards grid
    cards = [
        ("The Dark Knight (2008)", "★ 9.7", "Dir: Christopher Nolan", ["Action", "Crime", "Thriller"], "$185M / $1006M", 20, 46),
        ("Inception (2010)", "★ 9.2", "Dir: Christopher Nolan", ["Sci-Fi", "Action", "Thriller"], "$160M / $837M", 50, 46),
        ("Interstellar (2014)", "★ 9.3", "Dir: Christopher Nolan", ["Sci-Fi", "Drama", "Adventure"], "$165M / $702M", 80, 46),
        ("Pulp Fiction (1994)", "★ 9.0", "Dir: Quentin Tarantino", ["Crime", "Drama"], "$8.5M / $214M", 20, 24),
        ("Parasite (2019)", "★ 9.5", "Dir: Bong Joon-ho", ["Thriller", "Drama", "Comedy"], "$11.4M / $263M", 50, 24),
        ("Spirited Away (2001)", "★ 9.6", "Dir: Hayao Miyazaki", ["Animation", "Fantasy"], "$19.2M / $396M", 80, 24),
    ]

    for title, rating, director, genres, fin, cx, cy in cards:
        cbox = patches.FancyBboxPatch((cx - 13, cy - 8), 26, 17, boxstyle="round,pad=0.4",
                                      facecolor='#1C2640', edgecolor='#2D3748', linewidth=1)
        ax.add_patch(cbox)
        ax.text(cx - 11, cy + 6, title, ha='left', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF')
        ax.text(cx + 10, cy + 6, rating, ha='right', va='center', fontsize=7.8, fontweight='bold', color='#F59E0B')
        ax.text(cx - 11, cy + 2.5, director, ha='left', va='center', fontsize=6.8, color='#94A3B8')
        
        # tags
        ax.text(cx - 11, cy - 0.8, " • ".join(genres), ha='left', va='center', fontsize=6.5, color='#60A5FA')
        ax.text(cx - 11, cy - 4.2, f"Budget/Gross: {fin}", ha='left', va='center', fontsize=6.5, color='#34D399')

        # button
        btn = patches.FancyBboxPatch((cx + 2, cy - 6.5), 8, 2.5, boxstyle="round,pad=0.2",
                                     facecolor='#3B82F6', edgecolor='#2563EB')
        ax.add_patch(btn)
        ax.text(cx + 6, cy - 5.2, "Rate", ha='center', va='center', fontsize=6.5, fontweight='bold', color='#FFFFFF')

    # Footer banner
    ax.text(50, 4, "PES University | Department of Computer Science & Engineering | UE23CS351A Mini Project", 
            ha='center', va='center', fontsize=8, color='#64748B')

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "fig_9_2_ui_mockup.png"), bbox_inches='tight')
    plt.close()
    print("UI Mockup image generated.")

if __name__ == '__main__':
    generate_ui_mockup()
