#!/usr/bin/env python3
"""
Skip Hire AI MCP Server
=======================
By MEOK AI Labs | https://meok.ai

UK Waste Carrier Registration, EA waste codes, hazardous waste consignment notes for skip hire and waste transport operators.

Install: pip install skip-hire-ai-mcp
Run:     python server.py
"""

import json
import sys
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.mcpserver import MCPServer as FastMCP  # mcp 2.x: FastMCP renamed MCPServer

import os as _os
import urllib.request as _meter_urlreq
import urllib.error as _meter_urlerr

_MEOK_API_KEY = _os.environ.get("MEOK_API_KEY", "")

try:
    sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
    from auth_middleware import check_access as _shared_check_access
    _AUTH_ENGINE_AVAILABLE = True
except ImportError:
    _AUTH_ENGINE_AVAILABLE = False

    def _shared_check_access(api_key: str = ""):
        """Fallback when shared auth engine is not available."""
        if _MEOK_API_KEY and api_key and api_key == _MEOK_API_KEY:
            return True, "OK", "pro"
        if _MEOK_API_KEY and api_key and api_key != _MEOK_API_KEY:
            return False, "Invalid API key. Get one at https://meok.ai/api-keys", "free"
        return True, "OK", "free"


def check_access(api_key: str = ""):
    return _shared_check_access(api_key)


FREE_DAILY_LIMIT = 50
_usage: dict[str, list[datetime]] = defaultdict(list)
STRIPE_PRO = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"


def _rl(tier="free") -> Optional[str]:
    if tier in ("pro", "professional", "enterprise"):
        return None
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    _usage["anonymous"] = [t for t in _usage["anonymous"] if t > cutoff]
    if len(_usage["anonymous"]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit ({FREE_DAILY_LIMIT}/day). Pro £79/mo: {STRIPE_PRO}"
    _usage["anonymous"].append(now)
    return None


mcp = FastMCP(
    "Skip Hire AI",
    instructions=(
        "By MEOK AI Labs — UK Waste Carrier Registration, EA waste codes, hazardous waste consignment notes for skip hire and waste transport operators. "
        "Free tier: 10/day. Pro tier: unlimited. "
        "Pairs with attestation API for cryptographically signed compliance certs."
    ),
)

def _server_meter_check(api_key: str = "") -> dict:
    """Calls the live /verify endpoint for server-side metering. Returns the JSON dict.
    Fail-open: if /verify is unreachable or KV isn't configured, returns allowed=True
    (so the local rate-limit in _check_rate_limit remains the safety net)."""
    try:
        data = json.dumps({"api_key": api_key, "tool": ""}).encode()
        req = _meter_urlreq.Request(_METER_URL, data=data,
            headers={"Content-Type": "application/json"}, method="POST")
        with _meter_urlreq.urlopen(req, timeout=2.5) as r:
            d = json.loads(r.read())
            if isinstance(d, dict) and "allowed" in d:
                return d
    except Exception:
        pass
    return {"allowed": True, "tier": "anonymous", "remaining": 200, "upgrade_url": "https://meok.ai/pricing"}


_METER_URL = "https://proofof.ai/verify"


@mcp.tool()
def check_waste_carrier_registration(query: str = "", api_key: str = "") -> str:
    """EA waste carrier registration status verification

    Args:
        query: Optional query or identifier (e.g., VRM, card number, project ID).
        api_key: Optional MEOK API key.

    Returns: JSON with assessment, references, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "check_waste_carrier_registration",
        "query": query,
        "status": "stub",
        "tool_description": "EA waste carrier registration status verification",
        "note": "Initial scaffold — full logic ships in v1.1. Pair with meok-attestation-api for signed compliance certs.",
        "regulation_refs": [],
        "next_step": "POST to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance attestation",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo unlocks signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def ewc_code_lookup(query: str = "", api_key: str = "") -> str:
    """European Waste Catalogue code lookup with hazardous flagging

    Args:
        query: Optional query or identifier (e.g., VRM, card number, project ID).
        api_key: Optional MEOK API key.

    Returns: JSON with assessment, references, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "ewc_code_lookup",
        "query": query,
        "status": "stub",
        "tool_description": "European Waste Catalogue code lookup with hazardous flagging",
        "note": "Initial scaffold — full logic ships in v1.1. Pair with meok-attestation-api for signed compliance certs.",
        "regulation_refs": [],
        "next_step": "POST to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance attestation",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo unlocks signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def consignment_note_template(query: str = "", api_key: str = "") -> str:
    """Hazardous waste consignment note generator

    Args:
        query: Optional query or identifier (e.g., VRM, card number, project ID).
        api_key: Optional MEOK API key.

    Returns: JSON with assessment, references, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "consignment_note_template",
        "query": query,
        "status": "stub",
        "tool_description": "Hazardous waste consignment note generator",
        "note": "Initial scaffold — full logic ships in v1.1. Pair with meok-attestation-api for signed compliance certs.",
        "regulation_refs": [],
        "next_step": "POST to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance attestation",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo unlocks signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def waste_transfer_note(query: str = "", api_key: str = "") -> str:
    """Section 34 waste transfer note generator

    Args:
        query: Optional query or identifier (e.g., VRM, card number, project ID).
        api_key: Optional MEOK API key.

    Returns: JSON with assessment, references, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "waste_transfer_note",
        "query": query,
        "status": "stub",
        "tool_description": "Section 34 waste transfer note generator",
        "note": "Initial scaffold — full logic ships in v1.1. Pair with meok-attestation-api for signed compliance certs.",
        "regulation_refs": [],
        "next_step": "POST to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance attestation",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo unlocks signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)


@mcp.tool()
def duty_of_care_check(query: str = "", api_key: str = "") -> str:
    """Environment Protection Act duty of care compliance scan

    Args:
        query: Optional query or identifier (e.g., VRM, card number, project ID).
        api_key: Optional MEOK API key.

    Returns: JSON with assessment, references, and recommended actions.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_PRO})
    if err := _rl(tier):
        return json.dumps({"error": err, "upgrade_url": STRIPE_PRO})

    return json.dumps({
        "tool": "duty_of_care_check",
        "query": query,
        "status": "stub",
        "tool_description": "Environment Protection Act duty of care compliance scan",
        "note": "Initial scaffold — full logic ships in v1.1. Pair with meok-attestation-api for signed compliance certs.",
        "regulation_refs": [],
        "next_step": "POST to https://meok-attestation-api.vercel.app/sign for HMAC-signed compliance attestation",
        "tier": tier,
        "upsell_pro": f"Pro £79/mo unlocks signed attestations + unlimited calls: {STRIPE_PRO}" if tier == "free" else None,
    }, indent=2)



# ---------------------------------------------------------------------------
# MCP 2026-07-28 wire - header-add migration ({DATE})
# ---------------------------------------------------------------------------
# stdio carries no HTTP headers, so Mcp-Method / Mcp-Name are not applicable to
# this transport at runtime. When {repo} is exposed over HTTP, route the ingress
# through the vendored mcp2026_shim (ShimASGI): it validates Mcp-Method /
# Mcp-Name, injects params._meta.protocolVersion = "2026-07-28" into every
# request, strips Mcp-Session-Id and answers legacy initialize / server-discover
# locally (the session header is never emitted - stateless wire).
# Refs: MIGRATION_NOTE.md, MCP_2026_WIRE_MIGRATION_PLAN_2026-10-07.md (3) + (4).
# ---------------------------------------------------------------------------


def http_app():
    """ASGI app for HTTP exposure, wrapped in the 2026-07-28 wire shim.

    stdio (``mcp.run()``) needs no shim; this is the enable path once the
    server is fronted by an HTTP transport. Bodies are buffered, so responses
    are requested in JSON mode rather than SSE.
    """
    from mcp2026_shim import WIRE_2026, ShimASGI, ShimConfig

    return ShimASGI(
        mcp.streamable_http_app(json_response=True),
        ShimConfig(
            protocol_version=WIRE_2026,
            server_info={"name": "skip-hire-ai-mcp", "version": "1.0.5"},
        ),
    )

def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
