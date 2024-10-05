from dataclasses import dataclass, field
from typing import List

@dataclass
class Course:
    title: str
    code: str
    description: str