import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
# from tests.ui.test_demoshop_authorize import API_URL_DEMOSHOP, EMAIL_DEMOSHOP, PASSWORD_DEMOSHOP
# from tests.test_api import API_URL_REQRES
from utils.base_session import BaseSession

load_dotenv()
api_url_demoshop = os.getenv("API_URL_DEMOSHOP")
print(api_url_demoshop)
api_url_reqres = os.getenv("API_URL_REQRES")
print(api_url_reqres)
email = os.getenv("EMAIL")
print(email)
password = os.getenv("PASSWORD")
print(password)
web_url = os.getenv("WEB_URL_DEMOSHOP")
print(web_url)


@pytest.fixture(scope="session")
def demoshop():
    demoshop_session = BaseSession(api_url_demoshop)
    return demoshop_session


@pytest.fixture(scope="session")
def reqres():
    reqres_session = BaseSession(api_url_reqres)
    return reqres_session


@pytest.fixture(scope='session', autouse=True)
def app(demoshop):
    browser.config.base_url = web_url
    response = demoshop.post(url="/login",
                             json={
                                 "Email": email,
                                 "Password": password
                             },
                             allow_redirects=False
                             )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    yield
    browser.quit()
