import pytest
from playwright.sync_api import sync_playwright


# Locate the cookies consent dialog and click the "Accept All" button if it is present
def handle_cookies_dialog(page):
    accept_button_selector = "#cookiescript_accept"
    dialog_selector = "#cookiescript_injected"

    if page.locator(dialog_selector).is_visible(timeout=5000):
        if page.locator(accept_button_selector).is_visible():
            page.locator(accept_button_selector).click()


# Test to verify the homepage title and navigate to the courses overview page
def test_engeto_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.engeto.cz/")

        handle_cookies_dialog(page)

        assert "ENGETO" in page.title(), "Page title does not contain 'ENGETO'"

        it_courses_button = page.locator("text=PŘEHLED IT KURZŮ")
        assert it_courses_button.is_visible(), "'PŘEHLED IT KURZŮ' button is not visible on the homepage"

        it_courses_button.click()
        assert "prehled-kurzu" in page.url, "Did not navigate to the courses page"

        context.close()
        browser.close()


# Testing Python tester page's title and visibility of enroll button
def test_python_tester_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        context = browser.new_context()
        page = context.new_page()

        page.goto("https://engeto.cz/tester-s-pythonem/")

        assert "tester s Pythonem" in page.title(), "Page title does not contain 'tester s Pythonem'"

        heading = page.locator("h1")
        assert heading.is_visible(), "Main heading is not visible"
        assert "Tester s Pythonem" in heading.text_content(), "Main heading text does not match"

        enroll_button = page.locator("text=Přihlásit se")
        assert enroll_button.is_visible(), "'Přihlásit se' button is not visible"
        assert enroll_button.is_enabled(), "'Přihlásit se' button is not enabled"

        context.close()
        browser.close()


# Check other articles button on homepage
def test_display_other_articles_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://engeto.cz/")

        handle_cookies_dialog(page)

        articles_button = page.locator("text=Zobrazit další články")

        articles_button.wait_for(state="visible", timeout=5000)
        assert articles_button.is_visible(), "'Zobrazit další články' button is not visible"

        articles_button.click()
        assert "blog" in page.url, "Did not navigate to the blog page"

        context.close()
        browser.close()


if __name__ == "__main__":
    pytest.main([__file__])
