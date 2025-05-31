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

## 📁 フォルダ構成（説明付きで親切に）
```
Streamlit_ML_Preprocessing/
├── main.py                # アプリの起点。CSVアップロードや画面遷移を管理
├── pages/
│   ├── transform.py       # データ型の変換・欠損値補完ページ
│   └── stats.py           # 統計量・ヒートマップ表示ページ
├── requirements.txt       # インストールすべきパッケージ一覧
├── .gitignore             # venvなどを除外
└── README.md              # 使い方・目的のドキュメント
```
## 🧭 手順まとめ（コピペOK）
### 0. 前提事項
![image](https://github.com/user-attachments/assets/80f4b807-e7dc-4cdf-a5f8-8b628f8be778)

### 1. リポジトリをクローン（事前に新規ディレクトリを指定の上で実行）
```
git clone https://github.com/pomeshiba29/Streamlit_ML_Preprocessing.git
cd Streamlit_ML_Preprocessing
```
### 2. 仮想環境を作成（推奨）
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
### 3. 必要なライブラリをインストール
```
pip install -r requirements.txt
```
### 4. Streamlitアプリを起動
```
streamlit run main.py
```
