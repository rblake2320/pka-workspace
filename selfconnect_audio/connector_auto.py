"""
Auto-detect connector — picks SDK or Enterprise mode at runtime.

Priority:
  1. If context.enterprise_available → EnterpriseConnector
  2. If context.sdk_available        → SDKConnector
  3. Otherwise                       → NullConnector (logs, no mesh integration)

The connector mode can also be forced via config:
  connector: "sdk" | "enterprise" | "auto"
"""

from __future__ import annotations

import logging

from .bus import AudioEventBus
from .connector_sdk import SDKConnector
from .connector_enterprise import EnterpriseConnector

log = logging.getLogger(__name__)


class NullConnector:
    """No-op connector when neither SDK nor enterprise is available."""
    mode = "none"

    def start(self): log.warning("NullConnector: no SelfConnect available — mesh integration disabled")
    def close(self): pass


def make_connector(context, bus: AudioEventBus, forced_mode: str = "auto"):
    """
    Create the right connector based on available layers and forced_mode config.

    Args:
        context:      PluginContext with sdk_available / enterprise_available flags
        bus:          AudioEventBus instance
        forced_mode:  "auto" | "sdk" | "enterprise"
    """
    if forced_mode == "enterprise":
        if context.enterprise_available:
            return EnterpriseConnector(context, bus)
        log.warning("Forced enterprise mode but enterprise not available — falling back to SDK")

    if forced_mode == "sdk":
        if context.sdk_available:
            return SDKConnector(context, bus)
        log.warning("Forced SDK mode but SDK not available — using NullConnector")
        return NullConnector()

    # Auto-detect
    if context.enterprise_available:
        log.info("Auto-detected enterprise layer — using EnterpriseConnector")
        return EnterpriseConnector(context, bus)

    if context.sdk_available:
        log.info("Auto-detected SDK layer — using SDKConnector")
        return SDKConnector(context, bus)

    log.warning("Neither enterprise nor SDK is available — mesh integration disabled")
    return NullConnector()
