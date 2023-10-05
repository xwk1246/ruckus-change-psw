# 一件刷寫Ruckus switch router密碼與設定
## 功能
* 同時大量刷寫200+機器設定
* 以threading提升同時連線數
  
## 使用方式
```
cp .env.example .env
修改.env內欲更改設定
```
```
將裝置資訊匯入
devices.json
```
```
pipenv install
pipenv shell
python main.py
```
