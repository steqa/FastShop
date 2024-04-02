from typing import Annotated

from fastapi import Query


class Pagination:
    def __init__(
            self,
            skip: Annotated[int, Query(ge=0)] = 0,
            limit: Annotated[int, Query(ge=1)] = 100
    ):
        self.skip = skip
        self.limit = limit
