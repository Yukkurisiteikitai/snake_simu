# プロジェクトガイド：蛇シミュレーション完全版

## 🎉 プロジェクト完成！

「蛇がどうやって前進するのか」をプログラムで再現する、完全な学習プロジェクトが完成しました。

---

## 📦 何が入っているか

### 📚 教育ドキュメント（4ファイル）

| ファイル | 対象 | 時間 | 内容 |
|---------|------|------|------|
| `00_QUICK_START.md` | 全員 | 3分 | 全体像とクイックスタート |
| `01_high_school_math.md` | 数学が怪しい人 | 15分 | sin/cos と波について |
| `02_kinematics_explained.md` | FK を学ぶ人 | 20分 | 関節角→位置の計算 |
| `03_physics_explained.md` | 物理を学ぶ人 | 15分 | 異方性摩擦について |

### 🐍 実装ファイル（2個 + 1個テスト）

| ファイル | 目的 | 特徴 |
|---------|------|------|
| `phase1_basic.py` | 基本実装 | 蛇がくねくね（固定位置） |
| `phase2_with_friction.py` | 摩擦追加版 | 蛇が前進する！ |
| `test_phase1.py` | テスト | matplotlib なしで動作確認 |

### 🧩 モジュール（3個）

| ファイル | 役割 | 主な関数 |
|---------|------|---------|
| `components/cpg.py` | 脳（筋肉活動生成） | `get_muscle_activation()` |
| `components/kinematics.py` | 関節→位置 | `forward_kinematics()` |
| `components/friction.py` | 摩擦→前進 | `compute_friction_forces()` |

### 📖 参考ドキュメント（3ファイル）

| ファイル | 内容 |
|---------|------|
| `README.md` | プロジェクト概要 |
| `IMPLEMENTATION_SUMMARY.md` | 実装の詳細（開発者向け） |
| `QUICK_REFERENCE.md` | よく使うコード（リファレンス） |

### 🧪 実験スクリプト（3ファイル）

| ファイル | 内容 |
|---------|------|
| `examples/example_slow_undulation.py` | ゆっくり動く蛇 |
| `examples/example_fast_undulation.py` | 速く動く蛇 |
| `examples/example_friction_effect.py` | 摩擦係数の効果 |

---

## 🚀 今すぐ始める

### 1. インストール（1分）

```bash
cd /Users/yuuto/lab/snake_simulastion
pip install matplotlib numpy
```

### 2. テスト実行（1分）

```bash
python3 test_phase1.py
```

**出力**：「✓ Phase 1 テスト成功！」と表示されたら OK

### 3. Phase 1 実行（2分）

```bash
python3 phase1_basic.py
```

**見えること**：30個の関節を持つ蛇が、固定位置でくねくね動く

### 4. Phase 2 実行（2分）

```bash
python3 phase2_with_friction.py
```

**見えること**：同じ蛇が、摩擦のおかげで **右へ前進する！**

---

## 📚 学習パス（推奨順序）

### レベル1：全体像を把握（10分）

```bash
cat 00_QUICK_START.md       # 全体像
python3 test_phase1.py      # 動作確認
python3 phase1_basic.py     # 見て確認
```

### レベル2：数学を理解（30分）

```bash
cat 01_high_school_math.md  # sin/cos を学ぶ
cat 02_kinematics_explained.md
cat 03_physics_explained.md
```

コード内のコメントも読む：
```bash
head -50 components/cpg.py
head -50 components/kinematics.py
```

### レベル3：コードを読む（30分）

```bash
# 各モジュールを読む
cat components/cpg.py
cat components/kinematics.py
cat components/friction.py

# Phase 1 の実装を読む
cat phase1_basic.py

# Phase 2 の実装を読む
cat phase2_with_friction.py
```

### レベル4：実験する（自由）

```bash
# 実験スクリプトを実行
python3 examples/example_slow_undulation.py
python3 examples/example_fast_undulation.py
python3 examples/example_friction_effect.py

# パラメータを変えて実験
# エディタで例を編集 → 実行 → 観察 → 修正
```

---

## 🎯 各ファイルの読む順序

### 最小限バージョン（30分）

```
1. 00_QUICK_START.md       ← ここから始める
2. test_phase1.py          ← 動作確認
3. phase1_basic.py         ← 実行して見る
4. phase2_with_friction.py ← 実行して見る
完！
```

### 標準バージョン（2時間）

```
1. 00_QUICK_START.md
2. 01_high_school_math.md          ← 数学を理解
3. 02_kinematics_explained.md      ← FK を理解
4. 03_physics_explained.md         ← 物理を理解
5. phase1_basic.py                 ← コードを読む
6. components/cpg.py               ← モジュール読む
7. components/kinematics.py
8. components/friction.py
9. phase2_with_friction.py
完！
```

### 詳細バージョン（4時間）

```
上記に加えて：
- IMPLEMENTATION_SUMMARY.md  ← 実装の詳細
- QUICK_REFERENCE.md         ← リファレンス
- examples/ のスクリプト      ← 実験
- パラメータを変えて実験
完！
```

---

## 💡 学習ポイント

### プログラミング

✅ **モジュール設計**
- 複雑な問題を小さな部品（CPG → 筋肉 → FK → 摩擦）に分ける
- 各部品の責任を明確に

✅ **可視化**
- matplotlib でアニメーション作成
- リアルタイムデータの表示

✅ **テスト駆動**
- 単体テスト（各モジュールの確認）
- 統合テスト（全体の動作確認）

### 数学

✅ **三角関数（sin/cos）**
- 周期的な波を作る
- 角度から位置を計算

✅ **ベクトル**
- 方向と大きさを表現
- 力の分解（前後・左右）

✅ **力学**
- F = ma（ニュートン第2法則）
- 摩擦の効果

### 生物学・神経科学

✅ **神経制御**
- 脳からの指令がどう体を動かすか
- CPG（Central Pattern Generator）の役割

✅ **筋肉**
- 活性度から力が生まれる
- 左右の筋肉の協調

✅ **ロコモーション**
- 蛇行の物理的仕組み
- 環境との相互作用

---

## 🔬 各フェーズの目的

### Phase 1: 基本を理解する

**目標**：CPG → 筋肉 → 関節角 → FK のフロー理解

**コード**：`phase1_basic.py`

**学べること**：
- 波をプログラムで作れる
- 角度から位置が計算できる
- 30個の関節が協調して蛇の形を作る

**制限**：
- 蛇の頭が固定（移動しない）
- 摩擦がない（物理的に現実的でない）

### Phase 2: 物理を追加する

**目標**：異方性摩擦から前進が生まれることを理解

**コード**：`phase2_with_friction.py`

**学べること**：
- 横方向の摩擦が大きいことで、横への動きが打ち消される
- 結果として前後への動きだけが残り、前進する
- これが蛇行による移動の物理

**特徴**：
- 蛇が実際に移動する
- 視覚的に「前進」が見える
- 摩擦係数の効果を実感できる

### Phase 3 以降（未実装）

**案**：
- 筋肉の詳細モデル（Hill型）
- 関節のトルク計算
- 環境の複雑化（障害物など）
- 3D への拡張
- 学習・最適化

---

## 🎓 これで学べる教科・スキル

| 分野 | 学べること | ファイル |
|------|-----------|---------|
| 数学 | sin/cos、ベクトル、力学 | `01_high_school_math.md` など |
| 物理 | 力学、摩擦、エネルギー | `03_physics_explained.md` |
| プログラミング | モジュール設計、可視化 | `phase1_basic.py` など |
| 神経科学 | CPG、筋肉制御 | `components/cpg.py` |
| ロボティクス | FK、制御、環境相互作用 | `phase2_with_friction.py` |
| 生物学 | 蛇行のメカニズム | `03_physics_explained.md` |

---

## 🧪 実験アイデア

### 1. パラメータを変えてみる

```python
# fast_snake.py を作って：
simulator.frequency = 5.0  # 高速
simulator.wavelength = 2.0  # 短波
```

**観察**：蛇がどうなる？

### 2. 関節数を変える

```python
# 小さな蛇
simulator = SnakeSimulatorPhase2(num_joints=10)

# 大きな蛇
simulator = SnakeSimulatorPhase2(num_joints=60)
```

**観察**：移動速度は？見た目は？

### 3. 摩擦係数を変える

```python
# 摩擦が小さい（滑りやすい）
simulator.c_lateral = 5.0

# 摩擦が大きい（滑りにくい）
simulator.c_lateral = 20.0
```

**観察**：前進速度は？

### 4. グラフを追加

Phase 2 のコードを修正して：
- 速度の時系列
- 加速度
- エネルギー効率

を計算・表示

---

## 🐛 トラブルシューティング

### 問題：`ImportError: No module named 'matplotlib'`

**解決**：
```bash
pip install matplotlib numpy
```

### 問題：蛇が動かない（Phase 1 は見えるのに Phase 2 で動かない）

**原因**：摩擦係数が等方的

**解決**：
```python
assert simulator.c_lateral > simulator.c_forward
# OK: c_lateral=10, c_forward=1
# NG: c_lateral=1, c_forward=1
```

### 問題：アニメーションが遅い

**原因**：matplotlib は遅い

**対策**：
- `interval` を増やす（フレームスキップ）
- より高速な描画ライブラリを使う（pygame など）

### 問題：理論と実装が一致しない

**デバッグ**：
1. `test_phase1.py` を実行
2. 各ステップの出力を確認
3. 単体テストを追加

---

## 📊 プロジェクト統計

| 項目 | 値 |
|------|-----|
| 総ファイル数 | 13 |
| コード行数 | ~1500 |
| ドキュメント行数 | ~2500 |
| 教育ドキュメント数 | 4 |
| モジュール数 | 3 |
| 実装数 | 2 |
| テストスクリプト | 1 |
| 実験スクリプト | 3 |

---

## ✨ 特徴

### 🎓 教育的

- 高校数学で理解可能
- ステップバイステップで学べる
- 実装とドキュメントが対応

### 🏗️ よく設計

- モジュール間の責任が明確
- 各部品が独立して動作
- テスト可能な設計

### 🚀 拡張可能

- Phase 3 への道が見える
- 各部品を置き換え可能
- 新しい機能を足しやすい

### 👁️ ビジュアル

- アニメーションで原理が直感的に理解できる
- グラフで時系列データを表示
- デバッグが容易

---

## 🎯 完成チェックリスト

実装が完了した項目：

- ✅ CPG（脳）の実装
- ✅ 筋肉モデル（活性度分割）
- ✅ 関節角計算
- ✅ 順運動学（FK）
- ✅ 異方性摩擦モデル
- ✅ Phase 1（固定位置版）
- ✅ Phase 2（移動版）
- ✅ ビジュアライゼーション
- ✅ テストスクリプト
- ✅ 高校数学ドキュメント（sin/cos）
- ✅ FK 解説ドキュメント
- ✅ 物理解説ドキュメント
- ✅ 実装詳細ドキュメント
- ✅ クイックスタート
- ✅ クイックリファレンス

---

## 🚀 次のステップ

### 短期（1時間）

1. Phase 1 を実行して理解
2. Phase 2 を実行して感動
3. ドキュメントを読んで理論を学ぶ

### 中期（1週間）

1. コードを全部読む
2. パラメータを変えて実験
3. 新しい例を書く

### 長期（1ヶ月）

1. Phase 3 を実装（筋肉の詳細モデル）
2. 3D 版を作る
3. 学習・最適化を追加

---

## 📞 質問・サポート

各ドキュメントを読んでも不明な点は：

1. `IMPLEMENTATION_SUMMARY.md` で実装の詳細を確認
2. `QUICK_REFERENCE.md` でコード例を確認
3. コード内のコメント・docstring を読む
4. `test_phase1.py` でテストして動作確認

---

## 🎉 最後に

このプロジェクトを完了したら、こう思えるはずです：

> **「蛇がなぜ前進するのか、物理とプログラムで完全に説明できる」**

では、始めましょう！

```bash
python3 phase1_basic.py  # ← ここからスタート！
```
