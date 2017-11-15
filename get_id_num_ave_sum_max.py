import json
import click

@click.command()
@click.argument('ids_file', type=click.File('r'))
def main(ids_file):
    num_list = []
    ids_list = json.load(ids_file)
    max_count = 0
    for ids_dict in ids_list:
        num_list += [len(ids_dict)]
        if len(ids_dict) == 50:
            max_count += 1
    sum_id_num = sum(num_list)

    print("取得件数結果",num_list)
    print("合計件数",sum_id_num)
    print("平均件数",sum_id_num / len(ids_list))
    print("50件あった範囲の個数",max_count)
    print("取得範囲数",len(ids_list))

if __name__ == '__main__':
    main()
