
import os
import re
import base64
from urllib.parse import unquote, urlparse
from playwright.sync_api import sync_playwright

COURSE = "https://vitolcc.vit.ac.in/course/view.php?id=72"
SAVE_DIR = "VIT_Course_PDFs_FINAL"

os.makedirs(SAVE_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(COURSE)

    print("Log in to VIT Moodle if required.")
    input("Expand all course sections, then press ENTER here: ")

    links = page.locator("a[href]").evaluate_all("""
        els => els.map(a => ({
            url: a.href,
            title: a.innerText.trim()
        }))
    """)

    targets = []
    for item in links:
        url = item["url"]
        if (
            "/mod/resource/view.php" in url
            or "/pluginfile.php/" in url
            or ".pdf" in url.lower()
        ):
            targets.append(item)

    # Remove duplicate URLs
    unique = {}
    for item in targets:
        unique[item["url"]] = item

    targets = list(unique.values())

    print(f"Found {len(targets)} resource links.")

    saved = 0

    for i, item in enumerate(targets, 1):
        url = item["url"]
        title = item["title"] or f"document_{i}"

        print(f"\n[{i}/{len(targets)}] {title}")

        try:
            result = page.evaluate("""
                async (url) => {
                    const response = await fetch(url, {
                        credentials: "include",
                        redirect: "follow"
                    });

                    const type = response.headers.get("content-type") || "";
                    const disposition =
                        response.headers.get("content-disposition") || "";

                    if (!response.ok) {
                        return {
                            error: "HTTP " + response.status,
                            type
                        };
                    }

                    if (!type.toLowerCase().includes("pdf")) {
                        return {
                            error: "Not a PDF",
                            type,
                            finalUrl: response.url
                        };
                    }

                    const buffer = await response.arrayBuffer();
                    const bytes = new Uint8Array(buffer);

                    let binary = "";
                    for (let i = 0; i < bytes.length; i += 8192) {
                        binary += String.fromCharCode(
                            ...bytes.subarray(i, i + 8192)
                        );
                    }

                    return {
                        data: btoa(binary),
                        disposition,
                        finalUrl: response.url,
                        type
                    };
                }
            """, url)

            if "data" not in result:
                print("SKIPPED:", result)
                continue

            data = base64.b64decode(result["data"])

            if not data.startswith(b"%PDF-"):
                print("Invalid PDF signature. Skipping.")
                continue

            match = re.search(
                r'filename\*?=(?:UTF-8\'\')?["\']?([^"\';]+)',
                result["disposition"],
                re.I
            )

            name = unquote(match.group(1)) if match else title

            if not name.lower().endswith(".pdf"):
                name += ".pdf"

            name = re.sub(r'[<>:"/\\|?*]', "_", name).strip()
            path = os.path.join(SAVE_DIR, name)

            if os.path.exists(path):
                root, ext = os.path.splitext(name)
                name = f"{root}_{i}{ext}"
                path = os.path.join(SAVE_DIR, name)

            with open(path, "wb") as f:
                f.write(data)

            print(f"DOWNLOADED: {name} ({len(data)} bytes)")
            saved += 1

        except Exception as e:
            print("ERROR:", str(e))

    print("\n========== COMPLETE ==========")
    print("Valid PDFs downloaded:", saved)
    print("Folder:", os.path.abspath(SAVE_DIR))

    browser.close()
