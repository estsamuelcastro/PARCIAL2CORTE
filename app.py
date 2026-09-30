from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CSV_LIVE = DATA / "live_telemetry.csv"
JSON_LIVE = DATA / "live_summary.json"
CSV_SAMPLE = DATA / "sample_coins.csv"

DENOMS = [50, 100, 200, 500, 1000]
LABELS = ["$50", "$100", "$200", "$500", "$1.000"]

st.set_page_config(page_title="Monedas inteligentes COP", page_icon="🪙", layout="wide")
st.title("🪙 Sistema logístico de monedas inteligentes")
st.caption("Dashboard de integración: PyBullet + telemetría + ESP32 + asistente | Moneda: COP")

with st.sidebar:
    st.header("Conexión")
    esp32_ip = st.text_input("IP del ESP32", "192.168.1.50")
    use_live = st.checkbox("Usar telemetría de la simulación", value=True)
    st.write("Denominaciones: $50, $100, $200, $500 y $1.000")
    st.button("Actualizar datos")


def load_df() -> pd.DataFrame:
    path = CSV_LIVE if use_live and CSV_LIVE.exists() else CSV_SAMPLE
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=["timestamp", "event", "coin", "quantity", "weight_g", "value_cop", "cup_id", "state", "route_x", "route_y"])


def load_summary() -> dict:
    if JSON_LIVE.exists() and use_live:
        try:
            return json.loads(JSON_LIVE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def cop(value: float) -> str:
    return f"${value:,.0f} COP".replace(",", ".")


df = load_df()
summary = load_summary()
coin_df = df[pd.to_numeric(df.get("coin"), errors="coerce").notna()].copy() if not df.empty else df

if not coin_df.empty:
    total_coins = int(coin_df["quantity"].sum())
    total_value = float(coin_df["value_cop"].sum())
    total_weight = float(coin_df["weight_g"].sum())
else:
    total_coins = int(summary.get("total_coins", 0))
    total_value = float(summary.get("total_value_cop", 0))
    total_weight = float(summary.get("total_weight_g", 0))

state = summary.get("state", df["state"].iloc[-1] if not df.empty else "IDLE")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Monedas procesadas", total_coins)
c2.metric("Valor procesado", cop(total_value))
c3.metric("Peso acumulado", f"{total_weight:.2f} g")
c4.metric("Estado", state)

st.subheader("Cantidad por denominación")
if not coin_df.empty:
    dist = coin_df.groupby("coin", as_index=True)["quantity"].sum().reindex(DENOMS, fill_value=0)
    dist.index = LABELS
    st.bar_chart(dist)
else:
    st.info("Ejecuta la simulación o carga los datos de prueba.")

st.subheader("Peso y valor por recipiente")
if not coin_df.empty:
    grouped = coin_df.groupby(["cup_id", "coin"], as_index=False)[["quantity", "weight_g", "value_cop"]].sum()
    grouped["denominacion"] = grouped["coin"].map(dict(zip(DENOMS, LABELS)))
    grouped["valor_cop"] = grouped["value_cop"].map(cop)
    st.dataframe(grouped[["cup_id", "denominacion", "quantity", "weight_g", "valor_cop"]], use_container_width=True)

st.subheader("Ruta del carro")
route = df[pd.to_numeric(df.get("route_x"), errors="coerce").notna()] if not df.empty else pd.DataFrame()
if not route.empty:
    route_plot = route[["route_x", "route_y"]].astype(float).set_index("route_x")
    st.line_chart(route_plot)
    st.caption("La ruta incluye tres obstáculos representados en el URDF y una meta.")
else:
    st.info("La ruta aparecerá después de ejecutar la simulación.")

st.subheader("Estado del ESP32")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Consultar /status"):
        try:
            r = requests.get(f"http://{esp32_ip}/status", timeout=2)
            st.json(r.json())
        except requests.RequestException as exc:
            st.error(f"No se pudo consultar el ESP32: {exc}")
with col_b:
    value_to_send = st.selectbox("Enviar orden de clasificación", DENOMS, format_func=lambda v: dict(zip(DENOMS, LABELS))[v])
    if st.button("Clasificar en ESP32"):
        try:
            r = requests.get(f"http://{esp32_ip}/sort", params={"value": value_to_send}, timeout=3)
            st.json(r.json())
        except requests.RequestException as exc:
            st.error(f"No se pudo enviar la orden al ESP32: {exc}")

st.subheader("Asistente de datos")
question = st.text_input("Pregunta", "¿Cuántas monedas de $200 se procesaron?")
if st.button("Consultar asistente"):
    q = question.lower().replace(".", "")
    found = None
    for val, label in zip(DENOMS, LABELS):
        if label.lower() in q or str(val) in q:
            found = val
            break
    if found is not None:
        n = int(coin_df.loc[coin_df["coin"] == found, "quantity"].sum()) if not coin_df.empty else 0
        st.info(f"Se registran {n} monedas de {dict(zip(DENOMS, LABELS))[found]}.")
    elif "peso" in q:
        st.info(f"El peso acumulado es {total_weight:.2f} g.")
    elif "valor" in q or "total" in q:
        st.info(f"El valor acumulado es {cop(total_value)}.")
    elif "cuánt" in q or "cuanto" in q or "cantidad" in q:
        st.info(f"El sistema registra {total_coins} monedas.")
    else:
        st.info("Consulta una denominación, el peso, el valor acumulado o la cantidad total.")

with st.expander("Últimos eventos"):
    st.dataframe(df.tail(30), use_container_width=True)
