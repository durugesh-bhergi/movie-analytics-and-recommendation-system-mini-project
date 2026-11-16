"""
Movie Analytics & Recommendation System - Complete Database Setup & Test Script
Course: UE23CS351A - DBMS Project | PES University

Features:
- DDL Schema Execution (16 normalized relations with PK, FK, CHECK, and UNIQUE constraints)
- Database-backed Role-Based Access Control (RBAC) with hashed credentials
- Hierarchical Movie Franchises & Recursive Query Execution (WITH RECURSIVE)
- Database Triggers for automated statistics recalculation and audit trails
- Full DML Seeding (Acclaimed films, franchises, directors, cast, reviews, watchlists)
"""
import sqlite3
import os
import hashlib

DB_DIR = r"C:\Users\Admin\Desktop\DBMS LAB\movie_analytics_dbms"
DB_PATH = os.path.join(DB_DIR, "movie_analytics.db")

def hash_pw(pw, salt):
    return hashlib.sha256((pw + salt).encode('utf-8')).hexdigest()

def build_database():
    print(f"Building Database at: {DB_PATH}")
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Existing database removed.")
        except Exception as e:
            print(f"Note: {e}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==========================================
    # 1. DDL: Schema Creation
    # ==========================================
    ddl = """
    -- 1. Roles Table (RBAC)
    CREATE TABLE roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name VARCHAR(30) NOT NULL UNIQUE,
        description VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT (DATETIME('now')),
        CHECK (role_name IN ('ADMIN', 'CRITIC', 'USER'))
    );

    -- 2. Permissions Table
    CREATE TABLE permissions (
        permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        permission_key VARCHAR(50) NOT NULL UNIQUE,
        module VARCHAR(50) NOT NULL,
        description VARCHAR(255) NOT NULL
    );

    -- 3. Role Permissions (M:N)
    CREATE TABLE role_permissions (
        role_id INT NOT NULL,
        permission_id INT NOT NULL,
        PRIMARY KEY (role_id, permission_id),
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
        FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE
    );

    -- 4. Users Table
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        salt VARCHAR(64) NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        join_date DATE DEFAULT (DATE('now')),
        tier VARCHAR(20) DEFAULT 'Standard' CHECK (tier IN ('Standard', 'Premium', 'Critic')),
        is_active BOOLEAN DEFAULT 1
    );

    -- 5. User Roles (M:N)
    CREATE TABLE user_roles (
        user_id INT NOT NULL,
        role_id INT NOT NULL,
        assigned_at DATETIME DEFAULT (DATETIME('now')),
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    );

    -- 6. Directors Table
    CREATE TABLE directors (
        director_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        birth_year INT CHECK (birth_year >= 1850),
        nationality VARCHAR(50) DEFAULT 'Unknown',
        awards_count INT DEFAULT 0 CHECK (awards_count >= 0)
    );

    -- 7. Production Companies Table
    CREATE TABLE production_companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name VARCHAR(100) NOT NULL UNIQUE,
        headquarters VARCHAR(100),
        founded_year INT CHECK (founded_year >= 1800)
    );

    -- 8. Movie Franchises Table (For Recursive Queries)
    CREATE TABLE movie_franchises (
        franchise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        franchise_name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        founded_year INT
    );

    -- 9. Movies Table
    CREATE TABLE movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(150) NOT NULL,
        release_year INT NOT NULL CHECK (release_year >= 1888),
        duration_min INT NOT NULL CHECK (duration_min > 0),
        language VARCHAR(30) DEFAULT 'English',
        budget_millions DECIMAL(10,2) CHECK (budget_millions >= 0),
        revenue_millions DECIMAL(10,2) CHECK (revenue_millions >= 0),
        director_id INT,
        company_id INT,
        franchise_id INT,
        parent_movie_id INT,
        sequence_order INT DEFAULT 1 CHECK (sequence_order >= 1),
        avg_rating DECIMAL(3,2) DEFAULT 0.00,
        total_votes INT DEFAULT 0,
        FOREIGN KEY (director_id) REFERENCES directors(director_id) ON DELETE SET NULL,
        FOREIGN KEY (company_id) REFERENCES production_companies(company_id) ON DELETE SET NULL,
        FOREIGN KEY (franchise_id) REFERENCES movie_franchises(franchise_id) ON DELETE SET NULL,
        FOREIGN KEY (parent_movie_id) REFERENCES movies(movie_id) ON DELETE SET NULL
    );

    -- 10. Genres Table
    CREATE TABLE genres (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT
    );

    -- 11. Movie_Genres (M:N)
    CREATE TABLE movie_genres (
        movie_id INT NOT NULL,
        genre_id INT NOT NULL,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
    );

    -- 12. Cast Members Table
    CREATE TABLE cast_members (
        cast_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
        birth_year INT CHECK (birth_year >= 1850)
    );

    -- 13. Movie_Cast (M:N)
    CREATE TABLE movie_cast (
        movie_id INT NOT NULL,
        cast_id INT NOT NULL,
        role_name VARCHAR(100) NOT NULL,
        lead_order INT DEFAULT 1 CHECK (lead_order >= 1),
        PRIMARY KEY (movie_id, cast_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (cast_id) REFERENCES cast_members(cast_id) ON DELETE CASCADE
    );

    -- 14. Ratings & Reviews Table
    CREATE TABLE ratings_reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        rating_score DECIMAL(2,1) NOT NULL CHECK (rating_score >= 0.5 AND rating_score <= 10.0),
        review_text TEXT,
        review_date DATETIME DEFAULT (DATETIME('now')),
        UNIQUE (user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
    );

    -- 15. Watchlists Table
    CREATE TABLE watchlists (
        watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        movie_id INT NOT NULL,
        status VARCHAR(20) DEFAULT 'Planned' CHECK (status IN ('Planned', 'Watching', 'Completed', 'Dropped')),
        added_date DATETIME DEFAULT (DATETIME('now')),
        UNIQUE (user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
    );

    -- 16. Ratings Audit Log Table (Trigger Target)
    CREATE TABLE ratings_audit (
        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type VARCHAR(10) NOT NULL CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE')),
        user_id INT,
        movie_id INT,
        old_rating DECIMAL(2,1),
        new_rating DECIMAL(2,1),
        action_timestamp DATETIME DEFAULT (DATETIME('now'))
    );

    -- Secondary B-Tree Indexes
    CREATE INDEX idx_movies_year ON movies(release_year);
    CREATE INDEX idx_movies_rating ON movies(avg_rating);
    CREATE INDEX idx_movies_franchise ON movies(franchise_id);
    CREATE INDEX idx_movies_parent ON movies(parent_movie_id);
    CREATE INDEX idx_reviews_movie ON ratings_reviews(movie_id);
    CREATE INDEX idx_reviews_user ON ratings_reviews(user_id);
    CREATE INDEX idx_user_roles_user ON user_roles(user_id);
    CREATE INDEX idx_role_permissions_role ON role_permissions(role_id);
    """
    cur.executescript(ddl)
    print("Schema DDL created successfully (16 relations).")

    # ==========================================
    # 2. TRIGGERS
    # ==========================================
    triggers = """
    -- Trigger 1: AFTER INSERT ON ratings_reviews
    CREATE TRIGGER trg_after_rating_insert
    AFTER INSERT ON ratings_reviews
    BEGIN
        UPDATE movies
        SET avg_rating = (
            SELECT ROUND(AVG(rating_score), 2)
            FROM ratings_reviews
            WHERE movie_id = NEW.movie_id
        ),
        total_votes = (
            SELECT COUNT(*)
            FROM ratings_reviews
            WHERE movie_id = NEW.movie_id
        )
        WHERE movie_id = NEW.movie_id;

        INSERT INTO ratings_audit (action_type, user_id, movie_id, old_rating, new_rating, action_timestamp)
        VALUES ('INSERT', NEW.user_id, NEW.movie_id, NULL, NEW.rating_score, DATETIME('now'));
    END;

    -- Trigger 2: AFTER UPDATE ON ratings_reviews
    CREATE TRIGGER trg_after_rating_update
    AFTER UPDATE OF rating_score ON ratings_reviews
    BEGIN
        UPDATE movies
        SET avg_rating = (
            SELECT ROUND(AVG(rating_score), 2)
            FROM ratings_reviews
            WHERE movie_id = NEW.movie_id
        )
        WHERE movie_id = NEW.movie_id;

        INSERT INTO ratings_audit (action_type, user_id, movie_id, old_rating, new_rating, action_timestamp)
        VALUES ('UPDATE', NEW.user_id, NEW.movie_id, OLD.rating_score, NEW.rating_score, DATETIME('now'));
    END;

    -- Trigger 3: AFTER DELETE ON ratings_reviews
    CREATE TRIGGER trg_after_rating_delete
    AFTER DELETE ON ratings_reviews
    BEGIN
        UPDATE movies
        SET avg_rating = COALESCE((
            SELECT ROUND(AVG(rating_score), 2)
            FROM ratings_reviews
            WHERE movie_id = OLD.movie_id
        ), 0.0),
        total_votes = (
            SELECT COUNT(*)
            FROM ratings_reviews
            WHERE movie_id = OLD.movie_id
        )
        WHERE movie_id = OLD.movie_id;

        INSERT INTO ratings_audit (action_type, user_id, movie_id, old_rating, new_rating, action_timestamp)
        VALUES ('DELETE', OLD.user_id, OLD.movie_id, OLD.rating_score, NULL, DATETIME('now'));
    END;
    """
    cur.executescript(triggers)
    print("Triggers created successfully.")

    # ==========================================
    # 3. DML: Seed Data
    # ==========================================
    # Seed Roles
    cur.execute("INSERT INTO roles (role_id, role_name, description) VALUES (1, 'ADMIN', 'Superuser administrative privileges');")
    cur.execute("INSERT INTO roles (role_id, role_name, description) VALUES (2, 'CRITIC', 'Accredited film reviewer privileges');")
    cur.execute("INSERT INTO roles (role_id, role_name, description) VALUES (3, 'USER', 'Standard audience consumer privileges');")

    # Seed Permissions
    permissions = [
        (1, 'movie:read', 'catalog', 'View movie details and statistics.'),
        (2, 'movie:create', 'catalog', 'Register new movie titles.'),
        (3, 'movie:update', 'catalog', 'Modify movie details.'),
        (4, 'movie:delete', 'catalog', 'Delete movie titles.'),
        (5, 'review:create', 'reviews', 'Submit ratings and reviews.'),
        (6, 'review:delete_any', 'reviews', 'Moderate user reviews.'),
        (7, 'audit:read', 'system', 'Inspect DBMS trigger audit log.'),
        (8, 'vector:manage', 'vector_engine', 'Manage NoSQL documents & vector index.'),
        (9, 'analytics:read', 'analytics', 'View financial & recursive queries.')
    ]
    cur.executemany("INSERT INTO permissions VALUES (?, ?, ?, ?);", permissions)

    # Seed Role Permissions
    # ADMIN gets 1-9
    for p in range(1, 10):
        cur.execute("INSERT INTO role_permissions VALUES (1, ?);", (p,))
    # CRITIC gets 1, 5, 9
    for p in [1, 5, 9]:
        cur.execute("INSERT INTO role_permissions VALUES (2, ?);", (p,))
    # USER gets 1, 5
    for p in [1, 5]:
        cur.execute("INSERT INTO role_permissions VALUES (3, ?);", (p,))

    # Seed Users
    default_pw = "Password@123"
    users_data = [
        (1, 'alex_admin', 'alex@cinepulse.io', 'salt_alex_01', 'Alex Mercer', '2023-01-15', 'Critic'),
        (2, 'sarah_critic', 'sarah@cinepulse.io', 'salt_sarah_02', 'Sarah Connor', '2023-02-20', 'Critic'),
        (3, 'raj_patel', 'raj.patel@pes.edu', 'salt_raj_03', 'Raj Patel', '2023-03-10', 'Standard'),
        (4, 'elena_r', 'elena.rodriguez@gmail.com', 'salt_elena_04', 'Elena Rodriguez', '2023-04-05', 'Premium'),
        (5, 'david_kim', 'dkim@outlook.com', 'salt_david_05', 'David Kim', '2023-05-18', 'Standard'),
        (6, 'priya_critic', 'priya.sharma@pes.edu', 'salt_priya_06', 'Priya Sharma', '2023-06-22', 'Critic'),
        (7, 'marcus_v', 'marcus.v@yahoo.com', 'salt_marcus_07', 'Marcus Vance', '2023-07-30', 'Standard'),
        (8, 'ananya_sen', 'ananya.sen@pes.edu', 'salt_ananya_08', 'Ananya Sen', '2023-08-14', 'Premium'),
        (9, 'bruce_admin', 'bruce@wayneenterprises.com', 'salt_bruce_09', 'Bruce Wayne', '2023-09-01', 'Critic'),
        (10, 'john_doe', 'jdoe@gmail.com', 'salt_john_10', 'John Doe', '2023-10-10', 'Standard')
    ]
    for uid, uname, email, salt, fname, jdate, tier in users_data:
        p_hash = hash_pw(default_pw, salt)
        cur.execute("INSERT INTO users (user_id, username, email, password_hash, salt, full_name, join_date, tier, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1);",
                    (uid, uname, email, p_hash, salt, fname, jdate, tier))

    # User Roles
    cur.execute("INSERT INTO user_roles VALUES (1, 1, DATETIME('now'));") # Alex: ADMIN
    cur.execute("INSERT INTO user_roles VALUES (9, 1, DATETIME('now'));") # Bruce: ADMIN
    cur.execute("INSERT INTO user_roles VALUES (2, 2, DATETIME('now'));") # Sarah: CRITIC
    cur.execute("INSERT INTO user_roles VALUES (6, 2, DATETIME('now'));") # Priya: CRITIC
    cur.execute("INSERT INTO user_roles VALUES (3, 3, DATETIME('now'));") # Raj: USER
    cur.execute("INSERT INTO user_roles VALUES (4, 3, DATETIME('now'));")
    cur.execute("INSERT INTO user_roles VALUES (5, 3, DATETIME('now'));")
    cur.execute("INSERT INTO user_roles VALUES (7, 3, DATETIME('now'));")
    cur.execute("INSERT INTO user_roles VALUES (8, 3, DATETIME('now'));")
    cur.execute("INSERT INTO user_roles VALUES (10, 3, DATETIME('now'));")

    # Directors
    directors = [
        (1, 'Christopher Nolan', 1970, 'British', 8),
        (2, 'Quentin Tarantino', 1963, 'American', 7),
        (3, 'Martin Scorsese', 1942, 'American', 12),
        (4, 'Bong Joon-ho', 1969, 'South Korean', 5),
        (5, 'Hayao Miyazaki', 1941, 'Japanese', 6),
        (6, 'Denis Villeneuve', 1967, 'Canadian', 4),
        (7, 'Francis Ford Coppola', 1939, 'American', 10),
        (8, 'Greta Gerwig', 1983, 'American', 3)
    ]
    cur.executemany("INSERT INTO directors VALUES (?, ?, ?, ?, ?);", directors)

    # Production Companies
    companies = [
        (1, 'Warner Bros. Pictures', 'Burbank, California', 1923),
        (2, 'Paramount Pictures', 'Hollywood, California', 1912),
        (3, 'Studio Ghibli', 'Koganei, Tokyo', 1985),
        (4, 'A24', 'New York City, New York', 2012),
        (5, 'CJ Entertainment', 'Seoul, South Korea', 1995),
        (6, 'Universal Pictures', 'Universal City, California', 1912),
        (7, 'Syncopy Films', 'London, United Kingdom', 2001)
    ]
    cur.executemany("INSERT INTO production_companies VALUES (?, ?, ?, ?);", companies)

    # Movie Franchises
    franchises = [
        (1, 'The Dark Knight Trilogy', 'Christopher Nolan gritty DC superhero crime saga.', 2005),
        (2, 'Dune Saga', 'Frank Herbert epic science fiction adaptation by Denis Villeneuve.', 2021),
        (3, 'The Godfather Trilogy', 'Mario Puzo epic American mafia chronicle directed by Francis Ford Coppola.', 1972)
    ]
    cur.executemany("INSERT INTO movie_franchises VALUES (?, ?, ?, ?);", franchises)

    # Movies (With parent_movie_id for Recursive Franchise Hierarchy)
    movies = [
        (1, 'Inception', 2010, 148, 'English', 160.00, 836.80, 1, 1, None, None, 1),
        (2, 'Interstellar', 2014, 169, 'English', 165.00, 701.70, 1, 2, None, None, 1),
        (4, 'Oppenheimer', 2023, 180, 'English', 100.00, 957.80, 1, 6, None, None, 1),
        (14, 'Dunkirk', 2017, 106, 'English', 100.00, 527.00, 1, 1, None, None, 1),
        # Dark Knight Trilogy
        (16, 'Batman Begins', 2005, 140, 'English', 150.00, 373.60, 1, 1, 1, None, 1),
        (3, 'The Dark Knight', 2008, 152, 'English', 185.00, 1006.00, 1, 1, 1, 16, 2),
        (17, 'The Dark Knight Rises', 2012, 164, 'English', 250.00, 1081.10, 1, 1, 1, 3, 3),
        # Dune Saga
        (18, 'Dune: Part One', 2021, 155, 'English', 165.00, 402.00, 6, 1, 2, None, 1),
        (8, 'Dune: Part Two', 2024, 166, 'English', 190.00, 714.40, 6, 1, 2, 18, 2),
        # The Godfather Trilogy
        (9, 'The Godfather', 1972, 175, 'English', 6.00, 291.00, 7, 2, 3, None, 1),
        (19, 'The Godfather Part II', 1974, 202, 'English', 13.00, 88.00, 7, 2, 3, 9, 2),
        # Classics
        (5, 'Pulp Fiction', 1994, 154, 'English', 8.50, 213.90, 2, 4, None, None, 1),
        (6, 'Parasite', 2019, 132, 'Korean', 11.40, 263.10, 4, 5, None, None, 1),
        (7, 'Spirited Away', 2001, 125, 'Japanese', 19.20, 395.80, 5, 3, None, None, 1),
        (10, 'Goodfellas', 1990, 145, 'English', 25.00, 47.10, 3, 1, None, None, 1),
        (11, 'Kill Bill: Vol. 1', 2003, 111, 'English', 30.00, 180.90, 2, 4, None, None, 1),
        (12, 'Princess Mononoke', 1997, 134, 'Japanese', 23.50, 170.00, 5, 3, None, None, 1),
        (13, 'Barbie', 2023, 114, 'English', 145.00, 1445.60, 8, 1, None, None, 1),
        (15, 'Taxi Driver', 1976, 114, 'English', 1.90, 28.30, 3, 2, None, None, 1)
    ]
    for m in movies:
        cur.execute("""
            INSERT INTO movies (movie_id, title, release_year, duration_min, language, budget_millions, revenue_millions,
                                director_id, company_id, franchise_id, parent_movie_id, sequence_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, m)

    # Genres
    genres = [
        (1, 'Sci-Fi', 'Science fiction exploring futuristic concepts.'),
        (2, 'Action', 'High-energy storytelling featuring physical feats and conflict.'),
        (3, 'Drama', 'Narratives focusing on emotional and relational character development.'),
        (4, 'Crime', 'Plots centered on criminal activities, justice, and detectives.'),
        (5, 'Thriller', 'Intense suspense, excitement, and psychological anticipation.'),
        (6, 'Animation', 'Artistic computer-generated or illustrated pictures.'),
        (7, 'Fantasy', 'Mythological, magical, and supernatural realms.'),
        (8, 'Biography', 'Dramatization of non-fictional historical human lives.'),
        (9, 'Adventure', 'Heroic expeditions, exploration, and journeys.'),
        (10, 'Comedy', 'Lighthearted storytelling intended to amuse and entertain.')
    ]
    cur.executemany("INSERT INTO genres VALUES (?, ?, ?);", genres)

    # Movie Genres (M:N)
    mg = [
        (1, 1), (1, 2), (1, 5),
        (2, 1), (2, 3), (2, 9),
        (3, 2), (3, 4), (3, 5),
        (4, 8), (4, 3),
        (5, 4), (5, 3),
        (6, 5), (6, 3), (6, 10),
        (7, 6), (7, 7), (7, 9),
        (8, 1), (8, 2), (8, 9),
        (9, 4), (9, 3),
        (10, 4), (10, 3), (10, 8),
        (11, 2), (11, 4),
        (12, 6), (12, 7), (12, 2),
        (13, 10), (13, 7), (13, 9),
        (14, 2), (14, 3), (14, 8),
        (15, 3), (15, 4), (15, 5),
        (16, 2), (16, 4), (16, 5),
        (17, 2), (17, 5), (17, 3),
        (18, 1), (18, 9), (18, 3),
        (19, 4), (19, 3)
    ]
    cur.executemany("INSERT INTO movie_genres VALUES (?, ?);", mg)

    # Cast Members
    cast = [
        (1, 'Leonardo DiCaprio', 'Male', 1974),
        (2, 'Matthew McConaughey', 'Male', 1969),
        (3, 'Christian Bale', 'Male', 1974),
        (4, 'Heath Ledger', 'Male', 1979),
        (5, 'Cillian Murphy', 'Male', 1976),
        (6, 'John Travolta', 'Male', 1954),
        (7, 'Samuel L. Jackson', 'Male', 1948),
        (8, 'Song Kang-ho', 'Male', 1967),
        (9, 'Timothée Chalamet', 'Male', 1995),
        (10, 'Zendaya', 'Female', 1996),
        (11, 'Al Pacino', 'Male', 1940),
        (12, 'Robert De Niro', 'Male', 1943),
        (13, 'Uma Thurman', 'Female', 1970),
        (14, 'Margot Robbie', 'Female', 1990),
        (15, 'Anne Hathaway', 'Female', 1982)
    ]
    cur.executemany("INSERT INTO cast_members VALUES (?, ?, ?, ?);", cast)

    # Movie Cast
    m_cast = [
        (1, 1, 'Dom Cobb', 1), (1, 5, 'Robert Fischer', 2),
        (2, 2, 'Cooper', 1), (2, 15, 'Brand', 2),
        (3, 3, 'Bruce Wayne / Batman', 1), (3, 4, 'Joker', 2),
        (4, 5, 'J. Robert Oppenheimer', 1),
        (5, 6, 'Vincent Vega', 1), (5, 7, 'Jules Winnfield', 2),
        (6, 8, 'Kim Ki-taek', 1),
        (8, 9, 'Paul Atreides', 1), (8, 10, 'Chani', 2),
        (9, 11, 'Michael Corleone', 1), (9, 12, 'Vito Corleone', 2),
        (10, 12, 'James Conway', 1), (11, 13, 'The Bride', 1),
        (13, 14, 'Barbie', 1), (15, 12, 'Travis Bickle', 1),
        (16, 3, 'Bruce Wayne / Batman', 1),
        (17, 3, 'Bruce Wayne / Batman', 1), (17, 15, 'Selina Kyle / Catwoman', 2),
        (18, 9, 'Paul Atreides', 1), (18, 10, 'Chani', 2),
        (19, 11, 'Michael Corleone', 1), (19, 12, 'Young Vito Corleone', 2)
    ]
    cur.executemany("INSERT INTO movie_cast VALUES (?, ?, ?, ?);", m_cast)

    # Ratings & Reviews (Fires Trigger 1 trg_after_rating_insert!)
    ratings = [
        (1, 1, 9.2, 'Mind-bending cinematic masterpiece with incredible visuals.', '2024-01-10 14:30:00'),
        (2, 1, 9.5, 'Christopher Nolan at his very best. Hans Zimmer score is perfection.', '2024-01-12 16:45:00'),
        (3, 1, 8.8, 'Complex layered narrative that requires multiple viewings.', '2024-01-15 10:20:00'),
        (4, 2, 9.4, 'Emotional, visually stunning journey across space and time.', '2024-02-01 19:10:00'),
        (5, 2, 9.0, 'One of the greatest modern science fiction films ever made.', '2024-02-04 11:00:00'),
        (6, 2, 9.6, 'A triumph of scientific curiosity, family love, and score.', '2024-02-08 21:15:00'),
        (1, 3, 9.8, 'The benchmark for all superhero movies. Heath Ledger is iconic.', '2024-02-12 18:00:00'),
        (2, 3, 9.9, 'Unmatched tension and moral conflict in Gotham.', '2024-02-14 20:30:00'),
        (7, 3, 9.5, 'Dark, gritty, and philosophically engaging.', '2024-02-18 12:40:00'),
        (8, 4, 9.1, 'A breathtaking historical biography on nuclear ethics.', '2024-03-01 15:20:00'),
        (9, 4, 9.3, 'Cillian Murphy gives the performance of a lifetime.', '2024-03-05 17:50:00'),
        (3, 5, 9.0, 'Non-linear storytelling genius with unforgettable dialogue.', '2024-03-10 13:10:00'),
        (6, 5, 8.9, 'Iconic pop culture film that reshaped 90s cinema.', '2024-03-12 22:00:00'),
        (2, 6, 9.6, 'A razor-sharp social satire dissecting wealth inequality.', '2024-03-15 18:30:00'),
        (4, 6, 9.4, 'Brilliantly paced thriller with unexpected dark comedic turns.', '2024-03-18 14:05:00'),
        (5, 7, 9.7, 'The gold standard of animation. Pure magic and emotion.', '2024-03-20 16:40:00'),
        (8, 7, 9.5, 'Stunning Ghibli art style and wonderful world building.', '2024-03-22 19:25:00'),
        (1, 8, 9.0, 'Epic scale sci-fi opera. Arrakis feels tangible and terrifying.', '2024-03-25 21:00:00'),
        (9, 8, 9.2, 'Incredible sound design and breathtaking cinematography.', '2024-03-28 11:30:00'),
        (3, 9, 9.8, 'The undisputed patriarch of crime dramas. Immaculate.', '2024-04-01 13:15:00'),
        (7, 9, 9.7, 'Flawless pacing, timeless script, and legendary performances.', '2024-04-03 17:00:00'),
        (2, 10, 8.8, 'Scorsese captures mob life like no one else can.', '2024-04-05 19:45:00'),
        (4, 11, 8.5, 'Stylish martial arts homage packed with kinetic energy.', '2024-04-08 15:30:00'),
        (6, 12, 9.3, 'A profound environmental fable with mature themes.', '2024-04-10 18:10:00'),
        (8, 13, 8.2, 'Clever feminist commentary wrapped in vibrant humor.', '2024-04-12 14:20:00'),
        (1, 16, 8.9, 'Superb origin reboot establishing the gritty Gotham realism.', '2024-04-15 11:00:00'),
        (2, 17, 8.7, 'A fitting conclusion to an iconic superhero trilogy.', '2024-04-18 16:20:00'),
        (3, 18, 8.8, 'Hypnotic and grand sci-fi world-building.', '2024-04-20 19:40:00'),
        (1, 19, 9.7, 'A rare sequel that equals or surpasses the original.', '2024-04-22 21:10:00')
    ]
    cur.executemany("INSERT INTO ratings_reviews (user_id, movie_id, rating_score, review_text, review_date) VALUES (?, ?, ?, ?, ?);", ratings)

    # Watchlists
    watchlists = [
        (1, 4, 'Completed', '2024-01-05 12:00:00'),
        (1, 8, 'Completed', '2024-01-10 15:00:00'),
        (1, 13, 'Planned', '2024-02-01 10:00:00'),
        (2, 8, 'Completed', '2024-02-05 11:30:00'),
        (2, 12, 'Planned', '2024-02-10 14:15:00'),
        (3, 2, 'Watching', '2024-02-15 18:00:00'),
        (3, 8, 'Planned', '2024-02-20 09:30:00'),
        (4, 1, 'Completed', '2024-03-01 16:45:00'),
        (4, 4, 'Planned', '2024-03-05 13:20:00'),
        (5, 3, 'Completed', '2024-03-10 17:10:00'),
        (6, 1, 'Planned', '2024-03-15 19:00:00'),
        (7, 6, 'Planned', '2024-03-20 20:30:00'),
        (8, 9, 'Planned', '2024-03-25 10:45:00'),
        (9, 14, 'Planned', '2024-03-30 14:00:00'),
        (10, 1, 'Watching', '2024-04-02 16:30:00')
    ]
    cur.executemany("INSERT INTO watchlists (user_id, movie_id, status, added_date) VALUES (?, ?, ?, ?);", watchlists)

    conn.commit()
    print("DML Seeding committed successfully!")

    # ==========================================
    # 4. VERIFY QUERIES & TRIGGERS
    # ==========================================
    print("\n--- Verifying Triggers ---")
    cur.execute("SELECT movie_id, title, avg_rating, total_votes FROM movies WHERE movie_id IN (1, 3, 8);")
    for row in cur.fetchall():
        print(f"Movie #{row[0]}: {row[1]} -> Avg Rating: {row[2]}, Total Votes: {row[3]}")

    cur.execute("SELECT COUNT(*) FROM ratings_audit;")
    audit_count = cur.fetchone()[0]
    print(f"Total audit logs generated by triggers: {audit_count}")

    print("\n--- Testing Recursive Franchise Query (WITH RECURSIVE) ---")
    rec_query = """
    WITH RECURSIVE FranchiseTree AS (
        SELECT 
            m.movie_id,
            m.title,
            mf.franchise_name,
            m.parent_movie_id,
            m.release_year,
            m.revenue_millions,
            1 AS franchise_depth,
            m.title AS lineage_path,
            m.revenue_millions AS cumulative_revenue
        FROM movies m
        JOIN movie_franchises mf ON m.franchise_id = mf.franchise_id
        WHERE m.parent_movie_id IS NULL

        UNION ALL

        SELECT 
            child.movie_id,
            child.title,
            parent.franchise_name,
            child.parent_movie_id,
            child.release_year,
            child.revenue_millions,
            parent.franchise_depth + 1 AS franchise_depth,
            parent.lineage_path || ' -> ' || child.title AS lineage_path,
            ROUND(parent.cumulative_revenue + child.revenue_millions, 2) AS cumulative_revenue
        FROM movies child
        JOIN FranchiseTree parent ON child.parent_movie_id = parent.movie_id
    )
    SELECT franchise_name, franchise_depth, title, release_year, '$' || revenue_millions || 'M' AS gross,
           '$' || cumulative_revenue || 'M' AS cumulative, lineage_path
    FROM FranchiseTree
    ORDER BY franchise_name, franchise_depth;
    """
    cur.execute(rec_query)
    for r in cur.fetchall():
        print(f"Level {r[1]} | {r[0]} | {r[2]} ({r[3]}) | Gross: {r[4]} | Cumul: {r[5]} | Path: {r[6]}")

    print("\n--- Testing RBAC Permission Authorization ---")
    rbac_query = """
    SELECT u.username, r.role_name, p.permission_key, p.description
    FROM users u
    JOIN user_roles ur ON u.user_id = ur.user_id
    JOIN roles r ON ur.role_id = r.role_id
    JOIN role_permissions rp ON r.role_id = rp.role_id
    JOIN permissions p ON rp.permission_id = p.permission_id
    WHERE u.username = 'alex_admin' AND p.permission_key = 'movie:delete';
    """
    cur.execute(rbac_query)
    row = cur.fetchone()
    print(f"User '{row[0]}' with role '{row[1]}' has permission '{row[2]}' ({row[3]}) -> GRANTED")

    conn.close()
    print("\nDatabase initialization and verification completed successfully!")

if __name__ == '__main__':
    build_database()
