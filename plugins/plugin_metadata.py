from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class PluginMetadata:
    """
    Immutable descriptive metadata for a Cipher plugin.

    Unlike PluginManifest (runtime/plugin loading),
    this class represents metadata that can be displayed
    in the Plugin Manager UI or used for searching.
    """

    name: str

    version: str

    author: str

    description: str

    category: str = "General"

    homepage: str = ""

    repository: str = ""

    license: str = ""

    tags: List[str] = field(default_factory=list)

    dependencies: List[str] = field(default_factory=list)

    min_cipher_version: str = "1.0.0"

    icon: str = ""

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "PluginMetadata":

        return cls(
            name=data.get("name", ""),
            version=data.get("version", "1.0.0"),
            author=data.get("author", ""),
            description=data.get("description", ""),
            category=data.get("category", "General"),
            homepage=data.get("homepage", ""),
            repository=data.get("repository", ""),
            license=data.get("license", ""),
            tags=list(data.get("tags", [])),
            dependencies=list(
                data.get("dependencies", [])
            ),
            min_cipher_version=data.get(
                "min_cipher_version",
                "1.0.0",
            ),
            icon=data.get("icon", ""),
        )

    @property
    def identifier(self) -> str:
        """
        Unique identifier for this plugin.
        """

        return f"{self.name}@{self.version}"

    @property
    def has_dependencies(self) -> bool:

        return bool(self.dependencies)

    @property
    def has_repository(self) -> bool:

        return bool(self.repository)

    @property
    def has_homepage(self) -> bool:

        return bool(self.homepage)