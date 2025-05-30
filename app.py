import streamlit as st
from collections import Counter

# ——————————————————————————————
# 앱 설정
# ——————————————————————————————
st.set_page_config(
    page_title="성격유형 진단 챗봇",
    layout="centered"
)
st.title("🔍 성격유형 진단 챗봇")
st.write("아래 질문에 답변해 주세요 (괄호 속 설명은 숨겨져 있습니다).")

# ——————————————————————————————
# 세션 상태 초기화
# ——————————————————————————————
if "history" not in st.session_state:
    st.session_state.history = []   # (question, visible_answer)
if "types" not in st.session_state:
    st.session_state.types = []     # 응답별 유형 코드

# ——————————————————————————————
# 질문 & 옵션 정의 (괄호 내용 제외)
# ——————————————————————————————
questions = [
    {
        "text": "1/5. 내가 가장 '나답다'고 느끼는 순간은 언제인가요?",
        "options": [
            ("A. 다양한 사람들의 의견을 듣고 균형 있게 정리할 때", "BOND"),
            ("B. 내가 던진 한 마디가 모두를 웃게 만들었을 때", "HAEP"),
            ("C. 바로 실행에 옮겨 무언가를 만들어냈을 때", "IMVP"),
            ("D. 누군가의 마음을 어루만져줄 수 있었을 때", "CARE"),
        ]
    },
    {
        "text": "2/5. 새로운 봉사활동에 참여하게 된다면, 나는…",
        "options": [
            ("A. 다 같이 잘 어울릴 수 있도록 사람들을 연결해볼 것 같아요", "BOND"),
            ("B. 축제처럼 즐겁게 분위기를 띄우는 역할을 할 것 같아요", "HAEP"),
            ("C. 실질적인 도움이 되도록 계획을 세우고 바로 움직일 것 같아요", "IMVP"),
            ("D. 힘든 사람 옆에 조용히 앉아 진심으로 함께해줄 것 같아요", "CARE"),
        ]
    },
    {
        "text": "3/5. 주변 친구들이 자주 하는 내 칭찬은?",
        "options": [
            ('A. "네가 있으면 다들 잘 지내는 것 같아"', "BOND"),
            ('B. "넌 분위기 메이커야! 재밌어!"', "HAEP"),
            ('C. "진짜 추진력 대박이야, 항상 믿음 가"', "IMVP"),
            ('D. "너는 사람 마음을 참 잘 알아봐주는 것 같아"', "CARE"),
        ]
    },
    {
        "text": "4/5. 여러 사람이 함께 하는 모임에서 나는…",
        "options": [
            ("A. 서로 잘 어울릴 수 있도록 조율자 역할을 맡는다", "BOND"),
            ("B. 사람들을 웃게 하며 분위기를 이끈다", "HAEP"),
            ("C. 필요한 일을 먼저 찾아 실행에 옮긴다", "IMVP"),
            ("D. 조용히 주변을 살피며 도와줄 사람을 찾는다", "CARE"),
        ]
    },
    {
        "text": "5/5. 어떤 상황에서 가장 먼저 마음이 움직이나요?",
        "options": [
            ("A. 갈등 상황에서 누군가 중심을 잡아야 할 때", "BOND"),
            ("B. 낯선 환경에서 새로운 인연을 만들 기회가 생겼을 때", "HAEP"),
            ("C. 문제를 해결할 수 있는 기회가 보일 때", "IMVP"),
            ("D. 누군가 조용히 힘들어하고 있을 때", "CARE"),
        ]
    },
]

# ——————————————————————————————
# 이미지 매핑 (결과 표시용)
# ——————————————————————————————
image_urls = {
    "BOND": "https://github.com/gyoon0103/personal/blob/main/BOND.png",
    "HAEP": "https://github.com/gyoon0103/personal/blob/main/HAEP.png",
    "IMVP": "https://github.com/gyoon0103/personal/blob/main/IMVP.png",
    "CARE": "https://github.com/gyoon0103/personal/blob/main/CARE.png",
}

# 유형별 설명
type_descriptions = {
    "BOND": "당신은 사람들 사이의 균형을 맞추고 조화를 이루는 데 탁월한 재능이 있습니다.",
    "HAEP": "당신은 주변을 밝게 만들고 사람들에게 긍정적인 에너지를 전달하는 능력이 있습니다.",
    "IMVP": "당신은 실행력이 뛰어나고 문제 해결에 있어 효율적인 접근 방식을 가지고 있습니다.",
    "CARE": "당신은 타인의 감정을 섬세하게 이해하고 진심 어린 위로를 전할 수 있는 따뜻한 마음을 가졌습니다."
}

# ——————————————————————————————
# 대화 내역 표시
# ——————————————————————————————
for q, a in st.session_state.history:
    st.markdown(f"💬 **Q:** {q}")
    st.markdown(f"👤 **A:** {a}")

# ——————————————————————————————
# 질문 흐름
# ——————————————————————————————
current = len(st.session_state.history)

if current < len(questions):
    q = questions[current]
    st.markdown(f"💬 **{q['text']}**")
    # 사용자에게는 A/B/C/D+질문 텍스트만 보이도록
    labels = [opt[0] for opt in q["options"]]
    choice = st.radio("선택하세요:", labels, key=f"q{current}")
    
    if st.button("다음", key=f"submit{current}"):
        # 선택된 라벨에 대응하는 유형 코드 찾기
        mapping = {opt[0]: opt[1] for opt in q["options"]}
        selected_type = mapping[choice]
        # 기록
        st.session_state.history.append((q["text"], choice))
        st.session_state.types.append(selected_type)
        st.rerun()

else:
    # ——————————————————————————————
    # 결과 계산 & 표시
    # ——————————————————————————————
    counts = Counter(st.session_state.types)
    result_type = counts.most_common(1)[0][0]

    st.markdown("---")
    st.success("🎉 성격유형 진단 결과")
    
    # 이미지 로딩 시도
    try:
        st.image(image_urls[result_type], caption=f"{result_type} 유형", use_container_width=True)
    except Exception as e:
        st.warning("이미지를 불러올 수 없습니다.")
    
    # 결과 설명
    st.markdown(f"### 당신은 **{result_type}** 유형입니다!")
    st.write(type_descriptions[result_type])
    
    # 응답 분포 표시
    st.markdown("### 응답 분포")
    total = len(st.session_state.types)
    for type_code, count in counts.most_common():
        percentage = (count / total) * 100
        st.write(f"- {type_code}: {percentage:.1f}% ({count}회)")
    
    # 다시하기 버튼
    if st.button("다시 진단하기"):
        st.session_state.history = []
        st.session_state.types = []
        st.rerun()
