# PerliteRation_and\Nodularity.py

## 概要

**PerliteRation_and_Nodularity.py**は、球状黒鉛鋳鉄品（FCD）の組織画像について、パーライト面積率や黒鉛球状化率（JIS G5502-2022 球状黒鉛鋳鉄品のISO法およびJIS法による）を求めるプログラムです。ここでは、組織画像は下図のように黒鉛とパーライトの両方が見られるものをいいます。
<br><br>

![28233843](https://github.com/repositoryfiles/PerliteRatio_and_Nodularity/assets/91704559/7cbe9919-eb64-4e36-8328-ec1f6a0f9e55)

<br>
図 球状黒鉛鋳鉄品の組織画像（エッチング済み）
<br><br>

## 動作環境

**PerliteRation_and_Nodularity.py**は、[Python](https://www.python.jp/)がインストールされたパソコンで動作します。このプログラムの実行には、画像処理のライブラリ[OpenCV](https://opencv.org/)が必要です。
<br><br>

## 使い方

1. **PerliteRatio_and_Nodularity.py**を適当なフォルダに置きます。
2. **PerliteRatio_and_Nodularity.py**の10行目以降を設定します。
- **miniGraSize**には、認識させたい黒鉛やパーライトの最小サイズを設定します。最小サイズ/画像の幅　のように数式でも、最小サイズ/画像の幅の計算値でも、どちらで設定してもOKです。
- **maxGraSize**には、黒鉛と認識させたい最大サイズを設定します。miniGraSizeと同様、数式でも、数値でも、どちらで設定してもOKです。
- **Width**には、#画像処理およびwindowに出力される画像の幅の初期値を設定します。
- **Height=0**ここは変更しないでください。Heightという変数を定義しているだけです。
- **iDir**はダイアログ「画像ファイルを選んでください」で最初に表示させたいフォルダを設定します。

3. 上記2.の**iDir**に設定したフォルダにSample_A～Cのような組織画像を格納して**PerliteRation_and_Nodularity.py**を実行します。
**PerliteRation_and_Nodularity.py.py**と組織画像は全角文字を含まないフォルダに格納してください。
4. プログラムを実行すると最初にダイアログ「画像ファイルを選んでください」が表示されるので、調べたい組織画像を選択します。少し待つと、windowが二つ表示されます。二つのwindowは重なっているかもしれません。その場合は並べて表示させてください。windowの一つは読み込まれた元画像（**Original**）、もう一つはパーライトと黒鉛が水色と赤色に塗分けられた画像（**Result**）です。Resultの黒鉛とパーライトの塗分けは、**maxGraSize**で定義されたサイズで行われています。<br>
一方、コンソールには<br>
All : 9.22e+05, Perlite : 3.15e+05, Graphite : 3.63e+04, Ferrite : 5.7e+05<br>
Perlite area ratio (%) : 35.6<br>
Graphite area : 3.94 %<br>
Spheroidal graphite iron castings, ISO: 66.35%, JIS: 67.76%<br>
のように、画素数、パーライト面積率、黒鉛面積率、黒鉛球状化率が表示されます。
5. **Original**を見ながら、**Result**の黒鉛とパーライトの塗分けを修正します。黒鉛と分類されている部分をパーライトにしたい場合は、そこをクリックすると瞬時に変更されます。パーライトを黒鉛にしたい場合も同様です。これに伴い、コンソールの表示されているパーライト面積率や黒鉛球状化率の値も更新されます。windowに表示されている画像については、いつでも保存できます。
6. どちらかの画像を閉じるか、任意のキーを押すと、プログラムは終了します。終了方法は、プログラムの最後の部分を書き換えれば変更できます。

## ご利用に関して
- このプログラムでは、組織画像中のパーライトと黒鉛を画像処理によって輪郭として抽出しているため、黒鉛とパーライトが接触している組織画像ではパーライトと黒鉛を抽出できません。
- 組織画像を見て黒鉛とパーライトを識別できない方は、このプログラムのご利用は難しいと思います。
- ご利用結果について当方は責任は負いません。

## 開発環境
- Windows11
- VSC 1.85.2
- Python 3.9.18
- OpenCV 4.5.0
