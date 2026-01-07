import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Marché Emplois Tech",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2563EB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMetric > label {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuration pour le scraping
REQUEST_DELAY = 2  # Délai en secondes entre les requêtes
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Fonctions utilitaires pour le scraping
def detect_work_mode(text):
    """Détecte le type de contrat (Remote/Hybrid/On-site) depuis le texte"""
    if not text:
        return "Non spécifié"
    
    text_lower = text.lower()
    remote_keywords = ['remote', 'télétravail', 'work from home', 'wfh', 'fully remote', '100% remote']
    hybrid_keywords = ['hybrid', 'hybride', 'partially remote', 'flexible', '2-3 days']
    onsite_keywords = ['on-site', 'on site', 'onsite', 'office', 'bureau', 'présentiel']
    
    remote_count = sum(1 for keyword in remote_keywords if keyword in text_lower)
    hybrid_count = sum(1 for keyword in hybrid_keywords if keyword in text_lower)
    onsite_count = sum(1 for keyword in onsite_keywords if keyword in text_lower)
    
    if remote_count > 0 and remote_count >= hybrid_count:
        return "Remote"
    elif hybrid_count > 0:
        return "Hybrid"
    elif onsite_count > 0:
        return "On-site"
    else:
        return "Non spécifié"

def extract_experience_level(text):
    """Extrait le niveau d'expérience requis depuis le texte"""
    if not text:
        return "Non spécifié"
    
    text_lower = text.lower()
    patterns = {
        "Junior": [r'junior', r'entry level', r'0-2 years', r'1-2 years', r'debutant'],
        "Mid-level": [r'mid-level', r'mid level', r'2-5 years', r'3-5 years', r'intermediate'],
        "Senior": [r'senior', r'5\+ years', r'5+ years', r'experienced', r'expérimenté'],
        "Lead/Principal": [r'lead', r'principal', r'staff', r'architect', r'10\+ years']
    }
    
    for level, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, text_lower):
                return level
    
    return "Non spécifié"

def extract_tech_stack(text):
    """Extrait les technologies mentionnées dans la description"""
    if not text:
        return []
    
    tech_keywords = {
        'Python', 'JavaScript', 'Java', 'TypeScript', 'Go', 'Rust', 'C++', 'C#',
        'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'FastAPI',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
        'PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Elasticsearch',
        'Git', 'CI/CD', 'Jenkins', 'GitHub Actions',
        'Machine Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
        'GraphQL', 'REST API', 'Microservices', 'Kafka', 'RabbitMQ'
    }
    
    found_techs = []
    text_lower = text.lower()
    
    for tech in tech_keywords:
        pattern = r'\b' + re.escape(tech.lower()) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            found_techs.append(tech)
    
    return found_techs

def extract_salary_range(text):
    """Extrait la fourchette salariale depuis le texte"""
    if not text:
        return None, None
    
    patterns = [
        r'\$?(\d+)[kK]?\s*-\s*\$?(\d+)[kK]?',
        r'€?(\d+)[,.]?\d*\s*-\s*€?(\d+)[,.]?\d*',
        r'(\d+)\s*to\s*(\d+)\s*k',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                min_sal = int(match.group(1).replace(',', '').replace('.', ''))
                max_sal = int(match.group(2).replace(',', '').replace('.', ''))
                if min_sal < 1000:
                    min_sal *= 1000
                if max_sal < 1000:
                    max_sal *= 1000
                return min_sal, max_sal
            except:
                continue
    
    return None, None

def extract_job_details_from_aijobs(url, soup=None):
    """Extrait les détails complets d'une offre d'emploi depuis aijobs.ai"""
    if soup is None:
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            return None
    
    job_data = {
        'job_title': None,
        'company_name': None,
        'location': None,
        'work_mode': None,
        'experience_level': None,
        'salary_min': None,
        'salary_max': None,
        'tech_stack': [],
        'job_description': None,
        'job_type': None,
        'job_url': url
    }
    
    title_elem = soup.find("div", class_="post-main-title2")
    if title_elem:
        job_data['job_title'] = title_elem.get_text(strip=True)
    
    company_elem = soup.find("span", string=lambda x: x and "at" in str(x).lower())
    if company_elem:
        company_span = company_elem.find_next_sibling("span")
        if company_span:
            job_data['company_name'] = company_span.get_text(strip=True)
    
    if not job_data['company_name']:
        company_link = soup.find("a", href=re.compile(r"/company/"))
        if company_link:
            company_name_elem = company_link.find("span", class_="tw-card-title")
            if company_name_elem:
                job_data['company_name'] = company_name_elem.get_text(strip=True)
    
    job_type_elem = soup.find("span", class_=re.compile(r"tw-bg-\[#0BA02C\]"))
    if job_type_elem:
        job_data['job_type'] = job_type_elem.get_text(strip=True)
    
    location_elem = soup.find("div", class_="remote")
    if location_elem:
        location_p = location_elem.find("p", class_="tw-mb-0")
        if location_p:
            job_data['location'] = location_p.get_text(strip=True)
    
    desc_container = soup.find("div", class_="job-description-container")
    if desc_container:
        description_text = desc_container.get_text(separator=' ', strip=True)
    else:
        body = soup.find('body')
        if body:
            description_text = body.get_text(separator=' ', strip=True)
        else:
            description_text = ""
    
    job_data['job_description'] = description_text[:5000]
    job_data['work_mode'] = detect_work_mode(description_text)
    job_data['experience_level'] = extract_experience_level(description_text)
    job_data['tech_stack'] = extract_tech_stack(description_text)
    
    min_sal, max_sal = extract_salary_range(description_text)
    job_data['salary_min'] = min_sal
    job_data['salary_max'] = max_sal
    
    if not min_sal and not max_sal:
        salary_section = soup.find("div", string=re.compile(r"Salary", re.IGNORECASE))
        if salary_section:
            salary_text = salary_section.get_text()
            min_sal, max_sal = extract_salary_range(salary_text)
            job_data['salary_min'] = min_sal
            job_data['salary_max'] = max_sal
    
    return job_data

def collect_job_urls_from_aijobs(max_pages=3, location="United%20States"):
    """Collecte les URLs des offres d'emploi depuis aijobs.ai"""
    BASE_URL = "https://aijobs.ai"
    job_urls = []
    
    for page_num in range(1, max_pages + 1):
        try:
            url = f"{BASE_URL}/engineer?location={location}&page={page_num}"
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all("a", class_="jobcardStyle1")
            page_job_urls = []
            
            for card in job_cards:
                href = card.get("href")
                if href:
                    if href.startswith('/'):
                        href = urljoin(BASE_URL, href)
                    if href not in page_job_urls:
                        page_job_urls.append(href)
            
            job_urls.extend(page_job_urls)
            time.sleep(REQUEST_DELAY)
            
        except Exception as e:
            continue
    
    return list(set(job_urls))

@st.cache_data
def load_and_process_data():
    """Charge et traite les données d'emplois"""
    try:
        df = pd.read_csv('data/donnees_marche_emploi.csv')
    except FileNotFoundError:
        return None
    
    # Nettoyer les données
    df_clean = df.copy()
    
    # Nettoyer les salaires
    if 'salary_min' in df_clean.columns:
        df_clean['salary_min'] = pd.to_numeric(df_clean['salary_min'], errors='coerce')
    if 'salary_max' in df_clean.columns:
        df_clean['salary_max'] = pd.to_numeric(df_clean['salary_max'], errors='coerce')
    
    # Calculer le salaire moyen si nécessaire
    if 'avg_salary' not in df_clean.columns or df_clean['avg_salary'].isna().all():
        df_clean['avg_salary'] = df_clean.apply(
            lambda row: (row['salary_min'] + row['salary_max']) / 2 
            if pd.notna(row['salary_min']) and pd.notna(row['salary_max']) 
            else None, axis=1
        )
    
    # Nettoyer les colonnes
    df_clean['work_mode'] = df_clean.get('work_mode', pd.Series()).fillna('Non spécifié')
    df_clean['experience_level'] = df_clean.get('experience_level', pd.Series()).fillna('Non spécifié')
    df_clean['location'] = df_clean.get('location', pd.Series()).fillna('Non spécifiée')
    
    return df_clean

def process_scraped_data(jobs_list):
    """Traite les données scrapées pour les rendre compatibles avec le dashboard"""
    if not jobs_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(jobs_list)
    
    # Convertir tech_stack en string
    df['tech_stack_str'] = df['tech_stack'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    
    # Calculer le salaire moyen
    df['avg_salary'] = df.apply(
        lambda row: (row['salary_min'] + row['salary_max']) / 2 
        if pd.notna(row['salary_min']) and pd.notna(row['salary_max']) 
        else None, axis=1
    )
    
    # Nettoyer les colonnes
    df['work_mode'] = df.get('work_mode', pd.Series()).fillna('Non spécifié')
    df['experience_level'] = df.get('experience_level', pd.Series()).fillna('Non spécifié')
    df['location'] = df.get('location', pd.Series()).fillna('Non spécifiée')
    
    return df

def extract_tech_from_string(tech_str):
    """Extrait les technologies depuis une chaîne séparée par virgules"""
    if pd.isna(tech_str) or not tech_str:
        return []
    return [t.strip() for t in str(tech_str).split(',') if t.strip()]

def create_work_mode_chart(df):
    """Crée un graphique de la distribution des types de contrats"""
    work_mode_counts = df['work_mode'].value_counts()
    
    # Palette de couleurs moderne
    colors = ['#6366F1', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981']
    
    fig = px.pie(
        values=work_mode_counts.values,
        names=work_mode_counts.index,
        title='Distribution des Types de Contrats',
        color_discrete_sequence=colors[:len(work_mode_counts)]
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    return fig

def create_experience_level_chart(df):
    """Crée un graphique de la distribution par niveau d'expérience"""
    exp_counts = df['experience_level'].value_counts()
    
    # Ordre logique des niveaux
    order = ['Junior', 'Mid-level', 'Senior', 'Lead/Principal', 'Non spécifié']
    exp_counts = exp_counts.reindex([x for x in order if x in exp_counts.index])
    
    fig = px.bar(
        x=exp_counts.index,
        y=exp_counts.values,
        title='Distribution par Niveau d\'Expérience',
        labels={'x': 'Niveau d\'Expérience', 'y': 'Nombre d\'Offres'},
        color=exp_counts.values,
        color_continuous_scale='Viridis'
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1.5)),
        hovertemplate='<b>%{x}</b><br>Nombre d\'offres: %{y}<extra></extra>',
        text=exp_counts.values,
        textposition='outside'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        height=450
    )
    return fig

def create_salary_by_work_mode(df):
    """Crée un graphique des salaires par type de contrat"""
    if 'avg_salary' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    # Palette de couleurs moderne
    color_map = {
        'Remote': '#6366F1',
        'Hybrid': '#8B5CF6',
        'On-site': '#EC4899',
        'Non spécifié': '#94A3B8'
    }
    
    fig = px.box(
        salary_data,
        x='work_mode',
        y='avg_salary',
        title='Distribution des Salaires par Type de Contrat',
        labels={'work_mode': 'Type de Contrat', 'avg_salary': 'Salaire Moyen (€)'},
        color='work_mode',
        color_discrete_map=color_map
    )
    fig.update_traces(
        boxmean='sd',
        hovertemplate='<b>%{x}</b><br>Salaire: €%{y:,.0f}<extra></extra>'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        showlegend=False,
        height=450
    )
    return fig

def create_salary_by_experience(df):
    """Crée un graphique des salaires par niveau d'expérience"""
    if 'avg_salary' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    # Ordre logique
    order = ['Junior', 'Mid-level', 'Senior', 'Lead/Principal']
    salary_data['experience_level'] = pd.Categorical(
        salary_data['experience_level'], 
        categories=[x for x in order if x in salary_data['experience_level'].unique()],
        ordered=True
    )
    salary_data = salary_data.sort_values('experience_level')
    
    # Palette de couleurs dégradée moderne
    color_map = {
        'Junior': '#10B981',
        'Mid-level': '#3B82F6',
        'Senior': '#8B5CF6',
        'Lead/Principal': '#EC4899'
    }
    
    fig = px.box(
        salary_data,
        x='experience_level',
        y='avg_salary',
        title='Distribution des Salaires par Niveau d\'Expérience',
        labels={'experience_level': 'Niveau d\'Expérience', 'avg_salary': 'Salaire Moyen (€)'},
        color='experience_level',
        color_discrete_map=color_map
    )
    fig.update_traces(
        boxmean='sd',
        hovertemplate='<b>%{x}</b><br>Salaire: €%{y:,.0f}<extra></extra>'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=18, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        showlegend=False,
        height=450
    )
    return fig

def create_top_tech_chart(df, top_n=15):
    """Crée un graphique des technologies les plus recherchées"""
    if 'tech_stack_str' not in df.columns:
        return None
    
    all_techs = []
    for tech_str in df['tech_stack_str'].dropna():
        techs = extract_tech_from_string(tech_str)
        all_techs.extend(techs)
    
    if not all_techs:
        return None
    
    tech_counter = Counter(all_techs)
    top_techs = tech_counter.most_common(top_n)
    
    techs_df = pd.DataFrame(top_techs, columns=['Technology', 'Count'])
    
    fig = px.bar(
        techs_df,
        x='Count',
        y='Technology',
        orientation='h',
        title=f'Top {top_n} Technologies les Plus Recherchées',
        labels={'Count': 'Nombre d\'Offres', 'Technology': 'Technologie'},
        color='Count',
        color_continuous_scale='Plasma'
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>%{y}</b><br>Nombre d\'offres: %{x}<extra></extra>',
        text=techs_df['Count'],
        textposition='outside'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=600
    )
    return fig

def create_location_chart(df, top_n=10):
    """Crée un graphique des localisations les plus fréquentes"""
    location_counts = df['location'].value_counts().head(top_n)
    
    fig = px.bar(
        x=location_counts.values,
        y=location_counts.index,
        orientation='h',
        title=f'Top {top_n} Localisations',
        labels={'x': 'Nombre d\'Offres', 'y': 'Localisation'},
        color=location_counts.values,
        color_continuous_scale='Turbo'
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>%{y}</b><br>Nombre d\'offres: %{x}<extra></extra>',
        text=location_counts.values,
        textposition='outside'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=500
    )
    return fig

def create_salary_distribution(df):
    """Crée un histogramme de la distribution des salaires"""
    if 'avg_salary' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    median_salary = salary_data['avg_salary'].median()
    mean_salary = salary_data['avg_salary'].mean()
    
    fig = px.histogram(
        salary_data,
        x='avg_salary',
        nbins=25,
        title='Distribution des Salaires',
        labels={'avg_salary': 'Salaire Moyen (€)', 'count': 'Nombre d\'Offres'},
        color_discrete_sequence=['#6366F1']
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>Salaire:</b> €%{x:,.0f}<br><b>Nombre d\'offres:</b> %{y}<extra></extra>'
    )
    
    # Ajouter ligne médiane
    fig.add_vline(
        x=median_salary,
        line_dash="dash",
        line_color="#EF4444",
        line_width=2,
        annotation_text=f"Médiane: €{median_salary:,.0f}",
        annotation_position="top",
        annotation_font_size=12,
        annotation_font_color="#EF4444"
    )
    
    # Ajouter ligne moyenne
    fig.add_vline(
        x=mean_salary,
        line_dash="dot",
        line_color="#10B981",
        line_width=2,
        annotation_text=f"Moyenne: €{mean_salary:,.0f}",
        annotation_position="top",
        annotation_font_size=12,
        annotation_font_color="#10B981"
    )
    
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        height=500
    )
    return fig

def create_salary_vs_tech_count_scatter(df):
    """Crée un scatter plot Salaire vs Nombre de Technologies"""
    if 'avg_salary' not in df.columns or 'tech_stack_str' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    # Calculer le nombre de technologies par offre
    salary_data['tech_count'] = salary_data['tech_stack_str'].apply(
        lambda x: len(extract_tech_from_string(x)) if pd.notna(x) else 0
    )
    
    # Filtrer les données avec au moins une technologie
    scatter_data = salary_data[salary_data['tech_count'] > 0].copy()
    if scatter_data.empty:
        return None
    
    fig = px.scatter(
        scatter_data,
        x='tech_count',
        y='avg_salary',
        color='work_mode',
        size='tech_count',
        hover_data=['job_title', 'company_name'],
        title='Relation entre Salaire et Nombre de Technologies',
        labels={'tech_count': 'Nombre de Technologies', 'avg_salary': 'Salaire Moyen (€)'},
        color_discrete_map={
            'Remote': '#6366F1',
            'Hybrid': '#8B5CF6',
            'On-site': '#EC4899',
            'Non spécifié': '#94A3B8'
        }
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1), opacity=0.7),
        hovertemplate='<b>%{hovertext}</b><br>Technologies: %{x}<br>Salaire: €%{y:,.0f}<extra></extra>',
        hovertext=scatter_data['job_title']
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', title='Nombre de Technologies'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_top_companies_chart(df, top_n=10):
    """Crée un graphique des meilleures entreprises par salaire moyen"""
    if 'company_name' not in df.columns or 'avg_salary' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    company_stats = salary_data.groupby('company_name')['avg_salary'].agg(['mean', 'count']).reset_index()
    company_stats = company_stats[company_stats['count'] >= 1]
    company_stats = company_stats.sort_values('mean', ascending=False).head(top_n)
    
    fig = px.bar(
        company_stats,
        x='mean',
        y='company_name',
        orientation='h',
        title=f'Top {top_n} Entreprises par Salaire Moyen',
        labels={'mean': 'Salaire Moyen (€)', 'company_name': 'Entreprise'},
        color='mean',
        color_continuous_scale='Viridis',
        hover_data=['count']
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>%{y}</b><br>Salaire moyen: €%{x:,.0f}<br>Nombre d\'offres: %{customdata[0]}<extra></extra>',
        text=company_stats['mean'].apply(lambda x: f"€{x:,.0f}")
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=500
    )
    return fig

def create_tech_salary_correlation(df, top_n=10):
    """Crée un graphique montrant le salaire moyen par technologie"""
    if 'tech_stack_str' not in df.columns or 'avg_salary' not in df.columns:
        return None
    
    salary_data = df[df['avg_salary'].notna()].copy()
    if salary_data.empty:
        return None
    
    # Extraire toutes les technologies et leurs salaires
    tech_salaries = {}
    for idx, row in salary_data.iterrows():
        techs = extract_tech_from_string(row.get('tech_stack_str', ''))
        salary = row['avg_salary']
        for tech in techs:
            if tech not in tech_salaries:
                tech_salaries[tech] = []
            tech_salaries[tech].append(salary)
    
    # Calculer le salaire moyen par technologie
    tech_avg_salary = {
        tech: np.mean(salaries) 
        for tech, salaries in tech_salaries.items() 
        if len(salaries) >= 2  # Au moins 2 offres
    }
    
    if not tech_avg_salary:
        return None
    
    # Trier et prendre le top N
    sorted_techs = sorted(tech_avg_salary.items(), key=lambda x: x[1], reverse=True)[:top_n]
    techs_df = pd.DataFrame(sorted_techs, columns=['Technology', 'AvgSalary'])
    
    fig = px.bar(
        techs_df,
        x='AvgSalary',
        y='Technology',
        orientation='h',
        title=f'Top {top_n} Technologies par Salaire Moyen',
        labels={'AvgSalary': 'Salaire Moyen (€)', 'Technology': 'Technologie'},
        color='AvgSalary',
        color_continuous_scale='Plasma'
    )
    fig.update_traces(
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>%{y}</b><br>Salaire moyen: €%{x:,.0f}<extra></extra>',
        text=techs_df['AvgSalary'].apply(lambda x: f"€{x:,.0f}"),
        textposition='outside'
    )
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat='€,.0f'),
        yaxis=dict(showgrid=False, categoryorder='total ascending'),
        height=500
    )
    return fig

def create_comparison_chart(original_df, filtered_df):
    """Crée un graphique comparant les données avant et après filtres"""
    if original_df.empty or filtered_df.empty:
        return None
    
    comparison_data = {
        'Métrique': ['Total Offres', 'Salaire Médian', 'Salaire Moyen'],
        'Avant Filtres': [
            len(original_df),
            original_df['avg_salary'].median() if 'avg_salary' in original_df.columns else 0,
            original_df['avg_salary'].mean() if 'avg_salary' in original_df.columns else 0
        ],
        'Après Filtres': [
            len(filtered_df),
            filtered_df['avg_salary'].median() if 'avg_salary' in filtered_df.columns else 0,
            filtered_df['avg_salary'].mean() if 'avg_salary' in filtered_df.columns else 0
        ]
    }
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Avant Filtres',
        x=comp_df['Métrique'],
        y=comp_df['Avant Filtres'],
        marker_color='#94A3B8',
        text=comp_df['Avant Filtres'].apply(lambda x: f"{x:,.0f}" if x > 100 else f"{x:,.2f}"),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Après Filtres',
        x=comp_df['Métrique'],
        y=comp_df['Après Filtres'],
        marker_color='#6366F1',
        text=comp_df['Après Filtres'].apply(lambda x: f"{x:,.0f}" if x > 100 else f"{x:,.2f}"),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Comparaison Avant/Après Filtres',
        xaxis_title='Métrique',
        yaxis_title='Valeur',
        barmode='group',
        font=dict(family="Arial, sans-serif", size=12),
        title_font=dict(size=20, color='#1F2937'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def get_all_technologies(df):
    """Extrait toutes les technologies uniques du DataFrame"""
    if 'tech_stack_str' not in df.columns:
        return []
    
    all_techs = set()
    for tech_str in df['tech_stack_str'].dropna():
        techs = extract_tech_from_string(tech_str)
        all_techs.update(techs)
    
    return sorted(list(all_techs))

def main():
    st.markdown('<h1 class="main-header">💼 Dashboard Marché Emplois Tech</h1>', unsafe_allow_html=True)
    
    # Initialiser session_state pour stocker les données scrapées
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = None
    
    # Section de choix : Données existantes ou Scraping
    st.sidebar.header("📥 Source de Données")
    data_source = st.sidebar.radio(
        "Choisir la source de données",
        ["📁 Données existantes", "🌐 Scraper depuis internet"],
        help="Utilisez les données sauvegardées ou scrapez de nouvelles données"
    )
    
    df = None
    
    if data_source == "📁 Données existantes":
        # Charger les données existantes
        with st.spinner('Chargement des données...'):
            df = load_and_process_data()
        
        if df is None or df.empty:
            st.warning("⚠️ Aucune donnée sauvegardée trouvée. Utilisez l'option de scraping pour créer des données.")
            st.info("💡 Vous pouvez aussi exécuter le notebook `Partie1-scraper_emplois.ipynb` pour créer le fichier CSV.")
            return
        
        st.success(f"✅ {len(df)} offres d'emploi chargées depuis le fichier CSV")
    
    else:
        # Section de scraping
        st.sidebar.header("⚙️ Paramètres de Scraping")
        
        max_pages = st.sidebar.slider("Nombre de pages à scraper", 1, 5, 3)
        max_jobs = st.sidebar.slider("Nombre maximum d'emplois", 10, 100, 50)
        
        # Sélection de localisation avec options prédéfinies
        location_options = {
            "🇺🇸 États-Unis": "United%20States",
            "🇫🇷 France": "France",
            "🇬🇧 Royaume-Uni": "United%20Kingdom",
            "🇨🇦 Canada": "Canada",
            "🇩🇪 Allemagne": "Germany",
            "🇪🇸 Espagne": "Spain",
            "🇮🇹 Italie": "Italy",
            "🇳🇱 Pays-Bas": "Netherlands",
            "🇧🇪 Belgique": "Belgium",
            "🌍 Tous les pays": "All"
        }
        
        selected_location_option = st.sidebar.selectbox(
            "Localisation",
            options=list(location_options.keys()),
            index=0,
            help="Sélectionnez un pays ou choisissez 'Tous les pays'"
        )
        
        # Récupérer la valeur encodée
        location = location_options[selected_location_option]
        
        # Option pour saisie personnalisée
        custom_location = st.sidebar.text_input(
            "Ou saisir une localisation personnalisée",
            value="",
            help="Laissez vide pour utiliser la sélection ci-dessus. Utilisez %20 pour les espaces (ex: 'Paris%20France')"
        )
        
        if custom_location:
            location = custom_location
        
        if st.sidebar.button("🚀 Lancer le Scraping", type="primary"):
            if st.session_state.scraped_data is None:
                # Lancer le scraping
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Collecter les URLs
                status_text.text("🔍 Collecte des URLs d'emplois...")
                job_urls = collect_job_urls_from_aijobs(max_pages=max_pages, location=location)
                progress_bar.progress(0.3)
                
                # Extraire les détails
                status_text.text(f"📋 Extraction des détails de {min(max_jobs, len(job_urls))} emplois...")
                all_jobs = []
                
                for i, job_url in enumerate(job_urls[:max_jobs], 1):
                    job_data = extract_job_details_from_aijobs(job_url)
                    if job_data and job_data.get('job_title'):
                        all_jobs.append(job_data)
                    
                    # Mettre à jour la barre de progression
                    progress = 0.3 + (i / min(max_jobs, len(job_urls))) * 0.7
                    progress_bar.progress(progress)
                    status_text.text(f"📋 Traitement: {i}/{min(max_jobs, len(job_urls))} emplois...")
                    
                    time.sleep(REQUEST_DELAY)
                
                # Traiter les données
                status_text.text("🔄 Traitement des données...")
                df = process_scraped_data(all_jobs)
                
                # Sauvegarder dans session_state
                st.session_state.scraped_data = df
                
                # Sauvegarder dans le fichier CSV
                if not df.empty:
                    columns_to_save = [
                        'job_title', 'company_name', 'location', 'work_mode', 
                        'experience_level', 'salary_min', 'salary_max', 'avg_salary',
                        'tech_stack_str', 'job_description', 'job_url'
                    ]
                    save_df = df[[col for col in columns_to_save if col in df.columns]].copy()
                    save_df.to_csv('data/donnees_marche_emploi.csv', index=False, encoding='utf-8')
                
                progress_bar.progress(1.0)
                status_text.text(f"✅ {len(df)} emplois scrapés et sauvegardés avec succès!")
                st.success(f"✅ Scraping terminé ! {len(df)} offres d'emploi récupérées.")
            else:
                st.info("💡 Données déjà scrapées dans cette session. Cliquez sur 'Réinitialiser' pour scraper à nouveau.")
        
        if st.sidebar.button("🔄 Réinitialiser"):
            st.session_state.scraped_data = None
            st.rerun()
        
        # Utiliser les données scrapées ou existantes
        if st.session_state.scraped_data is not None:
            df = st.session_state.scraped_data
            st.info(f"📊 Utilisation des données scrapées: {len(df)} offres")
        else:
            # Essayer de charger les données existantes en fallback
            df = load_and_process_data()
            if df is None or df.empty:
                st.info("👆 Configurez les paramètres ci-dessus et cliquez sur 'Lancer le Scraping' pour commencer.")
                return
    
    if df is None or df.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        return
    
    # Sidebar - Filtres
    st.sidebar.header("🔍 Filtres")
    
    # Recherche textuelle
    search_query = st.sidebar.text_input("🔎 Recherche (titre, entreprise)", "")
    
    # Filtre par type de contrat
    work_modes = ['Tous'] + sorted(df['work_mode'].unique().tolist())
    selected_work_mode = st.sidebar.selectbox("Type de Contrat", work_modes)
    
    # Filtre par niveau d'expérience
    experience_levels = ['Tous'] + sorted(df['experience_level'].unique().tolist())
    selected_experience = st.sidebar.selectbox("Niveau d'Expérience", experience_levels)
    
    # Filtre par localisation
    locations = ['Toutes'] + sorted(df['location'].unique().tolist())
    selected_location = st.sidebar.selectbox("Localisation", locations)
    
    # Filtre multi-sélection pour les technologies
    all_techs = get_all_technologies(df)
    if all_techs:
        selected_techs = st.sidebar.multiselect(
            "🔧 Technologies recherchées",
            options=all_techs,
            default=[],
            help="Sélectionnez une ou plusieurs technologies"
        )
    else:
        selected_techs = []
    
    # Filtre par nombre de technologies
    if 'tech_stack_str' in df.columns:
        df['tech_count'] = df['tech_stack_str'].apply(
            lambda x: len(extract_tech_from_string(x)) if pd.notna(x) else 0
        )
        max_tech_count = int(df['tech_count'].max()) if 'tech_count' in df.columns else 10
        tech_count_range = st.sidebar.slider(
            "Nombre de Technologies",
            min_value=0,
            max_value=max_tech_count,
            value=(0, max_tech_count),
            help="Filtrer par nombre de technologies mentionnées"
        )
    else:
        tech_count_range = (0, 10)
    
    # Filtre par salaire
    if 'avg_salary' in df.columns:
        salary_data = df[df['avg_salary'].notna()]
        if not salary_data.empty:
            min_salary = float(salary_data['avg_salary'].min())
            max_salary = float(salary_data['avg_salary'].max())
            salary_range = st.sidebar.slider(
                "Plage de Salaire (€)",
                min_value=min_salary,
                max_value=max_salary,
                value=(min_salary, max_salary),
                step=1000.0
            )
        else:
            salary_range = (0, 200000)
    else:
        salary_range = (0, 200000)
    
    # Appliquer les filtres
    filtered_df = df.copy()
    
    # Recherche textuelle
    if search_query:
        mask = (
            filtered_df['job_title'].str.contains(search_query, case=False, na=False) |
            filtered_df['company_name'].str.contains(search_query, case=False, na=False) |
            filtered_df['job_description'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_work_mode != 'Tous':
        filtered_df = filtered_df[filtered_df['work_mode'] == selected_work_mode]
    
    if selected_experience != 'Tous':
        filtered_df = filtered_df[filtered_df['experience_level'] == selected_experience]
    
    if selected_location != 'Toutes':
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    
    # Filtre par technologies (multi-sélection)
    if selected_techs:
        tech_mask = filtered_df['tech_stack_str'].apply(
            lambda x: any(tech in str(x) for tech in selected_techs) if pd.notna(x) else False
        )
        filtered_df = filtered_df[tech_mask]
    
    # Filtre par nombre de technologies
    if 'tech_count' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['tech_count'] >= tech_count_range[0]) & 
            (filtered_df['tech_count'] <= tech_count_range[1])
        ]
    
    if 'avg_salary' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['avg_salary'].isna()) | 
            ((filtered_df['avg_salary'] >= salary_range[0]) & (filtered_df['avg_salary'] <= salary_range[1]))
        ]
    
    # Statistiques principales
    st.header("📊 Statistiques Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Offres",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        if 'avg_salary' in filtered_df.columns:
            salary_data = filtered_df[filtered_df['avg_salary'].notna()]
            if not salary_data.empty:
                median_salary = salary_data['avg_salary'].median()
                st.metric(
                    label="Salaire Médian",
                    value=f"€{median_salary:,.0f}",
                    delta=f"€{median_salary - df[df['avg_salary'].notna()]['avg_salary'].median():,.0f}" if len(filtered_df) != len(df) else None
                )
            else:
                st.metric(label="Salaire Médian", value="N/A")
        else:
            st.metric(label="Salaire Médian", value="N/A")
    
    with col3:
        unique_companies = filtered_df['company_name'].nunique() if 'company_name' in filtered_df.columns else 0
        st.metric(
            label="Entreprises",
            value=f"{unique_companies:,}",
            delta=f"{unique_companies - df['company_name'].nunique():,}" if len(filtered_df) != len(df) and 'company_name' in df.columns else None
        )
    
    with col4:
        remote_count = len(filtered_df[filtered_df['work_mode'] == 'Remote'])
        st.metric(
            label="Offres Remote",
            value=f"{remote_count:,}",
            delta=f"{remote_count - len(df[df['work_mode'] == 'Remote']):,}" if len(filtered_df) != len(df) else None
        )
    
    # Section de comparaison avant/après filtres
    if len(filtered_df) != len(df):
        st.header("📊 Impact des Filtres")
        comparison_chart = create_comparison_chart(df, filtered_df)
        if comparison_chart:
            st.plotly_chart(comparison_chart, use_container_width=True, key="comparison_chart")
    
    # Section des graphiques
    st.header("📈 Analyses du Marché")
    
    # Créer des onglets
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Types de Contrats", 
        "Niveaux d'Expérience", 
        "Technologies", 
        "Salaires", 
        "Géographie",
        "Analyses Avancées"
    ])
    
    with tab1:
        st.subheader("Analyse des Types de Contrats")
        if len(filtered_df) > 0:
            work_mode_chart = create_work_mode_chart(filtered_df)
            st.plotly_chart(work_mode_chart, use_container_width=True, key="work_mode_pie")
            
            # Statistiques détaillées
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Répartition par type de contrat :**")
                work_mode_stats = filtered_df['work_mode'].value_counts()
                st.dataframe(work_mode_stats, use_container_width=True)
            
            with col2:
                if 'avg_salary' in filtered_df.columns:
                    salary_by_mode = create_salary_by_work_mode(filtered_df)
                    if salary_by_mode:
                        st.plotly_chart(salary_by_mode, use_container_width=True, key="salary_by_mode_tab1")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    with tab2:
        st.subheader("Analyse par Niveau d'Expérience")
        if len(filtered_df) > 0:
            exp_chart = create_experience_level_chart(filtered_df)
            st.plotly_chart(exp_chart, use_container_width=True, key="exp_level_bar")
            
            if 'avg_salary' in filtered_df.columns:
                salary_by_exp = create_salary_by_experience(filtered_df)
                if salary_by_exp:
                    st.plotly_chart(salary_by_exp, use_container_width=True, key="salary_by_exp_tab2")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    with tab3:
        st.subheader("Technologies les Plus Recherchées")
        if len(filtered_df) > 0:
            tech_chart = create_top_tech_chart(filtered_df)
            if tech_chart:
                st.plotly_chart(tech_chart, use_container_width=True, key="top_tech_chart")
            else:
                st.info("Données de technologies non disponibles.")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    with tab4:
        st.subheader("Analyse des Salaires")
        if len(filtered_df) > 0:
            salary_dist = create_salary_distribution(filtered_df)
            if salary_dist:
                st.plotly_chart(salary_dist, use_container_width=True, key="salary_dist_hist")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'avg_salary' in filtered_df.columns:
                    salary_by_mode = create_salary_by_work_mode(filtered_df)
                    if salary_by_mode:
                        st.plotly_chart(salary_by_mode, use_container_width=True, key="salary_by_mode_tab4")
            
            with col2:
                if 'avg_salary' in filtered_df.columns:
                    salary_by_exp = create_salary_by_experience(filtered_df)
                    if salary_by_exp:
                        st.plotly_chart(salary_by_exp, use_container_width=True, key="salary_by_exp_tab4")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    with tab5:
        st.subheader("Analyse Géographique")
        if len(filtered_df) > 0:
            location_chart = create_location_chart(filtered_df)
            st.plotly_chart(location_chart, use_container_width=True, key="location_chart")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    with tab6:
        st.subheader("Analyses Avancées")
        if len(filtered_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 Relation Salaire vs Technologies**")
                scatter_chart = create_salary_vs_tech_count_scatter(filtered_df)
                if scatter_chart:
                    st.plotly_chart(scatter_chart, use_container_width=True, key="salary_tech_scatter")
                else:
                    st.info("Données insuffisantes pour cette analyse.")
            
            with col2:
                st.write("**🏢 Top Entreprises**")
                companies_chart = create_top_companies_chart(filtered_df)
                if companies_chart:
                    st.plotly_chart(companies_chart, use_container_width=True, key="top_companies")
                else:
                    st.info("Données insuffisantes pour cette analyse.")
            
            st.write("**💰 Technologies les Mieux Payées**")
            tech_salary_chart = create_tech_salary_correlation(filtered_df)
            if tech_salary_chart:
                st.plotly_chart(tech_salary_chart, use_container_width=True, key="tech_salary_corr")
            else:
                st.info("Données insuffisantes pour cette analyse.")
        else:
            st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    
    # Tableau des emplois
    st.header("📋 Liste des Offres d'Emploi")
    
    display_columns = []
    if 'job_title' in filtered_df.columns:
        display_columns.append('job_title')
    if 'company_name' in filtered_df.columns:
        display_columns.append('company_name')
    if 'location' in filtered_df.columns:
        display_columns.append('location')
    if 'work_mode' in filtered_df.columns:
        display_columns.append('work_mode')
    if 'experience_level' in filtered_df.columns:
        display_columns.append('experience_level')
    if 'avg_salary' in filtered_df.columns:
        display_columns.append('avg_salary')
    
    if display_columns:
        display_df = filtered_df[display_columns].copy()
        
        # Formater le salaire
        if 'avg_salary' in display_df.columns:
            display_df['avg_salary'] = display_df['avg_salary'].apply(
                lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
            )
        
        # Renommer les colonnes
        column_mapping = {
            'job_title': 'Titre',
            'company_name': 'Entreprise',
            'location': 'Localisation',
            'work_mode': 'Type de Contrat',
            'experience_level': 'Niveau',
            'avg_salary': 'Salaire Moyen'
        }
        display_df = display_df.rename(columns=column_mapping)
        
        # Trier par salaire si disponible
        if 'Salaire Moyen' in display_df.columns:
            # Trier par valeur numérique
            sort_df = filtered_df[display_columns].copy()
            sort_df = sort_df.sort_values('avg_salary', ascending=False, na_position='last')
            sort_df['avg_salary'] = sort_df['avg_salary'].apply(
                lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A"
            )
            sort_df = sort_df.rename(columns=column_mapping)
            st.dataframe(sort_df, use_container_width=True, height=400)
        else:
            st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.warning("Aucune colonne à afficher.")
    
    # Bouton de téléchargement
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger les données filtrées (CSV)",
        data=csv,
        file_name="emplois_filtres.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()

