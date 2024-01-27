# coding: utf-8
import cv2
import tkinter
from tkinter import filedialog
import sys
import io
import math

#環境設定
miniGraSize=15/880 #（認識させる黒鉛最小サイズ）/（画像の幅）　これより小さい粒は評価に用いない
maxGraSize=60/880 #（認識させる黒鉛最大サイズ）/（画像の幅）　初期状態において、これより大きい粒はパーライトと認識させる
Width=640#画像処理および出力時の画像の幅
Height=0#画像処理および出力時の画像の高さの初期値（プログラム中で元画像の縦横比から計算）
iDir='c:/Data'#画像ファイルが格納されているフォルダ
marumi_ratio = 0.6 #黒鉛球状化率の算出で用いる丸み係数

#マウスの操作があるとき呼ばれる関数
#パーライトをクリックしたら黒鉛に変換し、黒鉛をクリックしたらパーライトに変換する
def callback(event, x, y, flags, param):
    global contours, contours_p, contours_g

    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(x, y) #ウィンドウ内の座表示を表示(x=0～639, y=0～479)
        #パーライトがクリックされたか調べ、クリックされたなら黒鉛に変換する
        flag = 0
        for e, cnt in enumerate(contours_p):
            if cv2.pointPolygonTest(cnt, (x, y), False) >= 0:
                contours_g.append(contours_p[e])
                del contours_p[e]
                #print('delete perlite')
                draw_result()
                #ここまでのif文の命令を実行したら、次のfor文は実行しないようflagを立てる
                flag = 1

        #黒鉛がクリックされたか調べ、クリックされたならパーライトに変換する
        if flag == 0:
            for e, cnt in enumerate(contours_g):
                if cv2.pointPolygonTest(cnt, (x, y), False) >= 0:
                    contours_p.append(contours_g[e])
                    del contours_g[e]
                    #print('delete graphite')
                    draw_result()

        #黒鉛とパーライトの個数がマウスクリックで変わったことを確認
        #print(f'Graphite : {len(contours_g)}, Perlite : {len(contours_p)}')
        

def draw_result():
    global img_color, img_inv_binary, contours, contours_p, contours_g

    #リサイズ後のimg_colorのクローン
    copy_img_color = img_color.copy()
    
    #輪郭の描画
    cv2.drawContours(copy_img_color, contours_g, -1, (0,0,255), -1)
    cv2.drawContours(copy_img_color, contours_p, -1, (255,255,0), -1)

    #結果の表示
    cv2.imshow('Result', copy_img_color) 

    #全体の画素数
    whole_area = copy_img_color.size
    
    #白部分の画素数
    white_area = cv2.countNonZero(img_inv_binary)

    #黒部分の画素数
    black_area = whole_area - white_area
    
    #黒鉛の画素数
    graphite_area = 0
    #print(len(contours_g))
    for i in range(len(contours_g)):
        graphite_area += cv2.contourArea(contours_g[i])

    #パーライトの画素数
    perlite_area = 0
    #print(len(contours_p))
    for i in range(len(contours_p)):
        perlite_area += cv2.contourArea(contours_p[i])

    #フェライトの画素数
    ferrite_area = whole_area - perlite_area - graphite_area

    #print(f'Perlite : {perlite_area :.3g}, Graphite : {graphite_area :.3g}, Perlite+Graphite : {perlite_area + graphite_area :.3g}')
    print(f'All : {whole_area :.3g}, Perlite : {perlite_area :.3g}, Graphite : {graphite_area :.3g}, Ferrite : {ferrite_area :.3g}')
    print(f'Perlite area ratio (%) : {100 * perlite_area / (ferrite_area + perlite_area) :.3g}')

    # #黒鉛の面積率
    print(f'Graphite area : {100 * graphite_area / whole_area :.3g} %')

    #黒鉛球状化率の算出
    contours1 = []
    contours1 = select_contours(contours_g, Width, Height, miniGraSize)

    sum_graphite_areas = 0
    sum_graphite_areas_5and6 = 0
    num_graphite1 = num_graphite2 = num_graphite3 = num_graphite4 = num_graphite5 = 0

    for i, cnt in enumerate(contours1): 
        graphite_area = cv2.contourArea(cnt)
        sum_graphite_areas += graphite_area
        hull = cv2.convexHull(cnt) # 凸包
        x, y, graphite_radius = get_graphite_length(hull)
        marumi = graphite_area / ((graphite_radius ** 2) * math.pi)

        # ISO法による形状ⅤとⅥの黒鉛判定
        if marumi >= marumi_ratio:
            sum_graphite_areas_5and6 += graphite_area
            #cv2.drawContours(img_color_ISO, contours1, i, (0, 0, 255), -1) #赤色

        # JIS法による形状分類
        if marumi <= 0.2:
            num_graphite1 += 1
            #cv2.drawContours(img_color_JIS, contours1, i, (255, 255, 0), -1) #水色
        if 0.2 < marumi <= 0.4:
            num_graphite2 += 1
            #cv2.drawContours(img_color_JIS, contours1, i, (0, 255, 0), -1) #緑
        if 0.4 < marumi <= 0.7:
            num_graphite3 += 1
            #cv2.drawContours(img_color_JIS, contours1, i, (128, 0, 128), -1) #紫
        if 0.7 < marumi <= 0.8:
            num_graphite4 += 1
            #cv2.drawContours(img_color_JIS, contours1, i, (255, 0, 0), -1) #青
        if 0.8 < marumi:
            num_graphite5 += 1
            #cv2.drawContours(img_color_JIS, contours1, i, (0, 0,255), -1) #赤

    # 球状化率（ISO法）
    nodularity_ISO = sum_graphite_areas_5and6 / sum_graphite_areas * 100
    # 球状化率（JIS法）
    nodularity_JIS = (0.3 * num_graphite2 + 0.7 * num_graphite3 + 0.9 * num_graphite4 + 1.0 * num_graphite5)/ len(contours1) * 100

    print(f'Spheroidal graphite iron castings, ISO: {nodularity_ISO:.2f}%, JIS: {nodularity_JIS:.2f}%')


def select_contours(contours, pic_width, pic_height, min_grainsize):
    contours1 = []
    for e, cnt in enumerate(contours):
        x_rect, y_rect, w_rect, h_rect = cv2.boundingRect(cnt)
        (x_circle, y_circle), radius_circle = cv2.minEnclosingCircle(cnt)
        if int(pic_width * min_grainsize) <= 2 * radius_circle \
            and 0 < int(x_rect) and 0 < int(y_rect) and \
            int(x_rect + w_rect) < pic_width and int(y_rect + h_rect) < pic_height:
            contours1.append(cnt)  
    return contours1

def get_graphite_length(hull):
    max_distance = 0
    for i, hull_x in enumerate(hull):
        for j, hull_y in enumerate(hull):
            if j + 1 < len(hull) and i != j + 1:
                dis_x = hull[j+1][0][0] - hull[i][0][0]
                dis_y = hull[j+1][0][1] - hull[i][0][1]
                dis = math.sqrt(dis_x**2 + dis_y**2)
                if dis > max_distance:
                    max_distance = dis
                    x = dis_x * 0.5 + hull[i][0][0]
                    y = dis_y * 0.5 + hull[i][0][1]
    return(x, y, max_distance * 0.5)


#画像ファイル選択
root=tkinter.Tk()
root.withdraw()
fTyp = [("jpg", "*.jpg"), ("BMP", "*.bmp"), ("png", "*.png"), ("tiff", "*.tif")] 
fname=filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir) 

#画像ファイルを選ばなかったときの処理（プログラム終了）
if fname == "":
    sys.exit()

#画像ファイルの読み込み
#カラーとグレースケールで読み込む
img_color= cv2.imread(fname)
img_gray = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

#画像ファイルのサイズの取得
img_height, img_width = img_gray.shape

#画面に表示させる高さの計算
Height=int(Width*img_height/img_width)

#読み込んだ画像を幅Width、高さHeightにリサイズ
img_color = cv2.resize(img_color, (Width, Height))
cv2.imshow('Original', img_color) 

img_gray = cv2.resize(img_gray, (Width, Height))

#画像のノイズ除去
kernel_size = 3
img_gray  = cv2.blur(img_gray , (kernel_size, kernel_size))

#img_grayを反転二値化してimg_gray_inv_binaryに代入、二値化閾値は大津の二値化を使用
ret, img_inv_binary=cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

contours = []
#contours, hier = cv2.findContours(img_inv_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
contours, hier = cv2.findContours(img_inv_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

contours_p = []
contours_g = []

#最初に定義したminiGraSizeとmaxGraSizeにより、個々のcontourを黒鉛contours_gとパーライトcontours_pに振り分ける
for e, cnt in enumerate(contours):
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    if int(Width * miniGraSize) <= 2 * radius and 2 * radius < int(Width * maxGraSize):
        contours_g.append(cnt) 
    if int(Width * maxGraSize) <= 2 * radius:
        contours_p.append(cnt) 

draw_result()

cv2.setMouseCallback('Result',callback)

# 任意のキーまたは「閉じる」ボタンをクリックするとウィンドウを閉じてプログラムを終了する
while True:
    key = cv2.waitKey(100) & 0xff
    if key != 255 or cv2.getWindowProperty('Result', cv2.WND_PROP_VISIBLE) !=  1 or cv2.getWindowProperty('Original', cv2.WND_PROP_VISIBLE) !=  1:
        break
cv2.destroyAllWindows()
