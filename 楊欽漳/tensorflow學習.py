import MetaTrader5 as mt5
from datetime import datetime, timedelta
import tkinter 
# 初始化MetaTrader 5连接
if not mt5.initialize():
    print("MetaTrader 5 initialization failed")
    mt5.shutdown()