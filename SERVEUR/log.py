import logging
class LOG():
    def __init__(self,FILE_LOG):
        self.FILE_LOG = FILE_LOG

    def start_log(self):
            self.Log_Format = "%(levelname)s %(asctime)s - %(message)s"
            logging.basicConfig(filename = self.FILE_LOG,filemode = "a",format = self.Log_Format)
            self.logger = logging.getLogger()
            # info : debug : info : warning : error : critical 