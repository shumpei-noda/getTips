import json
import click
from colorama import Fore, Back, Style

@click.command()
@click.argument('col_size', default=0)
@click.argument('row_size', default=0)
@click.argument('ids_file', type=click.File('r'))
def main(col_size, row_size, ids_file):
    num_list = []
    ids_list = json.load(ids_file)
    max_count = 0
    for ids_dict in ids_list:
        num_list += [len(ids_dict)]
        if len(ids_dict) == 50:
            max_count += 1
    sum_id_num = sum(num_list)
    print("取得件数結果")
    for i in range(col_size):
        print('')
        for j in range(row_size):
            color = None
            if num_list[i * row_size + j] == 50:
                color = Fore.LIGHTRED_EX
            else:
                color = Fore.GREEN

            print(color + "{0:2d}".format(num_list[i * row_size + j]), end=' ')
    print('\n')
    color = Fore.BLACK
    print(color + "合計件数",sum_id_num)
    print("平均件数",sum_id_num / len(ids_list))
    print("50件あった範囲の個数",max_count)
    print("取得範囲数",len(ids_list))

if __name__ == '__main__':
    main()
