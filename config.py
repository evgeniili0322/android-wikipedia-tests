import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    app_id: str = 'test'
    browser_url: str = 'http://hub.browserstack.com/wd/hub'
    timeout: float = 10.0


config = Config()
