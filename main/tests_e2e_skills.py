"""Browser tests (Selenium) for /skills/manage/, one scenario per portfolio role.

They run in real headless Chrome against a live test server, so they cover what
the API tests cannot: the JavaScript modules, modals, toasts and row updates.
When Selenium or Chrome is not available the whole module is skipped, so
``python manage.py test main`` still works on any machine.
"""

import time
import unittest

from django.contrib.auth.models import Group, User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from main.models import Skill

try:
    from selenium import webdriver
    from selenium.common.exceptions import (
        NoSuchElementException, StaleElementReferenceException, WebDriverException,
    )
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
except ImportError:  # selenium is a dev-only dependency
    webdriver = None

PASSWORD = "pw-e2e-1"
# Makes every fetch() slow, so the state before the server answers can be inspected.
SLOW_FETCH = (
    "const original = window.fetch;"
    "window.fetch = (...args) => new Promise(r => setTimeout(() => r(original(...args)), %d));"
)
# Makes every POST fail with a 403 like the API would.
FAILING_POST = (
    "const original = window.fetch;"
    "window.fetch = (url, opts) => (opts && opts.method === 'POST')"
    " ? Promise.resolve(new Response(JSON.stringify({detail: 'Ditolak oleh server.'}),"
    " {status: 403, headers: {'Content-Type': 'application/json'}}))"
    " : original(url, opts);"
)


def make_driver():
    options = webdriver.ChromeOptions()
    for arg in ("--headless=new", "--window-size=1280,900", "--no-sandbox", "--disable-dev-shm-usage"):
        options.add_argument(arg)
    return webdriver.Chrome(options=options)


class SkillsPageBrowserTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        if webdriver is None:
            raise unittest.SkipTest("selenium is not installed")
        try:
            cls.driver = make_driver()
        except WebDriverException as error:
            raise unittest.SkipTest(f"Chrome is not available: {error.msg[:80]}")
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.quit()

    def setUp(self):
        User.objects.create_superuser("owner", "o@example.com", PASSWORD)
        editor = User.objects.create_user("editor", password=PASSWORD)
        editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        User.objects.create_user("visitor", password=PASSWORD)
        Skill.objects.all().delete()  # seeded rows would make row assertions fragile
        self.alpha = Skill.objects.create(name="Alpha", icon_url="https://x.io/a.svg", category="Lang")
        self.beta = Skill.objects.create(name="Beta", icon_url="https://x.io/b.svg", category="Tool")

    # --- helpers -----------------------------------------------------------

    def wait(self, condition, timeout=8):
        ignored = (StaleElementReferenceException, NoSuchElementException)
        return WebDriverWait(self.driver, timeout, ignored_exceptions=ignored).until(condition)

    def open_as(self, username):
        driver = self.driver
        driver.delete_all_cookies()
        driver.get(self.live_server_url + "/skills/manage/")
        if username:
            client = Client()
            client.login(username=username, password=PASSWORD)
            driver.add_cookie({"name": "sessionid", "value": client.cookies["sessionid"].value, "path": "/"})
        driver.get(self.live_server_url + "/skills/manage/")
        self.wait(lambda d: d.find_element(By.ID, "skills-table").is_displayed())

    def rows(self):
        for _ in range(5):
            try:
                return [
                    row.find_elements(By.TAG_NAME, "td")[0].text
                    for row in self.driver.find_elements(By.CSS_SELECTOR, "#skills-body tr")
                ]
            except StaleElementReferenceException:
                time.sleep(0.2)
        return []

    def star_button(self, skill):
        return self.driver.find_element(By.CSS_SELECTOR, f"#skill-{skill.id} button[data-action=star]")

    def count(self, selector):
        return len(self.driver.find_elements(By.CSS_SELECTOR, selector))

    def toast_text(self):
        def visible_toast(driver):
            for element in driver.find_elements(By.CSS_SELECTOR, "[class*=toast]"):
                if element.is_displayed() and element.text.strip():
                    return element.text
            return False
        return self.wait(visible_toast)

    # --- roles -------------------------------------------------------------

    def test_guest_sees_a_read_only_table(self):
        self.open_as(None)
        self.assertEqual(self.rows(), ["Alpha", "Beta"])
        self.assertEqual(self.count("#skills-body button"), 0)
        login_link = self.driver.find_element(By.CSS_SELECTOR, "#skills-body a.star-button")
        self.assertIn("/login", login_link.get_attribute("href"))
        self.assertEqual(self.count("[popovertarget=add-skill-modal]"), 0)

    def test_regular_user_stars_and_unstars_without_reloading(self):
        self.open_as("visitor")
        self.driver.execute_script("window.__marker = 1")
        self.assertEqual(self.star_button(self.alpha).text, "☆ 0")
        self.star_button(self.alpha).click()
        self.wait(lambda d: self.star_button(self.alpha).text == "★ 1")
        self.assertEqual(self.driver.execute_script("return window.__marker"), 1, "page reloaded")
        self.assertEqual(self.alpha.starred_by.count(), 1)
        self.star_button(self.alpha).click()
        self.wait(lambda d: self.star_button(self.alpha).text == "☆ 0")
        self.assertEqual(self.alpha.starred_by.count(), 0)
        self.assertEqual(self.count("#skills-body button[data-action=edit]"), 0)

    def test_editor_edits_with_patch_and_cannot_create_or_delete(self):
        self.open_as("editor")
        self.assertEqual(self.count("#skills-body button[data-action=delete]"), 0)
        self.assertEqual(self.count("[popovertarget=add-skill-modal]"), 0)
        self.driver.find_element(By.CSS_SELECTOR, f"#skill-{self.alpha.id} button[data-action=edit]").click()
        category = self.driver.find_element(By.ID, "edit_category")
        self.wait(lambda d: category.is_displayed())
        self.assertEqual(self.driver.find_element(By.ID, "edit_name").get_attribute("value"), "Alpha")
        category.clear()
        category.send_keys("Framework")
        self.driver.find_element(By.CSS_SELECTOR, "#edit-skill-form button[type=submit]").click()
        self.wait(lambda d: "Framework" in d.find_element(By.ID, f"skill-{self.alpha.id}").text)
        self.alpha.refresh_from_db()
        self.assertEqual((self.alpha.name, self.alpha.category), ("Alpha", "Framework"))
        self.assertIn("berhasil", self.toast_text().lower())

    def test_editor_sees_the_validation_error_in_a_toast(self):
        self.open_as("editor")
        self.driver.find_element(By.CSS_SELECTOR, f"#skill-{self.alpha.id} button[data-action=edit]").click()
        name = self.driver.find_element(By.ID, "edit_name")
        self.wait(lambda d: name.is_displayed())
        name.clear()
        name.send_keys("<b></b>")
        self.driver.find_element(By.CSS_SELECTOR, "#edit-skill-form button[type=submit]").click()
        self.assertIn("tidak boleh kosong", self.toast_text())
        self.alpha.refresh_from_db()
        self.assertEqual(self.alpha.name, "Alpha")

    def test_owner_adds_and_deletes_a_skill(self):
        self.open_as("owner")
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, "[popovertarget=add-skill-modal]").click()
        name = driver.find_element(By.ID, "id_name")
        self.wait(lambda d: name.is_displayed())
        name.send_keys("Gamma")
        driver.find_element(By.ID, "id_icon_url").send_keys("https://x.io/g.svg")
        driver.find_element(By.ID, "id_category").send_keys("Tool")
        driver.find_element(By.CSS_SELECTOR, "#skill-form button[type=submit]").click()
        self.wait(lambda d: "Gamma" in self.rows())
        gamma = Skill.objects.get(name="Gamma")
        driver.find_element(By.CSS_SELECTOR, f"[popovertarget=delete-skill-{gamma.id}]").click()
        confirm = driver.find_element(By.CSS_SELECTOR, f"#delete-skill-{gamma.id} button[data-action=delete]")
        self.wait(lambda d: confirm.is_displayed())
        confirm.click()
        self.wait(lambda d: "Gamma" not in self.rows())
        self.assertFalse(Skill.objects.filter(name="Gamma").exists())

    # --- search, filter, sort ---------------------------------------------

    def test_search_filter_and_sort(self):
        self.alpha.starred_by.add(User.objects.create_user("s1"))
        self.beta.starred_by.add(User.objects.create_user("s2"), User.objects.create_user("s3"))
        self.open_as(None)
        driver = self.driver
        self.assertEqual(self.rows(), ["Alpha", "Beta"])
        Select(driver.find_element(By.ID, "skills-sort-select")).select_by_value("stars")
        self.wait(lambda d: self.rows() == ["Beta", "Alpha"])
        Select(driver.find_element(By.ID, "skills-category-select")).select_by_value("Lang")
        self.wait(lambda d: self.rows() == ["Alpha"])
        Select(driver.find_element(By.ID, "skills-category-select")).select_by_value("")
        box = driver.find_element(By.ID, "skills-search-input")
        box.send_keys("zzz")
        self.wait(lambda d: d.find_element(By.ID, "empty").is_displayed())
        self.assertIn("Tidak ada skill", driver.find_element(By.ID, "empty-message").text)
        box.clear()
        box.send_keys("alp")
        self.wait(lambda d: self.rows() == ["Alpha"])

    # --- optimistic star ---------------------------------------------------

    def test_star_updates_instantly_before_the_server_answers(self):
        self.open_as("visitor")
        self.driver.execute_script(SLOW_FETCH % 1500)
        self.star_button(self.alpha).click()
        self.wait(lambda d: self.star_button(self.alpha).text == "★ 1", timeout=1)
        # The UI already changed, but the request is still in flight.
        self.assertEqual(self.alpha.starred_by.count(), 0)
        self.wait(lambda d: self.alpha.starred_by.count() == 1)
        self.assertEqual(self.star_button(self.alpha).text, "★ 1")

    def test_failed_star_is_rolled_back_and_explained(self):
        self.open_as("visitor")
        self.driver.execute_script(FAILING_POST)
        self.star_button(self.alpha).click()
        self.assertIn("Ditolak oleh server.", self.toast_text())
        self.wait(lambda d: self.star_button(self.alpha).text == "☆ 0")
        self.assertEqual(self.alpha.starred_by.count(), 0)

    def test_second_click_while_pending_is_ignored(self):
        self.open_as("visitor")
        self.driver.execute_script(SLOW_FETCH % 1000)
        self.star_button(self.alpha).click()
        self.wait(lambda d: self.star_button(self.alpha).text == "★ 1", timeout=1)
        self.star_button(self.alpha).click()  # would unstar if it raced the first request
        self.wait(lambda d: self.alpha.starred_by.count() == 1)
        time.sleep(1.5)
        self.assertEqual(self.alpha.starred_by.count(), 1)
        self.assertEqual(self.star_button(self.alpha).text, "★ 1")
