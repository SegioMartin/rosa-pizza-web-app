---
name: notebook-to-streamlit
description: Use when adding a Streamlit front end to an existing
  Jupyter Notebook or Python analysis. Covers separating analytical
  logic from interface code, connecting existing functions to widgets,
  dependency management, and rerun-safe state. Not for replacing the
  original analysis or building an unrelated app from scratch.
---

## Step 1 — Inspect the existing functions

Read the notebook functions and identify:

- reusable functions;
- required imports and dependencies;
- input parameters;
- returned values;
- validation rules;
- example calls and expected outputs.

Preserve the existing analytical approach unless the user explicitly
asks for changes. Do not edit protected starter files.

## Step 2 — Separate reusable logic

Move reusable calculations into a Python module, such as
`funcs.py`.

The analysis module should:

- contain no Streamlit imports;
- avoid interface-specific code;
- avoid unnecessary printing;
- accept inputs as function arguments;
- return values that the interface can display;
- keep the same defaults and calculations as the notebook.

The Streamlit file should be responsible for the interface only.

## Step 3 — Connect logic to the interface

Map interface values to the existing function arguments.

Validate user input before calling analytical functions. Keep
validation and error messages clear and close to the relevant input.

Do not duplicate calculations in the Streamlit file. Import and call
the existing functions instead.

## Step 4 — Manage dependencies

Use the project's existing dependency manager and preserve its
configuration.

Add only the dependencies required by the analysis and Streamlit
interface. Make sure the application can be run from a clean
environment using the project's documented command.