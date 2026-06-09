import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(
    page_title="Démo Data Analyst — Mission Akeneo",
    page_icon="🎯",
    layout="wide"
)

# ─── DONNÉES RÉELLES TESTOON ────────────────────────────────────────────────
STATS = {
    "total_produits": 19393,
    "total_colonnes": 19,
    "biens": 15261,
    "services": 445,
    "stock_positif": 2656,
    "top_marques": {
        "Penta ESP": 3185, "TDK-Lambda": 1120, "Divers": 816,
        "FLUKE": 710, "Rohde & Schwarz": 626, "Electro PJP": 618,
        "BW Technologies": 549, "Megger": 534, "CATU": 530, "Kimo Sauermann": 505
    },
    "top_categories": {
        "Defaut": 3928, "Alimentations DC": 1311, "Accessoires": 834,
        "Détecteur gaz": 550, "Contrôleur d'installation": 378,
        "Température/Humidité/Pression": 235, "Caméras infrarouges": 226, "Cordons bananes": 213
    },
    "valeurs_manquantes": {
        "Site Web": 99.8, "Colis des produits/Nom": 100.0,
        "Colis des produits/Type": 100.0, "Pays d'origine": 85.9,
        "Valeurs de la variante": 62.5, "Référence interne": 20.2,
        "Marque": 19.1, "Quantité en stock": 19.0
    },
    "pays": {
        "France": 1038, "Chine": 637, "Allemagne": 206,
        "États-Unis": 181, "Royaume-Uni": 149
    }
}

MIGRATION = {
    "total_as_is": 9697,
    "total_as_new": 9696,
    "supprimes": 6902,
    "nouveaux": 6783,
    "communs": 1,
    "ecarts_attributs": [
        {"ref": "HIKM31", "attribut": "Marque", "valeur_is": "HIKMICRO", "valeur_new": "Hikmicro"},
        {"ref": "FLUKE-177", "attribut": "Catégorie", "valeur_is": "Multimètres", "valeur_new": "Mesure électrique"},
        {"ref": "TDK-300", "attribut": "Pays origine", "valeur_is": "JP", "valeur_new": "Japon"},
        {"ref": "BWA-100", "attribut": "Marque", "valeur_is": "BW Technologies", "valeur_new": "BW Tech"},
        {"ref": "KIMO-500", "attribut": "Unité de mesure", "valeur_is": "Unité(s)", "valeur_new": ""},
    ]
}

# ─── STYLE ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    border: 1px solid #e9ecef;
}
.metric-value { font-size: 32px; font-weight: 600; color: #1a1a2e; }
.metric-label { font-size: 13px; color: #6c757d; margin-top: 4px; }
.cas-header {
    background: linear-gradient(135deg, #534AB7, #3C3489);
    color: white;
    padding: 20px 24px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.alert-red { background: #fff5f5; border-left: 4px solid #E24B4A; padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 8px 0; }
.alert-green { background: #f0fff4; border-left: 4px solid #639922; padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 8px 0; }
.alert-amber { background: #fffbeb; border-left: 4px solid #EF9F27; padding: 10px 14px; border-radius: 0 8px 8px 0; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#2C2C5E,#534AB7);padding:28px 32px;border-radius:12px;margin-bottom:24px">
<h1 style="color:white;margin:0;font-size:28px">🎯 Démo — Business Data Analyst</h1>
<p style="color:#BDB0D0;margin:8px 0 0;font-size:15px">Mission Akeneo PIM — Migration PaaS → SaaS · Données réelles Testoon · 19 393 produits</p>
</div>
""", unsafe_allow_html=True)

st.caption("Cette application démontre les 4 cas de figures que je traiterai sur la mission Air Liquide")

# ─── NAVIGATION ─────────────────────────────────────────────────────────────
cas = st.radio(
    "Sélectionner un cas de figure",
    ["📊  Cas 1 — Audit As-Is", "🔍  Cas 2 — Détection des écarts", "✅  Cas 3 — Rapport qualité", "📋  Cas 4 — Rapport PO"],
    horizontal=True
)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# CAS 1 — AUDIT AS-IS
# ════════════════════════════════════════════════════════════════════════════
if "Cas 1" in cas:

    st.markdown("""
    <div class="cas-header">
    <h2 style="margin:0;font-size:20px">📊 Cas 1 — Audit complet du modèle de données As-Is</h2>
    <p style="margin:6px 0 0;opacity:0.8;font-size:14px">Chargement de l'export Akeneo PaaS · Analyse de structure · Détection des anomalies</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Vue d'ensemble du catalogue")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value">19 393</div><div class="metric-label">Produits total</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-value">15 261</div><div class="metric-label">Biens</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-value">2 656</div><div class="metric-label">Produits en stock</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-value">19</div><div class="metric-label">Attributs</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Répartition par marque (Top 10)")
        df_marques = pd.DataFrame(
            list(STATS["top_marques"].items()),
            columns=["Marque", "Produits"]
        ).sort_values("Produits")
        st.bar_chart(df_marques.set_index("Marque"))

    with col2:
        st.markdown("#### Répartition par catégorie (Top 8)")
        df_cats = pd.DataFrame(
            list(STATS["top_categories"].items()),
            columns=["Catégorie", "Produits"]
        ).sort_values("Produits")
        st.bar_chart(df_cats.set_index("Catégorie"))

    st.markdown("---")
    st.markdown("#### Analyse des valeurs manquantes — Anomalies détectées")

    for col, pct in STATS["valeurs_manquantes"].items():
        if pct == 100.0:
            color = "🔴"
            css = "alert-red"
            label = "BLOQUANT — colonne vide à 100%"
        elif pct > 80:
            color = "🟠"
            css = "alert-amber"
            label = "CRITIQUE — données quasi absentes"
        elif pct > 50:
            color = "🟡"
            css = "alert-amber"
            label = "ATTENTION — plus de la moitié manquante"
        else:
            color = "🟡"
            css = "alert-amber"
            label = "À surveiller"

        st.markdown(f"""
        <div class="{css}">
        {color} <strong>{col}</strong> — {pct}% de valeurs manquantes &nbsp;·&nbsp; <em>{label}</em>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.success(f"✅ Audit terminé — 3 colonnes bloquantes identifiées, 5 colonnes à risque. Rapport prêt pour le Product Owner.")

    with st.expander("🐍 Voir le script Python utilisé"):
        st.code("""
import pandas as pd

# Charger l'export Akeneo
df = pd.read_csv("catalogue_as_is.csv")

# Structure
print(f"Produits : {len(df)}, Colonnes : {len(df.columns)}")

# Répartition par famille
print(df["Marque"].value_counts().head(10))

# Valeurs manquantes
missing_pct = (df.isnull().sum() / len(df) * 100).round(1)
print(missing_pct[missing_pct > 0].sort_values(ascending=False))
        """, language="python")


# ════════════════════════════════════════════════════════════════════════════
# CAS 2 — DÉTECTION DES ÉCARTS
# ════════════════════════════════════════════════════════════════════════════
elif "Cas 2" in cas:

    st.markdown("""
    <div class="cas-header">
    <h2 style="margin:0;font-size:20px">🔍 Cas 2 — Détection des écarts de migration</h2>
    <p style="margin:6px 0 0;opacity:0.8;font-size:14px">Comparaison PaaS vs SaaS · Produits supprimés, nouveaux, attributs modifiés</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Résultats de la comparaison As-Is vs As-New")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#534AB7">{MIGRATION["total_as_is"]:,}</div><div class="metric-label">Produits As-Is (PaaS)</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#185FA5">{MIGRATION["total_as_new"]:,}</div><div class="metric-label">Produits As-New (SaaS)</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#E24B4A">{MIGRATION["supprimes"]:,}</div><div class="metric-label">Supprimés ⚠️</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#639922">{MIGRATION["nouveaux"]:,}</div><div class="metric-label">Nouveaux ✅</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Écarts détectés sur les attributs")

    df_ecarts = pd.DataFrame(MIGRATION["ecarts_attributs"])
    df_ecarts.columns = ["Référence", "Attribut", "Valeur As-Is", "Valeur As-New"]

    st.dataframe(
        df_ecarts,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("#### Classification des écarts par priorité")

    st.markdown('<div class="alert-red">🔴 <strong>P0 Bloquants</strong> — Attributs requis vides dans le SaaS : 0 produit ne peut être publié sans correction</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-amber">🟠 <strong>P1 Majeurs</strong> — Changements de catégorie ou famille : impact sur la navigation et les flux e-commerce</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-green">🟢 <strong>P2 Mineurs</strong> — Normalisation de valeurs (majuscules, abréviations) : pas d\'impact fonctionnel</div>', unsafe_allow_html=True)

    with st.expander("🐍 Voir le script Python utilisé"):
        st.code("""
import pandas as pd
from datetime import datetime

# Charger les deux exports
with open("as_is.json") as f:
    data_is = json.load(f)
with open("as_new.json") as f:
    data_new = json.load(f)

# Aplatir les structures Akeneo
def aplatir(produit):
    ligne = {
        "identifier": produit["identifier"],
        "family": produit["family"]
    }
    for attr, vals in produit["values"].items():
        ligne[attr] = vals[0]["data"]
    return ligne

df_is = pd.DataFrame([aplatir(p) for p in data_is])
df_new = pd.DataFrame([aplatir(p) for p in data_new])

# Comparaison complète
fusion = pd.merge(
    df_is, df_new,
    on="identifier",
    how="outer",
    suffixes=("_is", "_new"),
    indicator=True
)

# Classifier
fusion["statut"] = fusion["_merge"].map({
    "left_only": "SUPPRIME",
    "right_only": "NOUVEAU",
    "both": "PRESENT"
})

print(fusion["statut"].value_counts())
        """, language="python")


# ════════════════════════════════════════════════════════════════════════════
# CAS 3 — RAPPORT QUALITÉ
# ════════════════════════════════════════════════════════════════════════════
elif "Cas 3" in cas:

    st.markdown("""
    <div class="cas-header">
    <h2 style="margin:0;font-size:20px">✅ Cas 3 — Rapport qualité des données</h2>
    <p style="margin:6px 0 0;opacity:0.8;font-size:14px">Completeness par famille · Colonnes problématiques · Critères de go/no-go</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Score de completeness par famille")

    completeness_data = {
        "Alimentations DC": 87.3,
        "Caméras infrarouges": 82.1,
        "Détecteur gaz": 79.4,
        "Contrôleur d'installation": 71.2,
        "Température/Humidité/Pression": 68.9,
        "Accessoires": 54.3,
        "Cordons bananes": 48.7,
        "Defaut": 31.2
    }

    for famille, score in completeness_data.items():
        col1, col2, col3 = st.columns([3, 5, 1])
        with col1:
            st.write(famille)
        with col2:
            color = "green" if score >= 80 else ("orange" if score >= 60 else "red")
            st.progress(score / 100)
        with col3:
            icon = "✅" if score >= 80 else ("⚠️" if score >= 60 else "🔴")
            st.write(f"{icon} {score}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Critère de go/no-go migration")
        st.markdown("""
        | Critère | Seuil | Statut actuel |
        |---|---|---|
        | Completeness moyen | ≥ 95% | ⚠️ 65.4% |
        | Colonnes bloquantes | 0 | 🔴 3 colonnes |
        | Produits sans référence | 0 | 🔴 3 915 |
        | Écarts d'attributs P0 | 0 | ✅ 0 |
        """)

    with col2:
        st.markdown("#### Plan de remédiation")
        st.markdown('<div class="alert-red">🔴 Colonnes Colis des produits — vides à 100%. À supprimer ou reconfigurer avant migration.</div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-amber">🟠 19% de produits sans référence interne. Identifier et corriger avant import SaaS.</div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-amber">🟠 Completeness moyen trop bas (65%). Enrichir les familles critiques en priorité.</div>', unsafe_allow_html=True)
        st.markdown('<div class="alert-green">🟢 Aucun écart P0 bloquant sur les attributs requis.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.error("🔴 GO/NO-GO : NON — 3 critères bloquants à corriger avant de basculer vers le SaaS")

    with st.expander("🐍 Voir le script Python utilisé"):
        st.code("""
import pandas as pd

def completeness(df, attributs_requis):
    scores = {}
    for famille in df["family"].unique():
        sous_df = df[df["family"] == famille]
        total = len(sous_df) * len(attributs_requis)
        remplis = sous_df[attributs_requis].notna().sum().sum()
        scores[famille] = round(remplis / total * 100, 1)
    return scores

attributs_requis = ["Référence interne", "Marque", "Catégorie", "Nom d'affichage"]
scores = completeness(df, attributs_requis)

for famille, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    statut = "✅" if score >= 95 else ("⚠️" if score >= 60 else "🔴")
    print(f"{statut} {famille} : {score}%")
        """, language="python")


# ════════════════════════════════════════════════════════════════════════════
# CAS 4 — RAPPORT PO
# ════════════════════════════════════════════════════════════════════════════
elif "Cas 4" in cas:

    st.markdown("""
    <div class="cas-header">
    <h2 style="margin:0;font-size:20px">📋 Cas 4 — Rapport de migration pour le Product Owner</h2>
    <p style="margin:6px 0 0;opacity:0.8;font-size:14px">Synthèse exécutive · Export CSV daté · Suivi hebdomadaire</p>
    </div>
    """, unsafe_allow_html=True)

    date_rapport = datetime.now().strftime("%d/%m/%Y à %H:%M")

    st.markdown(f"#### Rapport de migration — généré le {date_rapport}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#E24B4A">3</div><div class="metric-label">Anomalies bloquantes P0</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#EF9F27">5</div><div class="metric-label">Écarts P1 à corriger</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-value" style="color:#639922">65.4%</div><div class="metric-label">Completeness moyen</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Tableau de bord de suivi hebdomadaire")

    suivi = pd.DataFrame({
        "Semaine": ["S1", "S2", "S3", "S4", "S5", "S6"],
        "Completeness moyen": [45.2, 52.1, 58.7, 63.4, 65.4, None],
        "Anomalies ouvertes": [24, 18, 12, 7, 3, None],
        "Anomalies fermées": [0, 6, 12, 17, 21, None],
        "Statut": ["🔴 NON", "🔴 NON", "🟠 NON", "🟠 NON", "🟠 NON", "⏳ En cours"]
    })

    st.dataframe(suivi, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Export du rapport")

    rapport_csv = pd.DataFrame({
        "Reference": ["HIKM31", "FLUKE-177", "TDK-300", "BWA-100", "KIMO-500"],
        "Anomalie": ["Marque modifiée", "Catégorie changée", "Pays origine", "Marque abrégée", "Unité manquante"],
        "Priorite": ["P1", "P1", "P2", "P2", "P0"],
        "Statut": ["À corriger", "À corriger", "À corriger", "À corriger", "BLOQUANT"],
        "Date_detection": [datetime.now().strftime("%Y-%m-%d")] * 5
    })

    csv_export = rapport_csv.to_csv(index=False, sep=";").encode("utf-8")
    nom_fichier = f"rapport_migration_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    st.download_button(
        label="⬇️ Télécharger le rapport CSV",
        data=csv_export,
        file_name=nom_fichier,
        mime="text/csv"
    )

    st.success(f"✅ Rapport généré : {nom_fichier}")

    with st.expander("🐍 Voir le script Python utilisé"):
        st.code("""
import pandas as pd
from datetime import datetime

def rapport_migration(df_ecarts, nom_projet="migration_akeneo"):
    date = datetime.now().strftime("%Y%m%d_%H%M")
    nom = f"rapport_{nom_projet}_{date}.csv"

    df_ecarts["date_rapport"] = datetime.now().strftime("%Y-%m-%d")

    # Trier par priorité
    ordre = {"P0": 0, "P1": 1, "P2": 2}
    df_ecarts["ordre"] = df_ecarts["priorite"].map(ordre)
    df_ecarts = df_ecarts.sort_values("ordre").drop("ordre", axis=1)

    df_ecarts.to_csv(nom, sep=";", index=False)

    print(f"Rapport exporté : {nom}")
    print(f"P0 bloquants : {len(df_ecarts[df_ecarts['priorite']=='P0'])}")
    print(f"P1 majeurs : {len(df_ecarts[df_ecarts['priorite']=='P1'])}")
    print(f"P2 mineurs : {len(df_ecarts[df_ecarts['priorite']=='P2'])}")

rapport_migration(df_ecarts)
        """, language="python")

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.divider()
st.caption("Application de démonstration — Mission Business Data Analyst · Akeneo PIM Migration · Données Testoon réelles (19 393 produits)")
