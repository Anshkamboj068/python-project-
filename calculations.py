


def position_size(balance, risk_pct, entry, stop_loss, target=None):

    
    if balance <= 0 or risk_pct <= 0 or entry <= 0 or stop_loss <= 0:
        raise ValueError("Balance, risk %, entry and stop loss must be positive.")
    per_unit_risk = abs(entry - stop_loss)
    if per_unit_risk == 0:
        raise ValueError("Entry and stop loss cannot be the same price.")

    risk_amount = balance * risk_pct / 100
    quantity = risk_amount / per_unit_risk
    result = {
        "Risk amount": risk_amount,
        "Risk per unit": per_unit_risk,
        "Position size (units)": quantity,
        "Position value": quantity * entry,
    }
    if target:
        reward = abs(target - entry) * quantity
        result["Potential reward"] = reward
        result["Risk/Reward ratio"] = reward / risk_amount
    return result


def profit_loss(entry, exit_price, quantity, side="Buy", fee_pct=0.0):

   
    if entry <= 0 or exit_price <= 0 or quantity <= 0:
        raise ValueError("Entry, exit and quantity must be positive.")
    if fee_pct < 0:
        raise ValueError("Fee cannot be negative.")

    direction = 1 if side == "Buy" else -1
    gross = (exit_price - entry) * quantity * direction
    fees = (entry + exit_price) * quantity * fee_pct / 100
    net = gross - fees
    invested = entry * quantity
    return {
        "Gross P/L": gross,
        "Total fees": fees,
        "Net P/L": net,
        "Return on position (%)": net / invested * 100,
        "Position value": invested,
    }


def risk_reward(entry, stop_loss, target):

  
    if entry <= 0 or stop_loss <= 0 or target <= 0:
        raise ValueError("Entry, stop loss and target must be positive.")
    risk = abs(entry - stop_loss)
    reward = abs(target - entry)
    if risk == 0:
        raise ValueError("Entry and stop loss cannot be the same price.")
    ratio = reward / risk
    return {
        "Risk per unit": risk,
        "Reward per unit": reward,
        "Risk/Reward ratio": ratio,
        "Break-even win rate (%)": 100 / (1 + ratio),
    }


def margin_leverage(position_value, leverage, entry=None, side="Buy"):


    if position_value <= 0 or leverage < 1:
        raise ValueError("Position value must be positive and leverage at least 1.")
    result = {"Margin required": position_value / leverage}
    if entry:
        move = 1 / leverage
        liq = entry * (1 - move) if side == "Buy" else entry * (1 + move)
        result["Approx. liquidation price"] = liq
    return result
