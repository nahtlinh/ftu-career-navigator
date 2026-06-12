"""
FTU Career Navigator - MVP
Ứng dụng hỗ trợ sinh viên kinh tế FTU khám phá nghề nghiệp,
đánh giá mức độ phù hợp với thị trường việc làm, và tìm khóa học bổ sung kỹ năng.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FTU Career Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ---- Font ---- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ---- Background ---- */
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.04);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] * { color: #e0e0f0 !important; }

    /* ---- Cards ---- */
    .card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
    }
    .card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.4); }

    /* ---- Metric pill ---- */
    .metric-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3));
        border: 1px solid rgba(102,126,234,0.4);
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .metric-label { color: #a0a8c0; font-size: 13px; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 8px; }
    .metric-value { color: #fff; font-size: 36px; font-weight: 800; }
    .metric-sub { color: #7dd3fc; font-size: 13px; margin-top: 6px; }

    /* ---- Fit Score ring ---- */
    .score-wrap { text-align: center; padding: 20px 0; }
    .score-ring {
        display: inline-block;
        width: 160px; height: 160px;
        border-radius: 50%;
        background: conic-gradient(var(--c) var(--p), rgba(255,255,255,0.08) 0);
        position: relative;
        margin-bottom: 12px;
    }
    .score-ring::after {
        content: attr(data-score);
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%,-50%);
        font-size: 32px; font-weight: 800; color: #fff;
        background: #1a1a35; width: 120px; height: 120px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
    }

    /* ---- Section headers ---- */
    .section-title {
        color: #e0e0f0;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 6px;
        letter-spacing: -0.3px;
    }
    .section-sub { color: #8892b0; font-size: 13px; margin-bottom: 24px; }

    /* ---- Course cards ---- */
    .course-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 20px;
        height: 100%;
        transition: all 0.25s ease;
    }
    .course-card:hover {
        background: rgba(102,126,234,0.15);
        border-color: rgba(102,126,234,0.5);
        transform: translateY(-3px);
    }
    .course-platform {
        font-size: 11px; font-weight: 600; letter-spacing: 1px;
        color: #64ffda; text-transform: uppercase; margin-bottom: 8px;
    }
    .course-title { color: #e0e0f0; font-size: 15px; font-weight: 600; margin-bottom: 8px; line-height: 1.4; }
    .course-meta { color: #8892b0; font-size: 12px; margin-bottom: 12px; }
    .course-gap { color: #ff6b9d; font-size: 12px; font-weight: 600; margin-bottom: 12px; }
    .course-btn {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #fff !important;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
        transition: opacity 0.2s;
    }
    .course-btn:hover { opacity: 0.85; }

    /* ---- Sidebar nav pills ---- */
    .nav-pill {
        background: rgba(102,126,234,0.15);
        border-left: 3px solid #667eea;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 8px;
        font-weight: 600;
        color: #c0c8ff;
    }

    /* ---- Streamlit widget overrides ---- */
    .stSelectbox label, .stMultiSelect label { color: #a0a8c0 !important; font-size: 13px !important; }
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
    }

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
    }
    div[data-testid="metric-container"] label { color: #8892b0 !important; }
    div[data-testid="metric-container"] div[data-testid="metric-value"] { color: #fff !important; }

    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ---- Top Navigation High-Contrast Styling ---- */
    div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        display: flex !important;
        justify-content: space-around !important;
        gap: 10px !important;
        margin-bottom: 25px !important;
    }
    
    div[role="radiogroup"] label {
        background-color: transparent !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
    }
    
    div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    div[role="radiogroup"] label p {
        color: #FFFFFF !important; /* Force high-contrast white text */
        font-weight: 600 !important;
        font-size: 14px !important;
        opacity: 0.95 !important;
        margin: 0 !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    div[role="radiogroup"] label[data-checked="true"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    
    div[role="radiogroup"] input[type="radio"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 1. MOCK DATA
# ═══════════════════════════════════════════════════════════════

@st.cache_data
def load_job_market_data() -> pd.DataFrame:
    """Bảng kỹ năng yêu cầu theo từng vị trí công việc (thang điểm 100)."""
    data = [
        # ── Data Analyst ──────────────────────────────────────────────
        ("Data Analyst",        "Phân tích dữ liệu",        85),
        ("Data Analyst",        "Thống kê ứng dụng",        75),
        ("Data Analyst",        "Trực quan hóa dữ liệu",    70),
        ("Data Analyst",        "SQL & Cơ sở dữ liệu",      80),
        ("Data Analyst",        "Kinh tế học vi mô",         50),
        ("Data Analyst",        "Tư duy phản biện",          65),
        ("Data Analyst",        "Trình bày báo cáo",         60),
        ("Data Analyst",        "Tiếng Anh thương mại",      55),

        # ── Marketing Executive ────────────────────────────────────────
        ("Marketing Executive", "Marketing kỹ thuật số",    80),
        ("Marketing Executive", "Hành vi người tiêu dùng",  75),
        ("Marketing Executive", "Phân tích dữ liệu",        55),
        ("Marketing Executive", "Tư duy sáng tạo",          70),
        ("Marketing Executive", "Trình bày báo cáo",        65),
        ("Marketing Executive", "Tiếng Anh thương mại",     70),
        ("Marketing Executive", "Quản lý dự án",            60),
        ("Marketing Executive", "Kinh tế học vi mô",        45),

        # ── Financial Analyst ─────────────────────────────────────────
        ("Financial Analyst",   "Tài chính doanh nghiệp",  90),
        ("Financial Analyst",   "Thống kê ứng dụng",        70),
        ("Financial Analyst",   "Phân tích dữ liệu",        65),
        ("Financial Analyst",   "Kế toán tài chính",        85),
        ("Financial Analyst",   "Kinh tế học vĩ mô",        75),
        ("Financial Analyst",   "Tiếng Anh thương mại",     60),
        ("Financial Analyst",   "Trình bày báo cáo",        70),
        ("Financial Analyst",   "Tư duy phản biện",          65),

        # ── Business Development ──────────────────────────────────────
        ("Business Development","Quản lý dự án",             80),
        ("Business Development","Kinh tế học vi mô",          65),
        ("Business Development","Tiếng Anh thương mại",      85),
        ("Business Development","Tư duy sáng tạo",           75),
        ("Business Development","Trình bày báo cáo",         80),
        ("Business Development","Marketing kỹ thuật số",     55),
        ("Business Development","Phân tích dữ liệu",         50),
        ("Business Development","Hành vi người tiêu dùng",   60),

        # ── Supply Chain Analyst ──────────────────────────────────────
        ("Supply Chain Analyst","Quản lý dự án",              75),
        ("Supply Chain Analyst","Phân tích dữ liệu",          70),
        ("Supply Chain Analyst","Thống kê ứng dụng",          60),
        ("Supply Chain Analyst","SQL & Cơ sở dữ liệu",        55),
        ("Supply Chain Analyst","Kinh tế học vi mô",           65),
        ("Supply Chain Analyst","Tư duy phản biện",            70),
        ("Supply Chain Analyst","Trình bày báo cáo",          65),
        ("Supply Chain Analyst","Tiếng Anh thương mại",       60),
    ]
    return pd.DataFrame(data, columns=["Target_Job", "Skill", "Required_Score"])


@st.cache_data
def load_ftu_course_dict() -> pd.DataFrame:
    """Bảng ánh xạ môn học FTU → kỹ năng (Granted_Score tích lũy, thang 100)."""
    data = [
        ("Kinh tế lượng",                   "Thống kê ứng dụng",        60),
        ("Kinh tế lượng",                   "Phân tích dữ liệu",        40),
        ("Kinh tế vi mô",                   "Kinh tế học vi mô",        70),
        ("Kinh tế vĩ mô",                   "Kinh tế học vĩ mô",        70),
        ("Nguyên lý kế toán",               "Kế toán tài chính",        60),
        ("Tài chính doanh nghiệp",          "Tài chính doanh nghiệp",   75),
        ("Marketing căn bản",               "Marketing kỹ thuật số",    50),
        ("Marketing căn bản",               "Hành vi người tiêu dùng",  55),
        ("Hành vi người tiêu dùng",         "Hành vi người tiêu dùng",  70),
        ("Quản trị học",                    "Quản lý dự án",            55),
        ("Quản trị học",                    "Tư duy phản biện",          50),
        ("Kỹ năng giao tiếp tiếng Anh",    "Tiếng Anh thương mại",     65),
        ("Tiếng Anh thương mại",            "Tiếng Anh thương mại",     75),
        ("Thống kê kinh doanh",             "Thống kê ứng dụng",        65),
        ("Thống kê kinh doanh",             "Phân tích dữ liệu",        35),
        ("Trực quan hóa dữ liệu (Power BI)","Trực quan hóa dữ liệu",   70),
        ("Trực quan hóa dữ liệu (Power BI)","Phân tích dữ liệu",        30),
        ("Cơ sở dữ liệu & SQL",             "SQL & Cơ sở dữ liệu",      75),
        ("Kỹ năng thuyết trình",            "Trình bày báo cáo",        70),
        ("Kỹ năng thuyết trình",            "Tư duy sáng tạo",          40),
        ("Marketing kỹ thuật số",           "Marketing kỹ thuật số",    75),
        ("Marketing kỹ thuật số",           "Tư duy sáng tạo",          50),
    ]
    return pd.DataFrame(data, columns=["Course_Name", "Skill_Acquired", "Granted_Score"])


# Mock salary data per job
SALARY_DATA = {
    "Data Analyst":         {"salary": "15–25 triệu VNĐ", "growth": "+22% YoY", "openings": 1_340},
    "Marketing Executive":  {"salary": "12–20 triệu VNĐ", "growth": "+15% YoY", "openings": 2_180},
    "Financial Analyst":    {"salary": "18–30 triệu VNĐ", "growth": "+18% YoY", "openings": 890},
    "Business Development": {"salary": "14–24 triệu VNĐ", "growth": "+20% YoY", "openings": 1_650},
    "Supply Chain Analyst": {"salary": "13–22 triệu VNĐ", "growth": "+12% YoY", "openings": 760},
}

# Hardcoded course recommendations per skill gap
COURSE_DB = {
    "Phân tích dữ liệu": {
        "platform": "Coursera",
        "title": "Google Data Analytics Professional Certificate",
        "meta": "⏱ 6 tháng · Beginner · Có chứng chỉ",
        "price": "~$49/tháng",
        "url": "https://www.coursera.org/professional-certificates/google-data-analytics?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Thống kê ứng dụng": {
        "platform": "Udemy",
        "title": "Statistics for Data Science and Business Analysis",
        "meta": "⏱ 15 giờ · Beginner–Intermediate",
        "price": "~$14.99",
        "url": "https://www.udemy.com/course/statistics-for-data-science-and-business-analysis/?utm_source=ftu-navigator",
        "color": "#ec5252",
    },
    "SQL & Cơ sở dữ liệu": {
        "platform": "DataCamp",
        "title": "SQL Fundamentals Track",
        "meta": "⏱ 24 giờ · 6 khóa học",
        "price": "Miễn phí tuần đầu",
        "url": "https://www.datacamp.com/tracks/sql-fundamentals?utm_source=ftu-navigator",
        "color": "#03EF62",
    },
    "Trực quan hóa dữ liệu": {
        "platform": "Udemy",
        "title": "Microsoft Power BI Desktop for Business Intelligence",
        "meta": "⏱ 16 giờ · Intermediate",
        "price": "~$14.99",
        "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/?utm_source=ftu-navigator",
        "color": "#F2C811",
    },
    "Marketing kỹ thuật số": {
        "platform": "Google Skillshop",
        "title": "Google Digital Marketing & E-commerce Certificate",
        "meta": "⏱ 6 tháng · Miễn phí",
        "price": "Miễn phí 🎉",
        "url": "https://grow.google/certificates/digital-marketing-ecommerce/?utm_source=ftu-navigator",
        "color": "#34A853",
    },
    "Hành vi người tiêu dùng": {
        "platform": "Coursera",
        "title": "Consumer Neuroscience and Neuromarketing",
        "meta": "⏱ 8 giờ · Beginner",
        "price": "Miễn phí (audit)",
        "url": "https://www.coursera.org/learn/neuromarketing?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Tài chính doanh nghiệp": {
        "platform": "Coursera",
        "title": "Business and Financial Modeling Specialization (Wharton)",
        "meta": "⏱ 5 tháng · Intermediate",
        "price": "~$49/tháng",
        "url": "https://www.coursera.org/specializations/wharton-business-financial-modeling?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Kế toán tài chính": {
        "platform": "edX",
        "title": "Financial Accounting (MITx)",
        "meta": "⏱ 15 tuần · Intermediate",
        "price": "Miễn phí (audit)",
        "url": "https://www.edx.org/learn/accounting/massachusetts-institute-of-technology-financial-accounting?utm_source=ftu-navigator",
        "color": "#02262B",
    },
    "Tiếng Anh thương mại": {
        "platform": "Udemy",
        "title": "Business English: Write Professional Emails in English",
        "meta": "⏱ 2.5 giờ · Beginner",
        "price": "~$13.99",
        "url": "https://www.udemy.com/course/business-english-networking/?utm_source=ftu-navigator",
        "color": "#ec5252",
    },
    "Quản lý dự án": {
        "platform": "Google / Coursera",
        "title": "Google Project Management Certificate",
        "meta": "⏱ 6 tháng · Beginner",
        "price": "~$49/tháng",
        "url": "https://www.coursera.org/professional-certificates/google-project-management?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Tư duy phản biện": {
        "platform": "Coursera",
        "title": "Critical Thinking & Problem-Solving (University of Michigan)",
        "meta": "⏱ 16 giờ · Beginner",
        "price": "Miễn phí (audit)",
        "url": "https://www.coursera.org/learn/critical-thinking-skills?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Trình bày báo cáo": {
        "platform": "Udemy",
        "title": "Presentation Skills: Give a Great Business Presentation",
        "meta": "⏱ 5 giờ · Beginner",
        "price": "~$14.99",
        "url": "https://www.udemy.com/course/presentation-skills-complete-guide/?utm_source=ftu-navigator",
        "color": "#ec5252",
    },
    "Tư duy sáng tạo": {
        "platform": "IDEO U / Coursera",
        "title": "Design Thinking for Innovation",
        "meta": "⏱ 4 tuần · Beginner",
        "price": "Miễn phí (audit)",
        "url": "https://www.coursera.org/learn/uva-darden-design-thinking-innovation?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
    "Kinh tế học vi mô": {
        "platform": "edX",
        "title": "MicroMasters: Business Economics (Babson)",
        "meta": "⏱ 5 tháng · Intermediate",
        "price": "Miễn phí (audit)",
        "url": "https://www.edx.org/masters/micromasters/babsonx-business-economics?utm_source=ftu-navigator",
        "color": "#02262B",
    },
    "Kinh tế học vĩ mô": {
        "platform": "Coursera",
        "title": "Macroeconomics for Business (IESE Business School)",
        "meta": "⏱ 18 giờ · Intermediate",
        "price": "Miễn phí (audit)",
        "url": "https://www.coursera.org/learn/macroeconomics?utm_source=ftu-navigator",
        "color": "#4285F4",
    },
}

FALLBACK_COURSE = {
    "platform": "Coursera",
    "title": "Learning How to Learn",
    "meta": "⏱ 4 tuần · Beginner · Mọi lĩnh vực",
    "price": "Miễn phí (audit)",
    "url": "https://www.coursera.org/learn/learning-how-to-learn?utm_source=ftu-navigator",
    "color": "#667eea",
}

# ═══════════════════════════════════════════════════════════════
# 2. CORE LOGIC FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def calculate_user_skills(
    selected_courses: list[str],
    df_dict: pd.DataFrame,
) -> pd.Series:
    """
    Tính điểm kỹ năng người dùng từ danh sách môn học đã hoàn thành.
    Nếu cùng một kỹ năng được cấp từ nhiều môn, lấy giá trị MAX (không cộng dồn vô hạn).
    Trả về pd.Series với index là Skill, values là điểm (0–100).
    """
    if not selected_courses:
        return pd.Series(dtype=float)
    subset = df_dict[df_dict["Course_Name"].isin(selected_courses)]
    if subset.empty:
        return pd.Series(dtype=float)
    # Group by skill → take the MAX granted score (cap at 100)
    skill_scores = (
        subset.groupby("Skill_Acquired")["Granted_Score"]
        .max()
        .clip(upper=100)
    )
    return skill_scores


def calculate_fit_score(
    user_skills: pd.Series,
    job_skills: pd.DataFrame,
) -> float:
    """
    Tính Fit Score (%) giữa hồ sơ kỹ năng người dùng và yêu cầu công việc.
    Công thức: Tổng điểm đáp ứng / Tổng điểm yêu cầu × 100
    """
    if user_skills.empty or job_skills.empty:
        return 0.0
    total_required = job_skills["Required_Score"].sum()
    if total_required == 0:
        return 0.0
    total_met = 0.0
    for _, row in job_skills.iterrows():
        skill = row["Skill"]
        required = row["Required_Score"]
        user_score = user_skills.get(skill, 0)
        total_met += min(user_score, required)
    return round((total_met / total_required) * 100, 1)


def build_radar_data(
    user_skills: pd.Series,
    job_skills: pd.DataFrame,
) -> tuple[list, list, list]:
    """
    Chuẩn bị dữ liệu cho Radar Chart.
    Trả về (categories, user_values, job_values).
    """
    skills = job_skills["Skill"].tolist()
    job_vals = job_skills.set_index("Skill")["Required_Score"].tolist()
    user_vals = [float(user_skills.get(s, 0)) for s in skills]
    return skills, user_vals, job_vals


def get_top_gaps(
    user_skills: pd.Series,
    job_skills: pd.DataFrame,
    top_n: int = 3,
) -> list[dict]:
    """
    Xác định top N kỹ năng có khoảng cách lớn nhất giữa yêu cầu và thực tế.
    """
    gaps = []
    for _, row in job_skills.iterrows():
        skill = row["Skill"]
        required = row["Required_Score"]
        user_score = float(user_skills.get(skill, 0))
        gap = required - user_score
        if gap > 0:
            gaps.append({"skill": skill, "gap": gap, "required": required, "user": user_score})
    gaps.sort(key=lambda x: x["gap"], reverse=True)
    return gaps[:top_n]


# ═══════════════════════════════════════════════════════════════
# 3. CHART BUILDERS
# ═══════════════════════════════════════════════════════════════

PLOTLY_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#c0c8ff"),
    margin=dict(t=40, b=20, l=20, r=20),
)


def make_bar_chart(df_job: pd.DataFrame, target_job: str, top_n: int = 6) -> go.Figure:
    """Bar chart: Top N kỹ năng yêu cầu của một vị trí."""
    df = (
        df_job[df_job["Target_Job"] == target_job]
        .sort_values("Required_Score", ascending=False)
        .head(top_n)
    )
    colors = [
        f"rgba(102,126,234,{0.5 + 0.5 * (i / max(len(df) - 1, 1))})"
        for i in range(len(df))
    ]
    fig = go.Figure(
        go.Bar(
            x=df["Required_Score"],
            y=df["Skill"],
            orientation="h",
            marker_color=colors,
            marker_line_width=0,
            text=df["Required_Score"].astype(str),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Inter"),
        )
    )
    fig.update_layout(
        **PLOTLY_LAYOUT_BASE,
        xaxis=dict(range=[0, 105], showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#8892b0")),
        yaxis=dict(autorange="reversed", tickfont=dict(color="#c0c8ff", size=12)),
        height=320,
    )
    return fig


def make_radar_chart(
    categories: list,
    user_vals: list,
    job_vals: list,
) -> go.Figure:
    """Radar / Spider chart so sánh kỹ năng người dùng và yêu cầu công việc."""
    cats_closed = categories + [categories[0]]
    user_closed = user_vals + [user_vals[0]]
    job_closed = job_vals + [job_vals[0]]

    fig = go.Figure()
    # Job requirement trace
    fig.add_trace(go.Scatterpolar(
        r=job_closed, theta=cats_closed, fill="toself",
        name="Yêu cầu công việc",
        line=dict(color="#ff6b9d", width=2.5),
        fillcolor="rgba(255,107,157,0.15)",
    ))
    # User skill trace
    fig.add_trace(go.Scatterpolar(
        r=user_closed, theta=cats_closed, fill="toself",
        name="Kỹ năng của bạn",
        line=dict(color="#64ffda", width=2.5),
        fillcolor="rgba(100,255,218,0.12)",
    ))
    fig.update_layout(
        **{
            **PLOTLY_LAYOUT_BASE,
            "polar": dict(
                bgcolor="rgba(255,255,255,0.03)",
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color="#8892b0", size=10),
                    tickvals=[25, 50, 75, 100],
                ),
                angularaxis=dict(
                    tickfont=dict(color="#c0c8ff", size=11),
                    linecolor="rgba(255,255,255,0.1)",
                    gridcolor="rgba(255,255,255,0.07)",
                ),
            ),
            "legend": dict(
                orientation="h", x=0.5, xanchor="center", y=-0.12,
                font=dict(color="#c0c8ff", size=12),
                bgcolor="rgba(0,0,0,0)",
            ),
            "height": 480,
            "margin": dict(t=30, b=60, l=60, r=60),
        }
    )
    return fig


def make_gap_bar(gaps: list[dict]) -> go.Figure:
    """Horizontal bar chart hiển thị skill gap lớn nhất."""
    if not gaps:
        return go.Figure()
    skills = [g["skill"] for g in gaps]
    gap_vals = [g["gap"] for g in gaps]
    fig = go.Figure(go.Bar(
        x=gap_vals, y=skills, orientation="h",
        marker=dict(
            color=gap_vals,
            colorscale=[[0, "rgba(255,107,157,0.4)"], [1, "rgba(255,107,157,0.9)"]],
            showscale=False,
        ),
        text=[f"-{v:.0f} điểm" for v in gap_vals],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="white", size=12),
    ))
    fig.update_layout(
        **{
            **PLOTLY_LAYOUT_BASE,
            "xaxis": dict(range=[0, 105], showgrid=False, visible=False),
            "yaxis": dict(tickfont=dict(color="#c0c8ff", size=12)),
            "height": max(200, len(gaps) * 60),
            "margin": dict(t=10, b=10, l=10, r=10),
        }
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# 4. UI COMPONENTS
# ═══════════════════════════════════════════════════════════════

def render_metric_card(label: str, value: str, sub: str = "") -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """


def render_fit_score_html(score: float) -> str:
    color = "#64ffda" if score >= 70 else "#ffd166" if score >= 40 else "#ff6b9d"
    label = "🟢 Rất phù hợp" if score >= 70 else "🟡 Cần bổ sung" if score >= 40 else "🔴 Còn nhiều việc cần làm"
    pct = f"{score:.0f}%"
    deg = score / 100 * 360
    return f"""
    <div style="text-align:center; padding:20px 0;">
        <div style="
            display:inline-flex; align-items:center; justify-content:center;
            width:170px; height:170px; border-radius:50%;
            background: conic-gradient({color} {deg}deg, rgba(255,255,255,0.08) 0deg);
            margin-bottom: 16px;
        ">
            <div style="
                width:126px; height:126px; border-radius:50%;
                background: #1a1a35;
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
            ">
                <span style="font-size:30px; font-weight:800; color:{color};">{pct}</span>
                <span style="font-size:10px; color:#8892b0; margin-top:2px;">Fit Score</span>
            </div>
        </div>
        <div style="color:{color}; font-size:15px; font-weight:600;">{label}</div>
    </div>
    """


def render_course_card(info: dict, gap_skill: str = "", gap_val: float = 0) -> str:
    badge_color = info.get("color", "#667eea")
    gap_html = f'<div class="course-gap">📉 Thiếu {gap_val:.0f} điểm kỹ năng: <b>{gap_skill}</b></div>' if gap_skill else ""
    return f"""
    <div class="course-card">
        <div class="course-platform" style="color:{badge_color};">▶ {info['platform']}</div>
        <div class="course-title">{info['title']}</div>
        <div class="course-meta">{info['meta']}</div>
        {gap_html}
        <div style="display:flex; align-items:center; gap:12px;">
            <a href="{info['url']}" target="_blank" class="course-btn">Xem khóa học →</a>
            <span style="color:#8892b0; font-size:12px;">{info['price']}</span>
        </div>
    </div>
    """


# ═══════════════════════════════════════════════════════════════
# 5. PAGE RENDERERS
# ═══════════════════════════════════════════════════════════════

def page_market_insights(df_job: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">📊 Tổng quan Thị trường Việc làm</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Phân tích nhu cầu kỹ năng & xu hướng tuyển dụng theo vị trí công việc</div>', unsafe_allow_html=True)

    # ── Job selector ──────────────────────────────────────────
    job_options = df_job["Target_Job"].unique().tolist()
    col_sel, _ = st.columns([2, 3])
    with col_sel:
        selected_job_insight = st.selectbox(
            "Chọn vị trí để phân tích",
            options=job_options,
            index=0,
            key="insight_job",
        )

    salary_info = SALARY_DATA.get(selected_job_insight, {})

    # ── Key metrics ──────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(render_metric_card(
            "💰 Lương entry-level",
            salary_info.get("salary", "N/A"),
            "Gross / tháng",
        ), unsafe_allow_html=True)
    with m2:
        st.markdown(render_metric_card(
            "📈 Tăng trưởng ngành",
            salary_info.get("growth", "N/A"),
            "So với năm ngoái",
        ), unsafe_allow_html=True)
    with m3:
        st.markdown(render_metric_card(
            "🏢 Tin tuyển dụng (VN)",
            f"{salary_info.get('openings', 0):,}",
            "Cập nhật Q2/2025",
        ), unsafe_allow_html=True)
    with m4:
        n_skills = len(df_job[df_job["Target_Job"] == selected_job_insight])
        st.markdown(render_metric_card(
            "🔑 Kỹ năng cốt lõi",
            str(n_skills),
            "Theo khảo sát nhà tuyển dụng",
        ), unsafe_allow_html=True)

    st.markdown("---")

    # ── Bar chart + table ─────────────────────────────────────
    col_bar, col_tbl = st.columns([3, 2])
    with col_bar:
        st.markdown(f"**Top kỹ năng yêu cầu — {selected_job_insight}**")
        fig = make_bar_chart(df_job, selected_job_insight)
        st.plotly_chart(fig, width='stretch')
    with col_tbl:
        st.markdown("**Bảng chi tiết yêu cầu**")
        df_show = (
            df_job[df_job["Target_Job"] == selected_job_insight]
            .sort_values("Required_Score", ascending=False)
            .rename(columns={"Skill": "Kỹ năng", "Required_Score": "Điểm yêu cầu"})
            [["Kỹ năng", "Điểm yêu cầu"]]
            .reset_index(drop=True)
        )
        st.dataframe(
            df_show,
            hide_index=True,
            use_container_width=True,
            height=330,
        )

    st.markdown("---")

    # ── Heatmap: all jobs vs skills ───────────────────────────
    st.markdown("**🗺️ Bản đồ kỹ năng toàn thị trường**")
    pivot = df_job.pivot_table(
        index="Skill", columns="Target_Job", values="Required_Score", fill_value=0
    )
    fig_hm = px.imshow(
        pivot,
        color_continuous_scale="Viridis",
        aspect="auto",
        labels=dict(color="Điểm yêu cầu"),
    )
    fig_hm.update_layout(
        **PLOTLY_LAYOUT_BASE,
        height=420,
        coloraxis_colorbar=dict(tickfont=dict(color="#8892b0")),
        xaxis=dict(tickfont=dict(color="#c0c8ff", size=11), side="bottom"),
        yaxis=dict(tickfont=dict(color="#c0c8ff", size=11)),
    )
    st.plotly_chart(fig_hm, width='stretch')


def page_skill_matching(df_job: pd.DataFrame, df_dict: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">🎯 Máy Đánh giá Mức độ Phù hợp</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Chọn các môn học đã hoàn thành và vị trí mục tiêu để nhận báo cáo kỹ năng cá nhân hóa</div>', unsafe_allow_html=True)

    all_courses = sorted(df_dict["Course_Name"].unique().tolist())
    all_jobs = df_job["Target_Job"].unique().tolist()

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("""
        <div class="card">
            <div style="color:#64ffda; font-size:13px; font-weight:600; letter-spacing:0.5px; margin-bottom:12px;">
                📚 BƯỚC 1 — HỒ SƠ HỌC TẬP
            </div>
        """, unsafe_allow_html=True)

        selected_courses = st.multiselect(
            "Chọn các môn đã học tại FTU ✅",
            options=all_courses,
            placeholder="Tìm và chọn môn học...",
            key="courses",
        )
        selected_job = st.selectbox(
            "Chọn vị trí việc làm mục tiêu 🎯",
            options=all_jobs,
            key="target_job",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        # ── Skill profile ─────────────────────────────────────
        user_skills = calculate_user_skills(selected_courses, df_dict)
        job_df = df_job[df_job["Target_Job"] == selected_job]

        if not user_skills.empty:
            st.markdown("""
            <div class="card">
                <div style="color:#ffd166; font-size:13px; font-weight:600; letter-spacing:0.5px; margin-bottom:12px;">
                    📋 HỒ SƠ KỸ NĂNG CỦA BẠN
                </div>
            """, unsafe_allow_html=True)
            df_profile = user_skills.reset_index()
            df_profile.columns = ["Kỹ năng", "Điểm của bạn"]
            df_profile = df_profile.sort_values("Điểm của bạn", ascending=False)
            st.dataframe(df_profile, hide_index=True, use_container_width=True, height=220)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; padding:40px; color:#8892b0;">
                <div style="font-size:40px; margin-bottom:12px;">🎓</div>
                <div>Hãy chọn các môn học bạn đã hoàn thành để bắt đầu phân tích.</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────────
    fit_score = calculate_fit_score(user_skills, job_df)
    categories, user_vals, job_vals = build_radar_data(user_skills, job_df)

    st.markdown("---")
    col_score, col_radar = st.columns([1, 2], gap="large")

    with col_score:
        st.markdown(f"**Fit Score: {selected_job}**")
        st.markdown(render_fit_score_html(fit_score), unsafe_allow_html=True)

        if fit_score >= 70:
            msg = "💪 Hồ sơ của bạn rất ấn tượng! Hãy ứng tuyển ngay."
            color = "#64ffda"
        elif fit_score >= 40:
            msg = "📈 Tiềm năng tốt! Bổ sung thêm một vài kỹ năng sẽ giúp bạn nổi bật."
            color = "#ffd166"
        else:
            msg = "🚀 Hành trình mới bắt đầu! Xem gợi ý khóa học ở tab bên dưới."
            color = "#ff6b9d"
        st.markdown(f'<p style="color:{color}; font-size:13px; text-align:center; margin-top:8px;">{msg}</p>', unsafe_allow_html=True)

        # mini gap bars
        gaps = get_top_gaps(user_skills, job_df, top_n=5)
        if gaps:
            st.markdown("**Top kỹ năng cần bổ sung**")
            st.plotly_chart(make_gap_bar(gaps), width='stretch')

    with col_radar:
        if categories:
            st.markdown("**Biểu đồ Radar — So sánh Kỹ năng**")
            fig_radar = make_radar_chart(categories, user_vals, job_vals)
            st.plotly_chart(fig_radar, width='stretch')
        else:
            st.info("Vui lòng chọn môn học để hiển thị biểu đồ Radar.")


def page_course_recommender(df_job: pd.DataFrame, df_dict: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">💡 Gợi ý Khóa học Bổ sung</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Dựa trên phân tích khoảng cách kỹ năng, chúng tôi đề xuất các khóa học phù hợp nhất từ các nền tảng hàng đầu</div>', unsafe_allow_html=True)

    # Re-use session-state selections if available
    selected_courses = st.session_state.get("courses", [])
    selected_job = st.session_state.get("target_job", df_job["Target_Job"].unique()[0])

    if not selected_courses:
        st.markdown("""
        <div style="
            text-align:center; padding:60px;
            background:rgba(255,255,255,0.03);
            border:1px dashed rgba(255,255,255,0.15);
            border-radius:16px;
        ">
            <div style="font-size:48px; margin-bottom:16px;">📚</div>
            <div style="color:#8892b0; font-size:15px;">
                Vui lòng chọn môn học và vị trí mục tiêu ở trang
                <b style="color:#64ffda;">Skill Matching</b> trước.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    user_skills = calculate_user_skills(selected_courses, df_dict)
    job_df = df_job[df_job["Target_Job"] == selected_job]
    gaps = get_top_gaps(user_skills, job_df, top_n=3)

    # ── Summary banner ────────────────────────────────────────
    fit_score = calculate_fit_score(user_skills, job_df)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,rgba(102,126,234,0.2),rgba(118,75,162,0.2));
        border:1px solid rgba(102,126,234,0.3);
        border-radius:14px; padding:20px 24px; margin-bottom:28px;
        display:flex; align-items:center; gap:20px;
    ">
        <div style="font-size:40px;">🎯</div>
        <div>
            <div style="color:#c0c8ff; font-size:15px; font-weight:600;">
                Vị trí mục tiêu: <span style="color:#64ffda;">{selected_job}</span>
                &nbsp;·&nbsp; Fit Score hiện tại: <span style="color:#ffd166;">{fit_score:.0f}%</span>
            </div>
            <div style="color:#8892b0; font-size:13px; margin-top:4px;">
                Các khóa học bên dưới sẽ giúp bạn cải thiện điểm số và tăng khả năng được tuyển dụng.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not gaps:
        st.success("🎉 Chúc mừng! Bạn đã đáp ứng đủ toàn bộ yêu cầu của vị trí này.")
        return

    # ── 3 course cards ────────────────────────────────────────
    cols = st.columns(min(len(gaps), 3), gap="medium")
    for i, (col, gap) in enumerate(zip(cols, gaps)):
        skill = gap["skill"]
        course_info = COURSE_DB.get(skill, FALLBACK_COURSE)
        with col:
            st.markdown(render_course_card(course_info, skill, gap["gap"]), unsafe_allow_html=True)

    # ── Additional recommendations ────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📦 Xem thêm khóa học bổ trợ (cập nhật hàng tháng)"):
        extra_skills = [
            row["Skill"] for _, row in job_df.iterrows()
            if row["Skill"] not in [g["skill"] for g in gaps]
        ][:4]
        if extra_skills:
            extra_cols = st.columns(min(len(extra_skills), 4), gap="small")
            for col, skill in zip(extra_cols, extra_skills):
                course_info = COURSE_DB.get(skill, FALLBACK_COURSE)
                with col:
                    st.markdown(render_course_card(course_info), unsafe_allow_html=True)
        else:
            st.write("Không có gợi ý bổ sung cho vị trí này.")

    # ── Learning path ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🗺️ Lộ trình học tập đề xuất")
    path_cols = st.columns(len(gaps), gap="small")
    for i, (col, gap) in enumerate(zip(path_cols, gaps)):
        with col:
            skill = gap["skill"]
            course_info = COURSE_DB.get(skill, FALLBACK_COURSE)
            st.markdown(f"""
            <div style="
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.1);
                border-radius:12px; padding:16px; text-align:center;
            ">
                <div style="
                    background:{'#64ffda' if i==0 else '#ffd166' if i==1 else '#ff6b9d'};
                    color:#0f0c29; width:28px; height:28px;
                    border-radius:50%; display:inline-flex;
                    align-items:center; justify-content:center;
                    font-weight:800; font-size:14px; margin-bottom:10px;
                ">{i+1}</div>
                <div style="color:#c0c8ff; font-size:13px; font-weight:600; margin-bottom:6px;">{skill}</div>
                <div style="color:#8892b0; font-size:11px;">{course_info['platform']}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 6. SIDEBAR & MAIN ENTRY
# ═══════════════════════════════════════════════════════════════

def render_top_navigation() -> str:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 25px; margin-bottom: 25px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 32px;">🎓</span>
            <div>
                <h1 style="margin: 0; font-size: 22px; font-weight: 800; background: linear-gradient(135deg,#667eea,#764ba2,#64ffda); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">FTU Career Navigator</h1>
                <p style="margin: 0; color: #8892b0; font-size: 11px;">v1.0 MVP · Final Project 2025</p>
            </div>
        </div>
        <div style="color: #8892b0; font-size: 11px; text-align: right;">
            Dữ liệu minh họa · Dành cho mục đích học thuật<br>
            © 2025 FTU — TINH304 Final Project
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "📊  Market Insights": "market",
        "🎯  Skill Matching": "matching",
        "💡  Course Recommender": "recommender",
    }
    page_key = st.radio(
        "Điều hướng",
        list(pages.keys()),
        horizontal=True,
        label_visibility="collapsed",
        key="nav",
    )
    selected = pages[page_key]
    return selected


def main() -> None:
    df_job = load_job_market_data()
    df_dict = load_ftu_course_dict()

    selected_page = render_top_navigation()

    if selected_page == "market":
        page_market_insights(df_job)
    elif selected_page == "matching":
        page_skill_matching(df_job, df_dict)
    elif selected_page == "recommender":
        page_course_recommender(df_job, df_dict)


if __name__ == "__main__":
    main()
