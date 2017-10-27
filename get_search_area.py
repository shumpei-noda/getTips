LATITUDE_METER = 0.000008983148616
LONGITUDE_METER = 0.000010966382364
LATITUDE_KILOMETER = LATITUDE_METER * 1000
LONGITUDE_KILOMETER = LONGITUDE_METER * 1000

def get_search_ne_sw(center_latitude, center_longitude, w=1, col_size=10, row_size=10):
    if w > col_size or w > row_size:
        if col_size < row_size:
            w = col_size
        else:
            w = row_size

    # 東西南北4方位の緯度経度
    north_latitude = center_latitude + LATITUDE_KILOMETER * (row_size / 2)
    south_latitude = center_latitude - LATITUDE_KILOMETER * (row_size / 2)
    east_longitude = center_longitude + LONGITUDE_KILOMETER * (col_size / 2)
    west_longitude = center_longitude - LONGITUDE_KILOMETER * (col_size / 2)

    # 行と列の分割数
    n_split_col = col_size / w
    n_split_row = row_size / w

    # 分割された一区画の北東(ne)と南東(sw)の緯度経度を格納するリスト
    split_ll_list = [[[] for i in range(int(n_split_col))] for j in range(int(n_split_row))]

    for i in range(int(n_split_row)):
        for j in range(int(n_split_col)):
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

def main():
    center_latitude = 35.680910
    center_longitude = 139.767025
    ll_list = get_search_ne_sw(center_latitude, center_longitude, w=1, col_size=9, row_size=9)
    save_parameters(ll_list)
if __name__ == '__main__':
    main()
