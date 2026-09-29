# インストールガイド

このプロジェクトを環境構築する方法を説明します。

---

## クイックスタート（2分）

### 1. 依存関係をインストール

```bash
pip install -r requirements-minimal.txt
```

または、個別インストール：

```bash
pip install matplotlib numpy
```

### 2. テスト実行

```bash
python3 test_phase1.py
```

### 3. Phase 1 を実行

```bash
python3 phase1_basic.py
```

完了！🎉

---

## 詳細なインストール

### 前提条件

- **Python**: 3.7 以上
- **pip**: パッケージマネージャー

確認方法：

```bash
python3 --version
pip --version
```

### 方法1：最小限の依存関係（推奨）

```bash
# 最小限のパッケージだけインストール
pip install -r requirements-minimal.txt
```

**含まれるもの**：
- matplotlib（ビジュアライゼーション）
- numpy（数値計算）

**実行可能**：
- Phase 1
- Phase 2
- テストスクリプト
- 実験スクリプト

### 方法2：完全な依存関係

```bash
# 開発・テスト用パッケージも含める
pip install -r requirements.txt
```

**追加で含まれるもの**：
- pytest（テスト）
- black（コードフォーマッター）
- flake8（リンター）
- sphinx（ドキュメント生成）

---

## 仮想環境での実行（推奨）

### venv を使う場合

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows

# 依存関係をインストール
pip install -r requirements-minimal.txt

# 実行
python3 phase1_basic.py

# 終了時
deactivate
```

### conda を使う場合

```bash
# 環境を作成
conda create -n snake-sim python=3.9

# 環境を有効化
conda activate snake-sim

# 依存関係をインストール
pip install -r requirements-minimal.txt

# 実行
python3 phase1_basic.py

# 終了時
conda deactivate
```

---

## トラブルシューティング

### Q: `ModuleNotFoundError: No module named 'matplotlib'`

**原因**：matplotlib がインストールされていない

**解決**：
```bash
pip install matplotlib
```

### Q: `ModuleNotFoundError: No module named 'numpy'`

**原因**：numpy がインストールされていない

**解決**：
```bash
pip install numpy
```

### Q: `python3: command not found`

**原因**：Python 3 がインストールされていない

**解決**：
- macOS: `brew install python3`
- Ubuntu/Debian: `sudo apt install python3`
- Windows: python.org からダウンロード

### Q: `pip: command not found`

**原因**：pip がインストールされていない

**解決**：
```bash
python3 -m pip install --upgrade pip
```

### Q: バージョンが古い

**確認**：
```bash
pip show matplotlib numpy
```

**アップグレード**：
```bash
pip install --upgrade matplotlib numpy
```

---

## 動作確認

インストール後、以下が動作すれば OK：

### テスト1：モジュールのインポート

```bash
python3 -c "import matplotlib; print('✓ matplotlib OK')"
python3 -c "import numpy; print('✓ numpy OK')"
python3 -c "from components.cpg import get_muscle_activation; print('✓ CPG module OK')"
```

### テスト2：Phase 1 の非ビジュアル版

```bash
python3 test_phase1.py
```

**出力**：
```
============================================================
Phase 1: テスト実行
============================================================
...
✓ Phase 1 テスト成功！
```

### テスト3：Phase 1 のビジュアル版

```bash
python3 phase1_basic.py
```

**見えること**：ウィンドウが開いて蛇がアニメーション

### テスト4：Phase 2

```bash
python3 phase2_with_friction.py
```

**見えること**：蛇が移動しながらアニメーション

---

## 開発環境の構築（オプション）

コードを編集・開発する場合：

### コードフォーマッター（black）のインストール

```bash
pip install black
```

**使用方法**：
```bash
black phase1_basic.py
```

### リンター（flake8）のインストール

```bash
pip install flake8
```

**使用方法**：
```bash
flake8 phase1_basic.py
```

### テストフレームワーク（pytest）のインストール

```bash
pip install pytest
```

**使用方法**：
```bash
pytest test_phase1.py
```

---

## IDE での開発

### VS Code

**推奨拡張機能**：
1. Python（Microsoft）
2. Pylance
3. Black Formatter
4. Flake8

**インストール方法**：
- VS Code の拡張機能パネルで検索 → インストール

### PyCharm

**推奨設定**：
1. Preferences → Project → Python Interpreter
2. 仮想環境を選択
3. 依存関係が自動的に認識される

### Vim/Neovim

**セットアップ**：
```bash
pip install black flake8 pylsp-black pylsp
```

---

## アップグレード

### すべてを最新版にする

```bash
pip install --upgrade -r requirements.txt
```

### 特定パッケージだけアップグレード

```bash
pip install --upgrade matplotlib
pip install --upgrade numpy
```

---

## アンインストール

### プロジェクト用パッケージをすべて削除

```bash
pip uninstall -r requirements.txt -y
```

### 仮想環境を削除

```bash
# venv の場合
rm -rf venv

# conda の場合
conda remove --name snake-sim --all
```

---

## 動作確認チェックリスト

インストール完了後のチェック：

- [ ] Python 3.7以上がインストールされている
- [ ] `pip install -r requirements-minimal.txt` が成功した
- [ ] `python3 test_phase1.py` が「✓ テスト成功」を出力
- [ ] `python3 phase1_basic.py` でアニメーションが見える
- [ ] `python3 phase2_with_friction.py` で蛇が移動する

すべてチェック完了したら、プロジェクトの準備完了です！🎉

---

## サポート

問題が発生した場合：

1. **エラーメッセージを読む** — Python は詳しいエラーを出す
2. **requirements を確認** — `pip list` で何がインストール済みか確認
3. **テストを実行** — `python3 test_phase1.py` で各モジュール確認
4. **ドキュメント読む** — `01_high_school_math.md` など

---

## Python のバージョン互換性

| Python | サポート | 状態 |
|--------|---------|------|
| 3.11+ | ✅ | 推奨 |
| 3.10 | ✅ | 推奨 |
| 3.9 | ✅ | サポート |
| 3.8 | ✅ | サポート |
| 3.7 | ⚠️ | 最小限 |
| 3.6以下 | ❌ | 非サポート |

---

では、インストールを始めてください！

```bash
pip install -r requirements-minimal.txt
python3 phase1_basic.py
```
