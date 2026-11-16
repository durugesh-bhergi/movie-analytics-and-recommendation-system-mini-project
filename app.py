"""
Movie Analytics & Recommendation System - Interactive Web Application
Backend: Python HTTP / JSON API + SQLite3 Database Engine
Course: UE23CS351A - DBMS Project | PES University
"""
import http.server
import socketserver
import json
import sqlite3
import 
import urllib.parse

PORT = 8080
DB_PATH = os.path.join(os.path.dirname(__file__), "movie_analytics.db")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CinePulse | Movie Analytics & Recommendation System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0b0f19;
            --bg-secondary: #131b2e;
            --bg-card: #1c2640;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --accent-glow: rgba(59, 130, 246, 0.35);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --gold: #f59e0b;
            --success: #10b981;
            --border: #2d3748;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-bottom: 1px solid var(--border);
            padding: 1.2rem 2.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        .logo-group {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .logo-badge {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            font-weight: 800;
            font-size: 1.4rem;
            padding: 8px 14px;
            border-radius: 10px;
            box-shadow: 0 0 15px var(--accent-glow);
        }
        .logo-text h1 {
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .logo-text p {
            font-size: 0.78rem;
            color: var(--text-muted);
        }
        .nav-links {
            display: flex;
            gap: 12px;
        }
        .nav-btn {
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.88rem;
            transition: all 0.2s ease;
        }
        .nav-btn:hover, .nav-btn.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
            box-shadow: 0 0 12px var(--accent-glow);
        }
        main {
            flex: 1;
            padding: 2rem 2.5rem;
            max-width: 1440px;
            margin: 0 auto;
            width: 100%;
        }
        .kpi-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1.2rem;
            margin-bottom: 2rem;
        }
        .kpi-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 1.4rem;
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
        }
        .kpi-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--accent), transparent);
        }
        .kpi-label {
            font-size: 0.82rem;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-main);
        }
        .search-bar-row {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 1.2rem;
            border-radius: 12px;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 2rem;
            align-items: center;
        }
        .input-group {
            flex: 1;
            min-width: 220px;
        }
        .input-group input, .input-group select {
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 0.92rem;
            outline: none;
        }
        .input-group input:focus, .input-group select:focus {
            border-color: var(--accent);
            box-shadow: 0 0 8px var(--accent-glow);
        }
        .grid-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }
        .movie-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.4rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .movie-card:hover {
            transform: translateY(-4px);
            border-color: var(--accent);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }
        .movie-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-main);
        }
        .rating-badge {
            background: rgba(245, 158, 11, 0.15);
            color: var(--gold);
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .movie-meta {
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-bottom: 12px;
        }
        .genre-pills {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }
        .genre-pill {
            background: var(--bg-card);
            color: #93c5fd;
            font-size: 0.72rem;
            padding: 3px 8px;
            border-radius: 12px;
            border: 1px solid #1e3a8a;
        }
        .finances-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            background: var(--bg-card);
            padding: 8px 12px;
            border-radius: 8px;
            margin-bottom: 12px;
        }
        .fin-item span {
            color: var(--text-muted);
        }
        .fin-item strong {
            color: var(--success);
        }
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
            padding-top: 10px;
            border-top: 1px solid var(--border);
        }
        .rate-btn {
            background: var(--accent);
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .rate-btn:hover {
            background: var(--accent-hover);
        }
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(4px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            width: 90%;
            max-width: 480px;
            border-radius: 14px;
            padding: 1.8rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        }
        .modal h3 { margin-bottom: 1rem; }
        .form-row { margin-bottom: 1rem; }
        .form-row label { display: block; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 6px; }
        .form-row input, .form-row select, .form-row textarea {
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 1.4rem;
        }
        .cancel-btn {
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
        }
        /* Table View */
        .table-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
            text-align: left;
        }
        th, td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: var(--bg-card);
            color: #cbd5e1;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }
        tr:hover {
            background: rgba(255,255,255,0.02);
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-insert { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-update { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .badge-delete { background: rgba(239, 68, 68, 0.2); color: #f87171; }
    </style>
</head>
<body>
    <header>
        <div class="logo-group">
            <div class="logo-badge">CP</div>
            <div class="logo-text">
                <h1>CinePulse Analytics & Recommender</h1>
                <p>PES University | CSE | UE23CS351A DBMS Project</p>
            </div>
        </div>
        <div class="nav-links">
            <button class="nav-btn active" onclick="switchTab('catalog')">Movie Catalog</button>
            <button class="nav-btn" onclick="switchTab('recommendations')">Smart Recommender</button>
            <button class="nav-btn" onclick="switchTab('analytics')">SQL Analytics</button>
            <button class="nav-btn" onclick="switchTab('audit')">Audit Logs</button>
        </div>
    </header>

    <main>
        <!-- KPI Row -->
        <div class="kpi-row" id="kpiContainer">
            <div class="kpi-card">
                <div class="kpi-label">Total Titles</div>
                <div class="kpi-value" id="kpiMovies">-</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Community Reviews</div>
                <div class="kpi-value" id="kpiReviews">-</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Average Rating</div>
                <div class="kpi-value" id="kpiRating">-</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Global Box Office</div>
                <div class="kpi-value" id="kpiRevenue">-</div>
            </div>
        </div>

        <!-- Catalog Tab -->
        <div id="tabCatalog">
            <div class="search-bar-row">
                <div class="input-group">
                    <input type="text" id="searchInput" placeholder="Search by movie title..." onkeyup="filterMovies()">
                </div>
                <div class="input-group">
                    <select id="genreFilter" onchange="filterMovies()">
                        <option value="">All Genres</option>
                    </select>
                </div>
                <div class="input-group">
                    <select id="directorFilter" onchange="filterMovies()">
                        <option value="">All Directors</option>
                    </select>
                </div>
            </div>
            <div class="grid-cards" id="movieGrid"></div>
        </div>

        <!-- Recommendations Tab -->
        <div id="tabRecommendations" style="display: none;">
            <div class="search-bar-row">
                <div style="font-weight: 600; margin-right: 1rem;">Select Registered User:</div>
                <div class="input-group">
                    <select id="userSelect" onchange="loadRecommendations()"></select>
                </div>
                <div style="color: var(--text-muted); font-size: 0.85rem;">
                    Recommender executes dynamic hybrid content-based genre clustering & Bayesian score weighting.
                </div>
            </div>
            <div class="grid-cards" id="recGrid"></div>
        </div>

        <!-- SQL Analytics Tab -->
        <div id="tabAnalytics" style="display: none;">
            <h2 style="margin-bottom: 1rem; font-size: 1.3rem;">Analytical Queries & Aggregate Reports</h2>
            <div class="table-container" style="margin-bottom: 2rem;">
                <div style="padding: 1rem; font-weight: 700; background: var(--bg-card);">7.1 Genre Performance & Vote Density (GROUP BY & HAVING)</div>
                <div id="genreAnalyticsTable"></div>
            </div>
            <div class="table-container">
                <div style="padding: 1rem; font-weight: 700; background: var(--bg-card);">7.1 (B) Director Box Office Analytics & Profitability</div>
                <div id="directorAnalyticsTable"></div>
            </div>
        </div>

        <!-- Audit Logs Tab -->
        <div id="tabAudit" style="display: none;">
            <h2 style="margin-bottom: 1rem; font-size: 1.3rem;">DBMS Trigger Audit Log (ratings_audit table)</h2>
            <p style="color: var(--text-muted); margin-bottom: 1.2rem; font-size: 0.9rem;">
                Records automatically appended by SQL Triggers: <code>trg_after_rating_insert</code>, <code>trg_after_rating_update</code>, and <code>trg_after_rating_delete</code>.
            </p>
            <div class="table-container" id="auditTableContainer"></div>
        </div>
    </main>

    <!-- Modal for adding rating -->
    <div class="modal" id="rateModal">
        <div class="modal-content">
            <h3 id="modalMovieTitle">Rate Movie</h3>
            <div class="form-row">
                <label>Active User</label>
                <select id="modalUserSelect"></select>
            </div>
            <div class="form-row">
                <label>Rating Score (0.5 to 10.0)</label>
                <input type="number" id="modalScore" min="0.5" max="10.0" step="0.1" value="9.0">
            </div>
            <div class="form-row">
                <label>Review Commentary</label>
                <textarea id="modalReview" rows="3" placeholder="Share your analysis..."></textarea>
            </div>
            <div class="modal-actions">
                <button class="cancel-btn" onclick="closeRateModal()">Cancel</button>
                <button class="rate-btn" onclick="submitRating()">Save Rating (Fires Trigger)</button>
            </div>
        </div>
    </div>

    <script>
        let allMovies = [];
        let allGenres = [];
        let allDirectors = [];
        let allUsers = [];
        let selectedMovieId = null;

        async function init() {
            await fetchMetadata();
            await fetchMovies();
            await fetchKpis();
            await fetchUsers();
        }

        async function fetchMetadata() {
            const res = await fetch('/api/metadata');
            const data = await res.json();
            allGenres = data.genres;
            allDirectors = data.directors;

            const gSelect = document.getElementById('genreFilter');
            allGenres.forEach(g => {
                gSelect.innerHTML += `<option value="${g.genre_id}">${g.genre_name}</option>`;
            });

            const dSelect = document.getElementById('directorFilter');
            allDirectors.forEach(d => {
                dSelect.innerHTML += `<option value="${d.director_id}">${d.name}</option>`;
            });
        }

        async function fetchUsers() {
            const res = await fetch('/api/users');
            allUsers = await res.json();
            const uSelect = document.getElementById('userSelect');
            const mUserSelect = document.getElementById('modalUserSelect');
            uSelect.innerHTML = '';
            mUserSelect.innerHTML = '';
            allUsers.forEach(u => {
                uSelect.innerHTML += `<option value="${u.user_id}">${u.full_name} (${u.tier})</option>`;
                mUserSelect.innerHTML += `<option value="${u.user_id}">${u.full_name} (${u.username})</option>`;
            });
        }

        async function fetchKpis() {
            const res = await fetch('/api/kpis');
            const d = await res.json();
            document.getElementById('kpiMovies').innerText = d.total_movies;
            document.getElementById('kpiReviews').innerText = d.total_reviews;
            document.getElementById('kpiRating').innerText = d.avg_rating.toFixed(2) + ' ★';
            document.getElementById('kpiRevenue').innerText = '$' + d.total_revenue.toLocaleString() + 'M';
        }

        async function fetchMovies() {
            const res = await fetch('/api/movies');
            allMovies = await res.json();
            renderMovies(allMovies);
        }

        function renderMovies(movies) {
            const grid = document.getElementById('movieGrid');
            grid.innerHTML = '';
            if (movies.length === 0) {
                grid.innerHTML = '<div style="color: var(--text-muted); padding: 2rem;">No matching films found.</div>';
                return;
            }
            movies.forEach(m => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                const genresHtml = (m.genres || []).map(g => `<span class="genre-pill">${g}</span>`).join('');
                card.innerHTML = `
                    <div>
                        <div class="card-header">
                            <div class="movie-title">${m.title}</div>
                            <div class="rating-badge">★ ${m.avg_rating.toFixed(1)}</div>
                        </div>
                        <div class="movie-meta">${m.release_year} • ${m.duration_min} min • Dir: <strong>${m.director_name}</strong></div>
                        <div class="genre-pills">${genresHtml}</div>
                        <div class="finances-row">
                            <div class="fin-item"><span>Budget:</span> $${m.budget_millions}M</div>
                            <div class="fin-item"><span>Box Office:</span> <strong>$${m.revenue_millions}M</strong></div>
                        </div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 10px;">
                            <strong>Cast:</strong> ${m.cast_names || 'N/A'}
                        </div>
                    </div>
                    <div class="card-footer">
                        <span style="font-size: 0.75rem; color: var(--text-muted);">${m.total_votes} verified ratings</span>
                        <button class="rate-btn" onclick="openRateModal(${m.movie_id}, '${m.title.replace(/'/g, "\\'")}')">Rate / Review</button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function filterMovies() {
            const search = document.getElementById('searchInput').value.toLowerCase();
            const genreId = document.getElementById('genreFilter').value;
            const directorId = document.getElementById('directorFilter').value;

            const filtered = allMovies.filter(m => {
                const matchSearch = m.title.toLowerCase().includes(search) || (m.director_name && m.director_name.toLowerCase().includes(search));
                const matchGenre = !genreId || (m.genre_ids && m.genre_ids.includes(parseInt(genreId)));
                const matchDirector = !directorId || (m.director_id == parseInt(directorId));
                return matchSearch && matchGenre && matchDirector;
            });
            renderMovies(filtered);
        }

        function switchTab(tab) {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('tabCatalog').style.display = 'none';
            document.getElementById('tabRecommendations').style.display = 'none';
            document.getElementById('tabAnalytics').style.display = 'none';
            document.getElementById('tabAudit').style.display = 'none';

            if (tab === 'catalog') {
                document.getElementById('tabCatalog').style.display = 'block';
                event.target.classList.add('active');
            } else if (tab === 'recommendations') {
                document.getElementById('tabRecommendations').style.display = 'block';
                event.target.classList.add('active');
                loadRecommendations();
            } else if (tab === 'analytics') {
                document.getElementById('tabAnalytics').style.display = 'block';
                event.target.classList.add('active');
                loadAnalytics();
            } else if (tab === 'audit') {
                document.getElementById('tabAudit').style.display = 'block';
                event.target.classList.add('active');
                loadAuditLogs();
            }
        }

        async function loadRecommendations() {
            const userId = document.getElementById('userSelect').value;
            if (!userId) return;
            const res = await fetch(`/api/recommendations?user_id=${userId}`);
            const recs = await res.json();
            const grid = document.getElementById('recGrid');
            grid.innerHTML = '';
            if (recs.length === 0) {
                grid.innerHTML = '<div style="color: var(--text-muted); padding: 2rem;">No unwatched recommendations found for this user profile.</div>';
                return;
            }
            recs.forEach(r => {
                const card = document.createElement('div');
                card.className = 'movie-card';
                card.innerHTML = `
                    <div>
                        <div class="card-header">
                            <div class="movie-title">${r.title}</div>
                            <div class="rating-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: #059669;">
                                Score: ${r.recommendation_score}
                            </div>
                        </div>
                        <div class="movie-meta">${r.release_year} • Dir: ${r.director_name}</div>
                        <div class="finances-row" style="margin-top: 10px;">
                            <div class="fin-item"><span>Avg Community Rating:</span> <strong>${r.avg_rating} ★</strong></div>
                            <div class="fin-item"><span>Genre Affinity Match:</span> <strong>+${r.matching_genre_count}</strong></div>
                        </div>
                    </div>
                    <div class="card-footer" style="margin-top: 15px;">
                        <span style="font-size: 0.78rem; color: #93c5fd;">Recommended for User ${userId}</span>
                        <button class="rate-btn" onclick="openRateModal(${r.movie_id}, '${r.title.replace(/'/g, "\\'")}')">Watch & Rate</button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        async function loadAnalytics() {
            const res = await fetch('/api/analytics');
            const data = await res.json();

            // Genre Table
            let gHtml = '<table><thead><tr><th>Genre</th><th>Films Count</th><th>Avg Rating</th><th>Total Votes</th></tr></thead><tbody>';
            data.genres.forEach(g => {
                gHtml += `<tr><td><strong>${g.genre_name}</strong></td><td>${g.total_movies}</td><td>★ ${g.average_genre_rating}</td><td>${g.total_community_votes}</td></tr>`;
            });
            gHtml += '</tbody></table>';
            document.getElementById('genreAnalyticsTable').innerHTML = gHtml;

            // Director Table
            let dHtml = '<table><thead><tr><th>Director</th><th>Nationality</th><th>Films</th><th>Box Office Gross</th><th>Average Profit</th></tr></thead><tbody>';
            data.directors.forEach(d => {
                dHtml += `<tr><td><strong>${d.director_name}</strong></td><td>${d.nationality}</td><td>${d.films_directed}</td><td>$${d.total_revenue_millions}M</td><td>$${d.avg_profit_millions}M</td></tr>`;
            });
            dHtml += '</tbody></table>';
            document.getElementById('directorAnalyticsTable').innerHTML = dHtml;
        }

        async function loadAuditLogs() {
            const res = await fetch('/api/audit');
            const logs = await res.json();
            let html = '<table><thead><tr><th>Audit ID</th><th>Action</th><th>User</th><th>Movie Title</th><th>Old Rating</th><th>New Rating</th><th>Timestamp</th></tr></thead><tbody>';
            logs.forEach(l => {
                const badgeClass = l.action_type === 'INSERT' ? 'badge-insert' : (l.action_type === 'UPDATE' ? 'badge-update' : 'badge-delete');
                html += `<tr>
                    <td>#${l.audit_id}</td>
                    <td><span class="badge ${badgeClass}">${l.action_type}</span></td>
                    <td>${l.username || 'User ' + l.user_id}</td>
                    <td><strong>${l.movie_title || 'Movie ' + l.movie_id}</strong></td>
                    <td>${l.old_rating !== null ? l.old_rating + ' ★' : '-'}</td>
                    <td>${l.new_rating !== null ? l.new_rating + ' ★' : '-'}</td>
                    <td style="color: var(--text-muted); font-family: monospace;">${l.action_timestamp}</td>
                </tr>`;
            });
            html += '</tbody></table>';
            document.getElementById('auditTableContainer').innerHTML = html;
        }

        function openRateModal(movieId, title) {
            selectedMovieId = movieId;
            document.getElementById('modalMovieTitle').innerText = 'Rate: ' + title;
            document.getElementById('rateModal').style.display = 'flex';
        }

        function closeRateModal() {
            document.getElementById('rateModal').style.display = 'none';
        }

        async function submitRating() {
            const userId = document.getElementById('modalUserSelect').value;
            const score = document.getElementById('modalScore').value;
            const review = document.getElementById('modalReview').value;

            const res = await fetch('/api/rate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: parseInt(userId),
                    movie_id: parseInt(selectedMovieId),
                    rating_score: parseFloat(score),
                    review_text: review
                })
            });
            const result = await res.json();
            if (result.success) {
                alert('Success! Rating saved and SQL Trigger fired.');
                closeRateModal();
                await fetchMovies();
                await fetchKpis();
            } else {
                alert('Error: ' + result.error);
            }
        }

        window.onload = init;
    </script>
</body>
</html>
"""

class CinePulseHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
            return

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if path == '/api/kpis':
            cur.execute("SELECT COUNT(*) FROM movies;")
            total_m = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM ratings_reviews;")
            total_r = cur.fetchone()[0]
            cur.execute("SELECT AVG(avg_rating) FROM movies WHERE total_votes > 0;")
            avg_rt = cur.fetchone()[0] or 0.0
            cur.execute("SELECT SUM(revenue_millions) FROM movies;")
            tot_rev = cur.fetchone()[0] or 0.0
            self._send_json({
                'total_movies': total_m,
                'total_reviews': total_r,
                'avg_rating': round(avg_rt, 2),
                'total_revenue': round(tot_rev, 2)
            })

        elif path == '/api/movies':
            q = """
            SELECT m.movie_id, m.title, m.release_year, m.duration_min, m.avg_rating, m.total_votes,
                   m.budget_millions, m.revenue_millions, m.director_id,
                   d.name AS director_name, pc.company_name
            FROM movies m
            LEFT JOIN directors d ON m.director_id = d.director_id
            LEFT JOIN production_companies pc ON m.company_id = pc.company_id
            ORDER BY m.avg_rating DESC;
            """
            cur.execute(q)
            movies = [dict(row) for row in cur.fetchall()]

            # Attach genres and cast
            for m in movies:
                cur.execute("""
                    SELECT g.genre_id, g.genre_name 
                    FROM genres g 
                    JOIN movie_genres mg ON g.genre_id = mg.genre_id 
                    WHERE mg.movie_id = ?
                """, (m['movie_id'],))
                genres = cur.fetchall()
                m['genres'] = [g['genre_name'] for g in genres]
                m['genre_ids'] = [g['genre_id'] for g in genres]

                cur.execute("""
                    SELECT cm.name 
                    FROM cast_members cm 
                    JOIN movie_cast mc ON cm.cast_id = mc.cast_id 
                    WHERE mc.movie_id = ? 
                    ORDER BY mc.lead_order LIMIT 3
                """, (m['movie_id'],))
                m['cast_names'] = ", ".join([c['name'] for c in cur.fetchall()])

            self._send_json(movies)

        elif path == '/api/metadata':
            cur.execute("SELECT genre_id, genre_name FROM genres ORDER BY genre_name;")
            genres = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT director_id, name FROM directors ORDER BY name;")
            directors = [dict(r) for r in cur.fetchall()]
            self._send_json({'genres': genres, 'directors': directors})

        elif path == '/api/users':
            cur.execute("SELECT user_id, username, full_name, tier FROM users ORDER BY user_id;")
            users = [dict(r) for r in cur.fetchall()]
            self._send_json(users)

        elif path == '/api/recommendations':
            user_id = int(query.get('user_id', [1])[0])
            # Recommender algorithm: user preferred genres + unwatched movies
            q = """
            WITH UserTopGenres AS (
                SELECT mg.genre_id, COUNT(*) AS affinity
                FROM ratings_reviews rr
                JOIN movie_genres mg ON rr.movie_id = mg.movie_id
                WHERE rr.user_id = ? AND rr.rating_score >= 8.5
                GROUP BY mg.genre_id
                ORDER BY affinity DESC
                LIMIT 3
            ),
            UnwatchedMovies AS (
                SELECT m.movie_id, m.title, m.release_year, m.avg_rating, d.name AS director_name,
                       COUNT(mg.genre_id) AS matching_genre_count
                FROM movies m
                LEFT JOIN directors d ON m.director_id = d.director_id
                JOIN movie_genres mg ON m.movie_id = mg.movie_id
                WHERE mg.genre_id IN (SELECT genre_id FROM UserTopGenres)
                  AND m.movie_id NOT IN (SELECT movie_id FROM ratings_reviews WHERE user_id = ?)
                GROUP BY m.movie_id, m.title, m.release_year, m.avg_rating, d.name
            )
            SELECT movie_id, title, release_year, avg_rating, director_name, matching_genre_count,
                   ROUND((avg_rating * 0.7) + (matching_genre_count * 1.0), 2) AS recommendation_score
            FROM UnwatchedMovies
            ORDER BY recommendation_score DESC, avg_rating DESC
            LIMIT 6;
            """
            cur.execute(q, (user_id, user_id))
            recs = [dict(r) for r in cur.fetchall()]
            self._send_json(recs)

        elif path == '/api/analytics':
            q_genres = """
            SELECT g.genre_name,
                   COUNT(DISTINCT m.movie_id) AS total_movies,
                   ROUND(AVG(m.avg_rating), 2) AS average_genre_rating,
                   SUM(m.total_votes) AS total_community_votes
            FROM genres g
            JOIN movie_genres mg ON g.genre_id = mg.genre_id
            JOIN movies m ON mg.movie_id = m.movie_id
            GROUP BY g.genre_id, g.genre_name
            HAVING COUNT(DISTINCT m.movie_id) >= 2
            ORDER BY average_genre_rating DESC;
            """
            cur.execute(q_genres)
            g_rows = [dict(r) for r in cur.fetchall()]

            q_directors = """
            SELECT d.name AS director_name, d.nationality,
                   COUNT(m.movie_id) AS films_directed,
                   ROUND(SUM(m.revenue_millions), 2) AS total_revenue_millions,
                   ROUND(AVG(m.revenue_millions - m.budget_millions), 2) AS avg_profit_millions
            FROM directors d
            JOIN movies m ON d.director_id = m.director_id
            GROUP BY d.director_id, d.name
            HAVING SUM(m.revenue_millions) > 300.0
            ORDER BY total_revenue_millions DESC;
            """
            cur.execute(q_directors)
            d_rows = [dict(r) for r in cur.fetchall()]
            self._send_json({'genres': g_rows, 'directors': d_rows})

        elif path == '/api/audit':
            q_audit = """
            SELECT a.audit_id, a.action_type, a.user_id, a.movie_id, a.old_rating, a.new_rating,
                   a.action_timestamp, u.username, m.title AS movie_title
            FROM ratings_audit a
            LEFT JOIN users u ON a.user_id = u.user_id
            LEFT JOIN movies m ON a.movie_id = m.movie_id
            ORDER BY a.audit_id DESC
            LIMIT 20;
            """
            cur.execute(q_audit)
            logs = [dict(r) for r in cur.fetchall()]
            self._send_json(logs)
        else:
            self.send_response(404)
            self.end_headers()
        conn.close()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == '/api/rate':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                u_id = int(data['user_id'])
                m_id = int(data['movie_id'])
                score = float(data['rating_score'])
                review = data.get('review_text', '')

                conn = sqlite3.connect(DB_PATH)
                conn.execute("PRAGMA foreign_keys = ON;")
                cur = conn.cursor()

                # Upsert rating
                cur.execute("""
                    INSERT INTO ratings_reviews (user_id, movie_id, rating_score, review_text, review_date)
                    VALUES (?, ?, ?, ?, DATETIME('now'))
                    ON CONFLICT(user_id, movie_id) DO UPDATE SET
                        rating_score = excluded.rating_score,
                        review_text = excluded.review_text,
                        review_date = excluded.review_date;
                """, (u_id, m_id, score, review))
                conn.commit()
                conn.close()
                self._send_json({'success': True})
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)}, status=400)
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    print(f"Starting CinePulse Server on http://localhost:{PORT} ...")
    with socketserver.TCPServer(("", PORT), CinePulseHandler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
