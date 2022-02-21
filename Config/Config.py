
from pathlib import Path

class CommonPath:

    def __init__(self):

        self.isStartWhichInfra = 'F'

    def get_Root_Directory(self):
        if str(self.isStartWhichInfra).__eq__('T'):
            return '/TOM/ES'
        else:
            return '/ES'



class CommonDefine:
    # ------------------------------
    # -- Server, Local 실행 여부
    # ------------------------------
    # isStartWhichInfra = "T"
    isStartWhichInfra = "F"

    # File Buffer
    Scroll_Buffer_MaxSize = 1024 * 1024 * 20


class ElasticsearchConfig:

    def __init__(self):
        self.ElasticsearchIP = 'x.x.x.x:9200'
        print('\nElasticsearchConfig __init__ => {}'.format(self.ElasticsearchIP))

    def getElasticsearchIP(self):
        return self.ElasticsearchIP

