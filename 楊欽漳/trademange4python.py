import MetaTrader5 as mt5
from datetime import datetime, timedelta

# 初始化MetaTrader 5连接
if not mt5.initialize():
    print("MetaTrader 5 initialization failed")
    mt5.shutdown()

# 设置符号（Symbol）
symbol = "XAUUSD"

# 函数：部分平仓
def close_partial_position(ticket, percentage):
    position = mt5.positions_get(ticket=ticket)
    if position:
        volume = position[0].volume
        volume_to_close = volume * percentage / 100.0
        result = mt5.order_send(
            mt5.ORDER_TYPE_SELL if position[0].type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
            symbol=position[0].symbol,
            volume=volume_to_close,
            price=mt5.symbol_info_tick(symbol).bid if position[0].type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
            deviation=10,
            type_filling=mt5.ORDER_FILLING_FOK
        )
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Partial close failed: {result.comment}")
        else:
            print(f"Partial close successful: {volume_to_close} lots")

# 函数：设置止损和止盈
def set_sl_tp(ticket):
    position = mt5.positions_get(ticket=ticket)
    if position:
        open_price = position[0].price_open
        stop_loss = 0
        take_profit = 0
        min_stop_level_points = mt5.symbol_info(symbol).stops_level

        if min_stop_level_points < 0:
            min_stop_level_points = 10

        min_stop_level = min_stop_level_points * mt5.symbol_info(symbol).point
        
        if position[0].type == mt5.ORDER_TYPE_BUY:
            stop_loss = open_price - 200 * mt5.symbol_info(symbol).point
            take_profit = open_price + 300 * mt5.symbol_info(symbol).point
            if stop_loss > open_price - min_stop_level:
                stop_loss = open_price - min_stop_level
            if take_profit < open_price + min_stop_level:
                take_profit = open_price + min_stop_level
        else:
            stop_loss = open_price + 200 * mt5.symbol_info(symbol).point
            take_profit = open_price - 300 * mt5.symbol_info(symbol).point
            if stop_loss < open_price + min_stop_level:
                stop_loss = open_price + min_stop_level
            if take_profit > open_price - min_stop_level:
                take_profit = open_price - min_stop_level

        modify_result = mt5.order_modify(
            ticket=ticket,
            sl=stop_loss,
            tp=take_profit
        )
        if modify_result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to set SL/TP: {ticket} - Error: {modify_result.comment}")
        else:
            print(f"Set SL: {stop_loss}, TP: {take_profit} for ticket: {ticket}")

# 函数：判断盈利情况并部分平仓
def in_profits(ticket):
    position = mt5.positions_get(ticket=ticket)
    if position:
        open_price = position[0].price_open
        current_price = mt5.symbol_info_tick(symbol).bid if position[0].type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
        secured = 0

        if position[0].type == mt5.ORDER_TYPE_BUY:
            if current_price >= open_price + 140 * mt5.symbol_info(symbol).point:
                take_profit = open_price + 300 * mt5.symbol_info(symbol).point
                mt5.order_modify(ticket=ticket, tp=take_profit)
                close_partial_position(ticket, 50)
                secured = 1
        else:
            if current_price <= open_price - 140 * mt5.symbol_info(symbol).point:
                take_profit = open_price - 300 * mt5.symbol_info(symbol).point
                mt5.order_modify(ticket=ticket, tp=take_profit)
                close_partial_position(ticket, 50)
                secured = 1
        return secured
    else:
        print(f"Position not found for ticket: {ticket}")
        return 0

# 函数：检查所有订单并管理SL/TP
def check():
    total_orders = mt5.positions_total()
    secured = 0
    for i in range(total_orders):
        position = mt5.positions_get()[i]
        ticket = position.ticket
        if position.symbol == symbol:
            if position.sl == 0 or position.tp == 0:
                set_sl_tp(ticket)
            else:
                secured += in_profits(ticket)
    print(f"Secured: {secured}")

# 函数：管理订单
def manage_orders():
    check()

# 主逻辑
while True:
    manage_orders()
    mt5.sleep(1000)

# 关闭MetaTrader 5连接
mt5.shutdown()
