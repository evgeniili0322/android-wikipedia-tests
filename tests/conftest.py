import pytest
import os
import pydantic_settings
from appium.options.ios import XCUITestOptions
from appium import webdriver

from selene import browser
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv


class Config(pydantic_settings.BaseSettings):
    app_id: str = 'bs://sample.app'
    browser_url: str = 'http://hub.browserstack.com/wd/hub'
    timeout: float = 10.0


config = Config()


@pytest.fixture(scope='session', autouse=True)
def load_end():
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

    browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.timeout = config.timeout

    yield

    browser.quit()


ios = pytest.mark.parametrize('mobile_management', ['IOS'], indirect=True)

android = pytest.mark.parametrize('mobile_management', ['Android'], indirect=True)
