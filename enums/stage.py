from enum import Enum


class Stage(Enum):
    queue = 'in queue'
    processing = 'in processing'
    complete = 'complete'
