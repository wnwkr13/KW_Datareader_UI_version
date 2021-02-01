from typing import TYPE_CHECKING

from ui import decorator

if TYPE_CHECKING:
    from kiwoom.kiwoom import Kiwoom

'''
일봉 데이터 요청 
'''
@decorator.call_printer
def tr_receive_opt10081(kw: 'Kiwoom',sTrCode, sRQName):

    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print("데이터의 갯수는 %s / 600 " % rows)


    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [], 'trading_money': [] }
    ###조회하면 600일치까지 일봉데이터 받을 수 있음
    for i in range(rows):
        date = kw.get_comm_data(sTrCode, sRQName, i, "일자")
        close_price = kw.get_comm_data(sTrCode, sRQName, i, "현재가") # 3시 30분이후에 요청시 종가
        starting_price = kw.get_comm_data(sTrCode, sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode, sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode, sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode, sRQName, i, "거래량")
        trading_money = kw.get_comm_data(sTrCode, sRQName, i, "거래대금")


        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))
        data['trading_money'].append(int(trading_money))


    return data

'''
분봉데이터 요청
'''
@decorator.call_printer
def tr_receive_opt10080(kw: 'Kiwoom', sTrCode, sRQName):


    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print("데이터의 갯수는 %s / 900 " % rows)


    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [] }
    ###조회하면 600일치까지 일봉데이터 받을 수 있음
    for i in range(rows):

        date = kw.get_comm_data(sTrCode,sRQName, i, "체결시간")
        close_price = kw.get_comm_data(sTrCode,sRQName, i, "현재가")
        starting_price = kw.get_comm_data(sTrCode,sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode,sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode,sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode,sRQName, i, "거래량")



        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))


    return data

'''
주봉데이터 요청
'''
@decorator.call_printer
def tr_receive_opt10082(kw: 'Kiwoom', sTrCode, sRQName):


    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print("데이터의 갯수는 %s / 600 " % rows)


    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [], 'trading_money': [] }
    ###조회하면 600일치까지 일봉데이터 받을 수 있음
    for i in range(rows):

        date = kw.get_comm_data(sTrCode, sRQName, i, "일자")
        close_price = kw.get_comm_data(sTrCode, sRQName, i, "현재가") # 3시 30분이후에 요청시 종가
        starting_price = kw.get_comm_data(sTrCode, sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode, sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode, sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode, sRQName, i, "거래량")
        trading_money = kw.get_comm_data(sTrCode, sRQName, i, "거래대금")
        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))
        data['trading_money'].append(int(trading_money))

    return data
'''
월봉데이터 요청
'''
@decorator.call_printer
def tr_receive_opt10083(kw: 'Kiwoom', sTrCode, sRQName):


    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print("데이터의 갯수는 %s / 600 " % rows)


    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [], 'trading_money': [] }
    for i in range(rows):

        date = kw.get_comm_data(sTrCode, sRQName, i, "일자")
        close_price = kw.get_comm_data(sTrCode, sRQName, i, "현재가") # 3시 30분이후에 요청시 종가
        starting_price = kw.get_comm_data(sTrCode, sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode, sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode, sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode, sRQName, i, "거래량")
        trading_money = kw.get_comm_data(sTrCode, sRQName, i, "거래대금")


        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))
        data['trading_money'].append(int(trading_money))

    return data
'''
년봉데이터 요청
'''
@decorator.call_printer
def tr_receive_opt10094(kw: 'Kiwoom', sTrCode, sRQName):


    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print(rows)


    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [], 'trading_money': [] }

    for i in range(rows):

        date = kw.get_comm_data(sTrCode, sRQName, i, "일자")
        close_price = kw.get_comm_data(sTrCode, sRQName, i, "현재가") # 3시 30분이후에 요청시 종가
        starting_price = kw.get_comm_data(sTrCode, sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode, sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode, sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode, sRQName, i, "거래량")
        trading_money = kw.get_comm_data(sTrCode, sRQName, i, "거래대금")


        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))
        data['trading_money'].append(int(trading_money))

    return data

'''
틱봉데이터 요청
'''
@decorator.call_printer
def tr_receive_opt10079(kw: 'Kiwoom', sTrCode, sRQName):
    rows = kw.get_repeat_cnt(sTrCode, sRQName)
    print("데이터의 갯수는 %s / 900 " % rows)

    data = {'date': [], 'close_price': [], 'starting_price': [], 'high_price': [], 'low_price': [], 'trading_volume': [] }

    for i in range(rows):
        date = kw.get_comm_data(sTrCode, sRQName, i, "체결시간")
        close_price = kw.get_comm_data(sTrCode, sRQName, i, "현재가")  # 3시 30분이후에 요청시 종가
        starting_price = kw.get_comm_data(sTrCode, sRQName, i, "시가")
        high_price = kw.get_comm_data(sTrCode, sRQName, i, "고가")
        low_price = kw.get_comm_data(sTrCode, sRQName, i, "저가")
        trading_volume = kw.get_comm_data(sTrCode, sRQName, i, "거래량")

        data['date'].append(date)
        data['close_price'].append(abs(int(close_price)))
        data['starting_price'].append(abs(int(starting_price)))
        data['high_price'].append(abs(int(high_price)))
        data['low_price'].append(abs(int(low_price)))
        data['trading_volume'].append(int(trading_volume))

    return data