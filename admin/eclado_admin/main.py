import streamlit as st

from eclado_admin.asset_recovery import enable_asset_recovery
from eclado_admin.demo_auth import DEMO_EMAIL, logout_demo, require_demo_login
from eclado_admin.marketing_pages import (
    MARKETING_PAGES,
    render_marketing_page,
    select_workspace,
)
from eclado_admin.sales_pages import render_sales_page
from eclado_admin.ui_theme import apply_theme, brand

st.set_page_config(page_title="ECLADO | 사장님 대시보드", page_icon="🌿", layout="wide")
apply_theme()
enable_asset_recovery()
require_demo_login()

with st.sidebar:
    brand()
    st.caption("MARKETING INTELLIGENCE · Ver.1 초안")
    st.caption(f"{DEMO_EMAIL} · 데모 로그인")
    st.button("로그아웃", on_click=logout_demo, key="demo_logout", use_container_width=True)
    st.divider()
    st.markdown("### 매출 분석")
    sales_page = st.radio(
        "분석 메뉴",
        ["매출 요약", "매출 추이", "고객별 매출 추이", "매출·상품·리뷰 AI"],
        key="sales_page",
        label_visibility="collapsed",
        on_change=select_workspace,
        args=("sales",),
    )
    st.divider()
    st.markdown("### CRM · 마케팅")
    st.caption("합성 사례로 검토하는 기능 미리보기")
    if st.session_state.get("workspace_page", "sales") != "sales":
        st.button(
            "매출 분석으로 돌아가기",
            key="return_to_sales",
            on_click=select_workspace,
            args=("sales",),
            width="stretch",
        )
    for index, label in enumerate(MARKETING_PAGES):
        st.button(
            label,
            key=f"marketing_nav_{index}",
            on_click=select_workspace,
            args=(label,),
            width="stretch",
            type="primary" if st.session_state.get("workspace_page") == label else "secondary",
        )

workspace = st.session_state.get("workspace_page", "sales")
if workspace in MARKETING_PAGES:
    render_marketing_page(workspace)
else:
    render_sales_page(sales_page)
