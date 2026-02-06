import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Recepten Zoeken", page_icon="🔍", layout="wide")

# Import custom styles if available
try:
    from utils.styles import inject_custom_css
    inject_custom_css()
except:
    pass

st.title("🔍 Recepten Zoeken")
st.markdown("Zoek snelle en makkelijke recepten van **Lekker en Simpel**")

# Search input
search_query = st.text_input("Wat wil je koken?", placeholder="bijv. pasta, kip, vegetarisch...")

# Category filter
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Categorie", [
        "Alle categorieën",
        "Hoofdgerecht",
        "Vegetarisch",
        "Pasta",
        "Vis",
        "Vlees",
        "Soep",
        "Salade",
        "Ovenschotel",
        "Snacks"
    ])

with col2:
    only_quick = st.checkbox("Alleen snelle recepten (< 30 min)", value=True)

def search_recipes(query, category=None, quick_only=True):
    """Search recipes from lekkerensimpel.com"""
    recipes = []
    
    # Build search URL
    base_url = "https://www.lekkerensimpel.com/"
    
    if quick_only:
        search_url = f"{base_url}snelle-recepten/"
    else:
        search_url = base_url
    
    if query:
        search_url = f"{base_url}?s={query.replace(' ', '+')}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find recipe articles
        articles = soup.find_all('article', class_='post')
        
        if not articles:
            # Try alternative selectors
            articles = soup.find_all('div', class_='recipe-card')
        
        if not articles:
            # Try finding links to recipes
            links = soup.find_all('a', href=re.compile(r'lekkerensimpel\.com/[^/]+/$'))
            seen = set()
            for link in links[:20]:
                href = link.get('href', '')
                if href and href not in seen and 'category' not in href and 'tag' not in href:
                    seen.add(href)
                    title = link.get_text(strip=True)
                    if title and len(title) > 3:
                        # Try to get image
                        img = link.find('img')
                        img_url = img.get('src', '') if img else ''
                        
                        recipes.append({
                            'title': title,
                            'url': href,
                            'image': img_url,
                            'description': ''
                        })
        
        for article in articles[:12]:
            title_elem = article.find(['h2', 'h3', 'h4'])
            link_elem = article.find('a')
            img_elem = article.find('img')
            
            if title_elem and link_elem:
                title = title_elem.get_text(strip=True)
                url = link_elem.get('href', '')
                img_url = ''
                
                if img_elem:
                    img_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                
                # Get description if available
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                if title and url:
                    recipes.append({
                        'title': title,
                        'url': url,
                        'image': img_url,
                        'description': description[:150] + '...' if len(description) > 150 else description
                    })
    
    except Exception as e:
        st.error(f"Kon recepten niet laden: {str(e)}")
    
    return recipes

def get_recipe_details(url):
    """Get detailed recipe information"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        details = {
            'ingredients': [],
            'instructions': [],
            'prep_time': '',
            'servings': ''
        }
        
        # Find ingredients
        ing_section = soup.find('div', class_='wprm-recipe-ingredients') or soup.find('ul', class_='ingredients')
        if ing_section:
            items = ing_section.find_all('li')
            details['ingredients'] = [item.get_text(strip=True) for item in items]
        
        # Find instructions
        instr_section = soup.find('div', class_='wprm-recipe-instructions') or soup.find('ol', class_='instructions')
        if instr_section:
            steps = instr_section.find_all('li')
            details['instructions'] = [step.get_text(strip=True) for step in steps]
        
        # Find prep time
        time_elem = soup.find('span', class_='wprm-recipe-total-time-minutes')
        if time_elem:
            details['prep_time'] = time_elem.get_text(strip=True) + ' minuten'
        
        return details
    
    except Exception as e:
        return None

# Search button
if st.button("🔍 Zoeken", type="primary") or search_query:
    if search_query or category != "Alle categorieën":
        with st.spinner("Recepten zoeken..."):
            recipes = search_recipes(search_query, category, only_quick)
            
            if recipes:
                st.success(f"{len(recipes)} recepten gevonden!")
                
                # Display recipes in grid
                cols = st.columns(3)
                for idx, recipe in enumerate(recipes):
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div style="
                            background: white;
                            border-radius: 12px;
                            padding: 16px;
                            margin-bottom: 16px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                            border: 1px solid #e8e5de;
                        ">
                            <h4 style="color: #2c2c2c; margin-bottom: 8px;">{recipe['title']}</h4>
                            <p style="color: #666; font-size: 0.9em;">{recipe.get('description', '')}</p>
                            <a href="{recipe['url']}" target="_blank" style="
                                display: inline-block;
                                background: #e67e22;
                                color: white !important;
                                padding: 8px 16px;
                                border-radius: 6px;
                                text-decoration: none;
                                margin-top: 8px;
                                font-size: 0.9em;
                            ">Bekijk recept →</a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Geen recepten gevonden. Probeer een andere zoekterm.")
    else:
        st.warning("Voer een zoekterm in of selecteer een categorie.")

# Popular suggestions
st.markdown("---")
st.subheader("💡 Populaire zoektermen")

suggestion_cols = st.columns(6)
suggestions = ["Pasta", "Kip", "Ovenschotel", "Soep", "Salade", "Vegetarisch"]

for idx, suggestion in enumerate(suggestions):
    with suggestion_cols[idx]:
        if st.button(suggestion, key=f"sug_{idx}"):
            st.session_state['search_query'] = suggestion
            st.rerun()

# Direct link to website
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: #666;">Meer recepten ontdekken?</p>
    <a href="https://www.lekkerensimpel.com/snelle-recepten/" target="_blank" style="
        display: inline-block;
        background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
        color: white !important;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
    ">🍳 Bezoek Lekker en Simpel</a>
</div>
""", unsafe_allow_html=True)
