import tkinter as tk
from tkinter import messagebox
#import MetaTrader5 as mt5  # 确保已经安装并正确配置MetaTrader5模块
import numpy
class TradeManagementTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Trade Management Tool")

        # Create main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(padx=10, pady=10)

        # Title and close button
        title_frame = tk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        title_label = tk.Label(title_frame, text="Trade Management Tool", fg="red", font=("Arial", 14))
        title_label.pack(side=tk.LEFT)

        close_button = tk.Button(title_frame, text="X", command=root.quit, fg="red", font=("Arial", 14))
        close_button.pack(side=tk.RIGHT)

        # Input fields as buttons
        self.create_button_field(main_frame, "Take Profit", 1, self.set_take_profit)
        self.create_button_field(main_frame, "Stop Loss", 2, self.set_stop_loss)
        self.create_button_field(main_frame, "Partial TP", 3, self.set_partial_tp)
        self.create_button_field(main_frame, "Partial SL", 4, self.set_partial_sl)
        self.create_button_field(main_frame, "Set BE", 5, self.set_be)

        # Separator
        separator = tk.Frame(main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.grid(row=6, column=0, columnspan=2, pady=5, sticky='ew')

        # Alert section
        alert_label = tk.Label(main_frame, text="Alert", fg="black", font=("Arial", 12))
        alert_label.grid(row=7, column=0, columnspan=2)

        self.create_button_field(main_frame, "Above Price", 8, self.set_above_price)
        self.create_button_field(main_frame, "Below Price", 9, self.set_below_price)

    def create_button_field(self, parent, label_text, row, command):
        button = tk.Button(parent, text=label_text, font=("Arial", 12), command=command)
        button.grid(row=row, column=0, pady=5, sticky='e')
        
        entry = tk.Entry(parent, font=("Arial", 12))
        entry.grid(row=row, column=1, pady=5, sticky='w')
        
        return entry

    def set_take_profit(self):
        # 实现设置Take Profit的功能
        current_price = self.get_current_price()
        take_profit_value = current_price + 200 * 0.0001  # 假设点值为0.0001
        print(f"Setting Take Profit to {take_profit_value}")

    def set_stop_loss(self):
        # 实现设置Stop Loss的功能
        current_price = self.get_current_price()
        stop_loss_value = current_price - 200 * 0.0001
        print(f"Setting Stop Loss to {stop_loss_value}")

    def set_partial_tp(self):
        # 实现设置Partial Take Profit的功能
        print("Setting Partial TP")

    def set_partial_sl(self):
        # 实现设置Partial Stop Loss的功能
        print("Setting Partial SL")

    def set_be(self):
        # 实现设置Break Even的功能
        print("Setting BE")

    def set_above_price(self):
        # 实现设置Above Price Alert的功能
        print("Setting Above Price Alert")

    def set_below_price(self):
        # 实现设置Below Price Alert的功能
        print("Setting Below Price Alert")

    def get_current_price(self):
        # 获取当前价格的函数，这里需要实现从MetaTrader 5获取当前价格的逻辑
        return 1.2000  # 假设当前价格为1.2000

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeManagementTool(root)
    root.mainloop()
