import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="統計量と可視化", layout="wide")
st.title("② 統計量と相関の可視化")

if "converted_df" not in st.session_state:
    st.warning("前のページで型変換を行ってください。")
    st.stop()

df = st.session_state["converted_df"]

date_cols = df.select_dtypes(include=["datetime64[ns]"]).columns
num_cols = df.select_dtypes(include="number").columns
cat_cols = df.select_dtypes(include="object").columns

st.subheader("📅 日付データの可視化")
if len(date_cols) > 0 and len(num_cols) > 0:
    selected_date_col = st.selectbox("日付列を選択してください", date_cols, key="date_col")
    selected_value_col = st.selectbox("時系列で可視化したい数値列を選んでください", num_cols, key="value_col")
    if selected_date_col and selected_value_col:
        df_sorted = df.sort_values(by=selected_date_col)
        fig_time = px.line(df_sorted, x=selected_date_col, y=selected_value_col, title=f"{selected_value_col} の時系列推移")
        st.plotly_chart(fig_time, use_container_width=True)
else:
    st.info("⏳ 日付型の列が見つからないため、日付データの可視化はスキップされます。")

st.subheader("📊 数値統計量")
if len(num_cols) > 0:
    st.dataframe(df[num_cols].describe().T)

        # ✅ 数値データの欠損数を確認（追加）
    st.markdown("### 🩺 数値データの欠損数")
    num_missing_summary = pd.DataFrame({
        "欠損数": df[num_cols].isnull().sum(),
        "欠損率": (df[num_cols].isnull().mean() * 100).round(2).astype(str) + "%"
    })
    st.dataframe(num_missing_summary)

    def detect_outliers(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        return outliers, lower, upper

    st.subheader("📦 外れ値の確認（Boxプロット + 数値確認）")
    selected_col = st.selectbox("外れ値を確認する数値列を選択", num_cols)
    outliers, lower, upper = detect_outliers(df[selected_col].dropna())
    fig_box = px.box(df, y=selected_col, points="outliers", title=f"{selected_col} のBoxプロット（外れ値表示）")
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown(f"""**外れ値の検出結果（IQR法）**\n- 下限値：{lower:.2f}\n- 上限値：{upper:.2f}\n- 外れ値件数：**{len(outliers)}**""")
    with st.expander("🔍 外れ値一覧を表示"):
        st.dataframe(outliers.reset_index(drop=True).to_frame(name=selected_col))


#カテゴリ値確認
st.subheader("🔤 カテゴリ概要")
if len(cat_cols) > 0:
    summary = pd.DataFrame({
        "欠損数": df[cat_cols].isnull().sum(),
        "ユニーク数": df[cat_cols].nunique(),
        "最頻値": df[cat_cols].mode().iloc[0]
    })
    st.dataframe(summary)


#データ加工オプション
st.header("🛠️ データ加工オプション")
st.subheader("🔧 数値型 欠損値・外れ値補完")
num_fill_option = {}
outlier_fill_option = {}
for col in num_cols:
    if df[col].isnull().any():
        num_fill_option[col] = st.selectbox(f"{col} の欠損値補完方法", ["ゼロ埋め", "平均補完", "該当レコードの削除"], key=f"num_fill_{col}")
    

    _, lower, upper = detect_outliers(df[col].dropna())
    if len(df[(df[col] < lower) | (df[col] > upper)]) > 0:
        outlier_fill_option[col] = st.selectbox(f"{col} の外れ値補完方法（IQR外）", ["補完しない", "ゼロ埋め", "平均補完", "該当レコードの削除"], key=f"outlier_fill_{col}")
    


st.subheader("🧩 カテゴリ変数 欠損補完")
cat_fill_option = {}
for col in cat_cols:
    if df[col].isnull().any():
        cat_fill_option[col] = st.selectbox(f"{col} の欠損値補完方法", ["最頻値で補完", "不明で補完", "該当レコードの削除"], key=f"cat_fill_{col}")
    

st.subheader("🔁 カテゴリ変数のエンコーディング設定")
target_col = st.session_state.get("target_col", None)
id_like_cols = [col for col in cat_cols if "id" in col.lower()]
excluded_cols = set(id_like_cols)
if target_col:
    excluded_cols.add(target_col)
cat_target_cols = [col for col in cat_cols if col not in excluded_cols]
cat_encoding_option = {}
for col in cat_cols:
    if col in excluded_cols:
        st.markdown(f"🛑 {col} はIDまたは目的変数のため変換対象外です。")
    else:
        method = st.selectbox(f"{col} の変換方法", ["One-hotエンコーディング", "ラベルエンコーディング", "変換しない"], key=f"cat_enc_{col}")
        if method != "変換しない":
            cat_encoding_option[col] = method

if st.button("🚀 加工を実行して次ページへ"):
    transformed_df = df.copy()
    for col, method in num_fill_option.items():
        if method == "ゼロ埋め":
            transformed_df[col] = transformed_df[col].fillna(0)
        elif method == "平均補完":
            transformed_df[col] = transformed_df[col].fillna(transformed_df[col].mean())
        elif method == "該当レコードの削除":
            transformed_df = transformed_df[transformed_df[col].notna()]
    for col, method in outlier_fill_option.items():
        outliers, lower, upper = detect_outliers(transformed_df[col].dropna())
        if method == "ゼロ埋め":
            transformed_df.loc[(transformed_df[col] < lower) | (transformed_df[col] > upper), col] = 0
        elif method == "平均補完":
            transformed_df.loc[(transformed_df[col] < lower) | (transformed_df[col] > upper), col] = transformed_df[col].mean()
        elif method == "該当レコードの削除":
            transformed_df = transformed_df[(transformed_df[col] >= lower) & (transformed_df[col] <= upper)]
    for col, method in cat_fill_option.items():
        if method == "最頻値で補完":
            transformed_df[col] = transformed_df[col].fillna(transformed_df[col].mode().iloc[0])
        elif method == "不明で補完":
            transformed_df[col] = transformed_df[col].fillna("不明")
        elif method == "該当レコードの削除":
            transformed_df = transformed_df[transformed_df[col].notna()]
    for col, method in cat_encoding_option.items():
        if method == "ラベルエンコーディング":
            le = LabelEncoder()
            transformed_df[col] = le.fit_transform(transformed_df[col].astype(str))
        elif method == "One-hotエンコーディング":
            dummies = pd.get_dummies(transformed_df[col], prefix=col)
            transformed_df = pd.concat([transformed_df.drop(columns=col), dummies], axis=1)
    st.session_state["transformed_df"] = transformed_df
    st.switch_page("pages/transform.py")
