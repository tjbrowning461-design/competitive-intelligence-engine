from datetime import datetime
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright


MAX_CHARS_PER_PAGE = 15000
MAX_TOTAL_CHARS = 80000


DEFAULT_EXCLUDED_PATTERNS = [
    "login",
    "sign-in",
    "signin",
    "signup",
    "sign-up",
    "careers",
    "jobs",
    "privacy",
    "terms",
    "cookie",
    "contact",
    "accessibility",
]


def current_timestamp():

    return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )


def root_domain(url):

    hostname = (
        urlparse(url).hostname
        or ""
    ).lower()

    if hostname.startswith("www."):
        hostname = hostname[4:]

    return hostname


def clean_url(url):

    return (
        url.split("#")[0]
        .rstrip("/")
    )


def is_allowed_domain(
    candidate_url,
    base_url
):

    candidate = root_domain(
        candidate_url
    )

    base = root_domain(
        base_url
    )

    return (
        candidate == base
        or candidate.endswith(
            "." + base
        )
    )


def collect_links(
    browser,
    base_url,
    ignore_https_errors=False
):

    context = browser.new_context(
        ignore_https_errors=
            ignore_https_errors
    )

    page = context.new_page()

    try:

        page.goto(
            base_url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(
            2500
        )

        links = page.locator(
            "a"
        ).evaluate_all(
            """
            elements => elements.map(
                element => ({
                    href:
                        element.href || "",
                    text:
                        element.innerText || ""
                })
            )
            """
        )

        return links

    finally:

        context.close()


def discover_pages(
    base_url,
    page_categories,
    excluded_patterns=None
):

    print(
        "\nDiscovering useful pages..."
    )

    if excluded_patterns is None:

        excluded_patterns = (
            DEFAULT_EXCLUDED_PATTERNS
        )

    links = []

    with sync_playwright() as playwright:

        browser = (
            playwright.chromium.launch(
                headless=True
            )
        )

        try:

            try:

                links = collect_links(
                    browser,
                    base_url,
                    ignore_https_errors=False
                )

            except Exception as error:

                error_text = str(error)

                if "ERR_CERT" in error_text:

                    print(
                        "Certificate issue detected. "
                        "Retrying this public site "
                        "while ignoring the invalid "
                        "certificate..."
                    )

                    try:

                        links = collect_links(
                            browser,
                            base_url,
                            ignore_https_errors=True
                        )

                    except Exception as retry_error:

                        print(
                            "Could not discover "
                            f"additional pages: "
                            f"{retry_error}"
                        )

                        links = []

                else:

                    print(
                        "Could not discover "
                        f"additional pages: "
                        f"{error}"
                    )

                    links = []

        finally:

            browser.close()

    candidates = []

    for link in links:

        href = link.get(
            "href",
            ""
        )

        text = link.get(
            "text",
            ""
        )

        if not href:
            continue

        full_url = urljoin(
            base_url,
            href
        )

        full_url = clean_url(
            full_url
        )

        if not full_url.startswith(
            ("http://", "https://")
        ):
            continue

        if not is_allowed_domain(
            full_url,
            base_url
        ):
            continue

        searchable_text = (
            full_url.lower()
            + " "
            + text.lower()
        )

        if any(
            pattern in searchable_text
            for pattern
            in excluded_patterns
        ):
            continue

        candidates.append(
            {
                "url": full_url,
                "text": text
            }
        )

    selected_pages = [
        (
            "homepage",
            clean_url(base_url)
        )
    ]

    used_urls = {
        clean_url(base_url)
    }

    for category, keywords in (
        page_categories.items()
    ):

        best_url = None
        best_score = 0

        for candidate in candidates:

            url = candidate[
                "url"
            ]

            if url in used_urls:
                continue

            anchor_text = candidate[
                "text"
            ].lower()

            url_lower = url.lower()

            score = 0

            for keyword in keywords:

                keyword = (
                    keyword.lower()
                )

                if keyword in anchor_text:
                    score += 10

                if keyword in url_lower:
                    score += 15

            if score > best_score:

                best_score = score
                best_url = url

        if best_url:

            selected_pages.append(
                (
                    category,
                    best_url
                )
            )

            used_urls.add(
                best_url
            )

    return selected_pages


def scrape_single_page(
    browser,
    url,
    ignore_https_errors=False
):

    context = browser.new_context(
        ignore_https_errors=
            ignore_https_errors
    )

    page = context.new_page()

    try:

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(
            2500
        )

        text = (
            page.locator("body")
            .inner_text()
        )

        clean_lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:

                clean_lines.append(
                    line
                )

        return "\n".join(
            clean_lines
        )

    finally:

        context.close()


def scrape_pages(
    selected_pages,
    max_chars_per_page=
        MAX_CHARS_PER_PAGE,
    max_total_chars=
        MAX_TOTAL_CHARS
):

    collected_text = []
    sources = []

    with sync_playwright() as playwright:

        browser = (
            playwright.chromium.launch(
                headless=True
            )
        )

        try:

            for category, url in (
                selected_pages
            ):

                print(
                    f"\nScraping "
                    f"[{category.upper()}]: "
                    f"{url}"
                )

                try:

                    try:

                        clean_text = (
                            scrape_single_page(
                                browser,
                                url,
                                ignore_https_errors=False
                            )
                        )

                    except Exception as error:

                        if "ERR_CERT" in str(error):

                            print(
                                "Certificate issue "
                                "detected. Retrying..."
                            )

                            clean_text = (
                                scrape_single_page(
                                    browser,
                                    url,
                                    ignore_https_errors=True
                                )
                            )

                        else:

                            raise

                    clean_text = (
                        clean_text[
                            :max_chars_per_page
                        ]
                    )

                    print(
                        f"Captured "
                        f"{len(clean_text)} "
                        f"characters."
                    )

                    sources.append(
                        {
                            "url": url,
                            "category":
                                category,
                            "collected_at":
                                current_timestamp()
                        }
                    )

                    collected_text.append(
                        f"""
=== {category.upper()} SOURCE ===
URL: {url}

{clean_text}
"""
                    )

                except Exception as error:

                    print(
                        f"Could not scrape "
                        f"{url}: {error}"
                    )

                    print(
                        "Skipping this page "
                        "and continuing."
                    )

        finally:

            browser.close()

    combined_text = "\n".join(
        collected_text
    )

    return (
        combined_text[
            :max_total_chars
        ],
        sources
    )