"""Pytest suite for the Star-tree implementation."""

from __future__ import annotations

import random
from typing import List, Tuple

import pytest

from src.algorithm.star_tree import StarNode, StarTree


DIMENSION_NAMES: Tuple[str, ...] = (
    "Time_Period",
    "Region",
    "City",
    "Category",
    "Customer_Type",
    "Payment_Method",
)


def generate_synthetic_data(
    num_rows: int = 2000,
    seed: int = 42,
) -> Tuple[List[List[int]], List[float], List[int]]:
    """Create deterministic synthetic integer-encoded retail data."""

    rng = random.Random(seed)
    transactions: List[List[int]] = []
    sales_values: List[float] = []
    counts: List[int] = []

    for _ in range(num_rows):
        transaction = [
            rng.randint(0, 3),
            rng.randint(0, 4),
            rng.randint(0, 5),
            rng.randint(0, 3),
            rng.randint(0, 2),
            rng.randint(0, 4),
        ]
        transactions.append(transaction)
        sales_values.append(float(rng.randint(1, 12)))
        counts.append(rng.randint(1, 3))

    return transactions, sales_values, counts


def test_star_tree_initializes_successfully() -> None:
    """The tree should initialize with a compact root node."""

    tree = StarTree(min_sup=10.0)

    assert tree.root.attr_name == "ROOT"
    assert tree.root.attr_value == "ROOT"
    assert tree.root.total_sales == 0.0
    assert tree.root.count_txn == 0
    assert not hasattr(tree.root, "__dict__")
    assert StarNode.__slots__ == (
        "attr_name",
        "attr_value",
        "children",
        "total_sales",
        "count_txn",
    )


def test_empty_tree_returns_empty() -> None:
    """No transactions should produce an empty cube result."""

    tree = StarTree(min_sup=10.0)

    assert tree.simultaneous_aggregation() == []


def test_transaction_length_mismatch_raises() -> None:
    """Transactions with invalid length should raise a ValueError."""

    tree = StarTree(min_sup=10.0)

    with pytest.raises(ValueError):
        tree.insert_transaction([1, 2, 3], sales=1.0, count=1)


def test_high_support_branch_is_preserved() -> None:
    """A branch with enough sales should stay concrete in the cube output."""

    tree = StarTree(min_sup=15.0)
    transaction = [1, 2, 3, 4, 5, 6]

    tree.insert_transaction(transaction, sales=20.0, count=1)
    rows = tree.simultaneous_aggregation()

    assert any(
        all(row[dimension] == value for dimension, value in zip(DIMENSION_NAMES, transaction))
        and row["total_sales"] == pytest.approx(20.0)
        and row["count_txn"] == 1
        for row in rows
    )


def test_min_sup_boundary_is_kept() -> None:
    """Rows with total_sales equal to min_sup should remain in the cube."""

    tree = StarTree(min_sup=10.0)
    transaction = [1, 1, 1, 1, 1, 1]

    tree.insert_transaction(transaction, sales=10.0, count=2)
    rows = tree.simultaneous_aggregation()

    assert any(
        all(row[dimension] == value for dimension, value in zip(DIMENSION_NAMES, transaction))
        and row["total_sales"] == pytest.approx(10.0)
        and row["count_txn"] == 2
        for row in rows
    )


def test_low_support_branch_rolls_up_to_all() -> None:
    """A low-support leaf should be compressed into a row that contains ALL."""

    tree = StarTree(min_sup=15.0)
    tree.insert_transaction([0, 0, 0, 0, 0, 0], sales=10.0, count=1)
    tree.insert_transaction([0, 0, 0, 0, 0, 1], sales=10.0, count=1)

    rows = tree.simultaneous_aggregation()

    assert any(
        row["Time_Period"] == 0
        and row["Region"] == 0
        and row["City"] == 0
        and row["Category"] == 0
        and row["Customer_Type"] == 0
        and row["Payment_Method"] == "ALL"
        and row["total_sales"] == pytest.approx(20.0)
        and row["count_txn"] == 2
        for row in rows
    )


def test_low_support_value_keeps_lower_dimensions() -> None:
    """Star reduction should not wipe out lower dimensions."""

    tree = StarTree(min_sup=15.0)
    tree.insert_transaction([0, 0, 0, 1, 1, 1], sales=8.0, count=1)
    tree.insert_transaction([0, 0, 1, 1, 1, 1], sales=8.0, count=1)

    rows = tree.simultaneous_aggregation()

    assert any(
        row["City"] == "ALL"
        and row["Category"] == 1
        and row["Customer_Type"] == 1
        and row["Payment_Method"] == 1
        and row["total_sales"] == pytest.approx(16.0)
        for row in rows
    )


def test_synthetic_data_smoke() -> None:
    """Synthetic thousands-row data should be ingestible and aggregatable."""

    transactions, sales_values, counts = generate_synthetic_data(num_rows=1200)
    tree = StarTree(min_sup=30.0)

    for transaction, sales, count in zip(transactions, sales_values, counts):
        tree.insert_transaction(transaction, sales=sales, count=count)

    rows = tree.simultaneous_aggregation()

    assert isinstance(rows, list)
    assert rows
    assert all(set(row).issuperset({*DIMENSION_NAMES, "total_sales", "count_txn"}) for row in rows)
