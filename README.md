# Rosa's Pizza web app

A Streamlit app that recommends the delivery promise time for Rosa's Pizza.
Select a zone and a time block, choose a range of promised times to try, and
adjust the cost assumptions (profit margin, churn per late order, refund per
late order). The app returns the promise with the highest simulated net profit.

- `funcs.py`: analysis functions (no Streamlit code)
- `main.py`: Streamlit interface

## Run

```bash
uv sync
uv run streamlit run main.py
```
