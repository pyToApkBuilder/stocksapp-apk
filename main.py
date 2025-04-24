from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import json
import os
from tradingview_ta import TA_Handler, Interval

file_path = resource_find("fno_stocks.json")
if file_path:
    with open(file_path, "r") as f:
        stocks = json.load(f)
else:
    stocks = []

def get_data(symbol, interval):
    try:
        hand = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=interval,
        )
        a = hand.get_analysis()
        r = a.summary["RECOMMENDATION"]
        i = a.indicators
        return [symbol, r, round(i["close"], 2), round(i["RSI"], 2)]
    except:
        return None

class StockFilterApp(App):
    def build(self):
        self.selected_filter = "STRONG_BUY"
        self.selected_interval = Interval.INTERVAL_1_DAY

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
       
        title_label = Label(
            text="Stock Filter App",
            size_hint=(1, None),
            height=100,
            font_size=48,
            bold=True
        )

        filter_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100)
        interval_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100)

        filter_label = Label(text="Recommendation:", size_hint=(0.5, 1), halign='left', valign='middle')
        self.filter_spinner = Spinner(
            text=self.selected_filter,
            values=["STRONG_BUY", "STRONG_SELL", "BUY", "SELL"],
            size_hint=(0.5, 1)
        )
        self.filter_spinner.bind(text=self.on_filter_select)
        filter_row.add_widget(filter_label)
        filter_row.add_widget(self.filter_spinner)

        interval_label = Label(text="Interval:", size_hint=(0.5, 1), halign='left', valign='middle')
        self.interval_map = {
            "1m": Interval.INTERVAL_1_MINUTE,
            "5m": Interval.INTERVAL_5_MINUTES,
            "15m": Interval.INTERVAL_15_MINUTES,
            "1h": Interval.INTERVAL_1_HOUR,
            "2h": Interval.INTERVAL_2_HOURS,
            "1d": Interval.INTERVAL_1_DAY,
        }
        self.interval_spinner = Spinner(
            text="1d",
            values=list(self.interval_map.keys()),
            size_hint=(0.5, 1)
        )
        self.interval_spinner.bind(text=self.on_interval_select)
        interval_row.add_widget(interval_label)
        interval_row.add_widget(self.interval_spinner)

        self.filter_btn = Button(text="Filter Stocks", size_hint=(1, None), height=100)
        self.filter_btn.bind(on_release=self.filter_stocks)

        self.result_label = Label(size_hint_y=None, text="", halign="left", valign="top")
        self.result_label.bind(texture_size=self.update_label_height)
        scroll = ScrollView()
        scroll.add_widget(self.result_label)

        self.layout.add_widget(title_label)
        self.layout.add_widget(filter_row)
        self.layout.add_widget(interval_row)
        self.layout.add_widget(self.filter_btn)
        self.layout.add_widget(scroll)

        return self.layout

    def on_filter_select(self, spinner, text):
        self.selected_filter = text

    def on_interval_select(self, spinner, text):
        self.selected_interval = self.interval_map[text]

    def update_label_height(self, instance, size):
        self.result_label.height = size[1]
        self.result_label.text_size = (self.result_label.width, None)

    def filter_stocks(self, instance):
        self.result_label.text = "Starting filter..."
        threading.Thread(target=self.run_filter, daemon=True).start()

    def run_filter(self):
        Clock.schedule_once(lambda dt: self.append_result("Filtering started...\n\n"), 0)

        for symbol in stocks:
            data = get_data(symbol, self.selected_interval)
            show = False 

            if data:
                if self.selected_filter == "BUY" and data[1] in ["BUY", "STRONG_BUY"]:
                    show = True
                elif self.selected_filter == "SELL" and data[1] in ["SELL", "STRONG_SELL"]:
                    show = True
                elif data[1] == self.selected_filter:
                    show = True

                if show:
                    line = f"{data[0]:<10}  ||  {data[1]}  ||  Close: {data[2]}  ||  RSI: {data[3]}\n\n"
                    Clock.schedule_once(lambda dt, ln=line: self.append_result(ln), 0)
        Clock.schedule_once(lambda dt: self.append_result("Done filtering.\n"), 0)

    def append_result(self, text):
        self.result_label.text += text


if __name__ == "__main__":
    StockFilterApp().run()