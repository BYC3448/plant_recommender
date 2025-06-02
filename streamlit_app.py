import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="🌱 우리집 맞춤 식물 추천",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# OpenAI 클라이언트 초기화
@st.cache_resource
def init_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAI(api_key=api_key)
    return None

client = init_openai_client()

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #228B22;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .input-section {
        background-color: #F0FFF0;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #32CD32;
    }
    .result-section {
        background-color: #F5FFFA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #20B2AA;
    }
    .stButton > button {
        background-color: #32CD32;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #228B22;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<h1 class="main-header">🌱 우리집 맞춤 식물 추천</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">초보 식집사를 위한 맞춤형 실내 식물 추천 서비스</p>', unsafe_allow_html=True)

# 메인 레이아웃: 좌우 컬럼
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🏠 우리집 환경 정보</h3>', unsafe_allow_html=True)
    
    # 집의 향
    st.markdown("### 🧭 집의 향")
    house_direction = st.selectbox(
        "우리집은 어느 쪽을 향하고 있나요?",
        ["잘 모름", "남향", "동향", "서향", "북향", "남동향", "남서향", "북동향", "북서향"],
        help="창문이 주로 어느 방향을 향하는지 선택해주세요"
    )
    
    # 식물 배치 위치
    st.markdown("### 📍 식물을 둘 위치")
    plant_location = st.selectbox(
        "식물을 어디에 둘 예정인가요?",
        ["잘 모름", "베란다", "방안 창가", "거실", "주방", "화장실", "현관", "계단", "서재/공부방"],
        help="식물을 주로 배치할 공간을 선택해주세요"
    )
    
    # 통풍 정도
    st.markdown("### 💨 통풍 정도")
    ventilation = st.selectbox(
        "선택한 위치의 통풍은 어떤가요?",
        ["잘 모름", "아주 잘됨", "보통", "잘 안됨"],
        help="바람이 잘 통하는지 선택해주세요"
    )
    
    # 빛이 드는 시간
    st.markdown("### ☀️ 햇빛 시간")
    sunlight_hours = st.selectbox(
        "하루 중 햇빛이 몇 시간 정도 들어오나요?",
        ["잘 모름", "하루종일 (8시간 이상)", "오전 또는 오후 (4-8시간)", "잠깐만 (2-4시간)", "거의 안 들어옴 (2시간 미만)"],
        help="직접적인 햇빛이 들어오는 시간을 기준으로 선택해주세요"
    )
    
    # 빛의 강도
    st.markdown("### 🌞 햇빛 강도")
    sunlight_intensity = st.selectbox(
        "들어오는 햇빛의 강도는 어떤가요?",
        ["잘 모름", "직사광선 (매우 밝음)", "중간 강도 (적당히 밝음)", "약한 반사광 (은은함)", "매우 약함 (어두움)"],
        help="가장 밝을 때를 기준으로 선택해주세요"
    )
    
    # 겨울철 최저 온도
    st.markdown("### 🥶 겨울철 최저 온도")
    winter_temp = st.selectbox(
        "겨울철 집안 최저 온도는 어느 정도인가요?",
        ["잘 모름", "20°C 이상 (따뜻함)", "15-20°C (약간 쌀쌀함)", "10-15°C (춥다)", "10°C 미만 (매우 춥다)"],
        help="난방을 최소로 했을 때 기준으로 선택해주세요"
    )
    
    # 여름철 최고 온도
    st.markdown("### 🥵 여름철 최고 온도")
    summer_temp = st.selectbox(
        "여름철 집안 최고 온도는 어느 정도인가요?",
        ["잘 모름", "30°C 이상 (매우 더움)", "25-30°C (더움)", "20-25°C (적당함)", "20°C 미만 (시원함)"],
        help="에어컨을 사용하지 않았을 때 기준으로 선택해주세요"
    )
    
    # 습도
    st.markdown("### 💧 습도")
    humidity = st.selectbox(
        "집안 습도는 어떤 편인가요?",
        ["잘 모름", "매우 습함", "약간 습함", "보통", "건조함", "매우 건조함"],
        help="평소 느끼는 습도감을 기준으로 선택해주세요"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 추천 받기 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_button = st.button("🌱 내 집에 맞는 식물 추천받기", use_container_width=True)

with col2:
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🌿 맞춤 식물 추천 결과</h3>', unsafe_allow_html=True)
    
    if recommend_button:
        if not client:
            st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. 환경변수 OPENAI_API_KEY를 확인해주세요.")
        else:
            # 로딩 메시지
            with st.spinner("🔍 Ellie에게 맞는 완벽한 식물을 찾고 있어요..."):
                try:
                    # 사용자 입력 정보 정리
                    user_conditions = []
                    if house_direction != "잘 모름":
                        user_conditions.append(f"집의 향: {house_direction}")
                    if plant_location != "잘 모름":
                        user_conditions.append(f"식물 위치: {plant_location}")
                    if ventilation != "잘 모름":
                        user_conditions.append(f"통풍: {ventilation}")
                    if sunlight_hours != "잘 모름":
                        user_conditions.append(f"햇빛 시간: {sunlight_hours}")
                    if sunlight_intensity != "잘 모름":
                        user_conditions.append(f"햇빛 강도: {sunlight_intensity}")
                    if winter_temp != "잘 모름":
                        user_conditions.append(f"겨울 온도: {winter_temp}")
                    if summer_temp != "잘 모름":
                        user_conditions.append(f"여름 온도: {summer_temp}")
                    if humidity != "잘 모름":
                        user_conditions.append(f"습도: {humidity}")
                    
                    # OpenAI 프롬프트 작성
                    if user_conditions:
                        conditions_text = "\n".join([f"- {condition}" for condition in user_conditions])
                        prompt = f"""
당신은 식물 전문가입니다. 다음 환경 조건을 바탕으로 초보자가 키우기 쉬운 실내 식물 3개를 추천해주세요.

## 주어진 환경 조건:
{conditions_text}

## 요청사항:
1. 각 식물마다 다음 정보를 포함해주세요:
   - 식물 이름 (한국어 + 학명)
   - 이 식물을 추천하는 이유
   - 주요 특징
   - 물주기 빈도와 방법
   - 초보자를 위한 키우기 팁
   - 주의사항

2. 답변 형식:
   ## 🌱 추천 식물 1: [식물이름]
   **학명:** [학명]
   **추천 이유:** [이유]
   **특징:** [특징]
   **물주기:** [방법]
   **키우기 팁:** [팁]
   **주의사항:** [주의사항]
   
   (위 형식으로 3개 식물 모두 작성)

3. 주어지지 않은 환경 조건은 일반적인 실내 환경으로 가정하고 추천해주세요.
4. 초보자도 쉽게 키울 수 있는 식물로 추천해주세요.
"""
                    else:
                        prompt = """
당신은 식물 전문가입니다. 초보 식집사가 일반적인 실내 환경에서 키우기 쉬운 실내 식물 3개를 추천해주세요.

## 요청사항:
1. 각 식물마다 다음 정보를 포함해주세요:
   - 식물 이름 (한국어 + 학명)
   - 이 식물을 추천하는 이유
   - 주요 특징
   - 물주기 빈도와 방법
   - 초보자를 위한 키우기 팁
   - 주의사항

2. 답변 형식:
   ## 🌱 추천 식물 1: [식물이름]
   **학명:** [학명]
   **추천 이유:** [이유]
   **특징:** [특징]
   **물주기:** [방법]
   **키우기 팁:** [팁]
   **주의사항:** [주의사항]
   
   (위 형식으로 3개 식물 모두 작성)

3. 초보자도 쉽게 키울 수 있는 식물로 추천해주세요.
"""
                    
                    # OpenAI API 호출 (최신 문법)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "당신은 친절하고 전문적인 식물 전문가입니다."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=2000,
                        temperature=0.7
                    )
                    
                    # 결과 표시
                    result = response.choices[0].message.content
                    st.markdown(result)
                    
                    # 위키피디아 링크 섹션
                    st.markdown("---")
                    st.markdown("### 🔍 더 자세한 정보")
                    st.markdown("추천받은 식물에 대해 더 알고 싶다면:")
                    
                    col_wiki1, col_wiki2, col_wiki3 = st.columns(3)
                    with col_wiki1:
                        st.markdown("🌿 [위키피디아에서 실내식물 검색](https://ko.wikipedia.org/wiki/실내식물)")
                    with col_wiki2:
                        st.markdown("📚 [네이버 지식백과 식물도감](https://terms.naver.com/list.nhn?cid=48124)")
                    with col_wiki3:
                        st.markdown("🌱 [식물 키우기 가이드](https://blog.naver.com/PostList.nhn?blogId=garden_story)")
                    
                except Exception as e:
                    st.error(f"⚠️ 오류가 발생했습니다: {str(e)}")
                    st.info("💡 해결 방법:\n1. 인터넷 연결을 확인해주세요\n2. OpenAI API 키가 올바른지 확인해주세요\n3. 잠시 후 다시 시도해주세요")
    
    else:
        st.info("👈 왼쪽에서 우리집 환경을 선택하고 '식물 추천받기' 버튼을 눌러주세요!\n\n잘 모르는 항목은 '잘 모름'을 선택하시면 됩니다. 😊")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 하단 정보
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        🌱 초보 식집사를 위한 맞춤 식물 추천 서비스 | Made with ❤️ for Ellie
    </div>
    """,
    unsafe_allow_html=True
)