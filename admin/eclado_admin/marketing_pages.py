"""Isolated, fixed synthetic scenarios for reviewing the planned marketing UI.

These fixtures are not analytics over the sales upload or live customer records.
No database, AI provider, delivery or coupon integration is invoked here.
"""

import json
from collections.abc import Callable

import streamlit as st

MARKETING_PAGES = (
    "재주문 추천",
    "이탈 조기경보",
    "교차판매 추천",
    "리뷰 대응·캠페인",
    "마케팅 성과",
    "외부 신호·연동 상태",
)


def select_workspace(page: str) -> None:
    st.session_state["workspace_page"] = page


def _evidence(sample: str) -> None:
    st.caption(
        f"근거 기간 2026-08-01–2026-10-31 · 기준일 2026-11-01 · Asia/Seoul · {sample} · "
        "출처: 화면 검토용 고정 합성 사례 v1 · 생성형 AI 호출 없음"
    )


def _open_campaign(scenario: str) -> None:
    st.session_state["campaign_scenario"] = scenario
    select_workspace("리뷰 대응·캠페인")


def _draft_changed(code: str) -> None:
    st.session_state[f"draft_reviewed_{code}"] = False


def _reorder() -> None:
    _evidence("가상 거래처 1곳 · 주문 3건 · 주문 간격 2개")
    st.subheader("다음 구매 시점에 맞춘 거래처 관리")
    for column, label, value in zip(
        st.columns(3),
        ["거래처", "관측 구매 주기", "예상 재주문 구간"],
        ["가상 에스테틱 A", "28–32일", "11월 1일–5일"],
        strict=True,
    ):
        column.metric(label, value)
    with st.container(border=True):
        st.markdown("#### 가상 토너 A · 합성 상품")
        st.dataframe(
            [{"주문일": day, "수량": 6} for day in ["2026-08-05", "2026-09-02", "2026-10-04"]],
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "주문 간격 28일·32일을 마지막 주문일 10월 4일에 적용한 검토용 구간입니다. "
            "근거 간격이 2개뿐이므로 실제 구매 주기로 검증되지 않았습니다."
        )
        st.write("신뢰도: 낮음 · 주문 용도와 실제 소비량 확인 필요")
        st.info("실제 재고·소비량은 알 수 없습니다. 재고 부족을 확정하거나 자동 발주하지 않습니다.")
        st.button(
            "재주문 안내 초안 보기",
            on_click=_open_campaign,
            args=("재주문 안내",),
            key="reorder_draft",
        )


def _churn() -> None:
    _evidence("가상 거래처 2곳 · 행동 변화 비교 사례")
    st.subheader("관찰 신호를 확인하고 상담 우선순위 결정")
    st.dataframe(
        [
            {
                "거래처": "가상 에스테틱 A",
                "구매 주기": "28–32일 가정",
                "최근 구매": "2026-10-04",
                "관찰": "예상 주기 도래",
                "검토 우선순위": "보통",
            },
            {
                "거래처": "가상 에스테틱 B",
                "구매 주기": "30일 가정",
                "최근 구매": "2026-08-15",
                "관찰": "기준일 78일 미구매·주문금액 감소",
                "검토 우선순위": "높음",
            },
        ],
        hide_index=True,
        width="stretch",
    )
    st.write("사례 규칙: 예상 주기의 2배 초과 지연과 주문금액 감소가 겹치면 우선 상담 후보로 표시")
    st.info(
        "검증된 이탈 확률이 아닙니다. 거래처 휴무·다른 채널 주문·누락 이력을 먼저 확인하세요. "
        "부정 리뷰만으로 고객 성향이나 이탈 이유를 확정하지 않습니다."
    )
    st.button(
        "미구매 거래처 상담 초안 보기",
        on_click=_open_campaign,
        args=("장기 미구매 상담",),
        key="churn_draft",
    )


def _cross_sell() -> None:
    _evidence("가상 토너 A 구매 주문 40건 중 가상 크림 B 동시 구매 12건")
    st.subheader("함께 구매한 패턴으로 보는 추가 제안")
    left, right = st.columns(2)
    with left, st.container(border=True):
        st.markdown("#### 기준 상품 · 가상 토너 A")
        st.write("거래처 A의 구매 상품 · 예시 상품명이며 공식 카탈로그 상품과 무관")
    with right, st.container(border=True):
        st.markdown("#### 추천 후보 · 가상 크림 B")
        st.metric("합성 사례 동시 구매 비율", "30%")
        st.write("추천 이유: 같은 기간 토너 구매 주문 40건 중 12건에서 함께 구매")
    st.info(
        "추천 신뢰도: 검증 전 · 40건의 제한된 합성 표본입니다. "
        "개인의 피부 특성·효능·상품 적합성은 알 수 없습니다."
    )
    st.dataframe(
        [
            {"확인 항목": item, "상태": "확인 대기"}
            for item in [
                "현재 재고",
                "승인된 상품 속성·용도",
                "거래처 선호·거부 이력",
                "실제 판매 가격",
            ]
        ],
        hide_index=True,
        width="stretch",
    )

    st.button(
        "교차판매 제안 초안 보기",
        on_click=_open_campaign,
        args=("교차판매 제안",),
        key="cross_sell_draft",
    )


def _campaigns() -> None:
    _evidence("가상 거래처 A/B · 시나리오별 고정 합성 근거")
    scenario = st.selectbox(
        "캠페인 시나리오",
        ["재주문 안내", "부정 리뷰 상담", "생일 안내", "장기 미구매 상담", "교차판매 제안"],
        key="campaign_scenario",
    )
    code = {
        "재주문 안내": "reorder",
        "부정 리뷰 상담": "recovery",
        "생일 안내": "birthday",
        "장기 미구매 상담": "dormant",
        "교차판매 제안": "cross_sell",
    }[scenario]
    if code == "reorder":
        st.write("대상: 가상 에스테틱 A · 가상 토너 A · 예상 연락: 11월 1일–5일")
        draft = "안녕하세요. 최근 주문하신 상품의 추가 주문 계획이 있으시면 담당자에게 알려주세요."
    elif code == "recovery":
        st.write("대상: 가상 에스테틱 B · 가상 앰플 C · 구매 연결 합성 리뷰 1건")
        st.markdown("> 합성 리뷰: 사용 후 건조하게 느껴져 아쉬웠어요. (2점, 2026-10-28)")
        st.write("관찰: 사용감에 대한 불만 · 원인 가설: 확인 불가 · 대응: 담당자 상담")
        st.caption(
            "대체 상품은 검증된 속성이 없어 제시하지 않습니다. 리뷰 수정·삭제를 요청하지 않습니다."
        )
        draft = (
            "사용감에 아쉬움을 느끼셨다니 유감입니다. 남겨주신 의견을 확인했습니다. "
            "괜찮으시다면 담당자가 자세한 내용을 듣고 안내드리겠습니다."
        )
    elif code == "birthday":
        st.write("대상: 가상 거래처 A 담당자 · 직접 제공한 생일 11월 5일을 가정한 합성 사례")
        st.caption("연락 시점: 11월 5일 · 실제 생일·동의 정보는 미연결 · 생년월일 추정 없음")
        draft = "생일을 축하드립니다. 좋은 하루 보내시길 바랍니다."
    elif code == "dormant":
        st.write("대상: 가상 에스테틱 B · 78일 미구매·주문금액 감소 · 연락 시점: 담당자 확인 후")
        draft = (
            "안녕하세요. 상품 이용이나 주문과 관련해 도움이 필요하시면 담당자에게 말씀해 주세요."
        )
    else:
        st.write("대상: 가상 에스테틱 A · 토너 A 구매 주문 40건 중 크림 B 동시 구매 12건")
        st.caption("연락 시점: 상품 적합성·재고·선호 확인 후 · 효능 보증 없음")
        draft = (
            "추가 상품 안내를 원하시면 담당자가 상품 정보와 구매 조건을 확인해 안내드리겠습니다."
        )
    st.subheader("담당자 검토용 메시지")
    # Copy widget edits to independent state before the widget is removed on navigation.
    saved_key = f"saved_draft_{code}"
    widget_key = f"draft_text_{code}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = st.session_state.get(saved_key, draft)
    content = st.text_area(
        "메시지 초안", key=widget_key, height=150, on_change=_draft_changed, args=(code,)
    )
    st.session_state[saved_key] = content
    reviewed = st.checkbox("이 탭에서 초안 검토 표시", key=f"draft_reviewed_{code}")
    st.info("검토 표시 완료 · 운영 발송 승인이 아닙니다." if reviewed else "담당자 검토 대기")
    st.caption(
        "초안은 현재 세션 메모리에만 있습니다. 새로고침·로그아웃 시 사라질 수 있으니 내려받으세요."
    )
    st.dataframe(
        [
            {"발송 전 확인": item, "상태": "미확인 · 실행 차단"}
            for item in [
                "연락 목적·채널별 동의·수신거부",
                "시간·빈도·중복 발송 제한",
                "고객·주문·리뷰 연결",
                "예산·재고·쿠폰 조건",
                "권한·승인·감사 기록",
            ]
        ],
        hide_index=True,
        width="stretch",
    )
    st.write("쿠폰·선물: 제안 없음 · 실제 지급 비활성")
    st.download_button(
        "검토용 초안 다운로드",
        json.dumps(
            {
                "synthetic": True,
                "scenario": scenario,
                "message": content,
                "reviewed_in_tab": reviewed,
                "delivery_enabled": False,
            },
            ensure_ascii=False,
            indent=2,
        ),
        file_name=f"eclado-{code}-draft.json",
        mime="application/json",
    )
    st.button("실제 발송 · 연동 대기", disabled=True, key="send_campaign")


def _effectiveness() -> None:
    _evidence("합성 대상군 100곳 · 합성 비교군 100곳 · 가상 캠페인 1건")
    st.subheader("관찰된 결과와 캠페인 효과 구분")
    st.caption(
        "아래는 고정된 합성 결과 예시입니다. 이 UI의 초안 검토·발송 상태와 연결되지 않습니다."
    )
    st.dataframe(
        [
            {"지표": "배정 거래처", "합성 대상군": 100, "합성 비교군": 100},
            {"지표": "발송", "합성 대상군": 80, "합성 비교군": 0},
            {"지표": "수신", "합성 대상군": 76, "합성 비교군": 0},
            {"지표": "클릭", "합성 대상군": None, "합성 비교군": None},
            {"지표": "쿠폰 사용", "합성 대상군": 10, "합성 비교군": 0},
            {"지표": "재구매 거래처", "합성 대상군": 18, "합성 비교군": 12},
            {"지표": "할인 후 상품금액(원)", "합성 대상군": 1800000, "합성 비교군": 1200000},
            {"지표": "환불(원)", "합성 대상군": 100000, "합성 비교군": 50000},
            {"지표": "환불 차감 순매출(원)", "합성 대상군": 1700000, "합성 비교군": 1150000},
            {"지표": "캠페인 비용(원)", "합성 대상군": 100000, "합성 비교군": 0},
        ],
        hide_index=True,
        width="stretch",
    )
    st.metric("합성 배정 집단별 재구매율 차이", "+6%p", help="18/100 − 12/100")
    st.caption(
        "미수집 클릭은 빈 값으로 표시합니다. 쿠폰 할인은 할인 후 상품금액에 이미 반영된 예시입니다."
    )
    st.info(
        "관찰된 성과 예시입니다. 무작위 배정·집단 동질성·표본 크기가 검증되지 않아 "
        "인과 효과나 증분 매출로 확정할 수 없습니다. 매출은 이익과 다릅니다."
    )


def _operations() -> None:
    _evidence("합성 외부 신호 1건 · 합성 내부 매출 비교 1건")
    st.subheader("외부 신호와 매출 급변의 근거 검토")
    st.dataframe(
        [
            {
                "구분": "내부 합성 매출",
                "관측 시점": "2026-10-31",
                "신호": "직전 7일 대비 −20%",
                "출처": "고정 합성 사례 v1",
            },
            {
                "구분": "외부 합성 프로모션",
                "관측 시점": "2026-10-28",
                "신호": "동일 카테고리 할인 가정",
                "출처": "https://example.invalid/synthetic-promotion",
            },
        ],
        hide_index=True,
        width="stretch",
    )
    st.write("원인 가설: 할인 시기와 하락 시기가 겹쳤을 가능성 · 확인 수준: 원인 확인 불가")
    st.caption(
        ".invalid 주소는 합성 출처 표기입니다. 실제 외부 사이트를 조회하거나 수집하지 않았습니다."
    )
    st.write(
        "권장 확인: 내부 품절·가격 변경·환불·누락 주문을 먼저 대조하고 허가된 외부 자료와 비교"
    )
    st.subheader("데이터 연결 및 운영 상태")
    st.dataframe(
        [
            {"연결 영역": "라온몰 주문·회원·리뷰", "상태": "연동 대기", "최신 갱신": "미연결"},
            {
                "연결 영역": "공개 상품 카탈로그",
                "상태": "기존 스냅샷 · 매출 증거 아님",
                "최신 갱신": "매출·상품·리뷰 AI의 카탈로그에서 확인",
            },
            {
                "연결 영역": "Supabase 저장·직원 인증",
                "상태": "미연결 · 현재 데모 로그인",
                "최신 갱신": "미연결",
            },
            {"연결 영역": "Gemini", "상태": "미연결 · 생성형 분석 없음", "최신 갱신": "미연결"},
            {"연결 영역": "문자·쿠폰·발주", "상태": "비활성", "최신 갱신": "실행 없음"},
        ],
        hide_index=True,
        width="stretch",
    )
    st.info(
        "동기화 오류·누락·불일치: 연동 전이므로 검사되지 않았습니다. "
        "정상 또는 0건으로 간주하지 않습니다."
    )
    with st.expander("연동 계획의 문서 차이"):
        st.write(
            "적용한 README는 라온몰 관리자 API/공식 내보내기 및 플랫폼을 확인 전으로 기술합니다. "
            "기존 AGENTS·설계 문서는 Cafe24 확정 기록을 유지하고 있습니다. "
            "실제 연동 전에 플랫폼·권한·필드·갱신 주기를 확인해야 합니다."
        )


def render_marketing_page(page: str) -> None:
    st.title(f"CRM · {page}")
    st.warning(
        "합성 시나리오 미리보기 · 실제 ECLADO 실적이 아닙니다. "
        "매출 화면의 선택 기간·데이터·업로드 결과와 독립된 고정 사례입니다."
    )
    renderers: dict[str, Callable[[], None]] = dict(
        zip(
            MARKETING_PAGES,
            [_reorder, _churn, _cross_sell, _campaigns, _effectiveness, _operations],
            strict=True,
        )
    )
    renderers[page]()
