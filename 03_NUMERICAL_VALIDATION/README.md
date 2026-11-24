# Scalar numerical-validation materials

## Scope

This directory contains the separately documented scalar numerical-verification tests used to check selected numerical schemes in the manuscript:

1. A constant-order Caputo L1 scalar relaxation test, compared with the exact Mittag–Leffler solution.
2. A selected terminal-time variable-order endpoint-refinement test.
3. A manufactured-solution test with `x*(t) = t^2` for the specified terminal-time variable-order operator.

These are numerical test problems with known/reference solutions. They are **not** empirical calibration of the microbial-inoculation data and do **not** validate crop-specific biological parameters or the proposed crop–microbe–nitrogen model.

## Files

- `scripts/numerical_validation.py` — executable numerical verification workflow.
- `scripts/verify_source_workbook.py` — checks byte size and SHA-256 for the source workbook.
- `scripts/download_source_workbook.py` — helper to retrieve the published Supplementary Table S1 workbook.
- `outputs/constant_order_L1_recomputed.csv` — constant-order numerical results.
- `outputs/variable_order_endpoint_recomputed.csv` — selected variable-order endpoint results.
- `outputs/variable_order_manufactured_recomputed.csv` — manufactured-solution results.
- `reports/NUMERICAL_VALIDATION_RUN_LOG.txt` — execution environment and run summary.
- `requirements.txt` — dependencies for this numerical workflow.

## Run

From the repository root:

```bash
python -m pip install -r 03_NUMERICAL_VALIDATION/requirements.txt
python 03_NUMERICAL_VALIDATION/scripts/numerical_validation.py \
  --output-dir 03_NUMERICAL_VALIDATION/outputs_reproduced
```

The source workbook is included separately in `01_SOURCE_DATA/`. The empirical reanalysis is in `02_EMPIRICAL_ANALYSIS/` and is run independently using its own requirements file and script. The original historical Colab notebook was not recovered; the empirical script is a documented reconstruction. See the root `README.md` and `02_EMPIRICAL_ANALYSIS/README.md` for the correct empirical scope and limitations.
