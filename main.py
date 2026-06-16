import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# ---------------------------------------------------
# 1. 기본 설정 (wide 모드로 넓게 쓰기)
# ---------------------------------------------------
warnings.filterwarnings('ignore')
plt.rc('font', family='Malgun Gothic')  # Mac 사용자는 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="영화 흥행 트렌드 대시보드", page_icon="🎬", layout="wide")


# ---------------------------------------------------
# 2. 데이터 전처리
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel('역대_박스오피스.xlsx', skiprows=4)
    df.columns = df.columns.str.strip()
    df['관객수'] = df['관객수'].astype(str).str.replace(',', '').astype(float)
    df['관객수_만명'] = df['관객수'] / 10000
    df['개봉일'] = pd.to_datetime(df['개봉일'])
    df['개봉연도'] = df['개봉일'].dt.year
    df['개봉월'] = df['개봉일'].dt.month
    df['국적_분류'] = df['대표국적'].apply(lambda x: '한국' if x == '한국' else '외국')
    return df


df = load_data()

# ---------------------------------------------------
# 3. 웹페이지 제목 구성
# ---------------------------------------------------
st.title("🎬 역대 영화 흥행 트렌드 분석 대시보드")
st.markdown("**작성자:** [윤어진/첨단IT학부]")
st.markdown("---")

# ===================================================
# 윗줄 (Row 1): 섹션 2 그래프 두 개 나란히 배치
# ===================================================
st.header("2. 시기와 계절의 법칙 (타임라인 분석)")
st.write("관람객의 극장 방문 시기는 개인의 여가 시간, 방학, 명절 등 사회적 캘린더와 밀접하게 연관되어 있습니다.")

col1, col2 = st.columns(2)

# 왼쪽 칸 (col1)
with col1:
    st.subheader("2.1. 월별 누적 관객수 추이")
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    monthly_aud = df.groupby('개봉월')['관객수_만명'].sum().reset_index()
    sns.barplot(x='개봉월', y='관객수_만명', data=monthly_aud, palette='Blues_d', ax=ax1)
    ax1.set_title('1. 월별 전체 누적 관객수 추이', fontsize=13, fontweight='bold')
    ax1.set_xlabel('개봉 월')
    ax1.set_ylabel('누적 관객수 (만 명)')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # 💡 브라우저 크기에 맞춰 자동으로 줄어들게 설정 (use_container_width=True)
    st.pyplot(fig1, use_container_width=True)

    st.info("""
    **[그래프 1 해석: 월별 전체 누적 관객수 추이]**
    * **그래프 구조:** X축은 1~12월 개봉 월, Y축은 해당 월 개봉작들의 누적 관객수 합산을 나타내는 바 차트입니다.
    * **데이터 인사이트:** 1년 중 가장 거대한 두 번의 성수기를 뚜렷하게 보여줍니다. 
      * **① 여름 텐트폴 시즌(7~8월):** 방학과 휴가가 겹치며, 각 배급사들이 100억 원 이상의 텐트폴(대작) 영화를 집중적으로 쏟아내어 관객수가 폭발합니다. 
      * **② 연말 특수(12월):** 크리스마스와 연말 모임으로 가족/연인 관객이 몰리는 제2의 성수기입니다. 반면 3-4월과 10-11월은 전통적인 극장가 비수기임이 뚜렷한 골짜기(Valley)로 증명됩니다.
    """)

# 오른쪽 칸 (col2)
with col2:
    st.subheader("2.2. 국적별 개봉 월 선호도 비교")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    pivot_df = df.groupby(['국적_분류', '개봉월']).size().unstack(fill_value=0)
    sns.heatmap(pivot_df, cmap='YlGnBu', annot=True, fmt='d', linewidths=1, linecolor='white', ax=ax2)
    ax2.set_title('2. 국적별 개봉 월 분포 히트맵', fontsize=13, fontweight='bold')
    ax2.set_xlabel('개봉 월')
    ax2.set_ylabel('국적')

    # 💡 브라우저 크기에 맞춰 자동으로 줄어들게 설정
    st.pyplot(fig2, use_container_width=True)

    st.info("""
    **[그래프 2 해석: 국적별 개봉 월 분포 히트맵]**
    * **그래프 구조:** 특정 월에 개봉한 흥행 영화 편수가 많을수록 짙은 푸른색으로 표현되는 교차표 형태의 히트맵입니다.
    * **데이터 인사이트:** 두 국적 간의 뚜렷한 배급 전략 차이가 관찰됩니다. 
      * **① 한국 영화(명절 특수):** 1-2월(설날)과 9-10월(추석) 구간이 가장 짙습니다. 온 가족이 모이는 명절 특성상 전 세대가 즐길 수 있는 코미디/휴먼 드라마를 집중 배치합니다. 
      * **② 외국 영화(방학 블록버스터):** 5~7월 여름 초입 구간이 가장 짙습니다. 할리우드 마블(Marvel) 등 대형 블록버스터들이 북미 방학 시작에 맞춰 '글로벌 동시 개봉' 전략으로 한국 시장 파이를 잠식하고 있음을 시사합니다.
    """)

st.markdown("---")

# ===================================================
# 아랫줄 (Row 2): 그래프 3과 그래프 4 나란히 배치
# ===================================================
col3, col4 = st.columns(2)

# 왼쪽 칸 (col3)
with col3:
    st.subheader("2.3. 역대 연도별 흥행작 배출 추이")
    fig3, ax3 = plt.subplots(figsize=(7, 4.5))
    yearly_count = df.groupby('개봉연도').size().reset_index(name='개봉편수')
    ax3.fill_between(yearly_count['개봉연도'], yearly_count['개봉편수'], color="mediumpurple", alpha=0.3)
    ax3.plot(yearly_count['개봉연도'], yearly_count['개봉편수'], color="indigo", marker='o', linewidth=2.5, markersize=7)
    ax3.set_title('3. 역대 연도별 흥행작 배출 추이', fontsize=13, fontweight='bold')
    ax3.set_xlabel('개봉 연도')
    ax3.set_ylabel('박스오피스 진입 영화 수')
    ax3.grid(True, linestyle=':', alpha=0.6)

    # 💡 브라우저 크기에 맞춰 자동으로 줄어들게 설정
    st.pyplot(fig3, use_container_width=True)

    st.info("""
    **[그래프 3 해석: 역대 연도별 흥행작 배출 추이]**
    * **그래프 구조:** 선 아래 공간을 채워 전체 시장의 '볼륨(규모)' 변화를 극대화한 면적 차트(Area Chart)입니다.
    * **데이터 인사이트:** 한국 영화 산업의 '흥망성쇠'를 시각적으로 대변합니다. 
      * **① 황금기:** 2010년대에 들어서며 면적이 거대하게 부풀어 오르는 구간은 멀티플렉스 상영관 확장과 맞물린 극장가의 완벽한 전성기입니다. 
      * **② 붕괴와 과도기:** 2020년~2022년 구간에서 면적이 바닥으로 푹 꺼지며 타격감을 줍니다. 전 세계를 덮친 코로나19 팬데믹으로 인한 오프라인 극장 생태계의 붕괴를 보여주며, 
      최근 OTT 일상화라는 변수 속 극장가의 깊은 고민을 엿볼 수 있습니다.
    """)

# 오른쪽 칸 (col4)
with col4:
    st.header("3. 배급사 파워 게임")
    st.subheader("3.1. 흥행작 보유 Top 10 배급사 점유율")
    fig4, ax4 = plt.subplots(figsize=(6, 5.5))
    top10_dist = df['배급사'].value_counts().nlargest(10)
    ax4.pie(top10_dist, labels=top10_dist.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette('tab10'), pctdistance=0.85,
            textprops={'fontsize': 9, 'weight': 'bold'})
    centre_circle = plt.Circle((0, 0), 0.65, fc='white')
    fig4.gca().add_artist(centre_circle)
    ax4.set_title('4. 상위 10개 배급사 점유율', fontsize=13, fontweight='bold')

    # 💡 브라우저 크기에 맞춰 자동으로 줄어들게 설정
    st.pyplot(fig4, use_container_width=True)

    st.info("""
    **[그래프 4 해석: 상위 10개 배급사 흥행 점유율]**
    * **그래프 구조:** 상위 10개 배급사가 전체 흥행작 파이를 어떻게 나누어 가졌는지 보여주는 도넛 차트입니다.
    * **데이터 인사이트:** 영화 시장이 소수 거대 자본에 의해 어떻게 과점되어 있는지 보여줍니다. 
      * **① 4대 메이저의 지배력:** CJ, 롯데, 쇼박스, NEW 등 국내 4대 메이저가 도넛의 절반 이상을 차지합니다. 특히 선두 기업들은 자사 멀티플렉스(캡티브 마켓)를 활용해 초기 상영관을 압도적으로 확보하는 구조적 이점을 지닙니다. 
      * **② 거대 외국 자본:** 월트디즈니컴퍼니코리아의 붉은 파이 조각이 4대 메이저 못지않게 두텁게 나타나며, 강력한 마블/애니메이션 팬덤을 등에 업은 거대 자본의 파워를 증명합니다.
    """)