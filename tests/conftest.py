import pytest
import os
import allure
import allure_commons

from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from appium import webdriver
from selene import browser, support
from dotenv import load_dotenv

from config import config
from mobile_tests.utils import attach


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    user_name = os.getenv('USER_NAME')
    access_key = os.getenv('ACCESS_KEY')

    if request.param == 'Android':
        options = UiAutomator2Options().load_capabilities({
            "platformName": "android",
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",

            "app": config.app_id,

            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",

                "userName": user_name,
                "accessKey": access_key
            }
        })
    else:
        options = XCUITestOptions().load_capabilities({
            "app": config.app_id,

            "deviceName": "iPhone 11 Pro",
            "platformName": "ios",
            "platformVersion": "13",

            "bstack:options": {
                "userName": user_name,
                "accessKey": access_key,
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test"
            }
        })

    with allure.step('Init app session'):
        browser.config.driver = webdriver.Remote(
            config.browser_url,
            options=options
        )

    browser.config.timeout = config.timeout

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield browser

    attach.add_screenshot(browser)
    attach.add_xml(browser)

    session_id = browser.driver.session_id

    with allure.step('Tear down app session'):
        browser.quit()

    attach.attach_bstack_video(session_id, user_name, access_key)


# Device name parameters
ios = pytest.mark.parametrize('mobile_management', ['IOS'], indirect=True)
android = pytest.mark.parametrize('mobile_management', ['Android'], indirect=True)
