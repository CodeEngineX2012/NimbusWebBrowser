import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class NimbusBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nimbus")
        self.setGeometry(100, 100, 1280, 800)

        # Main container
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        main_layout.addWidget(self.tabs)

        # Toolbar (top, like Edge)
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Back / Forward / Reload / Home / New Tab buttons
        back_btn = QAction("◀", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.toolbar.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.toolbar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        self.toolbar.addAction(home_btn)

        new_tab_btn = QAction("＋", self)
        new_tab_btn.triggered.connect(lambda _: self.add_new_tab())
        self.toolbar.addAction(new_tab_btn)

        # URL bar inside toolbar (top, Edge style)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setFixedHeight(28)
        self.url_bar.setStyleSheet("""
            background-color: #ffffff; 
            border-radius: 4px; 
            padding: 4px; 
            font-size: 14px;
        """)
        self.toolbar.addWidget(self.url_bar)

        # Add initial tab
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

        # Edge-like theme
        self.apply_edge_style()

    # Add new tab
    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.page().profile().setPersistentCookiesPolicy(0)  # No cookies
        browser.page().profile().setHttpCacheType(0)  # No cache/history
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda q, browser=browser: self.update_url(q, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    # Double click tab bar to open new tab
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    # Close tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    # Update URL bar when tab changes
    def current_tab_changed(self, i):
        if self.tabs.currentWidget():
            qurl = self.tabs.currentWidget().url()
            self.update_url(qurl, self.tabs.currentWidget())

    # Navigate home
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    # Navigate to URL or Google search
    def navigate_to_url(self):
        url = self.url_bar.text()
        if " " in url:
            url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
        elif not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    # Update URL bar
    def update_url(self, q, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(q.toString())

    # Edge-like theme
    def apply_edge_style(self):
        style = """
            QMainWindow { background-color: #f3f3f3; }
            QToolBar { background-color: #e6e6e6; spacing: 6px; }
            QTabWidget::pane { border-top: 2px solid #aaa; }
            QTabBar::tab { background: #dcdcdc; color: #000000; padding: 8px; border-top-left-radius: 4px; border-top-right-radius: 4px; font-size: 14px; }
            QTabBar::tab:selected { background: #0078d7; color: #ffffff; }
        """
        self.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NimbusBrowser()
    window.show()
    sys.exit(app.exec_())
