from pydantic import BaseModel
from typing import List

class Package(BaseModel):
    package_list: List[str]
    transitive_stack: List[str] = []
    comp_package_count_threshold: int = None

class Packages(BaseModel):
    packages: List[Package]
