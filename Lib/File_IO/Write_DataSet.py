
import json
import os
import re
import ES_Private_Extract.Config.Config as Config

import os

DEFAULT_INPUT_PATH = './OUTPUT/'
os.makedirs(DEFAULT_INPUT_PATH, exist_ok=True)



def Delete_All_Files(prjFolder, file_type):
    """

    :param prjFolder:
    :param file_type:
    :return:
    """
    print('\n# DELETE ALL FILES -> {}, prjFolder -> {}'.format(prjFolder, file_type))

    if not os.path.exists(prjFolder):
        os.mkdir(prjFolder)

    for filename in os.listdir(prjFolder):
        result = re.search(file_type, filename)
        if result:
            os.remove(os.path.join(prjFolder,filename))


def file_write_with_path(list, path, file_name):
    """
    제안 INCRE _source만 저장
    :param list:
    :param path:
    :param file_name:
    :return:
    """

    if list:
        open_output_file = open(path + file_name, 'a', -1, "utf-8")
        # 결과로 쓰일 count.txt 열기
        # .replaceAll("\\s+", " ")
        open_output_file.write('[\n')
        for i in range(len(list)-1):
            open_output_file.write('{},\n'.format(list[i]))

        open_output_file.write('{}\n'.format(list[len(list)-1]))
        open_output_file.write(']')
        # 결과 저장
        open_output_file.close()



# noinspection PyUnusedLocal,PyShadowingBuiltins
def file_write_excel(Columns, list, file_name):
    """
    Excel 형태
    :param list:
    :param file_name:
    :return:
    """

    open_output_file = open(DEFAULT_INPUT_PATH + file_name, 'a', -1, "utf-8")

    loop  = 0

    # print('list -> ', list)
    for token in list:
        dict_result = json.loads(str(token))
        columns = []
        rows = []

        rows = [dict_result[column] for column in Columns]

        # print('rows -> ', rows)
        # print('\t'.join(rows))

        open_output_file.write('\t'.join(rows).replace('2B', '사외비B').replace('3A', '일반') + '\n')

    open_output_file.close()



# noinspection PyUnusedLocal,PyShadowingBuiltins
def file_write_excel_header(Columns, list, file_name):
    """
    Excel 형태
    :param list:
    :param file_name:
    :return:
    """

    open_output_file = open(DEFAULT_INPUT_PATH + file_name, 'w', -1, "utf-8")

    loop  = 0

    # print('list -> ', list)
    open_output_file.write('\t'.join(Columns)+ '\n')

    open_output_file.close()





