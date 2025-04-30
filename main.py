# requirements:  python3,kivy,kivy-garden,kivy-garden.matplotlib,matplotlib,yfinance,pillow,numpy,pandas



import yfinance as yf
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy_garden.matplotlib import FigureCanvasKivyAgg


class MainLayout(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.sym_input = TextInput(hint_text="Enter stock symbol", multiline=False,size_hint=(1,0.07))
        self.btn = Button(text="Fetch",size_hint=(1,0.1))
        self.btn.bind(on_press=self.fetch_data)
        self.result = Label(text="Enter a stock symbol and press Fetch",size_hint=(1,0.1))
        self.graph_container = BoxLayout()

        self.layout.add_widget(self.sym_input)
        self.layout.add_widget(self.btn)
        self.layout.add_widget(self.result)
        self.layout.add_widget(self.graph_container)

        return self.layout

    def fetch_data(self, instance):
        sym = self.sym_input.text.strip().upper()
        try:
            data = yf.Ticker(sym).history(period="6mo")
            if data.empty:
                self.result.text = f"No data found for '{sym}'"
                self.graph_container.clear_widgets()
            else:
                close_price = data.iloc[-1]['Close']
                self.result.text = f"{sym} last close: {close_price:.2f}"
                self.plot_graph(data)
        except Exception as e:
            self.result.text = f"Error: {str(e)}"
        self.sym_input.text = ""

    def plot_graph(self, data):
        plt.clf()  # Clear previous figure
        data['Close'].plot(title="Close Price", grid=True)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.tight_layout()

        self.graph_container.clear_widgets()
        self.graph_container.add_widget(FigureCanvasKivyAgg(plt.gcf()))


if __name__ == "__main__":
    MainLayout().run()
