# foursquareからtipsをとってくるやつ

## 概要
foursquareから任意の条件でtipsを取得する

## 使い方
1. get_tips.pyがあるディレクトリに移動する

2. clientIDとclientSecretIDを保存するファイルid.jsonの作成  
`touch token.json`  
で、get_tips.pyと同じディレクトリにtoken.jsonファイルを作成する  
作成したjsonファイル内にclientIDやclient secretIDを  
`{  
  "client_id": "??????????????",
  "client_secret": "?????????????"  
}`  
みたいな感じで書く  

3. 検索パラメータの指定    
`touch example_params.json`  
みたいな感じに適当な名前で適当な場所にjsonファイルを作成する  
作成したjsonファイルに   
`{
  "Tokyo": {
    "near": "Tokyo",
    "radius": "500",
    "categoryId": "4d4b7105d754a06374d81259"
  }
}`  
のような形でパラメータ設定をする  
パラメータを呼び出すためのkey(1つ目の"Tokyo")がtips保存時のファイル名になる  
4. プログラムの実行  
`python3 get_tips.py example_params.json`  
で多分動く
