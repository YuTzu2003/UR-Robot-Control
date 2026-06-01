# UR手臂夾取控制

製作控制UR機械手臂，透過Tkinter製作的GUI控制手臂移動並執行抓取動作。

## 專案功能
- **八向移動控制**：支援前、後、左、右及四個對角線方向的精準移動。
- **自動化抓取流程**：一鍵執行下行、抓取、升起、移動至定點及放開的完整流程。
- **即時狀態回饋**：介面下方會即時顯示當前系統狀態與執行結果。
- **安全邊界檢查**：內建邊界偵測機制，防止手臂超出預設的工作區域。
- **美化圖形介面**：採用現代化簡約風格，具備 24px 大字體，操作直觀清晰。

## 檔案結構
```text
├── main.py              # 程式進入點，啟動 GUI 與心跳偵測
├── gui/                 # 介面相關程式碼
│   └── main_window.py   # Tkinter 主視窗設計與 QSS 樣式
├── control/             # 控制邏輯
│   ├── state_machine.py # 核心狀態機，處理移動與抓取邏輯
│   ├── motion_commands.py # URScript 指令生成器
│   └── rg_control.py    # RG 夾爪控制指令
├── comm/                # 通訊相關
│   └── socket_client.py # 與 UR5 控制器連線的 TCP Socket 用戶端
├── utils/               # 工具程式
│   ├── boundary_checker.py # 邊界偵測邏輯
│   └── logger.py        # 系統日誌記錄
└── config/              # 設定檔
    └── parameters.json  # 系統參數設定
```

### 1. 環境需求
- Python 3.8 或以上版本
- 確保電腦與 UR5 機器手臂處於同一區域網路下

### 2. 安裝必要套件
請在終端機執行以下指令來安裝所需的相依套件：

```bash
pip install Tkinter
pip install pyModbusTCP
```

## 注意事項
- 啟動前請確保機器手臂已解除緊急停止狀態並處於 Remote 控制模式。
- 建議在正式運行前，先透過 `control.ipynb` 進行基礎連線與移動測試。