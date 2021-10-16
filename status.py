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


page = HtmlPage("template.html")
page.add_data("title", config["title"])
page.add_data("desc", config["desc"])

html = ""


def printstatus(service, result):
    html = "<tr><td>" + service + "</td>"
    if result == 0:
        html += "<td class='status'><span class='dot dot-ok'></span></td><tr>"
    else:
        html += "<td class='status'><span class='dot dot-fail'></span></td><tr>"
    return html


g_errors = 0
for section in config["sections"]:

    html_section = "<table class='result'>"
    error = 0
    for test in section["tests"]:
        a = os.system(test["cmd"])
        if a > 0:
            error += 1
        html_section += printstatus(test["name"], a)
    html_section += "</table></div>"

    report = " <small class='ok'>No outages</small>"
    if error > 0:
        report = " <small class='fail'>Some services are not working properly (" + str(
            error) + ")</small>"
    html += "<h3 class='section-title'>" + \
        section["title"] + report + "</h3><div class='section'>"
    html += html_section
    html += "</div>"
    g_errors += error

if g_errors > 0:
    page.add_data("popup", config["popup"])
else:
    page.add_data("popup", '')

page.add_data("content", html)
with open("status.html", "w") as status_out:
    status_out.write(page.get_html())
