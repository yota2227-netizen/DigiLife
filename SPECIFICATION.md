# DigiLife 仕様書 (Specification)

## 1. システム構成 (System Architecture)
DigiLifeは、Python (FastAPI) バックエンドと React フロントエンドで構成されるクライアント・サーバー型のアプリケーションです。両者はWebSocketを用いて双方向のリアルタイム通信を行います。

### アーキテクチャ図解
```mermaid
graph LR
    User[ユーザー] -->|操作| Frontend[Frontend (React)]
    Frontend -->|HTTP POST| API[API Endpoints]
    API -->|Action| Model[LifeForm Model]
    
    subgraph Backend (Python/FastAPI)
        Model -->|State Update| Sim[Simulation Loop]
        Sim -->|Decay/Recover| Model
        Sim -->|WebSocket Broadcast| Frontend
    end
    
    Model -->|Search Query| DuckDuckGo[DuckDuckGo API]
    DuckDuckGo -->|Text Content| Model
```

## 2. ディレクトリ構成と役割
### Backend (`/backend`)
- **`main.py`**: アプリケーションのエントリーポイント。FastAPIサーバーの起動、WebSocketエンドポイントの定義、CORS設定を行います。
- **`model.py`**: `LifeForm` クラスを定義。エネルギー、社交性、整合性のデータモデルと、それらを操作するビジネスロジック（`eat`, `talk`, `decay`等）を含みます。
- **`simulation.py`**: `Simulation` クラスを定義。非同期ループを管理し、1秒ごとの減衰処理 (`decay`) と自律行動チェック (`check_and_recover`) を実行し、結果をクライアントにブロードキャストします。

### Frontend (`/frontend`)
- **`src/App.jsx`**: メインUIコンポーネント。WebSocket接続の管理、アプリの状態保持 (`lifeForm` state)、全体のレイアウト定義を行います。
- **`src/components/StatusIndicator.jsx`**: パラメータの数値をプログレスバーとして可視化するコンポーネント。
- **`src/components/ActionPanel.jsx`**: ユーザーが操作するアクションボタン（食事、会話、睡眠）のパネル。
- **`src/components/CharacterDisplay.jsx`**: 現在のパラメータ状態に基づいて、キャラクターの画像（ドット絵）とアニメーションを制御します。
- **`src/components/RetroDevice.jsx`**: SVGフィルターを使用した高精細なレトロゲーム機風のフレームを描画します。

## 3. データモデル詳細 (`backend/model.py`)

### `LifeForm` クラス
PyDanticの `BaseModel` を継承し、以下の状態を管理します。

#### パラメータ
| パラメータ名 | 型 | 範囲 | 説明 |
| :--- | :--- | :--- | :--- |
| `token_balance` | int | 0 - 5000 | エネルギーの実体値（トークン数）。 |
| `social_token_balance` | int | 0 - 3000 | 社交性の実体値（トークン数）。 |
| `energy` | float | 0.0 - 100.0 | `token_balance` から算出される表示用％値。 |
| `social` | float | 0.0 - 100.0 | `social_token_balance` から算出される表示用％値。 |
| `integrity` | float | 0.0 - 100.0 | システム整合性。時間とともに減少。 |

#### 減衰レート (1秒あたり)
- **Energy**: 25 Tokens (約0.5%)
- **Social**: 24 Tokens (約0.8%)
- **Integrity**: 0.3%

#### 統計情報フィールド
ユーザーへのフィードバック用に以下の統計を保持します。
- **Search Stats**: `last_search_keyword`, `last_search_tokens`
- **Talk Stats**: `last_talk_topic`, `last_talk_tokens`
- **Overall**: `total_used_tokens` (Search獲得トークン + Talk消費トークンの合計)

## 4. 通信プロトコル

### WebSocket (`ws://localhost:8000/ws`)
- **方向**: Server -> Client (Broadcast)
- **頻度**: 1秒ごとのループ更新時。
- **初期接続待機**: バックエンド起動後、最初のクライアント接続があるまでシミュレーション（減衰）は開始されません（パラメータ低下の防止）。
- **フォーマット (JSON)**:
  ```json
  {
    "token_balance": 5000,
    "social_token_balance": 3000,
    "last_talk_topic": "デジタル哲学",
    ...
  }
  ```

## 5. アクションとロジック

### 5.1 食事 (Web検索) - `eat()`
- **プロセス**: ランダムキーワードでのWeb検索を実行し、テキスト量に応じて `token_balance` を回復します。
- **統計**: 検索結果のトークン数は `total_used_tokens` に加算されます。

### 5.2 会話 (Talk) - `talk()`
- **プロセス**: 定義済み10種類の話題からランダムに1つ選択し、**500 ~ 1000** の範囲でランダムな量のトークンを `social_token_balance` に加算します。
- **コスト**: エネルギーの10%相当のトークンを消費。
- **統計**: 回復したトークン量は `total_used_tokens` に加算されます。

### 5.3 睡眠 (Sleep) - `sleep()`
- **コスト**: エネルギーの5%相当のトークン。
- **回復量**: Integrity +20.0 (時間をかけて徐々に回復する場合あり)。

### 5.4 自律行動 (Autonomous Recovery)
1. **餓死回避**: Energy < 20% なら即座に `eat()`。
2. **パラメータ維持**: Social < 50% や Integrity < 20% の場合、**現在のエネルギーでコストが支払えるなら** 回復アクションを実行。
3. **予知保全**: 現在の減少スピードから「60秒以内に枯渇する」と予測された場合、事前に `eat()` してエネルギーを蓄える。

## 6. UI / UX 仕様
- **Talk Stats**: 最後の会話トピックと消費トークン数を表示。
- **接続期待機**: フロントエンド接続待ちの間は減衰しないため、アプリ起動直後は常にパラメータ100%から開始されます。
