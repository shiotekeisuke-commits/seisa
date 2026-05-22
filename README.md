# MCL Dashboard

Google Sheets からのリアルタイム自動更新ダッシュボード

## 概要

- **自動更新**: GitHub Actions で毎時間 Google Sheets からデータ取得
- **リアルタイム**: 変更があれば自動的に web サイトに反映
- **Web公開**: GitHub Pages で無料ホスト
- **URL**: https://shiotekeisuke-commits.github.io/seisa/

## ファイル構成

```
.
├── index.html              # ダッシュボード
├── data.json               # 自動生成されるデータ
├── scripts/
│   └── update_data.py      # 更新スクリプト
└── .github/workflows/
    └── update-data.yml     # 自動実行設定
```

## 更新スケジュール

- **毎時間 00分**: 自動更新実行
- **手動実行**: GitHub Actions から "Run workflow" をクリック

## トラブルシューティング

- データが更新されない → Actions ページで実行ログを確認
- 接続エラー → Google Sheets の URL が正しいか確認
- ページが表示されない → GitHub Pages が有効化されているか確認

## 更新履歴

自動生成
