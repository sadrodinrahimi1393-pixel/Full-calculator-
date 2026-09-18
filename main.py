# -*- coding: utf-8 -*-
import math
from functools import reduce
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from sympy import symbols, Eq, solve, sympify, SympifyError

PERSIAN_TO_ENGLISH_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

def normalize_number(text):
    return text.translate(PERSIAN_TO_ENGLISH_DIGITS).strip()

def get_real_value(text, placeholder_text):
    value = text.strip()
    if value == placeholder_text:
        return ""
    return normalize_number(value)

KV = r"""
#:import dp kivy.metrics.dp

<Root>:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(8)

    TabbedPanel:
        do_default_tab: False
        tab_width: self.width / 4

        TabbedPanelItem:
            text: "ب.م.م و ک.م.م"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                Label:
                    text: "اعداد را با فاصله جدا کنید (بین ۲ تا ۴ عدد):"
                    text_size: self.width, None
                    halign: "right"
                    size_hint_y: None
                    height: dp(48)
                TextInput:
                    id: gcd_numbers
                    text: "مثال: 12, 18, 24"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(18)
                Label:
                    id: gcd_result
                    text: ""
                    font_size: dp(17)
                    bold: True
                    color: 0.16, 0.73, 0.4, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: dp(80)
                Button:
                    text: "محاسبه"
                    size_hint_y: None
                    height: dp(52)
                    font_size: dp(18)
                    on_release: app.compute_gcd_lcm()
                Widget:

        TabbedPanelItem:
            text: "ریشه"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                Label:
                    text: "عدد:"
                    size_hint_y: None
                    height: dp(35)
                TextInput:
                    id: root_number
                    text: "مثال: 16"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(18)
                Label:
                    text: "درجه‌ی ریشه (۲ = جذر، ۳ = ریشه‌ی سوم، ...):"
                    size_hint_y: None
                    height: dp(45)
                TextInput:
                    id: root_degree
                    text: "مثال: 2"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(18)
                Label:
                    id: root_result
                    text: ""
                    font_size: dp(17)
                    bold: True
                    color: 0.16, 0.73, 0.4, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: dp(70)
                Button:
                    text: "محاسبه"
                    size_hint_y: None
                    height: dp(52)
                    font_size: dp(18)
                    on_release: app.compute_root()
                Widget:

        TabbedPanelItem:
            text: "توان"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                Label:
                    text: "پایه:"
                    size_hint_y: None
                    height: dp(35)
                TextInput:
                    id: power_base
                    text: "مثال: 2"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(18)
                Label:
                    text: "توان:"
                    size_hint_y: None
                    height: dp(35)
                TextInput:
                    id: power_exp
                    text: "مثال: 10"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(18)
                Label:
                    id: power_result
                    text: ""
                    font_size: dp(17)
                    bold: True
                    color: 0.16, 0.73, 0.4, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: dp(70)
                Button:
                    text: "محاسبه"
                    size_hint_y: None
                    height: dp(52)
                    font_size: dp(18)
                    on_release: app.compute_power()
                Widget:

        TabbedPanelItem:
            text: "معادله"
            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(7)
                Label:
                    text: "معادله را با متغیر 'x' وارد کنید:"
                    text_size: self.width, None
                    halign: "right"
                    size_hint_y: None
                    height: dp(45)
                Label:
                    text: "مثال: 2*x + 3 = 7    یا    x**2 - 5*x + 6 = 0"
                    color: 0.5, 0.5, 0.5, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: dp(55)
                TextInput:
                    id: equation
                    text: "مثال: x**2 - 5*x + 6 = 0"
                    multiline: False
                    halign: "center"
                    size_hint_y: None
                    height: dp(48)
                    font_size: dp(17)
                Label:
                    id: eq_result
                    text: ""
                    font_size: dp(16)
                    bold: True
                    color: 0.16, 0.73, 0.4, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: dp(100)
                Button:
                    text: "حل کن"
                    size_hint_y: None
                    height: dp(52)
                    font_size: dp(18)
                    on_release: app.compute_equation()
                Widget:
"""

class Root(BoxLayout):
    pass

class CalculatorApp(App):
    title = "ماشین‌حساب فوق‌العاده"

    def build(self):
        return Builder.load_string(KV)

    def error(self, message):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        box.add_widget(Label(text=message, halign="center"))
        close = Button(text="باشه", size_hint_y=None, height=dp(48))
        popup = Popup(title="خطا", content=box, size_hint=(.88, .34))
        close.bind(on_release=popup.dismiss)
        box.add_widget(close)
        popup.open()

    def compute_gcd_lcm(self):
        try:
            text = get_real_value(self.root.ids.gcd_numbers.text, "مثال: 12, 18, 24")
            if not text:
                self.error("لطفاً عددها را وارد کنید.")
                return
            numbers = [int(n.strip()) for n in text.split(" ") if n.strip()]
            if len(numbers) < 2 or len(numbers) > 4:
                self.error("لطفاً بین ۲ تا ۴ عدد وارد کنید.")
                return
            gcd_result = reduce(math.gcd, numbers)
            def lcm(a, b):
                return abs(a * b) // math.gcd(a, b)
            lcm_result = reduce(lcm, numbers)
            self.root.ids.gcd_result.text = f"اعداد: {numbers}\nب.م.م: {gcd_result}    ک.م.م: {lcm_result}"
        except ValueError:
            self.error("لطفاً فقط عدد صحیح وارد کنید (با فاصله جدا کنید).")

    def compute_root(self):
        try:
            number_text = get_real_value(self.root.ids.root_number.text, "مثال: 16")
            degree_text = get_real_value(self.root.ids.root_degree.text, "مثال: 2")
            if not number_text or not degree_text:
                self.error("لطفاً هر دو مقدار را وارد کنید.")
                return
            number, n = float(number_text), float(degree_text)
            if n == 0:
                self.error("درجه‌ی ریشه نمی‌تواند صفر باشد.")
                return
            if number < 0 and n % 2 == 0:
                self.error("نمی‌توان ریشه‌ی زوج یک عدد منفی را محاسبه کرد.")
                return
            result = -(-number) ** (1 / n) if number < 0 else number ** (1 / n)
            self.root.ids.root_result.text = f"نتیجه: {result:.6f}"
        except ValueError:
            self.error("لطفاً اعداد معتبر وارد کنید.")
        except ZeroDivisionError:
            self.error("درجه‌ی ریشه نمی‌تواند صفر باشد.")

    def compute_power(self):
        try:
            base_text = get_real_value(self.root.ids.power_base.text, "مثال: 2")
            exp_text = get_real_value(self.root.ids.power_exp.text, "مثال: 10")
            if not base_text or not exp_text:
                self.error("لطفاً هر دو مقدار را وارد کنید.")
                return
            result = float(base_text) ** float(exp_text)
            self.root.ids.power_result.text = f"نتیجه: {result}"
        except ValueError:
            self.error("لطفاً اعداد معتبر وارد کنید.")

    def compute_equation(self):
        equation_text = get_real_value(self.root.ids.equation.text, "مثال: x**2 - 5*x + 6 = 0")
        if not equation_text:
            self.error("لطفاً یک معادله وارد کنید.")
            return
        try:
            x = symbols("x")
            if "=" in equation_text:
                left_side, right_side = equation_text.split("=", 1)
                equation = Eq(sympify(left_side.strip()), sympify(right_side.strip()))
            else:
                equation = Eq(sympify(equation_text.strip()), 0)
            solutions = solve(equation, x)
            self.root.ids.eq_result.text = f"جواب(های) x: {solutions}" if solutions else "جوابی پیدا نشد."
        except SympifyError:
            self.error("متوجه این معادله نشدم. فرمت را بررسی کن.")
        except Exception as e:
            self.error(f"مشکلی پیش آمد: {e}")

if __name__ == "__main__":
    CalculatorApp().run()
