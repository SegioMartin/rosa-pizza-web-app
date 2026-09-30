import streamlit as st
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE

from funcs import choose_best_promise

st.set_page_config(page_title="Rosa's Pizza - Promise Time", page_icon="🍕")

st.title("🍕 Rosa's Pizza: best delivery promise")
st.write(
    "Pick a zone and a time block, choose which promised delivery times to "
    "try, and adjust the cost assumptions. The app simulates four weeks of "
    "orders for each promise and recommends the one with the highest net profit."
)

# --- Zone and time block ---
st.header("1. Zone and time block")
col_zone, col_block = st.columns(2)
zone = col_zone.selectbox("Zone", ZONES)
time_block = col_block.selectbox("Time block", TIME_BLOCKS)

# --- Promise range ---
st.header("2. Promised times to try")
promise_min, promise_max = st.slider(
    "Range of promised delivery times (minutes)",
    min_value=10,
    max_value=120,
    value=(30, 60),
    help=f"Today's promise is {PROMISE} minutes in every zone.",
)
step = st.number_input(
    "Step between promises (minutes)", min_value=1, max_value=60, value=5, step=1
)
promises = list(range(promise_min, promise_max + 1, int(step)))
st.caption(f"Promises to try: {', '.join(str(p) for p in promises)}")

# --- Costs ---
st.header("3. Cost assumptions")
col_margin, col_churn, col_refund = st.columns(3)
margin = col_margin.number_input(
    "Profit margin per order ($)",
    min_value=0.0,
    value=COSTS["margin"],
    step=0.5,
)
churn_orders = col_churn.number_input(
    "Future orders lost per late order",
    min_value=0.0,
    value=COSTS["churn_orders"],
    step=0.1,
)
refund = col_refund.number_input(
    "Refund per late order ($)",
    min_value=0.0,
    value=COSTS["refund"],
    step=0.5,
)

inputs_valid = True
if margin <= 0:
    st.error("Profit margin per order must be greater than $0.")
    inputs_valid = False

costs = {"refund": refund, "churn_orders": churn_orders, "margin": margin}

# --- Recommendation ---
st.header("4. Recommendation")
current_inputs = (zone, time_block, tuple(promises), tuple(sorted(costs.items())))

if st.button("Recommend promise time", type="primary", disabled=not inputs_valid):
    best_promise, best_net_profit = choose_best_promise(
        zone, time_block, promises, costs
    )
    st.session_state["result"] = (best_promise, best_net_profit)
    st.session_state["result_inputs"] = current_inputs

if "result" in st.session_state:
    best_promise, best_net_profit = st.session_state["result"]
    result_zone, result_block = st.session_state["result_inputs"][:2]

    if st.session_state["result_inputs"] != current_inputs:
        st.info("Inputs have changed. Click the button again to update the result.")

    if best_promise == 0 and best_net_profit == 0:
        st.warning(
            "No promise in the selected range gives a positive net profit "
            f"for {result_zone} / {result_block}."
        )
    else:
        st.subheader(f"{result_zone} / {result_block}")
        col_promise, col_profit = st.columns(2)
        col_promise.metric("Recommended promise", f"{best_promise:.0f} min")
        col_profit.metric("Net profit (4 weeks)", f"${best_net_profit:,.2f}")
