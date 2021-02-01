# coding=utf-8
import datetime


def call_printer(original_func):
    '''
    Decorator for showing time and function that has been used
    '''

    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print('[{:.22s}] 함수 `{}` 호출 되었습니다'.format(timestamp, original_func.__name__))
        return original_func(*args, **kwargs)

    return wrapper


def return_status_msg_setter(original_func):
    """
    After exiting original function, Decorator for showing time string on QMainwindow instance statursbar
    """

    def wrapper(self):
        ret = original_func(self)

        timestamp = datetime.datetime.now().strftime('%H:%M:%S')

        # args[0]는 인스턴스 (즉, self)를 의미한다.
        self.return_status_msg = '`{}` is completed[{}]'.format(original_func.__name__, timestamp)
        return ret

    return wrapper