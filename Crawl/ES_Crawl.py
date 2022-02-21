

import elasticsearch
import time
import os
import re
import datetime
import ES_Private_Extract.Config.Config as Config
import ES_Private_Extract.Crawl.Query as Query
import ES_Private_Extract.Lib.File_IO.Write_DataSet as Write
import ES_Private_Extract.Crawl.ES_Response as ES_FeedBack
import json, copy


def backslash_func(query):
    """

    :param str:
    :return:
    """
    query = str(query).replace("'",  '"')
    query = query.replace('"",', '\\"",')
    query = query.replace('""', '"\\"')
    query = query.replace('\\",', '",')
    query = query.replace("True", "true")

    return query


def start_Crawl_File(call_index, PATH, OPTION):
    """

    :param call_index:
    :param PATH:
    :param OPTION:
    :return:
    """

    from dateutil.relativedelta import relativedelta

    START_DATE = (datetime.date.today() - relativedelta(months=120)).strftime("%Y-%m-%d")
    END_DATE = datetime.date.today().strftime("%Y-%m-%d")

    total_count = 0

    es_client = elasticsearch.Elasticsearch(Config.ElasticsearchConfig().getElasticsearchIP(),
                                            http_auth=('elastic', 'x'),
                                            timeout=600)

    max_page_size = 200

    # ---
    # Query 분기
    # ---
    if str(OPTION).__eq__('JUMIN'):
        query_string = Query.jumin_query()
    elif str(OPTION).__eq__('PHONE'):
        query_string = Query.phone_query()
    elif str(OPTION).__eq__('PASSPORT'):
        query_string = Query.passport_query()


    response = es_client.search(
                                    index=call_index,
                                    body=query_string,
                                    scroll='10m',
                                    size=max_page_size)
    scroll_id = response['_scroll_id']

    # exit(1)

    get_list = {}
    loop = 0

    current_status_number = max_page_size
    get_list = ES_FeedBack.elasticsearch_source_response(response, OPTION)
    date_strng = datetime.datetime.today().strftime("%Y%m%d")

    # ---
    # HEADER
    # ---
    if str(OPTION).__eq__('JUMIN'):
        INPUT_EXCEL_SORT = ['구분', '주민등록번호패턴건수', '외국인등록번호패턴건수', '문서ID', '문서버전', '문서제목', '문서생성자ID', 'MAIL_ID', '직번', '소유자명', '부서명', '문서등급', '문서등록일']
    else:
        INPUT_EXCEL_SORT = ['구분', '문서ID', '문서버전', '문서제목', '문서생성자ID', 'MAIL_ID', '직번', '소유자명', '부서명', '문서등급', '문서등록일']

    Write.file_write_excel_header(INPUT_EXCEL_SORT, get_list, call_index + "_" + OPTION + "_RESULTS")
    # --

    # ---
    # BODY
    # ---
    if str(OPTION).__eq__('JUMIN'):
        OUTPUT_EXCEL_SORT = ['GUBUN', 'JUMIN_TOTAL_CNT', 'FOREIGN_TOTAL_CNT', 'KEY', 'VERSION', 'TITLE', 'ECM_CREATOR_ID', 'MAIL_ID', 'USER_NO', 'USER_NAME', 'DEPT_NAME', 'SECURITY_LEVEL', 'INPUTDATE']
    else:
        OUTPUT_EXCEL_SORT = ['GUBUN', 'KEY', 'VERSION', 'TITLE', 'ECM_CREATOR_ID', 'MAIL_ID', 'USER_NO', 'USER_NAME', 'DEPT_NAME', 'SECURITY_LEVEL', 'INPUTDATE']

    Write.file_write_excel(OUTPUT_EXCEL_SORT, get_list, call_index + "_" + OPTION + "_RESULTS")
    # --

    if get_list:

        # Write 1st
        loop += max_page_size
        # Write.file_write_with_path(get_list, PATH, call_index + "_elasticsearch_results_" + str(time.time()))
        Write.file_write_excel(OUTPUT_EXCEL_SORT, get_list, call_index + "_" + OPTION + "_RESULTS")
        print('\n\nfile_write')
        del get_list[:]

    while 1:
        # print('query',query)
        print('\n\n')
        print('#' * 40)
        print('loop', loop, response['hits']['total'])
        print('#' * 40)
        if loop >= int(response['hits']['total']['value']):
            break

        response = es_client.scroll(scroll_id=scroll_id, scroll='5m')
        scroll_id = response['_scroll_id']
        current_status_number = loop
        print("\n\n\n\n\n")
        get_list = ES_FeedBack.elasticsearch_source_response(response, OPTION)

        if get_list:
            if len(str(' '.join(get_list))) > int(Config.CommonDefine().Scroll_Buffer_MaxSize):
                # Write.file_write_with_path(get_list, PATH, call_index + "_elasticsearch_results_" + str(time.time()))
                Write.file_write_excel(OUTPUT_EXCEL_SORT, get_list, call_index + "_" + OPTION + "_RESULTS")
                print('\n\nfile_write')
                del get_list[:]

        loop += max_page_size

    if get_list:
        print('\n\nremain file_write')
        # Write.file_write_with_path(get_list, PATH, call_index + "_elasticsearch_results_" + str(time.time()))
        Write.file_write_excel(OUTPUT_EXCEL_SORT, get_list, call_index + "_" + OPTION + "_RESULTS")
        del get_list[:]




if __name__ == '__main__':

    INDICS = 'TEST_IDX'

    # ---
    # OUTPUT Directory
    # ---
    DEFAULT_INPUT_PATH = Write.DEFAULT_INPUT_PATH
    os.makedirs(DEFAULT_INPUT_PATH, exist_ok=True)

    Write.Delete_All_Files(DEFAULT_INPUT_PATH, '_elasticsearch_')

    # ---
    # 주민등록번호/외국인등록번호 패턴 체크
    # 핸드폰번호 패턴 체크
    # PASSPORT 패턴 체크
    # ---
    GUBUN = ['JUMIN', 'PHONE', 'PASSPORT']
    for OPTION in GUBUN:
        start_Crawl_File(call_index=INDICS, PATH= DEFAULT_INPUT_PATH, OPTION=OPTION)
