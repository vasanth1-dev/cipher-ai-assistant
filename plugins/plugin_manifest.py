from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PluginManifest:
    """
    Describes a Cipher plugin.

    This metadata is used by the Plugin Manager
    without importing the actual plugin module.
    """

    id: str
    name: str
    version: str
    author: str
    description: str = ""

    minimum_cipher_version: str = "2.0.0"

    enabled: bool = True

    entry_point: str = ""

    homepage: str = ""

    license: str = "MIT"

    tags: list[str] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)

    permissions: list[str] = field(default_factory=list)

    category: str = "General"

    # --------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "minimum_cipher_version": self.minimum_cipher_version,
            "enabled": self.enabled,
            "entry_point": self.entry_point,
            "homepage": self.homepage,
            "license": self.license,
            "tags": list(self.tags),
            "dependencies": list(self.dependencies),
            "permissions": list(self.permissions),
            "category": self.category,
        }

    # --------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            author=data["author"],
            description=data.get(
                "description",
                "",
            ),
            minimum_cipher_version=data.get(
                "minimum_cipher_version",
                "2.0.0",
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            entry_point=data.get(
                "entry_point",
                "",
            ),
            homepage=data.get(
                "homepage",
                "",
            ),
            license=data.get(
                "license",
                "MIT",
            ),
            tags=data.get(
                "tags",
                [],
            ),
            dependencies=data.get(
                "dependencies",
                [],
            ),
            permissions=data.get(
                "permissions",
                [],
            ),
            category=data.get(
                "category",
                "General",
            ),
        )