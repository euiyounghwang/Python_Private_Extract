# -*- coding: utf-8 -*-

import json
import ES_UnCopy_Detection.Config.Config as Config



def data_elastic_raw_json(hit):
   if 'TITLE' in hit['_source']:
        print(hit['_score'], json.dumps(hit['_source']['TITLE'], ensure_ascii=False))
        data = json.loads(json.dumps(hit['_source'], ensure_ascii=False))
        list.append(json.dumps(data, ensure_ascii=False))

   else:
       # print(hit['_score'], json.dumps(hit['_source']['PAGE_PARAM'], ensure_ascii=False))
       # print(hit['_score'], json.dumps(hit['_id'], ensure_ascii=False))
       print(json.dumps(hit['_id'], ",", ensure_ascii=False))
       # data = json.loads(json.dumps(hit, ensure_ascii=False))
       # list.append(json.dumps(data, ensure_ascii=False))
       list.append(hit)


# response['hits']['hits']
# field : elasticsearch 필드명
list = []
def elasticsearch_response(response, current_status_number=0, BUFFER_REMOVE=False):
    """
    elasticsearch에서 scroll 결과 처리
    1) 일반 쿼리에서는 제목 등 쿼리에 있는 항목 + index + type + id 값을 파일로 생성한다.
        index + type + id는 향후 컨텐츠 분석후 Tag 색인을 위해 필요로함
    2) 사전 쿼리에서는 용어사전을 기본으로해서 사전 포맷으로 변경하기 위함
    :param response:
    :return:
    """
    # print("\n\n\n\n\n")
    if BUFFER_REMOVE:
        list.clear()

    num_docs = len(response['hits']['hits'])
    total = response['hits']['total']
    print("{0} docs retrieved".format(num_docs))

    for hit in response['hits']['hits']:
        data_elastic_raw_json(hit)

    return list


def elasticsearch_source_response(response, OPTION, BUFFER_REMOVE=False):
    """

    :param response:
    :param OPTION:
    :param BUFFER_REMOVE:
    :return:
    """
    # print("\n\n\n\n\n")
    if BUFFER_REMOVE:
        list.clear()

    num_docs = response['hits']['total']['value']
    print("\n{0} docs retrieved\n".format(num_docs))
    for hit in response['hits']['hits']:
        print(hit['_score'], json.dumps(hit['_source']['TITLE'], ensure_ascii=False))
        data = json.loads(json.dumps(hit['_source'], ensure_ascii=False))

        # ---
        # JUMIN, FOREIGH, PHONE CHECK
        # ---
        import ES_Private_Extract.Lib.ES_Private_Utils as Private
        print(hit['highlight']['CONTENT'][0])
        CHECK_HIGHLIGHT = Private.Get_Hightlight(hit['highlight']['CONTENT'][0])
        # CHECK_HIGHLIGHT = ["1234561212121", "123456-1212121", "123456-1212121"]

        JUMIN_TOTAL_CNT, FOREIGN_TOTAL_CNT = 0, 0
        if str(OPTION).__eq__('JUMIN'):
            for each_highlight in CHECK_HIGHLIGHT:
                if each_highlight.isnumeric():
                    JUMIN_CNT, FOREIGN_CNT = Private.JUMIN_FORGIGN_COUNT(Private.JuminNumber_Check(each_highlight))
                    JUMIN_TOTAL_CNT += JUMIN_CNT
                    FOREIGN_TOTAL_CNT += FOREIGN_CNT

        data.update({'JUMIN_TOTAL_CNT': str(JUMIN_TOTAL_CNT)})
        data.update({'FOREIGN_TOTAL_CNT': str(FOREIGN_TOTAL_CNT)})
        data.update({'GUBUN': OPTION})

        list.append(json.dumps(data, ensure_ascii=False))

    return list



def elasticsearch_source_file_response(response, current_status_number=0):
    """
    _source Return
    :param response:
    :return:
    """
    num_docs = len(response['hits']['hits'])
    total = response['hits']['total']
    # print("{0} docs retrieved".format(num_docs))
    list = []
    for hit in response['hits']['hits']:
        # print(hit['_score'], json.dumps(hit['_id'], ensure_ascii=False))
        data = json.loads(json.dumps(hit['_source'], ensure_ascii=False))
        list.append(json.dumps(data, ensure_ascii=False))

    return list



################################################
################################################
################################################
# elasticsearch 결과 항목 조회
################################################
################################################
################################################
def elasticsearch_response_print(response):
    print("\n\n\n\n\n")
    num_docs = len(response['hits']['hits'])
    print("{0} docs retrieved".format(num_docs))

    for hit in response['hits']['hits']:
        print(hit['_score'], hit['_source']['TITLE'])