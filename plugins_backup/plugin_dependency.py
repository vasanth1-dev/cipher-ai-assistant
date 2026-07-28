from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

from core.logger import logger


@dataclass(slots=True)
class PluginDependency:
    """
    Represents the dependency information for a plugin.
    """

    name: str
    requires: List[str] = field(default_factory=list)
    optional: List[str] = field(default_factory=list)


class PluginDependencyResolver:
    """
    Resolves plugin dependencies and computes a safe
    loading order.

    The resolver performs a topological sort and detects
    circular dependencies.
    """

    def __init__(
       self,
    ) -> None:

        self._plugins: Dict[str, PluginDependency] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        dependency: PluginDependency,
    ) -> None:

        self._plugins[dependency.name] = dependency

    def clear(self) -> None:

        self._plugins.clear()

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def missing_dependencies(
        self,
        plugin_name: str,
    ) -> List[str]:

        plugin = self._plugins.get(plugin_name)

        if plugin is None:
            return []

        return [
            dep
            for dep in plugin.requires
            if dep not in self._plugins
        ]

    # --------------------------------------------------
    # Resolution
    # --------------------------------------------------

    def resolve(self) -> List[str]:

        resolved: List[str] = []
        visiting: Set[str] = set()
        visited: Set[str] = set()

        def visit(name: str) -> None:

            if name in visited:
                return

            if name in visiting:
                raise RuntimeError(
                    f"Circular plugin dependency detected: {name}"
                )

            plugin = self._plugins.get(name)

            if plugin is None:
                raise RuntimeError(
                    f"Unknown plugin dependency: {name}"
                )

            visiting.add(name)

            for dependency in plugin.requires:

                visit(dependency)

            visiting.remove(name)
            visited.add(name)

            resolved.append(name)

        for name in sorted(self._plugins):

            visit(name)

        logger.info(
            "Resolved plugin load order: %s",
            " -> ".join(resolved),
        )

        return resolved