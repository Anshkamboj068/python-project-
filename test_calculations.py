import unittest
import calculations as calc


class TestCalculations(unittest.TestCase):
    def test_position_size(self):
        r = calc.position_size(10000, 1, 100, 95, target=110)
        self.assertAlmostEqual(r["Risk amount"], 100)
        self.assertAlmostEqual(r["Position size (units)"], 20)
        self.assertAlmostEqual(r["Risk/Reward ratio"], 2)

    def test_profit_loss_buy_and_sell(self):
        self.assertAlmostEqual(calc.profit_loss(100, 110, 10, "Buy")["Net P/L"], 100)
        self.assertAlmostEqual(calc.profit_loss(100, 90, 10, "Sell")["Net P/L"], 100)

    def test_profit_loss_fees(self):
        r = calc.profit_loss(100, 110, 10, "Buy", fee_pct=0.1)
        self.assertAlmostEqual(r["Total fees"], 2.1)
        self.assertAlmostEqual(r["Net P/L"], 97.9)

    def test_risk_reward(self):
        r = calc.risk_reward(100, 95, 115)
        self.assertAlmostEqual(r["Risk/Reward ratio"], 3)
        self.assertAlmostEqual(r["Break-even win rate (%)"], 25)

    def test_margin_leverage(self):
        r = calc.margin_leverage(10000, 10, entry=100, side="Buy")
        self.assertAlmostEqual(r["Margin required"], 1000)
        self.assertAlmostEqual(r["Approx. liquidation price"], 90)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            calc.position_size(10000, 1, 100, 100)
        with self.assertRaises(ValueError):
            calc.margin_leverage(1000, 0.5)


if __name__ == "__main__":
    unittest.main()
