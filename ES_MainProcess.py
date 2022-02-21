
import os
import sys

# ---
# Command에서 실행할경우, 아래 경로 맞추어야함
# ---
sys.path.append('/ES/')

import ES_Private_Extract.Lib.File_IO.Write_DataSet as Write
import ES_Private_Extract.Crawl.ES_Crawl as Crawl



if __name__ == '__main__':

    INDICS = 'TEST_IDX'

    # ---
    # OUTPUT Directory
    # ---
    # DEFAULT_INPUT_PATH = '/ES/ES_Private_Extract/Crawl/OUTPUT/'
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
        Crawl.start_Crawl_File(call_index=INDICS, PATH= DEFAULT_INPUT_PATH, OPTION=OPTION)