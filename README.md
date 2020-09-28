# AnalogTVLike
png画像をアナログテレビ画面風に加工をするソフト。

# 使用方法
１．exeファイルを実行すると、コンソール画面（黒い画面）とエクスプローラーが開く。

２．加工したい画像を選ぶ。

３．画像が大きすぎる場合リサイズされる。（縦：1920px, 横:1080px以上のとき）

４．ポップアップウィンドウがでてきて、フレームの有り無しを選択。完成画像が表示されるので、確認したらそのウィンドウを閉じて、保存するを選ぶと完成。

５．完成した画像は加工前の画像が入っていたフォルダに出力されるよ。（出力前の画像名_(フレームありだったら、ここに"frame_"がはいる)output.png）

入力画像

![test](https://user-images.githubusercontent.com/56217982/90303722-6025eb00-deeb-11ea-9f9a-800338bba4f2.png)

出力画像（フレームなし）

![no_frame_output](https://user-images.githubusercontent.com/56217982/90303723-61571800-deeb-11ea-9e5c-09e8d66e3876.png)

出力画像（フレームあり）

![frame_output](https://user-images.githubusercontent.com/56217982/90303725-63b97200-deeb-11ea-91ac-67713beb98d6.png)

# setting.txtについて

数字を弄ると各閾値を変更できます。

1行目：ハーフトーン（線みたいなやつ）の濃さが変わる（０～２５５）。ここは小数を入れても切り捨てされる。

2行目：コントラストが変わる。あまり弄らない方がいいかもしれない。小数はOK

3行目：明るさ。明るい方がブラウン管を再現できるけど、やりすぎは白っぽくなってしまうので注意。小数OK

4行目：ガウスぼかしの閾値。お好みで使ってください。目安は0.8～1.8くらい。小数OK

5行目：赤っぽさ。敢えて赤っぽさを強めるために、設定している。気になる人は少し弄ってみるといいかも。小数を入れても切り捨てされる。


数字以外（大文字数字もダメ）は記述しないで。

デフォルト値（弄りすぎたときは、ここからコピペしてね）

153

0.8

1.3

1.3

10

# 注意事項

・自己責任でご使用ください。PCに何か問題が起きても、作者は責任を負いかねます。

・対応している画像（動作確認済み：GIF,PNG,JPG）以外で上手く動作しない場合があります。

・gifアニメにも対応しましたが、完成ビューは出てきません。

・出力先はその画像が存在していた場所に出力されるよ。

・大きい容量のGIFで、原因不明のフリーズが発生することがあるみたいです。実行を終了させて、もう一度起動することで動作は問題なく動きます。


試験的に公開しているバージョンですので、バグ等があれば報告していただけると幸いです。

34mori.nono.0828@Gメール

hira_655362@Twitter

