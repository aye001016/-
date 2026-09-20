import random
import time

import streamlit as st


st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️", layout="centered")

DEFAULT_MENUS = {
    "한식": ["김치찌개", "된장찌개", "순두부찌개", "부대찌개", "제육볶음", "불고기", "삼겹살", "갈비", "닭갈비", "찜닭", "닭볶음탕", "감자탕", "뼈해장국", "설렁탕", "곰탕", "육개장", "국밥", "비빔밥", "쌈밥", "백반", "보쌈", "족발", "낙지볶음", "오징어볶음", "갈치조림", "고등어구이", "간장게장", "아귀찜", "해물찜", "칼국수", "수제비", "냉면", "막국수", "김치볶음밥", "주꾸미볶음", "오리구이"],
    "중식": ["짜장면", "짬뽕", "볶음밥", "탕수육", "마라탕", "마라샹궈", "양꼬치", "훠궈", "딤섬", "샤오롱바오", "유린기", "깐풍기", "꿔바로우", "마파두부", "고추잡채", "유산슬", "동파육", "탄탄면", "우육면"],
    "일식": ["초밥", "회", "사시미덮밥", "돈카츠", "가츠동", "규동", "오야코동", "텐동", "우동", "소바", "라멘", "카레", "오므라이스", "야키소바", "오코노미야키", "타코야키", "샤브샤브", "스키야키", "장어덮밥"],
    "양식": ["파스타", "피자", "스테이크", "리소토", "라자냐", "그라탱", "뇨키", "함박스테이크", "바비큐", "폭립", "치킨 스테이크", "필라프", "오믈렛", "브런치", "샌드위치", "수제버거", "샐러드", "감바스"],
    "분식": ["떡볶이", "라볶이", "김밥", "라면", "쫄면", "순대", "튀김", "어묵", "만두", "군만두", "떡꼬치", "핫도그", "토스트", "컵밥"],
    "고기·구이": ["소고기 구이", "돼지고기 구이", "삼겹살", "목살", "돼지갈비", "소갈비", "양갈비", "곱창", "대창", "막창", "닭구이", "오리구이", "철판구이"],
    "치킨·패스트푸드": ["후라이드치킨", "양념치킨", "간장치킨", "숯불치킨", "닭강정", "햄버거", "핫도그", "피자", "토스트", "샌드위치", "타코", "부리토", "케밥"],
    "아시아·세계음식": ["쌀국수", "분짜", "반미", "팟타이", "똠얌꿍", "태국식 카레", "나시고렝", "미고렝", "인도 커리", "탄두리치킨", "난", "타코", "부리토", "퀘사디아", "케밥", "포케"],
    "해산물": ["회", "초밥", "물회", "해물탕", "조개구이", "대게", "킹크랩", "랍스터", "장어구이", "생선구이", "아귀찜", "해물찜", "낙지볶음", "주꾸미볶음", "굴 요리", "새우 요리", "해산물 파스타"],
    "가벼운 식사": ["샐러드", "포케", "샌드위치", "랩", "죽", "김밥", "쌀국수", "메밀소바", "두부 요리", "그릭요거트", "브런치", "수프", "베이글", "닭가슴살 식단"],
    "야식·안주": ["족발", "보쌈", "치킨", "닭발", "곱창", "막창", "골뱅이무침", "오돌뼈", "해물파전", "김치전", "두부김치", "먹태", "감자튀김", "떡볶이", "피자", "회", "조개구이", "나초"],
}

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(160deg, #fff9f1 0%, #fff0e5 100%);}
    .title {text-align:center; font-size:2.6rem; font-weight:900; color:#ef5f3c; margin-bottom:0;}
    .subtitle {text-align:center; color:#7d6258; margin:0.3rem 0 1.8rem;}
    .result {background:white; border:2px solid #ffad8f; border-radius:22px; padding:28px 14px;
             text-align:center; box-shadow:0 8px 25px rgba(239,95,60,.12); margin:1rem 0;}
    .result-category {color:#92746a; font-size:1rem;}
    .result-menu {color:#ef5f3c; font-size:2.3rem; font-weight:900; margin-top:5px;}
    .stButton > button {width:100%; border-radius:14px; height:3.2rem; font-weight:800;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "menus" not in st.session_state:
    st.session_state.menus = {k: list(v) for k, v in DEFAULT_MENUS.items()}
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None

st.markdown('<p class="title">🍽️ 오늘 뭐 먹지?</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">결정은 랜덤, 맛있게 먹는 건 진심!</p>', unsafe_allow_html=True)

categories = list(st.session_state.menus)
selected = st.multiselect(
    "먹고 싶은 카테고리를 골라주세요",
    categories,
    default=categories,
    placeholder="하나 이상 선택하세요",
)

col1, col2 = st.columns(2)
with col1:
    no_repeat = st.checkbox("최근 메뉴 제외", value=True, help="최근 10회에 뽑힌 메뉴를 우선 제외합니다.")
with col2:
    roll_seconds = st.select_slider("두근두근 시간", options=[0, 1, 2], value=1, format_func=lambda x: f"{x}초")

choices = [(cat, menu) for cat in selected for menu in st.session_state.menus.get(cat, [])]
if no_repeat:
    recent = {menu for _, menu in st.session_state.history[:10]}
    fresh = [pair for pair in choices if pair[1] not in recent]
    if fresh:
        choices = fresh

if st.button("🎲 오늘의 메뉴 뽑기", type="primary", use_container_width=True):
    if not choices:
        st.warning("선택 가능한 메뉴가 없어요. 카테고리나 메뉴를 추가해 주세요.")
    else:
        placeholder = st.empty()
        if roll_seconds:
            for _ in range(roll_seconds * 8):
                cat, menu = random.choice(choices)
                placeholder.markdown(
                    f'<div class="result"><div class="result-category">고르는 중… {cat}</div><div class="result-menu">{menu}</div></div>',
                    unsafe_allow_html=True,
                )
                time.sleep(0.125)
        result = random.choice(choices)
        st.session_state.result = result
        st.session_state.history.insert(0, result)
        st.session_state.history = st.session_state.history[:30]
        placeholder.empty()
        st.rerun()

if st.session_state.result:
    category, menu = st.session_state.result
    st.markdown(
        f'<div class="result"><div class="result-category">오늘의 선택 · {category}</div><div class="result-menu">{menu}</div></div>',
        unsafe_allow_html=True,
    )
    st.caption("마음에 안 들면 한 번만 더… 정말 한 번만! 😎")

with st.expander("✏️ 메뉴 추가·삭제"):
    add_tab, delete_tab = st.tabs(["메뉴 추가", "메뉴 삭제"])
    with add_tab:
        with st.form("add_menu", clear_on_submit=True):
            new_category = st.text_input("카테고리", placeholder="예: 디저트")
            new_menu = st.text_input("메뉴", placeholder="예: 빙수")
            if st.form_submit_button("추가"):
                category = new_category.strip()
                menu = new_menu.strip()
                if not category or not menu:
                    st.warning("카테고리와 메뉴를 모두 입력해 주세요.")
                elif menu in st.session_state.menus.get(category, []):
                    st.info("이미 등록된 메뉴예요.")
                else:
                    st.session_state.menus.setdefault(category, []).append(menu)
                    st.success(f"{category}에 '{menu}'를 추가했어요.")
                    st.rerun()
    with delete_tab:
        delete_category = st.selectbox("카테고리 선택", list(st.session_state.menus), key="delete_category")
        delete_options = st.session_state.menus.get(delete_category, [])
        delete_menus = st.multiselect("삭제할 메뉴", delete_options)
        if st.button("선택 메뉴 삭제", disabled=not delete_menus):
            st.session_state.menus[delete_category] = [m for m in delete_options if m not in delete_menus]
            if not st.session_state.menus[delete_category]:
                del st.session_state.menus[delete_category]
            st.rerun()

with st.expander("🕘 최근 뽑은 메뉴"):
    if st.session_state.history:
        for number, (category, menu) in enumerate(st.session_state.history, start=1):
            st.write(f"{number}. **{menu}**  ·  {category}")
        if st.button("기록 지우기"):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()
    else:
        st.caption("아직 뽑은 메뉴가 없어요.")

with st.sidebar:
    st.header("설정")
    total = sum(len(items) for items in st.session_state.menus.values())
    st.metric("등록된 메뉴", f"{total}개")
    st.metric("카테고리", f"{len(st.session_state.menus)}개")
    if st.button("기본 메뉴로 초기화"):
        st.session_state.menus = {k: list(v) for k, v in DEFAULT_MENUS.items()}
        st.session_state.history = []
        st.session_state.result = None
        st.rerun()
    st.caption("각 이용자가 추가·삭제한 메뉴는 해당 브라우저 세션에서만 유지됩니다.")

