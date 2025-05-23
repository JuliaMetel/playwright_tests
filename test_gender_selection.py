import time
from typing import Callable
import pytest
from PIL.ImageFile import ImageFile
from playwright.sync_api import expect, Page
from utils import wait_page_stable, is_elements_screenshots_equal
from page_one import PageOne
from page_two import PageTwo


class TestClass:
    @pytest.mark.parametrize(
        "sex", ["element_doll_base_female", "element_doll_base_male"]
    )
    def test_gender_selection_sex(self, page: Page, sex: str) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu).to_have_class("popupMenu")
        getattr(page_one, sex).click()
        expect(page_one.element_loading_menu).to_have_class("popupMenu hide")
        wait_page_stable(page)

    def test_loading_menu_header_welcome(self, page: Page) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_welcome).to_have_text(
            page_one.welcome_text
        )

    def test_loading_menu_header_select(self, page: Page) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu_select).to_have_text(page_one.select_text)

    @pytest.mark.parametrize(
        "sex", ["element_doll_base_male", "element_doll_base_female"]
    )
    def test_decals_head_1(
        self, page: Page, sex: str, get_screenshot: Callable[[str], ImageFile]
    ) -> None:
        page_one = PageOne(page)
        getattr(page_one, sex).click()
        page_two = PageTwo(page)
        wait_page_stable(page)
        page_two.element_eye.click()
        page_two.element_head_1.click()
        wait_page_stable(page)
        time.sleep(5)
        assert is_elements_screenshots_equal(
            get_screenshot(sex), page_two.element_canvas
        ), "Screenshots don't match"

    @pytest.mark.parametrize(
        "sex", ["element_doll_base_male", "element_doll_base_female"]
    )
    def test_turning_canvas(
        self, page: Page, sex: str, get_screenshot: Callable[[str], ImageFile]
    ) -> None:
        page_one = PageOne(page)
        expect(page_one.element_loading_menu).to_have_class("popupMenu")
        getattr(page_one, sex).click()
        expect(page_one.element_loading_menu).to_have_class("popupMenu hide")
        wait_page_stable(page)
        page_two = PageTwo(page)
        page_two.element_canvas.hover()
        box = page_two.element_canvas.bounding_box()
        assert box is not None, "Taking box from absent/not visible element"
        page.mouse.down(button="left")
        page.mouse.move(box["x"] + 1, box["y"] + 1, steps=15)
        page.mouse.up(button="left")
        time.sleep(5)
        assert is_elements_screenshots_equal(
            get_screenshot(sex), page_two.element_canvas
        ), "Screenshots don't match"
