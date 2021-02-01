
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *
from PyQt5.QtWidgets import *
from ui import decorator
from collections import deque, defaultdict

import time
import sys

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("This is Kiwoom Class")
        self.get_ocx_instance()  # OCX 방식을 파이썬에 사용할 수 있게 변환해 주는 함수
        self.event_slots()  # 키움과 연결하기 위한 시그널 / 슬롯 모음

        self.requestDelayCheck = APIDelayCheck()


    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # 레지스트리에 저장된 api 모듈 불러오기


    ##slot 요청 받을수있는 모음
    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot) ##로그인 요청
        self.OnReceiveTrData.connect(self.on_receive_trdata) ##tr 요청

    ##로그인 에러메시지
    def login_slot(self, errCode):
        if errCode == 0:
            print(errors(errCode))  ##에러코드 출력
        else:
            print(errors(errCode))
        self.login_event_loop.exit()



    #Login 요청 후 서버가 이벤트 발생시킬때까지 대기하는 method

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def on_receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, unused1, unused2, unused3, unused4):
        import kiwoom.tr_receive_handler as tr
        self.latest_tr_data = None

        if sPrevNext == '2':
            self.is_tr_Data = True
        else:
            self.is_tr_Data = False



        if sRQName == "주식일봉차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10081(self, sTrCode, sRQName)

        elif sRQName == "주식주봉차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10082(self, sTrCode, sRQName)

        elif sRQName == "주식월봉차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10083(self, sTrCode, sRQName)

        elif sRQName == "주식년봉차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10094(self, sTrCode, sRQName)

        elif sRQName == "주식분봉차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10080(self, sTrCode, sRQName)

        elif sRQName == "주식틱차트조회요청":
            self.latest_tr_data = tr.tr_receive_opt10079(self, sTrCode, sRQName)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass


    @decorator.call_printer
    def com_rq_data(self, sRQName, sTrCode, sPrevNext, sScrNo):
        '''
        서버에 조회 요청 method, set_input_value method를 호출하여 input 설정
        :param sRQName: tr이름
        :param sTrCode: tr code
        :param sPrevNext: load preveious page
        :param sScrNo: screen number 각 스크린넘버마다 100개 씩 가능
        :return:
        '''
        self.dynamicCall("CommRqData(QString, QString, int, QString)", sRQName, sTrCode, sPrevNext, sScrNo)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        self.requestDelayCheck.checkDelay()





    def get_comm_data(self, sTrCode, sRQName, sindex, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode,sRQName,sindex, item_name)
        return ret.strip()

    '''makret의 모든 종목코드를 서버로부터 가져와 반환 METHOD'''
    def get_code_list_by_market(self, market_code):
        """
        종목 코드 반환
        :param market_code:
        :return:
        """
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)  ###"종목;종목;종목;..."
        code_list = code_list.split(";")[:-1]  ##마지막 빈값 지우기
        return code_list

    '''종목 코드를 가져와 종목이름으로 반환하는 메소드'''
    def get_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    """서버와의 연결 상태를 반환하는 메소드"""
    def get_connect_state(self):
        """서버와의 연결 상태를 반환하는 메소드"""
        ret = self.dynamicCall("GetConnectState()")
        return ret

    '''CommRqData 함수를 통해 서버에 조회 요청시, 요청 이전에 SetInputValue 함수를 몇차례 호출하여 해당쵸엉에 필요한 input 넘겨줘야됨'''
    def set_input_value(self, input_dict):
        for key, val in input_dict.items():
            self.dynamicCall("SetInputValue(QString, QString)", key, val)

    def get_repeat_cnt(self, sTrCode, sRQName):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
        return ret

    '''로그인 할때 계좌정보얻기위한 method'''
    def get_Login_info(self, tag):
        ret =  self.dynamicCall("GetLoginInfo(String)", tag)
        return ret

    '''실투자 OR 모의투자 구분'''
    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret

    '''계좌정보'''


class APIDelayCheck:
    def __init__(self):
        """
        Kiwoom API 요청 제한을 피하기 위해 요청을 지연하는 클래스입니다.

        Parameters
        ----------
        logger:
            Kiwoom Class의 logger, defalut=None
        """
        # 1초에 5회, 1시간에 1,000회 제한
        self.rqHistory = deque(maxlen=1000)

        # if logger:
        #     self.logger = logger

    def checkDelay(self):
        """ TR 1초 5회 제한을 피하기 위해, 조회 요청을 지연합니다. """
        time.sleep(0.1)  # 기본적으로 요청 간에는 0.1초 delay

        if len(self.rqHistory) < 5:
            pass
        else:
            # 1초 delay (5회)
            oneSecRqTime = self.rqHistory[-4]

            # 1초 이내에 5번 요청하면 delay
            while True:
                RqInterval = time.time() - oneSecRqTime
                if RqInterval > 1:
                    break

        # 1hour delay (1000회)
        if len(self.rqHistory) == 1000:
            oneHourRqTime = self.rqHistory[0]
            oneHourRqInterval = time.time() - oneHourRqTime

            if oneHourRqInterval < 3610:
                delay = 3610 - oneHourRqInterval

                # if self.logger:
                #     self.logger.warning(
                #         "{} checkRequestDelay: Request delayed by {} seconds".format(
                #             dt.now(), delay
                #         )
                #     )

                time.sleep(delay)

        # 새로운 request 시간 기록
        self.rqHistory.append(time.time())

app = None

def main():
    global app
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.signal_login_commConnect()#로그인 요청 시그널 포함

if __name__ == "__main__":
    main()