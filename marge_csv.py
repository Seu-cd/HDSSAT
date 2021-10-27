import os

import pandas as pd
import requests

stock_dividend_path = "fy-stock-dividend.csv"
profit_loss_path = "fy-profit-and-loss.csv"
blance_path = "fy-balance-sheet.csv"
dividend_record_path = "国内株配当実績取得ツール_20210420.xlsm"
target_path = "fy-merged-sheet.csv"

csv_urls = [
    "https://f.irbank.net/files/0000/fy-balance-sheet.csv",
    "https://f.irbank.net/files/0000/fy-profit-and-loss.csv",
    "https://f.irbank.net/files/0000/fy-stock-dividend.csv",
]


def download_files(url, file_dir):

    # Web上のファイルデータをダウンロード
    response = requests.get(url)
    # HTTP Responseのエラーチェック
    try:
        response_status = response.raise_for_status()
    except Exception as exc:
        print("Error:{}".format(exc))

    # HTTP Responseが正常な場合は下記実行
    if response_status == None:

        # open()関数にwbを渡し、バイナリ書き込みモードで新規ファイル生成
        file = open(os.path.join(file_dir, os.path.basename(url)), "wb")

        # 各チャンクをwrite()関数でローカルファイルに書き込む
        for chunk in response.iter_content(100000):
            file.write(chunk)

        # ファイルを閉じる
        file.close()
        print("ダウンロード・ファイル保存完了")


def merge_csv():

    for url in csv_urls:
        download_files(url, "")

    blance_data_frame = pd.read_csv(
        blance_path, header=1, usecols=["コード", "年度", "自己資本比率"]
    )
    profit_data_frame = pd.read_csv(
        profit_loss_path, header=1, usecols=["コード", "売上高", "営業利益"]
    )
    stock_data_frame = pd.read_csv(
        stock_dividend_path, header=1, usecols=["コード", "一株配当", "配当性向"]
    )
    dividend_record_data_frame = pd.read_excel(
        dividend_record_path, header=1, usecols=["コード", "連続増配", "減配なし"]
    )

    data_list = [
        blance_data_frame,
        profit_data_frame,
        stock_data_frame,
        dividend_record_data_frame,
    ]

    tmp = data_list[0]
    for data in data_list[1:]:
        tmp = pd.merge(tmp, data, on="コード")
    tmp.to_csv(target_path, index=False, encoding="shift-jis")
