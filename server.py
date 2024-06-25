import random

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from optimization import Optimizer, Table


# -----------------------------------------
# funcs
# -----------------------------------------


def _check_table_can_solve(table: Table) -> bool:
    result_table = Optimizer.run(table=table)
    if result_table is not None:
        return True
    else:
        return False


def _solve_table(table: Table) -> Table:
    result_table = Optimizer.run(table=table)
    assert type(result_table) == Table
    return result_table


def _prepare_init_table(n_empty_cells: int) -> Table:
    seed = random.randint(1, 10000)
    empty_number_array = np.zeros(Table.table_size(), dtype=int)
    empty_table = Table(number_array=empty_number_array)
    result_table = Optimizer.run(table=empty_table, seed=seed)
    assert type(result_table) == Table
    result_table.convert_some_cells_to_zero(n_cells_to_zero=n_empty_cells, seed=seed)
    return result_table


# -----------------------------------------
# server
# -----------------------------------------


app = FastAPI()


class CanSolve(BaseModel):
    can_solve: bool


class NumberDict(BaseModel):
    number_dict: dict[int, dict[int, int]]


class NEmptyCells(BaseModel):
    n_empty_cells: int


@app.post("/api/check-table-can-solve", response_model=CanSolve)
def check_table_can_solve(number_dict: NumberDict):
    table = Table.from_number_dict(number_dict=number_dict.number_dict)
    can_solve = _check_table_can_solve(table=table)
    return {"can_solve": can_solve}


@app.post("/api/solve-table", response_model=NumberDict)
def solve_table(number_dict: NumberDict):
    init_table = Table.from_number_dict(number_dict=number_dict.number_dict)
    solved_table = _solve_table(table=init_table)
    return {"number_dict": solved_table.number_dict}


@app.post("/api/prepare-init-table", response_model=NumberDict)
def prepare_init_table(n_empty_cells: NEmptyCells):
    init_table = _prepare_init_table(n_empty_cells=n_empty_cells.n_empty_cells)
    return {"number_dict": init_table.number_dict}
