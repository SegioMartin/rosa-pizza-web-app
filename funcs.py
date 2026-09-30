import numpy as np
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times

SEED = 13  # fixed seed so simulated results are reproducible

def late_rate(
    zone: str = "all", time_block: str = "all", promise: float = PROMISE
) -> float:

    # it is better to check here whether zone and time_block are valid

    zones = ZONES if zone == "all" else [zone]
    time_blocks = TIME_BLOCKS if time_block == "all" else [time_block]

    all_delivery_times = []

    for zone in zones:
        for time_block in time_blocks:
            times = delivery_times(
                zone,
                time_block,
                promise,
                seed = SEED
            )
            all_delivery_times.extend(times)

    all_delivery_times = np.array(all_delivery_times)

    late_orders = np.sum(all_delivery_times > promise)
    # if there is no use of numpy: late_orders = sum([time for time in all_delivery_times if time > promise])
    # BUT numpy is faster (as it is made with C/C++) and more effective in general
    total_orders = len(all_delivery_times)

    return float(late_orders / total_orders * 100)

def average_delivery_time(
    zone: str = "all",
    time_block: str = "all",
    promise: float = PROMISE
) -> float:

    zones = ZONES if zone == "all" else [zone]
    time_blocks = TIME_BLOCKS if time_block == "all" else [time_block]

    all_delivery_times = []

    for current_zone in zones:
        for current_time_block in time_blocks:
            times = delivery_times(
                current_zone,
                current_time_block,
                promise,
                seed = SEED
            )
            all_delivery_times.extend(times)

    return float(np.mean(all_delivery_times))

def total_cost_per_late_order(
    costs: dict[str, float] = COSTS
) -> float:
    refund_cost = costs["refund"] #refund per a late order
    churn_cost = costs["churn_orders"] * costs["margin"] #future customers loss

    return float(refund_cost + churn_cost)

def choose_best_promise(
    zone: str,
    time_block: str,
    promises: list[float],
    costs: dict[str, float] = COSTS
) -> tuple[float, float]:

    late_order_cost = total_cost_per_late_order(costs)

    # initialyzing these variables in case there is no net_profit > best_net_profit case
    # so, if function returns (0, 0), it means there is no positive net_profit for provided promises
    best_promise = 0
    best_net_profit = 0

    for promise in promises:
        times = delivery_times(
            zone,
            time_block,
            promise,
            seed = SEED
        )

        total_orders = len(times)
        late_orders = int(np.sum(times > promise))

        revenue_profit = total_orders * costs["margin"]
        late_costs = late_orders * late_order_cost
        net_profit = revenue_profit - late_costs

        if net_profit > best_net_profit:
            best_promise = promise
            best_net_profit = net_profit

    return float(best_promise), float(best_net_profit)