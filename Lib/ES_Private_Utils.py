

import logging
import sys
import os
import warnings
import re

sys.path.append(os.getcwd())

warnings.filterwarnings('ignore')

# logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
# logging.basicConfig(filename='sample.log' , format='%(asctime)s | %(filename)s | %(levelname)s: %(message)s', level=logging.NOTSET)

import ES_Private_Extract.Lib.Utils.Util as Utils
import ES_Private_Extract.Lib.Logging.Custome_Logging as Logging

logger = Logging.Logger()

# JUMIN_COUNT, FOREIGN_COUNT = 0, 0

def JuminNumber_Check(Params) -> bool:
    """

    # 주민등록번호를 입력받아 올바른 주민번호인지 검증하라.
    # 주민번호 : ① ② ③ ④ ⑤ ⑥ - ⑦ ⑧ ⑨ ⑩ ⑪ ⑫ ⑬
    # 합계
    # = 마지막수를 제외한 12자리의 숫자에 2,3,4,5,6,7,8,9,2,3,4,5 를 순서대로 곱산수의 합
    # = ①×2 + ②×3 + ③×4 + ④×5 + ⑤×6 + ⑥×7 + ⑦×8 + ⑧×9 + ⑨×2 + ⑩×3 + ⑪×4 + ⑫×5
    # 나머지 = 합계를 11로 나눈 나머지
    # 검증코드 = 11 - 나머지
    # 여기서 검증코드가 ⑬자리에 들어 갑니다.

    123456 1818123 -> 3 CHECKSUM

    JUMIN_CHECKSUM_L_ARR = [2,3,4,5,6,7]  (주민번호앞자리각각 곱해서 더하고)
    JUMIN_CHECKSUM_R_ARR = [8,9,2,3,4,5]  (주민번호뒷자리-1각각 곱해서 더하고))

    :param str:
    :return:
    """

    JUMIN_STATUS = False
    FOREIGN_STATUS = False

    INPUT = str(Params).replace("-", "")

    if INPUT.__len__() != 13 or not INPUT.isnumeric():
        return False

    # print(Utils.bcolors().BOLD)
    logger.info("# " + JuminNumber_Check.__name__)
    logger.info("INPUT [{}]'s Length : {}".format(INPUT, INPUT.__len__()))

    # ---
    # JUMIN CHECKSUM
    JUMIN_CHECKSUM_L_ARR = [2,3,4,5,6,7]
    JUMIN_CHECKSUM_R_ARR = [8,9,2,3,4,5]
    # ---

    logger.info("-- INPUT's JUMIN LEN SUCCESS")
    L_OPERATOR = INPUT[:6]
    R_OPERATOR = INPUT[6:INPUT.__len__()-1]
    R_OPERATOR_ANSWER = INPUT[-1]
    logger.info("-- JUMIN LEFT : {}, RIGHT : {}".format(L_OPERATOR, R_OPERATOR))

    L_SUM = 0
    for i, each_char in enumerate(L_OPERATOR):
        # print(each_char, JUMIN_CHECKSUM_L_ARR[i])
        L_SUM += int(each_char) * int(JUMIN_CHECKSUM_L_ARR[i])

    print('\n')

    R_SUM = 0
    for i, each_char in enumerate(R_OPERATOR):
        # print(each_char, JUMIN_CHECKSUM_R_ARR[i])
        R_SUM += int(each_char) * int(JUMIN_CHECKSUM_R_ARR[i])

    # ---
    # JUMIN CHECK
    # ---
    JUMIN_FINAL_CHECK_PREDICT = 11 - ((L_SUM + R_SUM) % 11)
    if str(JUMIN_FINAL_CHECK_PREDICT).__len__() > 1:
        JUMIN_FINAL_CHECK_PREDICT = (11 - ((L_SUM + R_SUM) % 11)) % 10

    logger.info("JUMIN CHECK : L_SUM : {}, R_SUM : {} -> {}, CHECKSUM : {}".format(L_SUM, R_SUM, L_SUM + R_SUM, JUMIN_FINAL_CHECK_PREDICT))
    logger.info("R_OPERATOR_ANSWER : {}".format(R_OPERATOR_ANSWER))

    # ---
    # FOREIGN CHECK
    # ---

    FOREIGN_FINAL_CHECK_PREDICT = 13 - ((L_SUM + R_SUM) % 11)
    if str(FOREIGN_FINAL_CHECK_PREDICT).__len__() > 1:
        FOREIGN_FINAL_CHECK_PREDICT = (13 - ((L_SUM + R_SUM) % 11)) % 10

    logger.info("FOREIGN_FINAL_CHECK_PREDICT CHECK : L_SUM : {}, R_SUM : {} -> {}, CHECKSUM : {}".format(L_SUM, R_SUM, L_SUM + R_SUM, FOREIGN_FINAL_CHECK_PREDICT))
    logger.info("R_OPERATOR_ANSWER : {}".format(R_OPERATOR_ANSWER))

    if str(R_OPERATOR_ANSWER).__eq__(str(JUMIN_FINAL_CHECK_PREDICT)):
        JUMIN_STATUS = True

    if str(R_OPERATOR_ANSWER).__eq__(str(FOREIGN_FINAL_CHECK_PREDICT)):
        FOREIGN_STATUS = True

    logger.info("JUMIN RESULT : {}".format("SUCCESS" if str(R_OPERATOR_ANSWER).__eq__(str(JUMIN_FINAL_CHECK_PREDICT)) else "FAIL"))
    logger.info("FOREIGN RESULT : {}".format("SUCCESS" if str(R_OPERATOR_ANSWER).__eq__(str(FOREIGN_FINAL_CHECK_PREDICT)) else "FAIL"))

    # print(Utils.bcolors().ENDC)

    return [JUMIN_STATUS, FOREIGN_STATUS]





def JUMIN_FORGIGN_COUNT(result):
    """

    :param result:
    :return:

    """
    JUMIN_COUNT, FOREIGN_COUNT = 0, 0

    # global JUMIN_COUNT, FOREIGN_COUNT

    if list(result)[0]:
        JUMIN_COUNT += 1

    if list(result)[1]:
        FOREIGN_COUNT += 1

    return JUMIN_COUNT, FOREIGN_COUNT



def Get_Hightlight(INPUT):
    """
    Elasticsearch Each Row HIGHTLIGHT
    :param INPUT:
    :return:
    """

    # logger.info(INPUT)

    # ---
    # <b>주민</b><b>등록</b><b>번호</b> -> 주민등록번호
    # ---
    INPUT = str(INPUT).replace('</b><b>', '')

    print('\n')

    input_text = re.sub(r"\s+", " ", str(INPUT).strip())
    logger.info(input_text)

    print('\n')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(input_text, 'lxml')

    HIGHLIGHT_B = soup.find_all('b')

    # Hash_Key_Highlight = {}
    Hash_Key_Highlight = []
    for row in HIGHLIGHT_B:
        row = str(row).replace('<b>','').replace('</b>','')
        if row.isnumeric():
            # Hash_Key_Highlight.update({row : row})
            Hash_Key_Highlight.append(row)

    logger.info(Hash_Key_Highlight)
    logger.info(Hash_Key_Highlight.__len__())
    # logger.info(Hash_Key_Highlight.keys().__len__())

    print('\n')

    return Hash_Key_Highlight




if __name__ == '__main__':

    JUMIN_COUNT, FOREIGN_COUNT = 0, 0
    JUMIN_TOTAL_CNT, FOREIGN_TOTAL_CNT = 0, 0

    """
    # ---
    # JUMIN CHECKUSUM Boolean
    # JUMIN CHECKSUM : [True, False]
    # [주민번호여부, 외국인등록번호여부]
    # ---
    JUMIN_CNT, FOREIGN_CNT = JUMIN_FORGIGN_COUNT(JuminNumber_Check("1234561212121"))
    logger.info('#JUMIN CHECKSUM : -> JUMIN : {}, FOREIGN : {}'.format(JUMIN_CNT, FOREIGN_CNT))

    JUMIN_TOTAL_CNT += JUMIN_CNT
    FOREIGN_TOTAL_CNT += FOREIGN_CNT

    # ---
    # JUMIN CHECKUSUM Boolean
    # JUMIN CHECKSUM : [False, False]
    # [주민번호여부, 외국인등록번호여부]
    # ---
    JUMIN_CNT, FOREIGN_CNT = JUMIN_FORGIGN_COUNT(JuminNumber_Check("123456-1212121"))
    logger.info('#JUMIN CHECKSUM : -> JUMIN : {}, FOREIGN : {}'.format(JUMIN_CNT, FOREIGN_CNT))

    JUMIN_TOTAL_CNT += JUMIN_CNT
    FOREIGN_TOTAL_CNT += FOREIGN_CNT

    # ---
    # FOREIGN CHECKUSUM Boolean
    # JUMIN CHECKSUM : [False, True]
    # [주민번호여부, 외국인등록번호여부]
    # ---
    JUMIN_CNT, FOREIGN_CNT = JUMIN_FORGIGN_COUNT(JuminNumber_Check("123456-1212121"))
    logger.info('#JUMIN CHECKSUM : -> JUMIN : {}, FOREIGN : {}'.format(JUMIN_CNT, FOREIGN_CNT))

    JUMIN_TOTAL_CNT += JUMIN_CNT
    FOREIGN_TOTAL_CNT += FOREIGN_CNT
    """

    INPUT_HIGHLIGHT = ' 성     명 <b>1234561212121</b>'

    CHECK_HIGHLIGHT = Get_Hightlight(INPUT_HIGHLIGHT)
    # CHECK_HIGHLIGHT = ["1234561212121", "123456-1212121", "123456-1212121"]
    # CHECK_HIGHLIGHT = ['1234561212121', 'aa123', ]

    for each_highlight in CHECK_HIGHLIGHT:
        # print('each_highlight -> ', each_highlight)
        if each_highlight.isnumeric():
            JUMIN_CNT, FOREIGN_CNT = JUMIN_FORGIGN_COUNT(JuminNumber_Check(each_highlight))
            logger.info('#JUMIN CHECKSUM : -> JUMIN : {}, FOREIGN : {}'.format(JUMIN_CNT, FOREIGN_CNT))

            JUMIN_TOTAL_CNT += JUMIN_CNT
            FOREIGN_TOTAL_CNT += FOREIGN_CNT

    # ---
    # TOTAL COUNT
    # ---
    print(Utils.bcolors().BOLD + Utils.bcolors().YELLOW)
    logger.warn('#TOTAL JUMIN COUNT : {}, # TOTAL JUMIN COUNT : {}'.format(JUMIN_TOTAL_CNT, FOREIGN_TOTAL_CNT))
    print(Utils.bcolors().ENDC)
