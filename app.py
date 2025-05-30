import streamlit as st
from collections import Counter

# ——————————————————————————————
# 앱 설정
# ——————————————————————————————
st.set_page_config(
    page_title="나의 지구시민 유형 테스트",
    layout="centered"
)
st.title("🔍 나의 지구시민 유형 테스트")

st.write("🌍 당신 안에 있는 작은 빛 하나가 지구 어딘가를 비춥니다. 그 빛은 어떤 모습일까요. 나의 성향에 맞는 지구시민 역할을 알고, KOICA와 함께할 수 있는 활동을 찾아보세요.")

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
    }
]

# ——————————————————————————————
# 이미지 매핑 (결과 표시용)
# ——————————————————————————————
image_urls = {
    "BOND": "https://raw.githubusercontent.com/gyoon0103/personal/main/bond_v.png",
    "HAEP": "https://raw.githubusercontent.com/gyoon0103/personal/main/haep_v.png",
    "IMVP": "https://raw.githubusercontent.com/gyoon0103/personal/main/imvp_v.png",
    "CARE": "https://raw.githubusercontent.com/gyoon0103/personal/main/care_v.png",
}

# 유형별 설명
type_descriptions = {
    "BOND": {
        "title": "🤝 당신은 **BOND! – 균형 잡는 조정자형**",
        "subtitle": "Balanced Organizer for Network & Development",
        "description": """
사람들 사이의 균형을 맞추고 조화를 이루는 데 탁월한 재능이 있습니다.
당신은 서로 다른 의견을 가진 사람들을 이해하고 연결하는 다리 역할을 합니다.

**당신과 닮은 인물**

- 🕊 코피 아난 – 평화를 위해 대화의 다리를 놓은 UN 사무총장""",
    },
    "HAEP": {
        "title": "🌞 당신은 **HAEP! – 희망 전파자형**",
        "subtitle": "Hopeful Activist for Earth & People",
        "description": """
밝은 에너지로 주변을 환하게 비추는 희망의 전달자입니다.
당신이 있는 곳에는 언제나 웃음과 따뜻한 분위기가 가득합니다.

**당신과 닮은 인물**

- 🎭 로빈 윌리엄스 – 유쾌함 속에 깊은 따뜻함을 전한 배우""",
    },
    "IMVP": {
        "title": "⚡ 당신은 **IMVP! – 임팩트 메이커형**",
        "subtitle": "Impactful Volunteer for People",
        "description": """
문제를 보면 가만히 있지 못하고, 바로 실행에 옮기는 실천가입니다.
계획과 책임감, 리더십으로 세상에 변화를 만들어내는 사람입니다.

**당신과 닮은 인물**

- 🌍 넬슨 만델라 – 사회를 바꾼 의지의 리더""",
    },
    "CARE": {
        "title": "💗 당신은 **CARE! – 따뜻한 돌봄자형**",
        "subtitle": "Compassionate Advocate for Relief & Empathy",
        "description": """
타인의 마음을 누구보다 잘 이해하고, 조용히 곁을 지켜주는 사람입니다.
당신의 배려는 누군가에겐 큰 위로와 용기가 됩니다.

**당신과 닮은 인물**

- 🕊 테레사 수녀 – 삶으로 사랑을 실천한 인류의 어머니""",
    }
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
    st.markdown(type_descriptions[result_type]["title"])
    st.markdown(type_descriptions[result_type]["subtitle"])
    st.markdown(type_descriptions[result_type]["description"])
    
    # 응답 분포 표시
    st.markdown("### 📊 응답 분포")
    total = len(st.session_state.types)
    for type_code, count in counts.most_common():
        percentage = (count / total) * 100
        st.write(f"- {type_code}: {percentage:.1f}% ({count}회)")
    
    # 다시하기 버튼
    if st.button("🔄 다시 진단하기"):
        st.session_state.history = []
        st.session_state.types = []
        st.rerun()
