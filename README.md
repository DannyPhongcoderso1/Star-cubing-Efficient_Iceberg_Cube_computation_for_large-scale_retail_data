# Star-cubing Iceberg Cube Miner

Project Python + SQL for computing Iceberg Cube on large-scale retail POS data, with benchmark artifacts for Phase 6 (Task 13-15).

## Scope

- Iceberg cube computation with Star-tree aggregation.
- Comparative benchmark against BUC and Bottom-up.
- Log and chart artifacts for runtime, CPU/RAM, and output storage.

## Repository Layout

- `src/algorithm/star_tree.py`: Star-tree data structure and simultaneous aggregation.
- `src/algorithm/buc.py`: BUC iceberg cube implementation for benchmark.
- `src/algorithm/bottom_up.py`: Bottom-up cuboid enumeration implementation.
- `scripts/phase6_benchmark.py`: Benchmark runner and chart renderer.
- `docs/phase6/logs/`: Raw benchmark logs (`.csv`, `.json`) and summary.
- `docs/phase6/charts/`: Evidence charts (`runtime_line.png`, `memory_bar.png`, `storage_line.png`).
- `docs/phase6/`: Phase 6 documentation/report markdown files.

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Phase 6 Benchmark

Default profile (3 dataset sizes, 1 repeat each):

```bash
python scripts/phase6_benchmark.py --sizes 2000,5000,10000 --repeats 1 --min-sup 18000000
```

Custom profile example:

```bash
python scripts/phase6_benchmark.py --sizes 5000,10000,20000 --repeats 2 --min-sup 25000000 --seed 20260418
```

## Benchmark Outputs

After each successful run:

- `docs/phase6/logs/performance_log.csv`: Detailed run-level metrics.
- `docs/phase6/logs/performance_log.json`: JSON version for downstream tooling.
- `docs/phase6/logs/summary_by_algorithm.csv`: Mean metrics by algorithm.
- `docs/phase6/charts/runtime_line.png`: Runtime vs dataset size.
- `docs/phase6/charts/memory_bar.png`: Mean memory peak comparison.
- `docs/phase6/charts/storage_line.png`: Output storage trend.

## Documentation for Reporting

- `docs/phase6/phase6_algorithm_spec.md`: Task 15 technical specification and setup guide.
- `docs/phase6/phase6_report.md`: Phase 6 evidence report for Word/slide integration.
