from sqlalchemy import create_engine
import pymysql
import pandas as pd
from ui.decorator import *
from kiwoom.kiwoom import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


pymysql.install_as_MySQLdb()


form_class = uic.loadUiType("KW_data_reader.ui")[0]



class UI_Class(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("서비스를 시작합니다")
        self.kw = Kiwoom() #키움 클래스 연결



        #logins
        self.kw.signal_login_commConnect()
        self.get_account_number()
        self.account_num.addItems(self.account_list)

        self.account_info.clicked.connect(self.detail_account_balance)


        # status bar 에 출력할 메세지를 저장하는 변수
        # 어떤 모듈의 실행 완료를 나타낼 때 쓰인다.
        self.return_status_msg = ''
        self.return_msg = ''

        # timer 등록. tick per 1s
        self.timer_1s = QTimer(self)
        self.timer_1s.start(1000)
        self.timer_1s.timeout.connect(self.timeout_1s)

        '''
        데이터 집합
        '''

        self.day_push.clicked.connect(self.day_bong_total)
        self.week_push.clicked.connect(self.week_bong_total)
        self.month_push.clicked.connect(self.month_bong_total)
        self.year_push.clicked.connect(self.year_bong_total)
        self.one_min_push.clicked.connect(self.one_min_bong_total)
        self.three_min_push.clicked.connect(self.three_min_bong_total)
        self.five_min_push.clicked.connect(self.five_min_bong_total)
        self.fifteen_min_push.clicked.connect(self.fifteen_min_bong_total)
        self.thirty_min_push.clicked.connect(self.thirty_min_bong_total)
        self.sixty_min_push.clicked.connect(self.sixty_min_bong_total)
        self.whole_push.clicked.connect(self.whole_total)



        '''
        계좌평가 잔고내역역
        '''
    def timeout_1s(self):
        current_time = QTime.currentTime()

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kw.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        if self.return_status_msg == '':
            statusbar_msg = state_msg + " | " + time_msg
        else:
            statusbar_msg = state_msg + " | " + time_msg + " | " + self.return_status_msg

        self.statusbar.showMessage(statusbar_msg)



    '''
    종목 코드 반환
    '''
    def counting_fnc(self):
        kosdaq = self.kw.get_code_list_by_market("10")
        kospi = self.kw.get_code_list_by_market("0")
        total = kosdaq + kospi
        return total

###################################################################################################################
    '''
    모든종목 봉별 데이터 저장
    '''
    def day_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.long_term_data(i, "일봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def week_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.long_term_data(i, "주봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def month_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.long_term_data(i, "월봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def year_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.long_term_data(i, "년봉")
            print("%s 종목완료" % self.kw.get_code_name(i))
            print("#####################################")

    def one_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "1분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def three_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "3분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def five_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "5분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def fifteen_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "15분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def thirty_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "30분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")

    def sixty_min_bong_total(self):
        cnt = 0
        for i in self.counting_fnc():
            self.short_term_data(i, "60분봉")
            cnt += 1
            print("{0} 종목완료 {1}/{2}".format(self.kw.get_code_name(i), cnt, len(self.counting_fnc())))
            print("#####################################")





    def whole_total(self):
        print("Start one-min to three-min")
        self.one_min_bong_total()
        self.three_min_bong_total()
        time.sleep(30)
        print("Start day to year")
        self.day_bong_total()
        self.week_bong_total()
        self.month_bong_total()
        self.year_bong_total()
        time.sleep(30)
        print("Start five-min to sixty-min")
        self.five_min_bong_total()
        self.fifteen_min_bong_total()
        self.thirty_min_bong_total()
        self.sixty_min_bong_total()
        print("Whole clear")


#########################################################################################################







    ####계좌번호 ##
    def get_account_number(self):
        account_list = self.kw.get_Login_info("ACCNO")
        self.account_list = account_list.split(';')
        account_ID = self.kw.get_Login_info("USER_ID")
        account_NAME = self.kw.get_Login_info("USER_NAME")



    def detail_account_balance(self):

        input_dict = {}

        input_dict['계좌번호'] = self.account_list[0]
        input_dict['비밀번호'] = "6973"
        input_dict['비밀번호입력매체구분'] = "00"
        input_dict['조회구분'] = "2"

        self.kw.set_input_value(input_dict)
        self.kw.com_rq_data("계좌평가잔고내역요청", "opw00018", "0", "1001")
        self.return_msg = self.kw.latest_tr_data[1]
        self.total_buy_money.append(self.return_msg)
        # self.total_evaluated_price.toPlainText(self.kw.latest_tr_data[2])
        # self.total_profit_money.toPlainText(self.kw.latest_tr_data[3])
        # self.total_earing_rate_percent.toPlainText(self.kw.latest_tr_data[4])
        # self.total_taken_money.toPlainText(self.kw.latest_tr_data[5])



    def long_term_data(self, code=None, tick_unit=None):
        input_dict = {}
        data = None
        base_date = datetime.datetime.today().strftime('%Y%m%d')


        if tick_unit == "일봉":
            input_dict['종목코드'] = code
            input_dict['기준일자'] = base_date
            input_dict['수정주가구분'] = 1


            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식일봉차트조회요청", "opt10081", 0, "1000")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                time.sleep(TR_REQ_TIME_INTERVAL)
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식일봉차트조회요청", "opt10081", 2, "1000")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

            df = pd.DataFrame(data, columns=['close_price', 'starting_price', 'high_price', 'low_price', 'trading_volume', 'trading_money'],
                              index=data['date'])
            engine = create_engine('mysql+pymysql://root:' + "7426" + "@localhost:3306/stock_daily?charset=utf8", encoding='utf-8')
            df.to_sql('stock' + code, engine, if_exists='replace', index=True)

        elif tick_unit == "주봉":
            input_dict['종목코드'] = code
            input_dict['기준일자'] = base_date
            input_dict['끝일자'] = ''
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식주봉차트조회요청", "opt10082", 0, "1000")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                time.sleep(TR_REQ_TIME_INTERVAL)
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식주봉차트조회요청", "opt10082", 2, "1000")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val
            df = pd.DataFrame(data, columns=['close_price', 'starting_price', 'high_price', 'low_price', 'trading_volume','trading_money'],
                              index=data['date'])
            engine = create_engine('mysql+pymysql://root:' + "7426" + '@localhost:3306/stock_weekly', encoding='utf-8')
            df.to_sql('stock' + code, engine, if_exists='replace', index=True)

        elif tick_unit == "월봉":
            input_dict['종목코드'] = code
            input_dict['기준일자'] = base_date
            input_dict['끝일자'] = ''
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식월봉차트조회요청", "opt10083", 0, "1000")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                time.sleep(TR_REQ_TIME_INTERVAL)
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식월봉차트조회요청", "opt10083", 2, "1000")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val
            df = pd.DataFrame(data, columns=['close_price', 'starting_price', 'high_price', 'low_price', 'trading_volume', 'trading_money'],
                              index=data['date'])
            engine = create_engine('mysql+pymysql://root:' + "7426" + '@localhost:3306/stock_monthly', encoding='utf-8')
            df.to_sql('stock' + code, engine, if_exists='replace', index=True)

        elif tick_unit == "년봉":
            input_dict['종목코드'] = code
            input_dict['기준일자'] = base_date
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식년봉차트조회요청", "opt10094", 0, "1000")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                time.sleep(TR_REQ_TIME_INTERVAL)
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식년봉차트조회요청", "opt10094", 2, "1000")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val
            df = pd.DataFrame(data,columns=['close_price', 'starting_price', 'high_price', 'low_price', 'trading_volume','trading_money'],
                              index=data['date'])

            #DB 저장, password 항목란에 저장필요
            engine = create_engine('mysql+pymysql://root:' + "password" + '@localhost:3306/stock_yearly', encoding='utf-8')
            df.to_sql('stock' + code, engine, if_exists='replace', index=True)


    def short_term_data(self, code=None, tick_unit=None):


        input_dict = {}
        data = None


        #DB engine
        # engine = create_engine('mysql://root:' + "password" + '@localhost:3307/stock_db', encoding='utf-8')

        if tick_unit == "1분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "1"
            input_dict['수정주가구분'] = 1
            base_date = datetime.datetime.today().strftime('%Y%m%d, %H:%M:%S')

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1001")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                time.sleep(1)
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1001")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        elif tick_unit == "3분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "3"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1002")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1002")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        elif tick_unit == "5분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "5"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1003")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1003")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val



        elif tick_unit == "15분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "15"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1004")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1004")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        elif tick_unit == "30분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "30"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1005")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1005")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        elif tick_unit == "60분봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "60"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 0, "1006")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식분봉차트조회요청", "opt10080", 2, "1006")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        elif tick_unit == "틱봉":
            input_dict['종목코드'] = code
            input_dict['틱범위'] = "1"
            input_dict['수정주가구분'] = 1

            self.kw.set_input_value(input_dict)
            self.kw.com_rq_data("주식틱차트조회요청", "opt10079", 0, "1008")
            data = self.kw.latest_tr_data

            while self.kw.is_tr_Data == True:
                self.kw.set_input_value(input_dict)
                self.kw.com_rq_data("주식틱차트조회요청", "opt10079", 2, "1008")
                for key, val in self.kw.latest_tr_data.items():
                    data[key][-1:] = val

        ## Store Dataframe
        df = pd.DataFrame(data, columns=['close_price','starting_price','high_price','low_price','trading_volume'], index=data['date'])
        ## Make it to CSV file
        # df.to_csv("path".format(code), index=True, date_format='%Y%m%d%%H%M',
        #           encoding="utf-8")
        #Example:
        df.to_csv("D:/stock_data_csv/1min/A{}.csv".format(code), index=True, date_format='%Y%m%d%%H%M', encoding="utf-8")
        
        ## Using DB
        # df.to_sql('stock'+ code, engine, if_exists='replace')

###################################################################################################################



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = UI_Class()
    mainWindow.show()
    app.exec_() ##이벤트루프 종료 안되게 만드는 것