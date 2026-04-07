from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import sys
import threading
import uuid
import webbrowser
from urllib.parse import urlparse

from i18n import t


@dataclass
class WebsiteButtonProfile:
    id: str
    label: str
    links: list[str]


DEFAULT_PROFILES = [
    WebsiteButtonProfile(
        id="study",
        label="Study",
        links=[
            "https://www.wikipedia.org/",
            "https://www.khanacademy.org/",
            "https://scholar.google.com/",
        ],
    )
]


def profiles_file_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        base_dir = Path(local_app_data) / "BleemBox"
    else:
        base_dir = Path.home() / ".bleembox"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "website_buttons.json"


def load_website_profiles() -> list[WebsiteButtonProfile]:
    path = profiles_file_path()
    if not path.exists():
        save_website_profiles(DEFAULT_PROFILES)
        return [WebsiteButtonProfile(item.id, item.label, list(item.links)) for item in DEFAULT_PROFILES]

    try:
        raw_items = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        save_website_profiles(DEFAULT_PROFILES)
        return [WebsiteButtonProfile(item.id, item.label, list(item.links)) for item in DEFAULT_PROFILES]

    profiles: list[WebsiteButtonProfile] = []
    for raw_item in raw_items if isinstance(raw_items, list) else []:
        if not isinstance(raw_item, dict):
            continue

        profile_id = str(raw_item.get("id") or uuid.uuid4())
        label = str(raw_item.get("label") or "").strip()
        links = raw_item.get("links") or []
        if not label or not isinstance(links, list):
            continue

        cleaned_links = [str(link).strip() for link in links if str(link).strip()]
        profiles.append(WebsiteButtonProfile(id=profile_id, label=label, links=cleaned_links))

    if not profiles:
        save_website_profiles(DEFAULT_PROFILES)
        return [WebsiteButtonProfile(item.id, item.label, list(item.links)) for item in DEFAULT_PROFILES]

    return profiles


def save_website_profiles(profiles: list[WebsiteButtonProfile]) -> None:
    payload = [asdict(profile) for profile in profiles]
    profiles_file_path().write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_links_text(links: list[str]) -> str:
    return "\n".join(links)


def parse_links_text(raw_text: str) -> list[str]:
    links = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if not links:
        raise ValueError(t("web_launcher.links_required"))
    return links


def create_empty_profile() -> WebsiteButtonProfile:
    return WebsiteButtonProfile(
        id=uuid.uuid4().hex,
        label=t("web_launcher.new_button_name"),
        links=["https://www.example.com/"],
    )


def update_profile(profile: WebsiteButtonProfile, label: str, raw_links: str) -> WebsiteButtonProfile:
    cleaned_label = label.strip()
    if not cleaned_label:
        raise ValueError(t("web_launcher.label_required"))

    links = parse_links_text(raw_links)
    return WebsiteButtonProfile(id=profile.id, label=cleaned_label, links=links)


def open_profile_links(profile: WebsiteButtonProfile) -> int:
    if not profile.links:
        raise ValueError(t("web_launcher.links_required"))

    opened_count = 0
    for link in profile.links:
        normalized_link = normalize_url(link)
        _open_url(normalized_link)
        opened_count += 1

    return opened_count


def normalize_url(url: str) -> str:
    cleaned = url.strip()
    parsed = urlparse(cleaned)
    if parsed.scheme:
        return cleaned
    return f"https://{cleaned}"


def _open_url(url: str) -> None:
    if sys.platform == "win32":
        threading.Thread(target=os.startfile, args=(url,), daemon=True).start()
        return

    webbrowser.open_new_tab(url)
