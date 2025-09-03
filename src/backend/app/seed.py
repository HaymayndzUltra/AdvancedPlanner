from collections.abc import Iterable

from .models import TaskCreate
from .storage import store


def load_seed_data() -> None:
    examples: Iterable[TaskCreate] = [
        TaskCreate(title="Write docs", description="Draft service docs"),
        TaskCreate(title="Add tests", description="Ensure 80%+ coverage"),
        TaskCreate(title="Profile performance", description="Establish perf baseline"),
    ]
    for example in examples:
        base = example.title.strip().lower().replace(" ", "-")
        suffix = 1
        candidate = base
        while store.get_task(candidate) is not None:
            suffix += 1
            candidate = f"{base}-{suffix}"
        store.create_task(candidate, example)

