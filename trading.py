"""
le simulateur de bourse du projet "trader d'un jour"

    from trading import Stock

    stock = Stock(df, end='2015')         # df: vos cours, indexés par date
    for date, history in stock.days():    # history = les cours jusqu'à aujourd'hui inclus
        if history.Close.iloc[-1] < 100:
            stock.buy(2)                  # achète 2 actions au cours du jour
    stock.plot()

on achète / vend au cours de clôture (`Close`) du jour courant
`history` ne contient jamais le futur, donc pas moyen de tricher
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CASH = 1000   # capital de départ en $
FEE = 0.001   # 0.1% de frais à chaque achat / vente


class Stock:

    def __init__(self, df, start=None, end=None, cash=CASH, fee=FEE):
        """df: une dataframe indexée par date (croissante, sans NaT) avec une colonne Close
        start, end: pour ne simuler qu'une partie de la période, ex. Stock(df, '2008', '2010')"""
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("l'index de df doit être de type datetime (voir l'échauffement)")
        if df.index.hasnans:
            raise ValueError("l'index de df contient des NaT (voir l'échauffement)")
        if not df.index.is_monotonic_increasing:
            raise ValueError("df doit être triée par date croissante")
        if "Close" not in df.columns:
            raise ValueError("df doit avoir une colonne 'Close'")
        self.df = df.loc[start:end]
        if len(self.df) == 0:
            raise ValueError(f"aucune donnée entre {start} et {end}")
        self.fee = fee
        self._cash = cash
        self._shares = 0.0
        self._i = 0
        self._values = {}

    def days(self):
        """itère sur les jours: (date, cours jusqu'à ce jour inclus)"""
        for i in range(len(self.df)):
            self._i = i
            yield self.date(), self.df.iloc[:i + 1]
            self._values[self.date()] = self.value()

    def date(self):
        """la date du jour courant"""
        return self.df.index[self._i]

    def price(self):
        """le cours de clôture du jour courant"""
        return self.df.Close.iloc[self._i]

    def amount(self):
        """le nombre d'actions détenues"""
        return self._shares

    def bankAccount(self):
        """le cash disponible en $"""
        return self._cash

    def value(self):
        """la valeur totale: cash + actions au cours du jour"""
        return self._cash + self._shares * self.price()

    def buy(self, n=None):
        """achète n actions (fractions autorisées), par défaut tout ce qu'on peut"""
        unit = self.price() * (1 + self.fee)
        if n is None:
            n = self._cash / unit
        if n < 0:
            raise ValueError(f"on ne peut pas acheter {n} actions")
        if n * unit > self._cash * (1 + 1e-9):
            raise ValueError(f"{self.date():%Y-%m-%d}: {n:.2f} actions coûtent "
                             f"{n * unit:.2f} $, vous n'avez que {self._cash:.2f} $")
        self._cash = max(self._cash - n * unit, 0.0)
        self._shares += n

    def sell(self, n=None):
        """vend n actions, par défaut toutes"""
        if n is None:
            n = self._shares
        if n < 0:
            raise ValueError(f"on ne peut pas vendre {n} actions")
        if n > self._shares * (1 + 1e-9):
            raise ValueError(f"{self.date():%Y-%m-%d}: vous voulez vendre {n:.2f} "
                             f"actions, vous n'en avez que {self._shares:.2f}")
        self._cash += n * self.price() * (1 - self.fee)
        self._shares = max(self._shares - n, 0.0)

    def history(self):
        """la valeur du portefeuille jour par jour (après la boucle)"""
        return pd.Series(self._values, name="portefeuille")

    def plot(self):
        """compare votre portefeuille avec 'acheter le 1er jour et ne plus toucher'"""
        values = self.history()
        close = self.df.Close.loc[values.index]
        hold = values.iloc[0] * close / close.iloc[0]
        pd.DataFrame({"vous": values, "buy & hold": hold}).plot(
            logy=True, figsize=(12, 6), title="valeur du portefeuille ($)")
        plt.show()
        print(f"final: {values.iloc[-1]:.2f} $  (buy & hold: {hold.iloc[-1]:.2f} $)")


if __name__ == "__main__":
    df = pd.read_csv("data/Amazon.csv", skiprows=3, parse_dates=["Date"])
    df = df.dropna(subset=["Date"]).set_index("Date").sort_index()
    # tout acheter le 1er jour, tout vendre le dernier
    stock = Stock(df)
    for date, history in stock.days():
        if len(history) == 1:
            stock.buy()
        if len(history) == len(stock.df):
            stock.sell()
    close = stock.df.Close
    expected = CASH * (1 - FEE) ** 2 * close.iloc[-1] / close.iloc[0]
    assert np.isclose(stock.bankAccount(), expected) and stock.amount() == 0
    # on ne peut pas dépenser plus que son cash
    try:
        Stock(df).buy(10_000)
        assert False
    except ValueError as e:
        print("ok:", e)
    # une df mal préparée est refusée
    try:
        Stock(pd.read_csv("data/Amazon.csv", skiprows=3))
        assert False
    except ValueError as e:
        print("ok:", e)
    # le singe: au hasard chaque jour, sur une sous-période
    rng = np.random.default_rng(0)
    monkey = Stock(df, "2016", "2020")
    for date, history in monkey.days():
        monkey.buy() if rng.random() < 0.5 else monkey.sell()
    monkey.plot()
