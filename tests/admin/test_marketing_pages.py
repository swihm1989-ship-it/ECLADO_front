from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from eclado_admin.repositories.sales_repository import SalesRepository
from eclado_shared.schemas.sales import SalesAnalysis


def test_marketing_navigation_drafts_and_disabled_delivery() -> None:
    with patch.object(
        SalesRepository,
        "analyze",
        side_effect=lambda source, start, end, *args: SalesAnalysis(
            source=source, start=start, end=end, status="input pending"
        ),
    ):
        screen = AppTest.from_file(Path("admin/eclado_admin/main.py").resolve()).run(timeout=30)
        screen.text_input[0].set_value("user@example.com")
        screen.text_input[1].set_value("preview")
        screen.button[0].click().run(timeout=30)
        labels = [
            "재주문 추천",
            "이탈 조기경보",
            "교차판매 추천",
            "리뷰 대응·캠페인",
            "마케팅 성과",
            "외부 신호·연동 상태",
        ]
        for index, label in enumerate(labels):
            screen.button(key=f"marketing_nav_{index}").click().run(timeout=30)
            assert not screen.exception
            assert label in screen.title[0].value
            assert any("합성" in message.value for message in screen.warning)
        screen.button(key="marketing_nav_3").click().run(timeout=30)
        screen.text_area[0].set_value("담당자가 수정한 초안").run()
        screen.checkbox(key="draft_reviewed_reorder").check().run()
        assert any("검토 표시 완료" in message.value for message in screen.info)
        assert screen.button(key="send_campaign").disabled
        screen.text_area[0].set_value("검토 후 다시 수정한 초안").run()
        assert not screen.checkbox(key="draft_reviewed_reorder").value
        screen.selectbox(key="campaign_scenario").select("부정 리뷰 상담").run()
        assert screen.text_area[0].value != "담당자가 수정한 초안"
        screen.selectbox(key="campaign_scenario").select("재주문 안내").run()
        assert screen.text_area[0].value == "검토 후 다시 수정한 초안"
        for scenario in ["생일 안내", "장기 미구매 상담", "교차판매 제안"]:
            screen.selectbox(key="campaign_scenario").select(scenario).run()
            assert not screen.exception
            assert screen.text_area[0].value
            assert screen.button(key="send_campaign").disabled
        screen.button(key="return_to_sales").click().run(timeout=30)
        assert "매출 요약" in screen.title[0].value
        screen.radio(key="sales_page").set_value("매출 추이").run(timeout=30)
        assert not screen.exception
        assert "매출 추이" in screen.title[0].value
