"""Bounded recovery for missing frontend widget chunks after a deployment."""

from pathlib import Path

import streamlit as st
from streamlit.components.v2 import component

_recovery_component = component(
    "eclado_asset_recovery",
    js=(Path(__file__).with_name("assets") / "asset_recovery.js").read_text(encoding="utf-8"),
)


def enable_asset_recovery() -> None:
    _recovery_component(
        key="eclado_asset_recovery", data={"revision": f"{st.__version__}-v1"}, height=0
    )
