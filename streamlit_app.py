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
    st.markdown("우리집이 향하는 방향을 모두 선택해주세요:")
    house_direction = {}
    house_direction["잘 모름"] = st.checkbox("잘 모름", help="집의 향을 정확히 모르는 경우")
    house_direction["남향"] = st.checkbox("남향", help="남쪽을 향한 창문이 있는 경우")
    house_direction["동향"] = st.checkbox("동향", help="동쪽을 향한 창문이 있는 경우")
    house_direction["서향"] = st.checkbox("서향", help="서쪽을 향한 창문이 있는 경우")
    house_direction["북향"] = st.checkbox("북향", help="북쪽을 향한 창문이 있는 경우")
    house_direction["남동향"] = st.checkbox("남동향", help="남동쪽을 향한 창문이 있는 경우")
    house_direction["남서향"] = st.checkbox("남서향", help="남서쪽을 향한 창문이 있는 경우")
    house_direction["북동향"] = st.checkbox("북동향", help="북동쪽을 향한 창문이 있는 경우")
    house_direction["북서향"] = st.checkbox("북서향", help="북서쪽을 향한 창문이 있는 경우")
    
    # 식물 배치 위치
    st.markdown("### 📍 식물을 둘 위치")
    st.markdown("식물을 배치할 수 있는 모든 장소를 선택해주세요:")
    plant_location = {}
    plant_location["잘 모름"] = st.checkbox("잘 모름 ", help="어디에 둘지 정하지 못한 경우")
    plant_location["베란다"] = st.checkbox("베란다", help="햇빛이 잘 들고 통풍이 좋은 베란다")
    plant_location["방안 창가"] = st.checkbox("방안 창가", help="침실이나 방의 창문 근처")
    plant_location["거실"] = st.checkbox("거실", help="가족이 주로 생활하는 거실 공간")
    plant_location["주방"] = st.checkbox("주방", help="요리하는 주방 공간")
    plant_location["화장실"] = st.checkbox("화장실", help="습도가 높은 화장실")
    plant_location["현관"] = st.checkbox("현관", help="집 입구 현관 공간")
    plant_location["계단"] = st.checkbox("계단", help="계단이나 복도 공간")
    plant_location["서재/공부방"] = st.checkbox("서재/공부방", help="책을 읽거나 공부하는 공간")
    
    # 통풍 정도
    st.markdown("### 💨 통풍 정도")
    st.markdown("선택한 위치의 통풍 상태를 모두 선택해주세요:")
    ventilation = {}
    ventilation["잘 모름"] = st.checkbox("잘 모름  ", help="통풍 정도를 잘 모르는 경우")
    ventilation["아주 잘됨"] = st.checkbox("아주 잘됨", help="창문을 열면 바람이 시원하게 통하는 경우")
    ventilation["보통"] = st.checkbox("보통", help="적당히 바람이 통하는 경우")
    ventilation["잘 안됨"] = st.checkbox("잘 안됨", help="바람이 잘 통하지 않는 밀폐된 공간")
    
    # 빛이 드는 시간
    st.markdown("### ☀️ 햇빛 시간")
    st.markdown("하루 중 햇빛이 들어오는 시간대를 모두 선택해주세요:")
    sunlight_hours = {}
    sunlight_hours["잘 모름"] = st.checkbox("잘 모름   ", help="햇빛 시간을 정확히 모르는 경우")
    sunlight_hours["하루종일 (8시간 이상)"] = st.checkbox("하루종일 (8시간 이상)", help="아침부터 저녁까지 계속 햇빛이 드는 경우")
    sunlight_hours["오전 또는 오후 (4-8시간)"] = st.checkbox("오전 또는 오후 (4-8시간)", help="반나절 정도 햇빛이 드는 경우")
    sunlight_hours["잠깐만 (2-4시간)"] = st.checkbox("잠깐만 (2-4시간)", help="특정 시간대에만 햇빛이 드는 경우")
    sunlight_hours["거의 안 들어옴 (2시간 미만)"] = st.checkbox("거의 안 들어옴 (2시간 미만)", help="햇빛이 거의 들어오지 않는 경우")
    
    # 빛의 강도
    st.markdown("### 🌞 햇빛 강도")
    st.markdown("들어오는 햇빛의 강도를 모두 선택해주세요:")
    sunlight_intensity = {}
    sunlight_intensity["잘 모름"] = st.checkbox("잘 모름    ", help="햇빛 강도를 잘 모르는 경우")
    sunlight_intensity["직사광선 (매우 밝음)"] = st.checkbox("직사광선 (매우 밝음)", help="태양빛이 직접 들어와 매우 밝은 경우")
    sunlight_intensity["중간 강도 (적당히 밝음)"] = st.checkbox("중간 강도 (적당히 밝음)", help="적당히 밝은 간접광이 드는 경우")
    sunlight_intensity["약한 반사광 (은은함)"] = st.checkbox("약한 반사광 (은은함)", help="은은한 빛이 들어오는 경우")
    sunlight_intensity["매우 약함 (어두움)"] = st.checkbox("매우 약함 (어두움)", help="빛이 거의 들어오지 않아 어두운 경우")
    
    # 겨울철 최저 온도
    st.markdown("### 🥶 겨울철 최저 온도")
    st.markdown("겨울철 집안 온도 범위를 모두 선택해주세요:")
    winter_temp = {}
    winter_temp["잘 모름"] = st.checkbox("잘 모름     ", help="겨울철 온도를 정확히 모르는 경우")
    winter_temp["20°C 이상 (따뜻함)"] = st.checkbox("20°C 이상 (따뜻함)", help="겨울에도 따뜻하게 난방이 되는 경우")
    winter_temp["15-20°C (약간 쌀쌀함)"] = st.checkbox("15-20°C (약간 쌀쌀함)", help="약간 쌀쌀하지만 견딜만한 온도")
    winter_temp["10-15°C (춥다)"] = st.checkbox("10-15°C (춥다)", help="꽤 추운 온도 범위")
    winter_temp["10°C 미만 (매우 춥다)"] = st.checkbox("10°C 미만 (매우 춥다)", help="매우 추운 환경")
    
    # 여름철 최고 온도
    st.markdown("### 🥵 여름철 최고 온도")
    st.markdown("여름철 집안 온도 범위를 모두 선택해주세요:")
    summer_temp = {}
    summer_temp["잘 모름"] = st.checkbox("잘 모름      ", help="여름철 온도를 정확히 모르는 경우")
    summer_temp["30°C 이상 (매우 더움)"] = st.checkbox("30°C 이상 (매우 더움)", help="에어컨 없이는 견디기 힘든 더위")
    summer_temp["25-30°C (더움)"] = st.checkbox("25-30°C (더움)", help="더우지만 견딜만한 온도")
    summer_temp["20-25°C (적당함)"] = st.checkbox("20-25°C (적당함)", help="쾌적한 온도 범위")
    summer_temp["20°C 미만 (시원함)"] = st.checkbox("20°C 미만 (시원함)", help="시원한 환경")
    
    # 습도
    st.markdown("### 💧 습도")
    st.markdown("집안 습도 상태를 모두 선택해주세요:")
    humidity = {}
    humidity["잘 모름"] = st.checkbox("잘 모름       ", help="습도 상태를 잘 모르는 경우")
    humidity["매우 습함"] = st.checkbox("매우 습함", help="습도가 매우 높아 끈적한 느낌")
    humidity["약간 습함"] = st.checkbox("약간 습함", help="습도가 약간 높은 편")
    humidity["보통"] = st.checkbox("보통 ", help="습도가 적당한 상태")
    humidity["건조함"] = st.checkbox("건조함", help="습도가 낮아 건조한 느낌")
    humidity["매우 건조함"] = st.checkbox("매우 건조함", help="습도가 매우 낮아 매우 건조함")
    
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
                    # 사용자 입력 정보 정리 (체크박스 방식)
                    user_conditions = []
                    
                    # 각 카테고리별로 선택된 항목들 수집
                    selected_directions = [k for k, v in house_direction.items() if v and k != "잘 모름"]
                    if selected_directions:
                        user_conditions.append(f"집의 향: {', '.join(selected_directions)}")
                    
                    selected_locations = [k for k, v in plant_location.items() if v and k != "잘 모름"]
                    if selected_locations:
                        user_conditions.append(f"식물 위치: {', '.join(selected_locations)}")
                    
                    selected_ventilation = [k for k, v in ventilation.items() if v and k != "잘 모름"]
                    if selected_ventilation:
                        user_conditions.append(f"통풍: {', '.join(selected_ventilation)}")
                    
                    selected_sunlight_hours = [k for k, v in sunlight_hours.items() if v and k != "잘 모름"]
                    if selected_sunlight_hours:
                        user_conditions.append(f"햇빛 시간: {', '.join(selected_sunlight_hours)}")
                    
                    selected_sunlight_intensity = [k for k, v in sunlight_intensity.items() if v and k != "잘 모름"]
                    if selected_sunlight_intensity:
                        user_conditions.append(f"햇빛 강도: {', '.join(selected_sunlight_intensity)}")
                    
                    selected_winter_temp = [k for k, v in winter_temp.items() if v and k != "잘 모름"]
                    if selected_winter_temp:
                        user_conditions.append(f"겨울 온도: {', '.join(selected_winter_temp)}")
                    
                    selected_summer_temp = [k for k, v in summer_temp.items() if v and k != "잘 모름"]
                    if selected_summer_temp:
                        user_conditions.append(f"여름 온도: {', '.join(selected_summer_temp)}")
                    
                    selected_humidity = [k for k, v in humidity.items() if v and k != "잘 모름"]
                    if selected_humidity:
                        user_conditions.append(f"습도: {', '.join(selected_humidity)}")
                    
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