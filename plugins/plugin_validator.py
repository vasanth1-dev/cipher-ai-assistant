from __future__ import annotations

from typing import List

from core.logger import logger
from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest


class PluginValidator:
    """
    Validates plugin classes and manifests before registration.

    This validator performs structural checks only.
    It does not import or execute plugin code.
    """

    REQUIRED_MANIFEST_FIELDS = (
        "name",
        "version",
        "author",
        "description",
    )

    # --------------------------------------------------
    # Plugin Validation
    # --------------------------------------------------

    @classmethod
    def validate_plugin(
        cls,
        plugin: BasePlugin,
    ) -> bool:

        errors = cls.validate_manifest(plugin.manifest)

        if errors:

            logger.error(
                "Plugin '%s' validation failed.",
                plugin.__class__.__name__,
            )

            for error in errors:
                logger.error(error)

            return False

        return True

    # --------------------------------------------------
    # Manifest Validation
    # --------------------------------------------------

    @classmethod
    def validate_manifest(
        cls,
        manifest: PluginManifest,
    ) -> List[str]:

        errors: List[str] = []

        if not isinstance(manifest, PluginManifest):

            errors.append(
                "Invalid PluginManifest instance."
            )

            return errors

        # -----------------------------
        # Required fields
        # -----------------------------

        for field in cls.REQUIRED_MANIFEST_FIELDS:

            value = getattr(
                manifest,
                field,
                None,
            )

            if value is None:

                errors.append(
                    f"Manifest field '{field}' is missing."
                )

                continue

            if isinstance(value, str):

                if not value.strip():

                    errors.append(
                        f"Manifest field '{field}' is empty."
                    )

        # -----------------------------
        # Version
        # -----------------------------

        if not isinstance(manifest.version, str):

            errors.append(
                "Version must be a string."
            )

        # -----------------------------
        # Dependencies
        # -----------------------------

        dependencies = getattr(
            manifest,
            "dependencies",
            [],
        )

        if dependencies is None:
            dependencies = []

        if not isinstance(dependencies, list):

            errors.append(
                "Dependencies must be a list."
            )

        # -----------------------------
        # Keywords
        # -----------------------------

        keywords = getattr(
            manifest,
            "keywords",
            [],
        )

        if keywords is None:
            keywords = []

        if not isinstance(keywords, list):

            errors.append(
                "Keywords must be a list."
            )

        return errors

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    @staticmethod
    def is_valid(
        manifest: PluginManifest,
    ) -> bool:

        return (
            len(
                PluginValidator.validate_manifest(
                    manifest
                )
            )
            == 0
        )