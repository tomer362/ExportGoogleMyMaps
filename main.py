import time
import csv
from playwright.sync_api import sync_playwright


def wait_for_divs_to_stabilize(locator, stable_time=1.0, timeout=10):
    """
    Wait until the number of elements in the locator remains constant for at least stable_time seconds.

    :param locator: The Playwright locator.
    :param stable_time: Time in seconds the count should remain constant.
    :param timeout: Maximum time to wait.
    :return: The stable count of elements.
    """
    start_time = time.time()
    previous_count = -1
    stable_start = None

    while time.time() - start_time < timeout:
        current_count = locator.count()
        if current_count == previous_count:
            if stable_start is None:
                stable_start = time.time()
            elif time.time() - stable_start >= stable_time:
                # Count has been stable for the desired period.
                return current_count
        else:
            previous_count = current_count
            stable_start = None
        time.sleep(0.1)
    return locator.count()  # Return whatever count we have at timeout.


def main():
    # Provided Google My Maps URL
    mymaps_url = ""
    with sync_playwright() as p:
        # Set headless=True for background execution
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(mymaps_url)

        all_categories_under_div = page.locator('body > div').nth(0).locator(':scope > div').nth(2).locator(':scope > div').nth(1).locator(':scope > div').nth(0).locator(
            ':scope > div').nth(0).locator(':scope > div').nth(1).locator(':scope > div').nth(0).locator(':scope > div').nth(0).locator(':scope > div').nth(1).locator(':scope > div')

        wait_for_divs_to_stabilize(all_categories_under_div)
        print(f'Number of categories: {all_categories_under_div.count()}')
        for i in range(1, all_categories_under_div.count()):
            curr_elem = all_categories_under_div.nth(i)
            category_name = curr_elem.locator(':scope > div').nth(0).locator(':scope > div').nth(1)
            category_name.wait_for(timeout=5000)
            print(category_name.inner_text())
            
            internal_div_with_places = curr_elem.locator(':scope > div').nth(0).locator(':scope > div').nth(2)
            internal_div_with_places.wait_for(timeout=5000)
            print(f'Number of places in category: {internal_div_with_places.count()}')

        browser.close()


if __name__ == "__main__":
    main()
