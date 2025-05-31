# Streamlit_ML_Preprocessing
Streamlitによる機械学習の前処理（データ加工）ツール

## 📌 概要
本アプリは、CSVデータをアップロードして以下を行えるStreamlitアプリです：

- データ型の自動判定・手動変換
- 欠損値の補完（0埋め・平均補完）
- カテゴリ変数の変換（ラベル・One-hot）
- 統計量の表示とPlotlyによる可視化

## 🖥️ 使用技術
- Python
- Streamlit
- Pandas
- Plotly
- scikit-learn

## 📁 ディレクトリ構成
STREAMLIT_Preprocessing/
├── main.py # ホーム画面（csvアップロード、目的変数指定など）
├── pages/
│ ├── transform.py # データ型変換ページ
│ └── stats.py # 統計量・相関可視化ページ
└── requirements.txt # 必要なパッケージ一覧


## 🚀 使い方
```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate

# パッケージのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run main.py
