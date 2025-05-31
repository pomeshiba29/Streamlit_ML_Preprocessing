import streamlit as st
import pandas as pd

st.set_page_config(page_title="データ型変換", layout="wide")
st.title("① データの型を確認・変換")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    converted_df = df.copy()

    st.write("データのプレビュー", df.head())

    for col in df.columns:
        new_type = st.selectbox(
            f"{col} の型を変換（現在：{df[col].dtype}）",
            options=["そのまま", "数値(float)", "整数(int)", "文字列(str)", "日付(datetime)"],
            key=f"convert_{col}"
        )
        if new_type != "そのまま":
            try:
                if new_type == "数値(float)":
                    converted_df[col] = pd.to_numeric(df[col], errors="coerce")
                elif new_type == "整数(int)":
                    converted_df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif new_type == "文字列(str)":
                    converted_df[col] = df[col].astype(str)
                elif new_type == "日付(datetime)":
                    converted_df[col] = pd.to_datetime(df[col], errors="coerce")
                st.success(f"{col} を {new_type} に変換しました。")
            except Exception as e:
                st.error(f"{col} の変換に失敗：{e}")

    # 🎯 目的変数の選択
    st.subheader("🎯 目的変数を選択（任意）")
    target_col = st.selectbox(
        "目的変数を選択してください",
        options=[""] + list(converted_df.columns),
        key="target_select"
    )

    if target_col:
        st.session_state["target_col"] = target_col
        st.info(f"目的変数：**{target_col}** を選択しました。")

        # ✅ カテゴリ型かつ2値であればラベル付け
        if converted_df[target_col].dtype in ["object", "category"]:
            unique_vals = converted_df[target_col].dropna().astype(str).str.strip().unique()
            if len(unique_vals) == 2:
                st.subheader("🟢 正例（1）とする値を選択してください")
                unique_vals = sorted(unique_vals)
                positive_label = st.radio("正例にしたい値を選択：", options=unique_vals, key="positive_radio")

                if positive_label:
                    converted_df[target_col] = (
                        converted_df[target_col]
                        .astype(str)
                        .str.strip()
                        .apply(lambda x: 1 if x == positive_label else 0)
                        .astype("category")
                    )
                    st.success(f"`{target_col}` を 0/1 にラベル変換しました。")
            else:
                st.info(f"`{target_col}` はカテゴリ型ですが、ユニーク値が2つではありません（{len(unique_vals)}件）。ラベル変換は行いません。")
        else:
            st.info(f"`{target_col}` は数値型です。ラベル変換はスキップします。")
    else:
        st.session_state.pop("target_col", None)

    # 「決定」ボタンでセッションに保存して次ページへ
    if st.button("✅ 型変換とラベル変換を確定 → 次ページへ"):
        st.session_state["converted_df"] = converted_df
        st.switch_page("pages/stats.py")
