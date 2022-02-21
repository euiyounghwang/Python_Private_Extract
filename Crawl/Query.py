# -*- coding: utf-8 -*-

import sys
import json

def elasticsearch_definition_query(query):
    """

    :param query:
    :return:
    """
    # query_string = str(query) \
    #     .replace('/', '\\/') \
    #     .replace(':', ' ') \
    #     .replace('(', '') \
    #     .replace(')', '') \
    #     .replace('\\', '\\\\')

    import re
    Regular_Expression = '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'
    query_string = re.sub(Regular_Expression, '', query)

    return query_string



def json_format_make_query(query_string):
    """
    법무용 공통쿼리변환
    :param query_string:
    :return:
    """
    # query_string = str(query_string).replace("'","\"") \
    #     .replace(",","\",\"").replace("\"\",", "\"," ) \
    #     .replace(",\"", ",").replace(",,", ",\"").replace("\",",",")\
    #     .replace("True", "true")

    query_string = str(query_string).replace("'", "\"") \
        .replace("@", "\",\"") \
        .replace("True", "true")

    # query_string = str(query_string).replace("'", "\"") \
    #     .replace("True", "true")

    # print('json_format_make_query_law', query_string)

    # print('\n\n')
    print('#'*40)
    print(sys._getframe(1).f_code.co_name + "()")
    print('#'*40)
    # parsed = json.loads(query_string)
    # print(json.dumps(parsed, indent=3, sort_keys=True, ensure_ascii=False))

    return query_string


def query_common(startDate, endDate):
    query_string = {
        "_source": [
             "KEY",
            "VERSION",
            "TITLE",
            "MAIL_ID",
            "USER_NO",
            "USER_NAME",
            "INPUTDATE",
            "UPDATED_DATE",
            "COMPANY_CODE",
            "COMPANY_NAME",
            "DEPT_NAME",
            "USER_INFO",
            "SECURITY_LEVEL"
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "INPUTDATE": {
                                "gte": "%s" % startDate,
                                "format": "yyyy-MM-dd||yyyy",
                                "lte": "%s" % endDate
                            }
                        }
                    }
                ]
            }
        }
    }

    return query_string


def jumin_query():
    """

    :return:
    """
    query_string = {
        "track_total_hits": True,
        "_source": [
            "KEY",
            "VERSION",
            "TITLE",
            "MAIL_ID",
            "USER_NO",
            "USER_NAME",
            "INPUTDATE",
            "UPDATED_DATE",
            "COMPANY_CODE",
            "COMPANY_NAME",
            "DEPT_NAME",
            "USER_INFO",
            "SECURITY_LEVEL",
            "ECM_CREATOR_ID"
        ],
        "query": {
            "bool": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "regexp": {
                                    "CONTENT": "[4-9.][0-9.][0-1.][1-9.][0-3.][0-9.][0-3.][0-9.][0-3.][0-9.][0-9.][0-9.][0-9.]"
                                }
                            },
                            {
                                "range": {
                                    "INPUTDATE": {
                                        "format": "yyyy-MM-dd||yyyy",
                                        "gte": "2020-01-01"
                                    }
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "terms": {
                                    "SECURITY_LEVEL": [
                                        "1A",
                                        "2A"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "must": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": "주민등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "주민번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "여권번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "외국인등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "휴대전화번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "연락처",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "신용카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "계좌번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "비밀번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "from": 0,
        "highlight": {
            "order": "score",
            "pre_tags": [
                "<b>"
            ],
            "post_tags": [
                "</b>"
            ],
            "fields": {
                "*": {
                    "number_of_fragments": 0,
                    "type": "unified",
                    "fragment_size": 150
                }
            }
        },
        "docvalue_fields": [
            "CONTENT.truncated"
        ],
        "size": 15
    }

    return json_format_make_query(query_string)


def phone_query():
    """

    :return:
    """
    query_string = {
        "track_total_hits": True,
        "_source": [
            "KEY",
            "VERSION",
            "TITLE",
            "MAIL_ID",
            "USER_NO",
            "USER_NAME",
            "INPUTDATE",
            "UPDATED_DATE",
            "COMPANY_CODE",
            "COMPANY_NAME",
            "DEPT_NAME",
            "USER_INFO",
            "SECURITY_LEVEL",
            "ECM_CREATOR_ID"
        ],
        "query": {
            "bool": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "regexp": {
                                    "CONTENT": "[0-0.][0-1.][0-0.][0-9.][0-9.][0-9.][0-9.][0-9.][0-9.][0-9.][0-9.]"
                                }
                            },
                            {
                                "range": {
                                    "INPUTDATE": {
                                        "format": "yyyy-MM-dd||yyyy",
                                        "gte": "2020-01-01"
                                    }
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "terms": {
                                    "SECURITY_LEVEL": [
                                        "1A",
                                        "2A"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "must": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": "주민등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "주민번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "여권번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "외국인등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "휴대전화번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "연락처",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "신용카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "계좌번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "비밀번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "from": 0,
        "highlight": {
            "order": "score",
            "pre_tags": [
                "<b>"
            ],
            "post_tags": [
                "</b>"
            ],
            "fields": {
                "*": {
                    "number_of_fragments": 1,
                    "type": "unified",
                    "fragment_size": 150
                }
            }
        },
        "docvalue_fields": [
            "CONTENT.truncated"
        ],
        "size": 15
    }

    return json_format_make_query(query_string)


def passport_query():
    """

    :return:
    """
    query_string = {
        "track_total_hits": True,
        "_source": [
            "KEY",
            "VERSION",
            "TITLE",
            "MAIL_ID",
            "USER_NO",
            "USER_NAME",
            "INPUTDATE",
            "UPDATED_DATE",
            "COMPANY_CODE",
            "COMPANY_NAME",
            "DEPT_NAME",
            "USER_INFO",
            "SECURITY_LEVEL",
            "ECM_CREATOR_ID"
        ],
        "query": {
            "bool": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "regexp": {
                                    "CONTENT": "[a-z][a-z][0-9.][0-9.][0-9.][0-9.][0-9.][0-9.][0-9.]"
                                }
                            },
                            {
                                "range": {
                                    "INPUTDATE": {
                                        "format": "yyyy-MM-dd||yyyy",
                                        "gte": "2020-01-01"
                                    }
                                }
                            }
                        ],
                        "must_not": [
                            {
                                "terms": {
                                    "SECURITY_LEVEL": [
                                        "1A",
                                        "2A"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "must": [
                    {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": "주민등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "주민번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "여권번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "외국인등록번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "핸드폰",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "휴대전화번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "연락처",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "신용카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "카드번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "계좌번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "비밀번호",
                                        "type": "phrase",
                                        "lenient": True,
                                        "fields": [
                                            "KEY",
                                            "KEY.keyword",
                                            "TITLE",
                                            "TITLE.nGram",
                                            "TITLE.keyword",
                                            "CONTENT"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "from": 0,
        "highlight": {
            "order": "score",
            "pre_tags": [
                "<b>"
            ],
            "post_tags": [
                "</b>"
            ],
            "fields": {
                "*": {
                    "number_of_fragments": 1,
                    "type": "unified",
                    "fragment_size": 150
                }
            }
        },
        "docvalue_fields": [
            "CONTENT.truncated"
        ],
        "size": 15
    }

    return json_format_make_query(query_string)