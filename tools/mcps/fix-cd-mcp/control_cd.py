import asyncio
from playwright.async_api import async_playwright


async def run():
    async with async_playwright() as p:
        # Connect to Claude Desktop via CDP (port 9229)
        # Note: We connect to the BROWSER endpoint, which lets us see all targets
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9229")
        except Exception as e:
            print(f"Failed to connect: {e}")
            return

        print("Connected to Claude Desktop!")

        # List contexts/pages
        contexts = browser.contexts
        if not contexts:
            print("No contexts found.")
            # Sometimes default context is hidden?

        # Try to find the page
        page = None
        for ctx in contexts:
            for pg in ctx.pages:
                title = await pg.title()
                url = pg.url
                print(f"Found page: {title} ({url})")
                # Claude Desktop main window usually has title "Claude" or similar
                if "Claude" in title or "file://" in url:
                    page = pg
                    break
            if page:
                break

        if not page:
            # Maybe it's a background page?
            print("No visible page found. Checking targets...")
            # We might need to join the target manually if Playwright didn't auto-attach?
            # But connect_over_cdp usually does.
            pass

        if page:
            print(f"Attaching to page: {await page.title()}")

            # 1. Dump Sidebar
            # Sidebar items are likely in a list.
            # Try generic selectors for list items
            items = await page.locator(
                "nav li, nav div[role='button']"
            ).all_text_contents()
            print("Sidebar items found (text):")
            for item in items[:10]:
                print(f" - {item[:30]}...")

            # 2. Search for specific chat
            target_chat = "Cardiovascular death"
            print(f"Searching for '{target_chat}'...")

            # Use Playwright's robust text locator
            # "text=Cardiovascular death" (case insensitive usually?)
            chat_locator = page.get_by_text(target_chat, exact=False)

            if await chat_locator.count() > 0:
                print("Found chat! Clicking...")
                await chat_locator.first.click()

                # Wait for load (look for specific message or just wait)
                await page.wait_for_timeout(2000)

                # 3. Read Messages
                # Messages are usually in div.font-user-message or similar
                # Or look for user/assistant roles
                msgs = await page.locator(
                    ".font-claude-message, .font-user-message"
                ).all_text_contents()
                print(f"Extracted {len(msgs)} messages:")
                for m in msgs[-3:]:
                    print(f"---\n{m[:200]}\n---")
            else:
                print("Chat not found in sidebar.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
