import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    /* ==================== LIGHT THEME ==================== */
    
    /* Main app background - light cream/white */
    .stApp {
        background: linear-gradient(135deg, #fefefe 0%, #f5f5f0 100%);
    }
    
    /* Sidebar - soft warm white */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f6f0 100%);
        border-right: 1px solid #e0ddd5;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #333333;
    }
    
    /* Headers - dark text for contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #2c2c2c !important;
        font-weight: 600 !important;
    }
    
    /* Regular text - dark gray */
    p, span, label, .stMarkdown {
        color: #333333 !important;
    }
    
    /* ==================== CARDS & CONTAINERS ==================== */
    
    /* Recipe cards - white with subtle shadow */
    .recipe-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e5de;
        transition: all 0.3s ease;
        color: #333333;
    }
    
    .recipe-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .recipe-card h3 {
        color: #2c2c2c !important;
        margin-bottom: 12px;
    }
    
    .recipe-card p {
        color: #555555 !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        border: 1px solid #e8e5de;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #d35400 !important;
    }
    
    .metric-label {
        color: #666666 !important;
        font-size: 0.9rem;
        margin-top: 8px;
    }
    
    /* ==================== BUTTONS ==================== */
    
    .stButton > button {
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 6px rgba(211, 84, 0, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(211, 84, 0, 0.4) !important;
    }
    
    /* Secondary buttons */
    .secondary-btn {
        background: #f5f5f0 !important;
        color: #333333 !important;
        border: 1px solid #d0ccc0 !important;
    }
    
    /* ==================== FORM ELEMENTS ==================== */
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
        padding: 12px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #e67e22 !important;
        box-shadow: 0 0 0 2px rgba(230, 126, 34, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999999 !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #e67e22 !important;
        box-shadow: 0 0 0 2px rgba(230, 126, 34, 0.2) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #d0ccc0 !important;
        color: #333333 !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #e67e22 !important;
        color: white !important;
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #d0ccc0 !important;
        border-radius: 8px !important;
        color: #333333 !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: #e67e22 !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label > span {
        color: #333333 !important;
    }
    
    /* Radio buttons */
    .stRadio > label > span {
        color: #333333 !important;
    }
    
    /* ==================== DATA DISPLAY ==================== */
    
    /* Dataframes */
    .stDataFrame {
        background-color: #ffffff !important;
        border-radius: 8px !important;
        overflow: hidden;
        border: 1px solid #e8e5de !important;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: #ffffff !important;
    }
    
    /* Tables */
    .stTable {
        background-color: #ffffff !important;
    }
    
    .stTable th {
        background-color: #f8f6f0 !important;
        color: #333333 !important;
    }
    
    .stTable td {
        color: #333333 !important;
        border-bottom: 1px solid #e8e5de !important;
    }
    
    /* ==================== EXPANDERS ==================== */
    
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e8e5de !important;
        border-radius: 8px !important;
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f8f6f0 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e8e5de !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* ==================== TABS ==================== */
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f0 !important;
        color: #666666 !important;
        border-radius: 8px 8px 0 0 !important;
        border: 1px solid #e8e5de !important;
        border-bottom: none !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #e67e22 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #ffffff !important;
        border: 1px solid #e8e5de !important;
        border-radius: 0 8px 8px 8px !important;
        padding: 20px !important;
    }
    
    /* ==================== ALERTS & MESSAGES ==================== */
    
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #28a745 !important;
        color: #155724 !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 1px solid #17a2b8 !important;
        color: #0c5460 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border: 1px solid #ffc107 !important;
        color: #856404 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border: 1px solid #dc3545 !important;
        color: #721c24 !important;
        border-radius: 8px !important;
    }
    
    /* ==================== CUSTOM COMPONENTS ==================== */
    
    /* Day cards for meal planning */
    .day-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        border-left: 4px solid #e67e22;
        border-right: 1px solid #e8e5de;
        border-top: 1px solid #e8e5de;
        border-bottom: 1px solid #e8e5de;
    }
    
    .day-card h4 {
        color: #e67e22 !important;
        margin-bottom: 8px;
    }
    
    .day-card p {
        color: #555555 !important;
    }
    
    /* Ingredient tags */
    .ingredient-tag {
        display: inline-block;
        background: #fef5e7;
        color: #d35400 !important;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 0.85rem;
        border: 1px solid #f5d5a0;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
        color: white !important;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Time badges */
    .time-badge {
        display: inline-flex;
        align-items: center;
        background: #f0f0eb;
        color: #666666 !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        border: 1px solid #d0ccc0;
    }
    
    /* ==================== SCROLLBAR ==================== */
    
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
    
    /* ==================== LINKS ==================== */
    
    a {
        color: #d35400 !important;
        text-decoration: none;
    }
    
    a:hover {
        color: #e67e22 !important;
        text-decoration: underline;
    }
    
    /* ==================== DIVIDERS ==================== */
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #d0ccc0, transparent);
        margin: 24px 0;
    }
    
    /* ==================== SIDEBAR NAVIGATION ==================== */
    
    [data-testid="stSidebarNav"] {
        background-color: transparent;
    }
    
    [data-testid="stSidebarNav"] a {
        color: #333333 !important;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 2px 8px;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        background-color: #f0ebe0 !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background-color: #fef5e7 !important;
        color: #d35400 !important;
        font-weight: 600;
    }
    
    /* ==================== FOOTER ==================== */
    
    footer {
        color: #999999 !important;
    }
    
    footer a {
        color: #d35400 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)


def get_recipe_card_html(title, description, prep_time=None, category=None):
    """Generate HTML for a recipe card with light theme"""
    time_html = f'<span class="time-badge">⏱️ {prep_time} min</span>' if prep_time else ''
    category_html = f'<span class="category-badge">{category}</span>' if category else ''
    
    return f"""
    <div class="recipe-card">
        <h3>{title}</h3>
        <p>{description}</p>
        <div style="margin-top: 12px;">
            {time_html}
            {category_html}
        </div>
    </div>
    """


def get_day_card_html(day_name, meal_info):
    """Generate HTML for a day card in meal planning"""
    return f"""
    <div class="day-card">
        <h4>{day_name}</h4>
        <p>{meal_info}</p>
    </div>
    """


def get_metric_card_html(value, label, icon=""):
    """Generate HTML for a metric display card"""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def get_ingredient_tags_html(ingredients):
    """Generate HTML for ingredient tags"""
    tags = ''.join([f'<span class="ingredient-tag">{ing}</span>' for ing in ingredients])
    return f'<div style="margin: 8px 0;">{tags}</div>'
