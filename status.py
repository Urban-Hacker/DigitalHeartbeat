# Simple service to check the status:
import os

from config import *


class HtmlPage:

    def __init__(self, file):
        self._html = open(file, "r").read()

    def add_data(self, key, data):
        if (key == "popup"):
            data = self._gen_popup(data)
        self._html = self._html.replace("[[" + key + "]]", data)

    def _gen_popup(self, data):
        if data == "":
            return data
        return '<div class="section alert">' + data + '</div>'

    def get_html(self):
        return self._html


page = HtmlPage("templates/main.html")
page.add_data("title", config["title"])
page.add_data("desc", config["desc"])


def printstatus(service, result):
    page = HtmlPage("templates/entry.html")
    page.add_data("service", service)
    state = "ok"
    if result != 0:
        state = "fail"
    page.add_data("state", state)
    return page.get_html()


g_errors = 0
html = ""
for section in config["sections"]:
    sectionpage = HtmlPage("templates/section.html")

    html_section = ""
    error = 0
    for test in section["tests"]:
        a = os.system(test["cmd"])
        if a > 0:
            error += 1
        html_section += printstatus(test["name"], a)
    sectionpage.add_data("content", html_section)

    #report = " <small class='ok'>No outages</small>"
    # if error > 0:
    #    report = " <small class='fail'>Some services are not working properly (" + str(
    #        error) + ")</small>"

    sectionpage.add_data("title", section["title"])
    html += sectionpage.get_html()
    g_errors += error

if g_errors > 0:
    page.add_data("popup", config["popup"])
else:
    page.add_data("popup", '')

page.add_data("content", html)
with open("status.html", "w") as status_out:
    status_out.write(page.get_html())
