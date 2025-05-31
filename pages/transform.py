import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="加工後データ", layout="wide")
st.title("③ 加工後データの確認")

if "transformed_df" not in st.session_state or "target_col" not in st.session_state:
    st.warning("前のページで加工を実行してください。")
    st.stop()

df = st.session_state["transformed_df"]
target_col = st.session_state["target_col"]

# プレビュー
st.subheader("🧾 加工後データのプレビュー")
st.dataframe(df.head(100))

st.subheader("📐 データの情報")
st.markdown(f"- 行数：{df.shape[0]} 行")
st.markdown(f"- 列数：{df.shape[1]} 列")

# 🔽 加工後データをCSVでダウンロード
st.subheader("💾 加工済みデータのダウンロード")

csv = df.to_csv(index=False).encode('utf-8-sig')  # Excel互換なら utf-8-sig 推奨

st.download_button(
    label="📥 加工後CSVをダウンロード",
    data=csv,
    file_name="transformed_data.csv",
    mime="text/csv"
)

