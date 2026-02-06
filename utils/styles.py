import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    /* ── Global ──────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Cards ────────────────────────────────────────────────── */
    .card {
        background: linear-gradient(135deg, #1a1d23 0%, #22262e 100%);
        border: 1px solid rgba(255, 107, 53, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .card:hover {
        border-color: rgba(255, 107, 53, 0.4);
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.1);
        transform: translateY(-2px);
    }

    .card-accent {
        background: linear-gradient(135deg, rgba(255,107,53,0.1) 0%, rgba(255,107,53,0.05) 100%);
        border: 1px solid rgba(255, 107, 53, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-success {
        background: linear-gradient(135deg, rgba(46,204,113,0.1) 0%, rgba(46,204,113,0.05) 100%);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-warning {
        background: linear-gradient(135deg, rgba(241,196,15,0.1) 0%, rgba(241,196,15,0.05) 100%);
        border: 1px solid rgba(241, 196, 15, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Metrics ──────────────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, #1a1d23 0%, #22262e 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FF6B35;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.85);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-delta {
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    .metric-delta.positive { color: #2ecc71; }
    .metric-delta.negative { color: #e74c3c; }

    /* ── Roster Grid ───────────────────────────────────────────── */
    .roster-cell {
        background: #1a1d23;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.8rem;
        min-height: 80px;
        transition: all 0.2s ease;
    }
    .roster-cell:hover {
        border-color: rgba(255,107,53,0.3);
    }
    .roster-cell.assigned {
        border-color: rgba(46,204,113,0.4);
        background: linear-gradient(135deg, rgba(46,204,113,0.08) 0%, transparent 100%);
    }
    .roster-cell.empty {
        border-style: dashed;
        opacity: 0.6;
    }
    .roster-cell .chef-name {
        font-weight: 600;
        color: #fafafa;
        font-size: 0.9rem;
    }
    .roster-cell .dish-name {
        color: rgba(255,255,255,0.85);
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    /* ── Badges / Achievements ───────────────────────────────── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: linear-gradient(135deg, rgba(255,107,53,0.15) 0%, rgba(255,107,53,0.05) 100%);
        border: 1px solid rgba(255,107,53,0.3);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: #FF6B35;
        margin: 0.2rem;
    }
    .badge.gold {
        background: linear-gradient(135deg, rgba(241,196,15,0.2) 0%, rgba(241,196,15,0.05) 100%);
        border-color: rgba(241,196,15,0.4);
        color: #f1c40f;
    }
    .badge.silver {
        background: linear-gradient(135deg, rgba(189,195,199,0.2) 0%, rgba(189,195,199,0.05) 100%);
        border-color: rgba(189,195,199,0.4);
        color: #bdc3c7;
    }
    .badge.bronze {
        background: linear-gradient(135deg, rgba(205,127,50,0.2) 0%, rgba(205,127,50,0.05) 100%);
        border-color: rgba(205,127,50,0.4);
        color: #cd7f32;
    }

    /* ── Recipe Card ───────────────────────────────────────────── */
    .recipe-card {
        background: linear-gradient(135deg, #1a1d23 0%, #22262e 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .recipe-card:hover {
        border-color: rgba(255,107,53,0.3);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .recipe-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #fafafa;
        margin-bottom: 0.3rem;
    }
    .recipe-meta {
        display: flex;
        gap: 1rem;
        color: rgba(255,255,255,0.75);
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .recipe-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.3rem;
    }

    /* ── Tags ───────────────────────────────────────────────────── */
    .tag {
        display: inline-block;
        background: rgba(255,107,53,0.1);
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 12px;
        padding: 0.15rem 0.6rem;
        font-size: 0.75rem;
        color: #FF6B35;
    }
    .tag.dietary {
        background: rgba(46,204,113,0.1);
        border-color: rgba(46,204,113,0.2);
        color: #2ecc71;
    }

    /* ── Star Rating ───────────────────────────────────────────── */
    .stars {
        color: #f1c40f;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    .stars-small {
        color: #f1c40f;
        font-size: 0.9rem;
    }

    /* ── Chat Messages ─────────────────────────────────────────── */
    .chat-message {
        background: #1a1d23;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #FF6B35;
    }
    .chat-message .author {
        font-weight: 600;
        font-size: 0.85rem;
        color: #FF6B35;
    }
    .chat-message .time {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.65);
    }
    .chat-message .text {
        color: #fafafa;
        margin-top: 0.3rem;
        font-size: 0.9rem;
    }

    /* ── Leaderboard ───────────────────────────────────────────── */
    .leaderboard-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        background: #1a1d23;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .leaderboard-row.first {
        background: linear-gradient(135deg, rgba(241,196,15,0.12) 0%, transparent 100%);
        border-color: rgba(241,196,15,0.3);
    }
    .leaderboard-row.second {
        background: linear-gradient(135deg, rgba(189,195,199,0.1) 0%, transparent 100%);
        border-color: rgba(189,195,199,0.2);
    }
    .leaderboard-row.third {
        background: linear-gradient(135deg, rgba(205,127,50,0.1) 0%, transparent 100%);
        border-color: rgba(205,127,50,0.2);
    }
    .rank {
        font-size: 1.5rem;
        font-weight: 800;
        width: 2.5rem;
        text-align: center;
    }
    .rank.gold { color: #f1c40f; }
    .rank.silver { color: #bdc3c7; }
    .rank.bronze { color: #cd7f32; }

    /* ── Reactions ──────────────────────────────────────────────── */
    .reactions {
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
    }
    .reaction-btn {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 0.2rem 0.6rem;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .reaction-btn:hover {
        background: rgba(255,107,53,0.15);
        border-color: rgba(255,107,53,0.3);
    }

    /* ── Progress Bar Override ────────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FF6B35, #ff8c5a);
        border-radius: 10px;
    }

    /* ── Activity Feed ─────────────────────────────────────────── */
    .activity-item {
        display: flex;
        gap: 0.8rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.85rem;
    }
    .activity-icon {
        font-size: 1.2rem;
        width: 2rem;
        text-align: center;
    }
    .activity-text {
        color: rgba(255,255,255,0.9);
        flex: 1;
    }
    .activity-time {
        color: rgba(255,255,255,0.65);
        font-size: 0.75rem;
        white-space: nowrap;
    }

    /* ── Swap Card ──────────────────────────────────────────────── */
    .swap-card {
        background: linear-gradient(135deg, rgba(155,89,182,0.1) 0%, transparent 100%);
        border: 1px solid rgba(155,89,182,0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    /* ── Stat Number ───────────────────────────────────────────── */
    .stat-big {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35, #ff8c5a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* ── Buttons ──────────────────────────────────────────────── */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.3);
    }

    /* ── Sidebar ──────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #151920 100%);
    }

    /* ── Tabs ───────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 0.5rem 1.5rem;
    }

    /* ── Header Gradient ───────────────────────────────────────── */
    .hero-header {
        background: linear-gradient(135deg, rgba(255,107,53,0.15) 0%, rgba(255,107,53,0.02) 100%);
        border: 1px solid rgba(255,107,53,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .hero-header .subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 1.1rem;
    }

    /* ── Expander ───────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        border-radius: 12px;
        font-weight: 600;
    }

    /* ── Timer ──────────────────────────────────────────────────── */
    .timer-display {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #FF6B35;
        padding: 1rem;
    }

    /* ── Shopping List ──────────────────────────────────────────── */
    .shopping-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .shopping-item .amount {
        color: #FF6B35;
        font-weight: 600;
        min-width: 80px;
    }

    /* ── Notification dot ──────────────────────────────────────── */
    .notification-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #e74c3c;
        border-radius: 50%;
        margin-left: 4px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* ── Smooth scrolling ──────────────────────────────────────── */
    html { scroll-behavior: smooth; }

    /* ── Hide Streamlit branding ─────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: str = "", delta_positive: bool = True) -> str:
    delta_html = ""
    if delta:
        cls = "positive" if delta_positive else "negative"
        delta_html = f'<div class="metric-delta {cls}">{delta}</div>'
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """


def card(content: str, variant: str = "") -> str:
    cls = f"card-{variant}" if variant else "card"
    return f'<div class="{cls}">{content}</div>'


def badge_html(text: str, variant: str = "") -> str:
    cls = f"badge {variant}" if variant else "badge"
    return f'<span class="{cls}">{text}</span>'


def tag_html(text: str, dietary: bool = False) -> str:
    cls = "tag dietary" if dietary else "tag"
    return f'<span class="{cls}">{text}</span>'


def stars_html(rating: float, small: bool = False) -> str:
    full = int(rating)
    empty = 5 - full
    cls = "stars-small" if small else "stars"
    return f'<span class="{cls}">{"★" * full}{"☆" * empty}</span>'


def chat_message_html(author: str, text: str, time: str) -> str:
    return f"""
    <div class="chat-message">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span class="author">{author}</span>
            <span class="time">{time}</span>
        </div>
        <div class="text">{text}</div>
    </div>
    """


def activity_item_html(icon: str, text: str, time: str) -> str:
    return f"""
    <div class="activity-item">
        <div class="activity-icon">{icon}</div>
        <div class="activity-text">{text}</div>
        <div class="activity-time">{time}</div>
    </div>
    """


def roster_cell_html(chef: str = "", dish: str = "", assigned: bool = False) -> str:
    cls = "roster-cell assigned" if assigned else "roster-cell empty"
    if assigned:
        return f"""
        <div class="{cls}">
            <div class="chef-name">{chef}</div>
            <div class="dish-name">{dish if dish else '...'}</div>
        </div>
        """
    return f'<div class="{cls}"><div class="dish-name">Vrij</div></div>'


def leaderboard_row_html(rank: int, name: str, avatar: str, value: str, detail: str = "") -> str:
    rank_cls = {1: "gold", 2: "silver", 3: "bronze"}.get(rank, "")
    row_cls = {1: "first", 2: "second", 3: "third"}.get(rank, "")
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, str(rank))
    return f"""
    <div class="leaderboard-row {row_cls}">
        <div class="rank {rank_cls}">{medal}</div>
        <div style="font-size:1.5rem;">{avatar}</div>
        <div style="flex:1;">
            <div style="font-weight:600;">{name}</div>
            <div style="font-size:0.8rem;color:rgba(255,255,255,0.75);">{detail}</div>
        </div>
        <div style="font-size:1.3rem;font-weight:700;color:#FF6B35;">{value}</div>
    </div>
    """
