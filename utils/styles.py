import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    /* ==================== LIGHT THEME ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #fefefe 0%, #f5f5f0 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f6f0 100%);
        border-right: 1px solid #e0ddd5;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #333333;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2c2c2c !important;
        font-weight: 600 !important;
    }

    p, span, label, .stMarkdown {
        color: #333333 !important;
    }

    /* ── Cards ────────────────────────────────────────────────── */
    .card {
        background: #ffffff;
        border: 1px solid #e8e5de;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .card:hover {
        border-color: #d35400;
        box-shadow: 0 8px 24px rgba(211, 84, 0, 0.1);
        transform: translateY(-2px);
    }

    .card-accent {
        background: linear-gradient(135deg, rgba(230,126,34,0.08) 0%, rgba(230,126,34,0.02) 100%);
        border: 1px solid rgba(230, 126, 34, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-success {
        background: linear-gradient(135deg, rgba(46,204,113,0.08) 0%, rgba(46,204,113,0.02) 100%);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .card-warning {
        background: linear-gradient(135deg, rgba(241,196,15,0.08) 0%, rgba(241,196,15,0.02) 100%);
        border: 1px solid rgba(241, 196, 15, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── Metrics ──────────────────────────────────────────────── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e8e5de;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #d35400;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-delta {
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    .metric-delta.positive { color: #27ae60; }
    .metric-delta.negative { color: #c0392b; }

    /* ── Recipe Card ─────────────────────────────────────────── */
    .recipe-card {
        background: #ffffff;
        border: 1px solid #e8e5de;
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }
    .recipe-card:hover {
        border-color: #d35400;
        box-shadow: 0 4px 16px rgba(211, 84, 0, 0.12);
    }
    .recipe-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2c2c2c;
        margin-bottom: 0.3rem;
    }
    .recipe-meta {
        display: flex;
        gap: 1rem;
        color: #666666;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }

    /* ── Activity Feed ───────────────────────────────────────── */
    .activity-item {
        display: flex;
        gap: 0.8rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid #e8e5de;
        font-size: 0.85rem;
    }
    .activity-icon {
        font-size: 1.2rem;
        width: 2rem;
        text-align: center;
    }
    .activity-text {
        color: #333333;
        flex: 1;
    }
    .activity-time {
        color: #888888;
        font-size: 0.75rem;
        white-space: nowrap;
    }

    /* ── Roster Grid ─────────────────────────────────────────── */
    .roster-cell {
        background: #ffffff;
        border: 1px solid #e8e5de;
        border-radius: 12px;
        padding: 0.8rem;
        min-height: 80px;
        transition: all 0.2s ease;
    }
    .roster-cell:hover {
        border-color: #d35400;
    }
    .roster-cell.assigned {
        border-color: rgba(46,204,113,0.5);
        background: linear-gradient(135deg, rgba(46,204,113,0.08) 0%, transparent 100%);
    }
    .roster-cell.empty {
        border-style: dashed;
        opacity: 0.7;
    }
    .roster-cell .chef-name {
        font-weight: 600;
        color: #2c2c2c;
        font-size: 0.9rem;
    }
    .roster-cell .dish-name {
        color: #555555;
        font-size: 0.8rem;
        margin-top: 0.2rem;
    }

    /* ── Badges / Achievements ───────────────────────────────── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: linear-gradient(135deg, rgba(230,126,34,0.12) 0%, rgba(230,126,34,0.04) 100%);
        border: 1px solid rgba(230,126,34,0.3);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: #d35400;
        margin: 0.2rem;
    }
    .badge.gold {
        background: linear-gradient(135deg, rgba(241,196,15,0.15) 0%, rgba(241,196,15,0.05) 100%);
        border-color: rgba(241,196,15,0.5);
        color: #b8860b;
    }
    .badge.silver {
        background: linear-gradient(135deg, rgba(150,150,150,0.15) 0%, rgba(150,150,150,0.05) 100%);
        border-color: rgba(150,150,150,0.4);
        color: #666666;
    }
    .badge.bronze {
        background: linear-gradient(135deg, rgba(205,127,50,0.15) 0%, rgba(205,127,50,0.05) 100%);
        border-color: rgba(205,127,50,0.4);
        color: #8b4513;
    }

    /* ── Tags ─────────────────────────────────────────────────── */
    .tag {
        display: inline-block;
        background: rgba(230,126,34,0.1);
        border: 1px solid rgba(230,126,34,0.25);
        border-radius: 12px;
        padding: 0.15rem 0.6rem;
        font-size: 0.75rem;
        color: #d35400;
    }
    .tag.dietary {
        background: rgba(46,204,113,0.1);
        border-color: rgba(46,204,113,0.25);
        color: #27ae60;
    }

    /* ── Star Rating ─────────────────────────────────────────── */
    .stars {
        color: #f1c40f;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    .stars-small {
        color: #f1c40f;
        font-size: 0.9rem;
    }

    /* ── Buttons ──────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 6px rgba(211, 84, 0, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(211, 84, 0, 0.4) !important;
    }

    /* ── Hero Header ─────────────────────────────────────────── */
    .hero-header {
        background: linear-gradient(135deg, rgba(230,126,34,0.1) 0%, rgba(230,126,34,0.02) 100%);
        border: 1px solid rgba(230,126,34,0.25);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2c2c2c !important;
        margin-bottom: 0.3rem;
    }
    .hero-header .subtitle {
        color: #555555;
        font-size: 1.1rem;
    }

    /* ── Leaderboard ─────────────────────────────────────────── */
    .leaderboard-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        background: #ffffff;
        border: 1px solid #e8e5de;
    }
    .leaderboard-row.first {
        background: linear-gradient(135deg, rgba(241,196,15,0.1) 0%, transparent 100%);
        border-color: rgba(241,196,15,0.4);
    }
    .leaderboard-row.second {
        background: linear-gradient(135deg, rgba(189,195,199,0.1) 0%, transparent 100%);
        border-color: rgba(189,195,199,0.4);
    }
    .leaderboard-row.third {
        background: linear-gradient(135deg, rgba(205,127,50,0.1) 0%, transparent 100%);
        border-color: rgba(205,127,50,0.4);
    }
    .rank {
        font-size: 1.5rem;
        font-weight: 800;
        width: 2.5rem;
        text-align: center;
    }
    .rank.gold { color: #b8860b; }
    .rank.silver { color: #888888; }
    .rank.bronze { color: #8b4513; }

    /* ── Chat Messages ───────────────────────────────────────── */
    .chat-message {
        background: #ffffff;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #e67e22;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .chat-message .author {
        font-weight: 600;
        font-size: 0.85rem;
        color: #d35400;
    }
    .chat-message .time {
        font-size: 0.7rem;
        color: #888888;
    }
    .chat-message .text {
        color: #333333;
        margin-top: 0.3rem;
        font-size: 0.9rem;
    }

    /* ── Progress Bar Override ────────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e67e22, #f39c12);
        border-radius: 10px;
    }

    /* ── Form Elements ────────────────────────────────────────── */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #e67e22 !important;
        box-shadow: 0 0 0 2px rgba(230, 126, 34, 0.2) !important;
    }

    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
    }

    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
    }

    /* ── Tabs ─────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f0 !important;
        color: #666666 !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 0.5rem 1.5rem !important;
        border: 1px solid #e8e5de !important;
        border-bottom: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #d35400 !important;
        font-weight: 600 !important;
    }

    /* ── Expander ─────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e8e5de !important;
        border-radius: 12px !important;
        font-weight: 600;
        color: #333333 !important;
    }

    /* ── Timer ────────────────────────────────────────────────── */
    .timer-display {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #d35400;
        padding: 1rem;
    }

    /* ── Swap Card ────────────────────────────────────────────── */
    .swap-card {
        background: linear-gradient(135deg, rgba(155,89,182,0.08) 0%, transparent 100%);
        border: 1px solid rgba(155,89,182,0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    /* ── Stat Number ─────────────────────────────────────────── */
    .stat-big {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e67e22, #f39c12);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    /* ── Shopping List ────────────────────────────────────────── */
    .shopping-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0;
        border-bottom: 1px solid #e8e5de;
    }
    .shopping-item .amount {
        color: #d35400;
        font-weight: 600;
        min-width: 80px;
    }

    /* ── Scrollbar ────────────────────────────────────────────── */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f5f5f0;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: #c0bbb0;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #a0998a;
    }

    /* ── Hide Streamlit branding ─────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    html { scroll-behavior: smooth; }
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
            <div style="font-weight:600;color:#2c2c2c;">{name}</div>
            <div style="font-size:0.8rem;color:#666666;">{detail}</div>
        </div>
        <div style="font-size:1.3rem;font-weight:700;color:#d35400;">{value}</div>
    </div>
    """
