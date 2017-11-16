import click
import json

LATITUDE_METER = 0.000008983148616  # 1m移動した時の緯度の変化量
LONGITUDE_METER = 0.000010966382364 # 1m移動した時の経度の変化量
LATITUDE_KILOMETER = LATITUDE_METER *  1000     # 1km移動した時の緯度の変化量
LONGITUDE_KILOMETER = LONGITUDE_METER * 1000    # 1km移動した時の経度の変化量
AREA_LIMIT = 10000  # 面積10000km^2が検索上限

# 与えられたパラメータから範囲の分割をする
def get_search_ne_sw(center_latitude, center_longitude, w=1, col_size=10, row_size=10):

    if w * col_size * w * row_size > 10000:
        print("ダメです")
        # 適切なサイズに変換する方法が思い浮かばないので保留
        return
    if w <= 0:
        w = 1

    # 東西南北4方位の緯度経度
    north_latitude = center_latitude + LATITUDE_KILOMETER * ((col_size * w) / 2)
    south_latitude = center_latitude - LATITUDE_KILOMETER * ((col_size * w) / 2)
    east_longitude = center_longitude + LONGITUDE_KILOMETER * ((row_size * w) / 2)
    west_longitude = center_longitude - LONGITUDE_KILOMETER * ((row_size * w) / 2)

    # 分割された一区画の北東(ne)と南東(sw)の緯度経度を格納するリスト
    split_ll_list = [[[] for i in range(int(row_size))] for j in range(int(col_size))]

    for i in range(int(col_size)):
        for j in range(int(row_size)):
            ##四角形の右上端と左下端の緯度経度計算
            # 一区画の右上から左下の緯度経度の変化量
            d_latitude_area = LATITUDE_KILOMETER * w
            d_longitude_area = LONGITUDE_KILOMETER * w

            # 右上(ne)の緯度経度計算
            ne_latitude = north_latitude - (d_latitude_area * i)
            ne_longitude = east_longitude - (d_longitude_area * j)

            # 左下(sw)の緯度経度計算
            sw_latitude = north_latitude - (d_latitude_area * (i + 1))
            sw_longitude = east_longitude - (d_longitude_area * (j + 1))

            # リストに保存していく
            # リストは右上から左下にだんだんと移動していくと考えれば地図と同じ動きになる
            split_ll_list[i][j] += [(ne_latitude, ne_longitude)]
            split_ll_list[i][j] += [(sw_latitude, sw_longitude)]

    return split_ll_list

# 検索パラメータの保存
def save_parameters(ll_list, path):
    parameters = {}
    count = 0
    for ll_row in ll_list:
        for ll_col in ll_row:
            parameter = {}
            parameter['ll'] = str(ll_col[0][0]) + "," + str(ll_col[0][1])
            parameter['ne'] = str(ll_col[0][0]) + "," + str(ll_col[0][1])
            parameter['sw'] = str(ll_col[1][0]) + "," + str(ll_col[1][1])
            parameter['categoryId'] = "4d4b7105d754a06374d81259"
            parameter['intent'] = "browse"
            parameter_set_name = str(count) + "Test"
            parameters[parameter_set_name] = parameter
            count += 1
    parameters_json = json.dumps(parameters, sort_keys=True, ensure_ascii=False, indent=2)
    with open(path, "w") as fh:
        fh.write(parameters_json)
    return

# 指定した範囲を分割して得られたパラメータを標準出力する
def print_parameter(ll_list):
    parameters = []
    for ll_row in ll_list:
        for ll_col in ll_row:
            parameter = {}
            parameter['ll'] = str(ll_col[0][0]) + "," + str(ll_col[0][1])
            parameter['ne'] = str(ll_col[0][0]) + "," + str(ll_col[0][1])
            parameter['sw'] = str(ll_col[1][0]) + "," + str(ll_col[1][1])
            parameter['categoryId'] = "4d4b7105d754a06374d81259"    # 飲食店カテゴリID
            parameter['intent'] = "browse"                          # venueid取得方式
            parameter['limit'] = "50"
            parameters += [parameter]
    parameters_json = json.dumps(parameters, sort_keys=True, ensure_ascii=False, indent=2)

    print(parameters_json)
    return

@click.command()
@click.option('--center_latitude', default=0.0, prompt='center_latitude', help='中心緯度')
@click.option('--center_longitude', default=0.0, prompt='center_longitude', help='中心経度')
@click.option('--width', default=0.0, prompt='width', help='分割幅(縦横同じ、正方形)(col,row sizeよりも大きい値となると適切な値に変更)')
@click.option('--column_size', default=0.0, prompt='column_size', help='最大横幅(最大面積10000km^2)')
@click.option('--row_size', default=0.0, prompt='row_size', help='最大縦幅(最大面積10000km^2)')
def main(center_latitude, center_longitude, width, column_size, row_size):

    # 範囲分割パラメータを与え、その条件で検索範囲の分割を行う
    ll_list = get_search_ne_sw(float(center_latitude),
                               float(center_longitude),
                               float(width),
                               float(column_size),
                               float(row_size))
    # 分割したパラメータを標準出力
    print_parameter(ll_list)

if __name__ == '__main__':
    main()
