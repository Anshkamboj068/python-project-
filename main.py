import tkinter as tk
from tkinter import ttk, messagebox

import calculations as calc


def fmt(value):

    if isinstance(value, float):
        return f"{value:,.4f}".rstrip("0").rstrip(".") if abs(value) < 1000 else f"{value:,.2f}"
    return str(value)


class CalculatorTab(ttk.Frame):
   

    def __init__(self, parent, fields, compute, title):
        super().__init__(parent, padding=15)
        self.compute = compute
        self.vars = {}

        ttk.Label(self, text=title, font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        row = 1
        for label, key, kind, default in fields:
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", pady=4)
            var = tk.StringVar(value=default)
            if kind == "side":
                widget = ttk.Combobox(self, textvariable=var, values=["Buy", "Sell"],
                                      state="readonly", width=18)
            else:
                widget = ttk.Entry(self, textvariable=var, width=20)
            widget.grid(row=row, column=1, sticky="e", pady=4, padx=(15, 0))
            self.vars[key] = (var, kind)
            row += 1

        btns = ttk.Frame(self)
        btns.grid(row=row, column=0, columnspan=2, pady=12, sticky="ew")
        ttk.Button(btns, text="Calculate", command=self.run).pack(side="left", expand=True, fill="x")
        ttk.Button(btns, text="Clear", command=self.clear).pack(side="left", expand=True, fill="x", padx=(8, 0))

        self.result = tk.Text(self, height=9, width=38, state="disabled",
                              font=("Consolas", 10), relief="solid", borderwidth=1)
        self.result.grid(row=row + 1, column=0, columnspan=2, sticky="nsew")
        self.columnconfigure(1, weight=1)

    def read_inputs(self):
        values = {}
        for key, (var, kind) in self.vars.items():
            text = var.get().strip()
            if kind == "side":
                values[key] = text
            elif kind == "optional" and text == "":
                values[key] = None
            else:
                try:
                    values[key] = float(text)
                except ValueError:
                    raise ValueError(f"'{text}' is not a valid number.")
        return values

    def run(self):
        try:
            output = self.compute(**self.read_inputs())
        except ValueError as err:
            messagebox.showerror("Invalid input", str(err))
            return
        lines = [f"{name:<26}{fmt(val):>12}" for name, val in output.items()]
        self.show("\n".join(lines))

    def show(self, text):
        self.result.config(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.config(state="disabled")

    def clear(self):
        for var, kind in self.vars.values():
            if kind != "side":
                var.set("")
        self.show("")


class TradingCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trading Calculator")
        self.resizable(False, False)

        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        notebook = ttk.Notebook(self, padding=5)
        notebook.pack(fill="both", expand=True)

        notebook.add(CalculatorTab(
            notebook,
            [("Account balance", "balance", "number", "10000"),
             ("Risk per trade (%)", "risk_pct", "number", "1"),
             ("Entry price", "entry", "number", ""),
             ("Stop loss price", "stop_loss", "number", ""),
             ("Target price (optional)", "target", "optional", "")],
            calc.position_size, "Position Size"), text="Position Size")

        notebook.add(CalculatorTab(
            notebook,
            [("Side", "side", "side", "Buy"),
             ("Entry price", "entry", "number", ""),
             ("Exit price", "exit_price", "number", ""),
             ("Quantity", "quantity", "number", ""),
             ("Fee per side (%)", "fee_pct", "number", "0")],
            calc.profit_loss, "Profit / Loss"), text="Profit / Loss")

        notebook.add(CalculatorTab(
            notebook,
            [("Entry price", "entry", "number", ""),
             ("Stop loss price", "stop_loss", "number", ""),
             ("Target price", "target", "number", "")],
            calc.risk_reward, "Risk / Reward"), text="Risk / Reward")

        notebook.add(CalculatorTab(
            notebook,
            [("Side", "side", "side", "Buy"),
             ("Position value", "position_value", "number", ""),
             ("Leverage (x)", "leverage", "number", "10"),
             ("Entry price (optional)", "entry", "optional", "")],
            calc.margin_leverage, "Margin & Leverage"), text="Margin")


if __name__ == "__main__":
    TradingCalculatorApp().mainloop()
