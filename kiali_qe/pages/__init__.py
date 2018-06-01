"""update this doc"""
from widgetastic.widget import View, Text
from kiali_qe.components import (
    Button,
    DropDown,
    Filter,
    ListViewIstioConfig,
    ListViewServices,
    Login,
    MainMenu,
    Pagination,
    SortDropDown,
    CheckBoxFilter)
from kiali_qe.components.enums import (
    MainMenuEnum as MENU,
    UserMenuEnum as USER_MENU)
from kiali_qe.utils.log import logger
from kiali_qe.utils.conf import env as cfg

XP_DROP_DOWN = '//*[contains(@class, "dropdown")]/*[@id="{}"]/../..'
XP_BUTTON_SWITCH = '//*[contains(@class, "bootstrap-switch")]//*[text()="{}"]/../..'


class RootPage(View):
    PAGE_MENU = None

    def __init__(self, parent, logger=logger):
        View.__init__(self, parent, logger=logger)
        self.load()

    _login = Login()
    main_menu = MainMenu()
    page_header = Text(locator='//*[contains(@class, "container-fluid")]//h2')

    def load(self):
        # if login page displayed, do login
        self.login()
        # load particular page, only if PAGE_MENU is supplied
        if self.PAGE_MENU is not None and self.main_menu.selected != self.PAGE_MENU:
            self.main_menu.select(self.PAGE_MENU)

    def login(self, username=None, password=None, force_login=False):
        if force_login:
            if not self.logout():
                self.logger.warning('Existing session logout failed!')
                return False
        if self._login.is_displayed:
            # if username not supplied, take it from configuration
            if username is None:
                username = cfg.kiali.username
                password = cfg.kiali.password
            self._login.login(username=username, password=password)
        return not self._login.is_displayed

    def logout(self):
        if not self._login.is_displayed:
            self.navbar.user_menu.select(USER_MENU.LOGOUT.txt)
        return self._login.is_displayed

    def reload(self):
        self.browser.refresh()
        self.load()

    @property
    def navbar(self):
        return self.main_menu.navbar

    @property
    def page_header(self):
        return self.page_header_el.text


class GraphPage(RootPage):
    PAGE_MENU = MENU.GRAPH.text

    namespace = DropDown(locator=XP_DROP_DOWN.format('namespace-selector'))
    duration = DropDown(locator=XP_DROP_DOWN.format('graph_filter_interval_duration'))
    layout = DropDown(locator=XP_DROP_DOWN.format('graph_filter_layouts'))
    edge_labels = DropDown(locator=XP_DROP_DOWN.format('graph_filter_edges'))
    filter = CheckBoxFilter()
    refresh = Button(locator='.//button//*[contains(@class, "fa-refresh")]')
    # TODO: implement graph control code


class ServicesPage(RootPage):
    PAGE_MENU = MENU.SERVICES.text

    filter = Filter()
    sort = SortDropDown(locator=XP_DROP_DOWN.format('sortTypeMenu'))
    rate_interval = DropDown(locator=XP_DROP_DOWN.format('rateIntervalDropDown'))
    content = ListViewServices()
    pagination = Pagination()


class IstioMixerPage(RootPage):
    PAGE_MENU = MENU.ISTIO_CONFIG.text

    filter = Filter()
    sort = SortDropDown(locator=XP_DROP_DOWN.format('sortTypeMenu'))
    content = ListViewIstioConfig()
    pagination = Pagination()
