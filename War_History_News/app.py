"""
Major War Histories & News – Streamlit Application
===================================================
An interactive dashboard covering major wars in world history,
including statistics, timelines, and the latest war-related news.
"""

import datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Major War Histories & News",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.6rem;
            font-weight: 800;
            color: #c0392b;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .war-card {
            background: #1e1e2e;
            border-left: 5px solid #c0392b;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .news-card {
            background: #1e1e2e;
            border-left: 5px solid #2980b9;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .metric-box {
            background: #2c2c3e;
            border-radius: 8px;
            padding: 0.8rem;
            text-align: center;
        }
        a { color: #3498db; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# War data
# ---------------------------------------------------------------------------
WARS: list[dict] = [
    {
        "name": "Napoleonic Wars",
        "start_year": 1803,
        "end_year": 1815,
        "type": "Continental War",
        "region": "Europe",
        "countries_involved": "France, United Kingdom, Russia, Prussia, Austria, Spain, Portugal",
        "total_casualties": 3_500_000,
        "military_casualties": 2_500_000,
        "civilian_casualties": 1_000_000,
        "cause": "French expansionism under Napoleon Bonaparte; power struggles among European empires.",
        "outcome": "Coalition victory; Napoleon exiled; Congress of Vienna redrew European borders.",
        "description": (
            "A series of conflicts pitting the French Empire and its allies against "
            "the European powers from 1803 to 1815. Napoleon's ambition to dominate "
            "Europe ultimately ended with his defeat at Waterloo and the restoration "
            "of the Bourbon monarchy in France."
        ),
        "lat": 48.5,
        "lon": 11.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Napoleonic_Wars",
    },
    {
        "name": "American Civil War",
        "start_year": 1861,
        "end_year": 1865,
        "type": "Civil War",
        "region": "North America",
        "countries_involved": "United States (Union vs. Confederacy)",
        "total_casualties": 750_000,
        "military_casualties": 620_000,
        "civilian_casualties": 130_000,
        "cause": "Slavery, states' rights, sectional tensions between North and South.",
        "outcome": (
            "Union victory; abolition of slavery; Reconstruction era began; "
            "preserved United States as one nation."
        ),
        "description": (
            "Fought from 1861 to 1865, the American Civil War pitted the northern "
            "Union states against the southern Confederate states. The war ended "
            "slavery and fundamentally changed the character of the United States."
        ),
        "lat": 37.0,
        "lon": -79.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/American_Civil_War",
    },
    {
        "name": "World War I",
        "start_year": 1914,
        "end_year": 1918,
        "type": "World War",
        "region": "Europe / Global",
        "countries_involved": (
            "France, Germany, United Kingdom, Russia, Austria-Hungary, "
            "Ottoman Empire, United States, Italy, and others"
        ),
        "total_casualties": 20_000_000,
        "military_casualties": 10_000_000,
        "civilian_casualties": 10_000_000,
        "cause": (
            "Assassination of Archduke Franz Ferdinand; nationalism, imperialism, "
            "militarism, and the alliance system."
        ),
        "outcome": (
            "Allied victory; Treaty of Versailles; dissolution of German, "
            "Austro-Hungarian, Russian, and Ottoman empires."
        ),
        "description": (
            "Known as the 'Great War', WWI was a global conflict that erupted in "
            "Europe in 1914. It introduced industrial-scale warfare—trench warfare, "
            "chemical weapons, and aerial combat—resulting in unprecedented casualties."
        ),
        "lat": 49.0,
        "lon": 5.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/World_War_I",
    },
    {
        "name": "World War II",
        "start_year": 1939,
        "end_year": 1945,
        "type": "World War",
        "region": "Global",
        "countries_involved": (
            "Allied Powers: USA, UK, USSR, France, China; "
            "Axis Powers: Germany, Japan, Italy, and others"
        ),
        "total_casualties": 85_000_000,
        "military_casualties": 25_000_000,
        "civilian_casualties": 60_000_000,
        "cause": (
            "Rise of fascism, Nazi expansionism, Japanese imperialism, "
            "failure of appeasement policies."
        ),
        "outcome": (
            "Allied victory; Nuremberg Trials; founding of the United Nations; "
            "start of the Cold War; end of European colonial empires."
        ),
        "description": (
            "The deadliest conflict in human history, WWII involved most of the "
            "world's nations. It included the Holocaust, atomic bombings of "
            "Hiroshima and Nagasaki, and reshaped global politics for decades."
        ),
        "lat": 52.0,
        "lon": 15.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/World_War_II",
    },
    {
        "name": "Korean War",
        "start_year": 1950,
        "end_year": 1953,
        "type": "Proxy War",
        "region": "East Asia",
        "countries_involved": (
            "South Korea, United States, UN coalition vs. North Korea, China, USSR"
        ),
        "total_casualties": 5_000_000,
        "military_casualties": 1_200_000,
        "civilian_casualties": 3_800_000,
        "cause": "Ideological conflict between communist North Korea and capitalist South Korea.",
        "outcome": (
            "Armistice (1953); Korean peninsula remains divided along the 38th parallel; "
            "technically still ongoing without a formal peace treaty."
        ),
        "description": (
            "Often called the 'Forgotten War', the Korean War began with North "
            "Korea's invasion of the South in June 1950. UN forces led by the USA "
            "intervened, and China entered on the North Korean side, resulting in "
            "a costly stalemate."
        ),
        "lat": 37.5,
        "lon": 127.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Korean_War",
    },
    {
        "name": "Vietnam War",
        "start_year": 1955,
        "end_year": 1975,
        "type": "Proxy War",
        "region": "Southeast Asia",
        "countries_involved": (
            "North Vietnam, Viet Cong, China, USSR vs. South Vietnam, United States, "
            "South Korea, Australia"
        ),
        "total_casualties": 3_800_000,
        "military_casualties": 1_300_000,
        "civilian_casualties": 2_500_000,
        "cause": "Cold War ideology; Vietnamese independence and reunification movements.",
        "outcome": (
            "North Vietnamese victory; reunification of Vietnam under communist rule; "
            "US withdrawal; fall of Saigon (1975)."
        ),
        "description": (
            "The Vietnam War was a long, costly armed conflict that pitted the "
            "communist government of North Vietnam against South Vietnam and its "
            "principal ally, the United States. It remains a defining event in "
            "modern American and Vietnamese history."
        ),
        "lat": 16.0,
        "lon": 107.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Vietnam_War",
    },
    {
        "name": "Gulf War",
        "start_year": 1990,
        "end_year": 1991,
        "type": "Regional War",
        "region": "Middle East",
        "countries_involved": (
            "Coalition: USA, UK, Saudi Arabia, France, and 31 others vs. Iraq"
        ),
        "total_casualties": 100_000,
        "military_casualties": 50_000,
        "civilian_casualties": 50_000,
        "cause": "Iraq's invasion and annexation of Kuwait (August 1990).",
        "outcome": (
            "Coalition victory; liberation of Kuwait; Iraq agrees to cease-fire; "
            "Saddam Hussein remains in power."
        ),
        "description": (
            "Triggered by Iraq's invasion of Kuwait, the Gulf War saw a US-led "
            "coalition force Iraq to withdraw. Operation Desert Storm's air campaign "
            "and ground offensive lasted only 100 hours, but the conflict's "
            "repercussions shaped Middle Eastern geopolitics for decades."
        ),
        "lat": 29.5,
        "lon": 47.8,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Gulf_War",
    },
    {
        "name": "Afghanistan War",
        "start_year": 2001,
        "end_year": 2021,
        "type": "Asymmetric War",
        "region": "Central Asia",
        "countries_involved": (
            "USA, NATO allies, Afghan government vs. Taliban, Al-Qaeda"
        ),
        "total_casualties": 241_000,
        "military_casualties": 71_000,
        "civilian_casualties": 170_000,
        "cause": "September 11 attacks; US-led invasion to dismantle Al-Qaeda and remove the Taliban.",
        "outcome": (
            "Taliban recapture of Afghanistan (August 2021); US and NATO withdrawal; "
            "collapse of the Afghan government."
        ),
        "description": (
            "The longest war in US history, the Afghanistan War began after the "
            "9/11 attacks. Despite initial success in toppling the Taliban, a "
            "20-year insurgency followed before the Taliban reclaimed power "
            "upon US withdrawal in 2021."
        ),
        "lat": 33.9,
        "lon": 67.7,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/War_in_Afghanistan_(2001%E2%80%932021)",
    },
    {
        "name": "Iraq War",
        "start_year": 2003,
        "end_year": 2011,
        "type": "Asymmetric War",
        "region": "Middle East",
        "countries_involved": "USA, UK, Coalition forces vs. Iraq, later insurgent groups",
        "total_casualties": 600_000,
        "military_casualties": 50_000,
        "civilian_casualties": 550_000,
        "cause": (
            "Alleged Iraqi weapons of mass destruction; "
            "post-9/11 regional security concerns; regime change."
        ),
        "outcome": (
            "Saddam Hussein removed and executed; prolonged insurgency; "
            "rise of ISIS; US combat withdrawal in 2011."
        ),
        "description": (
            "Launched in 2003 by a US-led coalition, the Iraq War rapidly toppled "
            "Saddam Hussein's government but triggered a long and deadly insurgency. "
            "No WMDs were found, making the war highly controversial. It destabilized "
            "Iraq and contributed to the rise of ISIS."
        ),
        "lat": 33.3,
        "lon": 44.4,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Iraq_War",
    },
    {
        "name": "Syrian Civil War",
        "start_year": 2011,
        "end_year": 2024,
        "type": "Civil War",
        "region": "Middle East",
        "countries_involved": (
            "Syrian government (backed by Russia, Iran) vs. rebel groups, ISIS, "
            "Kurdish forces; US/NATO involvement"
        ),
        "total_casualties": 500_000,
        "military_casualties": 150_000,
        "civilian_casualties": 350_000,
        "cause": (
            "Arab Spring protests; crackdown by Assad government; "
            "sectarian and political tensions."
        ),
        "outcome": (
            "Assad government largely retained power with Russian support; "
            "ISIS defeated territorially; massive displacement and refugee crisis; "
            "regime fell to rebel coalition in late 2024."
        ),
        "description": (
            "Erupting from Arab Spring protests in 2011, the Syrian Civil War became "
            "one of the most destructive conflicts of the 21st century. Multiple "
            "factions—including government forces, rebel groups, ISIS, and Kurdish "
            "militias—fought for control, drawing in global powers and creating a "
            "massive humanitarian crisis."
        ),
        "lat": 34.8,
        "lon": 38.9,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Syrian_civil_war",
    },
    {
        "name": "Russia–Ukraine War",
        "start_year": 2022,
        "end_year": None,
        "type": "International War",
        "region": "Eastern Europe",
        "countries_involved": (
            "Russia vs. Ukraine (backed by NATO/Western allies)"
        ),
        "total_casualties": 500_000,
        "military_casualties": 450_000,
        "civilian_casualties": 50_000,
        "cause": (
            "Russia's full-scale invasion of Ukraine; NATO expansion concerns; "
            "contested territories (Donbas, Crimea)."
        ),
        "outcome": "Ongoing conflict as of 2024–2025.",
        "description": (
            "Russia launched a full-scale invasion of Ukraine on 24 February 2022, "
            "escalating the conflict that began with the annexation of Crimea in 2014. "
            "Ukraine, supported by Western weapons and financial aid, mounted fierce "
            "resistance. The war remains ongoing and is the largest armed conflict "
            "in Europe since World War II."
        ),
        "lat": 49.0,
        "lon": 32.0,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/Russo-Ukrainian_War",
    },
    {
        "name": "Israel–Gaza War",
        "start_year": 2023,
        "end_year": None,
        "type": "Regional War",
        "region": "Middle East",
        "countries_involved": "Israel vs. Hamas (Gaza Strip)",
        "total_casualties": 50_000,
        "military_casualties": 5_000,
        "civilian_casualties": 45_000,
        "cause": "Hamas attack on Israel on 7 October 2023; Israeli retaliatory military campaign.",
        "outcome": "Ongoing conflict; ceasefire negotiations ongoing as of 2025.",
        "description": (
            "On 7 October 2023, Hamas launched a large-scale terrorist attack on "
            "Israel, killing approximately 1,200 people and taking hundreds hostage. "
            "Israel responded with an extensive military campaign in the Gaza Strip, "
            "resulting in significant civilian casualties and a severe humanitarian "
            "crisis. The conflict drew intense international attention and debate."
        ),
        "lat": 31.5,
        "lon": 34.5,
        "image_url": "",
        "wiki": "https://en.wikipedia.org/wiki/2023_Israel%E2%80%93Hamas_war",
    },
]

# ---------------------------------------------------------------------------
# Static curated news articles (fallback / augmentation)
# ---------------------------------------------------------------------------
STATIC_NEWS: list[dict] = [
    {
        "title": "Ukraine War: Key Developments – March 2025",
        "source": "Reuters",
        "date": "2025-03-10",
        "summary": (
            "Frontline clashes continue in eastern Ukraine as both sides dig in. "
            "Peace talks remain stalled despite pressure from European mediators. "
            "Ukraine's drone campaign against Russian logistics depots has intensified."
        ),
        "url": "https://www.reuters.com/world/europe/",
        "tag": "Russia–Ukraine War",
    },
    {
        "title": "Gaza Ceasefire Talks: Latest Round of Negotiations",
        "source": "BBC News",
        "date": "2025-03-08",
        "summary": (
            "Mediators from Qatar, Egypt, and the United States are pushing for a "
            "renewed ceasefire deal between Israel and Hamas. Humanitarian aid access "
            "remains a central sticking point in the negotiations."
        ),
        "url": "https://www.bbc.com/news/world/middle_east",
        "tag": "Israel–Gaza War",
    },
    {
        "title": "Sudan's Civil War: UN Warns of Catastrophic Humanitarian Crisis",
        "source": "Al Jazeera",
        "date": "2025-03-05",
        "summary": (
            "The United Nations has warned that Sudan's ongoing civil war between "
            "the SAF and RSF has created one of the world's worst humanitarian crises, "
            "with over 8 million people displaced and millions facing famine."
        ),
        "url": "https://www.aljazeera.com/news/",
        "tag": "Sudan Conflict",
    },
    {
        "title": "NATO Increases Defence Spending Amid Global Tensions",
        "source": "The Guardian",
        "date": "2025-03-03",
        "summary": (
            "NATO members have pledged to increase defence spending to 2.5% of GDP "
            "as global security tensions remain elevated, particularly in Eastern "
            "Europe and the Indo-Pacific region."
        ),
        "url": "https://www.theguardian.com/world/",
        "tag": "Global Security",
    },
    {
        "title": "Myanmar Civil War: Resistance Forces Gain Ground",
        "source": "Associated Press",
        "date": "2025-02-28",
        "summary": (
            "Anti-junta forces in Myanmar have captured several key towns in Shan "
            "State, marking the most significant territorial gains since the 2021 "
            "military coup. The military junta faces mounting pressure on multiple fronts."
        ),
        "url": "https://apnews.com/",
        "tag": "Myanmar Conflict",
    },
    {
        "title": "Ethiopia's Tigray Region: Fragile Peace Holds After Two Years",
        "source": "CNN",
        "date": "2025-02-25",
        "summary": (
            "A peace agreement signed in November 2022 continues to hold in Ethiopia's "
            "Tigray region, though humanitarian challenges persist. Rebuilding efforts "
            "are underway, but deep political tensions remain unresolved."
        ),
        "url": "https://edition.cnn.com/world/africa/",
        "tag": "Tigray Conflict",
    },
    {
        "title": "Lessons from the Gulf War: 34 Years Later",
        "source": "Foreign Affairs",
        "date": "2025-02-20",
        "summary": (
            "Analysts reflect on the 1991 Gulf War's lasting impact on US military "
            "doctrine, coalition warfare, and Middle Eastern geopolitics. The conflict "
            "set precedents for future interventions and changed how wars are televised."
        ),
        "url": "https://www.foreignaffairs.com/",
        "tag": "Gulf War",
    },
    {
        "title": "World War II Artifacts Discovered in Polish Forest",
        "source": "History.com",
        "date": "2025-02-14",
        "summary": (
            "Archaeologists in Poland have unearthed a cache of WWII-era military "
            "equipment, including weapons and personal items, in a forest near the "
            "former Eastern Front. The discovery offers new insights into the war."
        ),
        "url": "https://www.history.com/",
        "tag": "World War II",
    },
]

# ---------------------------------------------------------------------------
# Helper – build DataFrame
# ---------------------------------------------------------------------------
@st.cache_data
def build_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(WARS)
    current_year = datetime.datetime.now().year
    df["end_year_display"] = df["end_year"].apply(
        lambda y: current_year if (y is None or (isinstance(y, float) and pd.isna(y))) else int(y)
    )
    df["duration_years"] = df["end_year_display"] - df["start_year"]
    df["end_label"] = df["end_year"].apply(
        lambda y: "Ongoing" if (y is None or (isinstance(y, float) and pd.isna(y))) else str(int(y))
    )
    df["casualties_millions"] = df["total_casualties"] / 1_000_000
    return df


# ---------------------------------------------------------------------------
# Helper – fetch live news via NewsAPI (optional)
# ---------------------------------------------------------------------------
def fetch_live_news(api_key: str, query: str = "war conflict") -> list[dict]:
    """Attempt to fetch news from NewsAPI; return empty list on failure."""
    try:
        url = (
            f"https://newsapi.org/v2/everything?q={query}"
            f"&language=en&sortBy=publishedAt&pageSize=8&apiKey={api_key}"
        )
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            articles = resp.json().get("articles", [])
            return [
                {
                    "title": a.get("title", ""),
                    "source": a.get("source", {}).get("name", "Unknown"),
                    "date": (a.get("publishedAt", "") or "")[:10],
                    "summary": a.get("description") or a.get("content") or "",
                    "url": a.get("url", "#"),
                    "tag": "Live News",
                }
                for a in articles
                if a.get("title")
            ]
    except Exception:
        pass
    return []


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar(df: pd.DataFrame):
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/"
        "Flag_of_the_United_Nations.svg/320px-Flag_of_the_United_Nations.svg.png",
        width=120,
    )
    st.sidebar.markdown("## ⚔️ War History & News")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Overview", "📚 War Encyclopedia", "📊 Statistics", "🗺️ World Map", "📰 News"],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filters")

    regions = ["All"] + sorted(df["region"].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)

    war_types = ["All"] + sorted(df["type"].unique().tolist())
    selected_type = st.sidebar.selectbox("War Type", war_types)

    year_min = int(df["start_year"].min())
    year_max = int(df["end_year_display"].max())
    year_range = st.sidebar.slider(
        "Time Period", year_min, year_max, (year_min, year_max), step=1
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 Live News (Optional)")
    news_api_key = st.sidebar.text_input(
        "NewsAPI Key", type="password", placeholder="Enter your NewsAPI key"
    )
    news_query = st.sidebar.text_input("News Search Query", value="war conflict")

    return page, selected_region, selected_type, year_range, news_api_key, news_query


# ---------------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------------
def page_overview(df: pd.DataFrame):
    st.markdown('<p class="main-header">⚔️ Major War Histories & News</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">An interactive dashboard exploring the world\'s '
        "most significant armed conflicts and the latest war-related news.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Wars Covered", len(df))
    with col2:
        ongoing = df[df["end_year"].isna()].shape[0]
        st.metric("🔴 Ongoing Conflicts", ongoing)
    with col3:
        total_cas = df["total_casualties"].sum()
        st.metric("💀 Total Casualties (est.)", f"{total_cas / 1_000_000:.1f}M")
    with col4:
        span = int(df["end_year_display"].max()) - int(df["start_year"].min())
        st.metric("📅 Years Covered", span)

    st.markdown("---")
    st.markdown("### 🕰️ War Timeline")

    timeline_data = []
    colors = {
        "World War": "#e74c3c",
        "Civil War": "#e67e22",
        "Proxy War": "#9b59b6",
        "Regional War": "#3498db",
        "Asymmetric War": "#1abc9c",
        "Continental War": "#f1c40f",
        "International War": "#e74c3c",
    }
    for _, row in df.iterrows():
        timeline_data.append(
            dict(
                Task=row["name"],
                Start=f"{int(row['start_year'])}-01-01",
                Finish=f"{int(row['end_year_display'])}-12-31",
                Type=row["type"],
            )
        )

    fig = px.timeline(
        pd.DataFrame(timeline_data),
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Type",
        color_discrete_map=colors,
        title="Timeline of Major Wars",
        labels={"Task": "War", "Type": "Type"},
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=480,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        title_font_size=16,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 💀 Casualties at a Glance")
    bar_df = df.sort_values("total_casualties", ascending=False)
    fig2 = px.bar(
        bar_df,
        x="name",
        y="total_casualties",
        color="type",
        labels={"name": "War", "total_casualties": "Total Casualties", "type": "Type"},
        title="Total Casualties by War",
        color_discrete_map=colors,
    )
    fig2.update_layout(
        xaxis_tickangle=-35,
        height=420,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        title_font_size=16,
    )
    st.plotly_chart(fig2, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Encyclopedia
# ---------------------------------------------------------------------------
def page_encyclopedia(df: pd.DataFrame):
    st.markdown("## 📚 War Encyclopedia")

    search = st.text_input("🔍 Search wars by name or keyword", "")
    if search:
        mask = (
            df["name"].str.contains(search, case=False)
            | df["cause"].str.contains(search, case=False)
            | df["description"].str.contains(search, case=False)
            | df["region"].str.contains(search, case=False)
        )
        display_df = df[mask]
    else:
        display_df = df

    if display_df.empty:
        st.info("No wars found matching your search.")
        return

    for _, row in display_df.iterrows():
        end_label = row["end_label"]
        duration = row["duration_years"]
        with st.expander(
            f"⚔️ {row['name']} ({row['start_year']} – {end_label})", expanded=False
        ):
            col1, col2, col3 = st.columns(3)
            col1.metric("Type", row["type"])
            col2.metric("Region", row["region"])
            col3.metric("Duration", f"{duration} yr{'s' if duration != 1 else ''}")

            col4, col5, col6 = st.columns(3)
            col4.metric("Total Casualties", f"{row['total_casualties']:,}")
            col5.metric("Military", f"{row['military_casualties']:,}")
            col6.metric("Civilian", f"{row['civilian_casualties']:,}")

            st.markdown(f"**Countries Involved:** {row['countries_involved']}")
            st.markdown(f"**Cause:** {row['cause']}")
            st.markdown(f"**Outcome:** {row['outcome']}")
            st.markdown(f"**Description:** {row['description']}")
            st.markdown(f"[📖 Read more on Wikipedia]({row['wiki']})")


# ---------------------------------------------------------------------------
# Page: Statistics
# ---------------------------------------------------------------------------
def page_statistics(df: pd.DataFrame):
    st.markdown("## 📊 Statistics & Analysis")

    # -- Casualties breakdown pie chart
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Casualties by War Type")
        type_cas = (
            df.groupby("type")["total_casualties"].sum().reset_index()
        )
        type_cas.columns = ["Type", "Total Casualties"]
        fig_pie = px.pie(
            type_cas,
            names="Type",
            values="Total Casualties",
            title="Total Casualties by War Type",
            hole=0.4,
        )
        fig_pie.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### Wars by Region")
        region_count = df["region"].value_counts().reset_index()
        region_count.columns = ["Region", "Count"]
        fig_bar = px.bar(
            region_count,
            x="Region",
            y="Count",
            title="Number of Wars per Region",
            color="Count",
            color_continuous_scale="Reds",
        )
        fig_bar.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # -- Civilian vs Military scatter
    st.markdown("### Civilian vs Military Casualties")
    fig_scatter = px.scatter(
        df,
        x="military_casualties",
        y="civilian_casualties",
        size="total_casualties",
        color="type",
        hover_name="name",
        labels={
            "military_casualties": "Military Casualties",
            "civilian_casualties": "Civilian Casualties",
        },
        title="Military vs Civilian Casualties (bubble size = total)",
    )
    fig_scatter.update_layout(
        height=420,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # -- Duration bar
    st.markdown("### War Duration (Years)")
    dur_df = df.sort_values("duration_years", ascending=False)
    fig_dur = px.bar(
        dur_df,
        x="name",
        y="duration_years",
        color="type",
        labels={"name": "War", "duration_years": "Duration (Years)"},
        title="Duration of Each War",
    )
    fig_dur.update_layout(
        xaxis_tickangle=-35,
        height=400,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
    )
    st.plotly_chart(fig_dur, use_container_width=True)

    # -- Raw data table
    st.markdown("### 📋 Raw Data Table")
    display_cols = [
        "name", "start_year", "end_label", "type", "region",
        "total_casualties", "military_casualties", "civilian_casualties",
        "duration_years",
    ]
    st.dataframe(
        df[display_cols].rename(columns={
            "name": "War",
            "start_year": "Start",
            "end_label": "End",
            "type": "Type",
            "region": "Region",
            "total_casualties": "Total Casualties",
            "military_casualties": "Military Casualties",
            "civilian_casualties": "Civilian Casualties",
            "duration_years": "Duration (yrs)",
        }),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------------------------
# Page: World Map
# ---------------------------------------------------------------------------
def page_world_map(df: pd.DataFrame):
    st.markdown("## 🗺️ Global War Map")
    st.markdown(
        "Each bubble represents a major conflict. "
        "Bubble **size** reflects total casualties; **colour** reflects war type."
    )

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size="total_casualties",
        color="type",
        hover_name="name",
        hover_data={
            "start_year": True,
            "end_label": True,
            "total_casualties": ":,",
            "lat": False,
            "lon": False,
        },
        projection="natural earth",
        title="Major Wars – World Map",
        size_max=50,
    )
    fig.update_layout(
        height=550,
        paper_bgcolor="#0e1117",
        font_color="white",
        geo=dict(
            bgcolor="#0e1117",
            landcolor="#2c2c3e",
            oceancolor="#1a1a2e",
            showocean=True,
            showcoastlines=True,
            coastlinecolor="#444",
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: News
# ---------------------------------------------------------------------------
def page_news(news_api_key: str, news_query: str):
    st.markdown("## 📰 War News")

    articles: list[dict] = []

    if news_api_key:
        with st.spinner("Fetching live news…"):
            articles = fetch_live_news(news_api_key, news_query)
        if articles:
            st.success(f"✅ Loaded {len(articles)} live articles from NewsAPI.")
        else:
            st.warning(
                "Could not fetch live news. Showing curated articles instead. "
                "Check your API key or network connection."
            )

    if not articles:
        articles = STATIC_NEWS

    filter_tag = st.selectbox(
        "Filter by topic",
        ["All"] + sorted({a["tag"] for a in articles}),
    )

    for article in articles:
        if filter_tag != "All" and article["tag"] != filter_tag:
            continue
        with st.container():
            st.markdown(
                f"""
                <div class="news-card">
                    <strong style="font-size:1.05rem;">{article['title']}</strong><br>
                    <small>📰 {article['source']} &nbsp;|&nbsp; 📅 {article['date']}
                    &nbsp;|&nbsp; 🏷️ {article['tag']}</small>
                    <p style="margin-top:0.5rem;">{article['summary']}</p>
                    <a href="{article['url']}" target="_blank">Read more →</a>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    df = build_dataframe()

    page, selected_region, selected_type, year_range, news_api_key, news_query = (
        render_sidebar(df)
    )

    # Apply sidebar filters (except Overview which shows all data intentionally)
    filtered_df = df.copy()
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["type"] == selected_type]
    filtered_df = filtered_df[
        (filtered_df["start_year"] >= year_range[0])
        & (filtered_df["end_year_display"] <= year_range[1])
    ]

    if page == "🏠 Overview":
        page_overview(df)  # always show full data on overview
    elif page == "📚 War Encyclopedia":
        page_encyclopedia(filtered_df)
    elif page == "📊 Statistics":
        page_statistics(filtered_df)
    elif page == "🗺️ World Map":
        page_world_map(filtered_df)
    elif page == "📰 News":
        page_news(news_api_key, news_query)

    # Footer
    st.markdown("---")
    st.markdown(
        "<small>Data sourced from open historical records and Wikipedia. "
        "Casualty figures are estimates from academic and governmental sources. "
        "This dashboard is for educational purposes only.</small>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
