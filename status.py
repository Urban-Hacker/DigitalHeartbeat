# Simple service to check the status:
import os
from shutil import copyfile
from datetime import datetime

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
        if g_errors == 1:
            return '<div class="section warn">' + data + '</div>'
        return '<div class="section alert">' + data + '</div>'

    def get_html(self):
        return self._html


class HtmlRender:

    def status(service, result):
        page = HtmlPage("templates/entry.html")
        page.add_data("service", service)
        state = "ok"
        if result != 0:
            state = "fail"
        page.add_data("state", state)
        return page.get_html()

    def text(section):
        page = HtmlPage("templates/section.html")
        page.add_data("title", section["title"])
        page.add_data("content", "<tr><td>" + section["desc"] + "</td></tr>")
        return page.get_html()

    def tests(section):
        global g_errors
        tests = section["tests"]
        page = HtmlPage("templates/section.html")
        page.add_data("title", section["title"])
        html = ""
        error = 0
        for test in tests:
            a = os.system(test["cmd"])
            if a > 0:
                error += 1
            html += HtmlRender.status(test["name"], a)
        g_errors += error

        page.add_data("content", html)
        if error > 1:
            page.add_data("state", "alert")
        elif error == 1:
            page.add_data("state", "warn")
        else:
            page.add_data("state", "allclear")
        return page.get_html()

    def graph():
        try:
            historicaldata = open("old.db", "r").read().replace(
                "[", "").replace("]", "").split(",")
        except:
            a = open("old.db", "w")
            a.write(str([]))
            historicaldata = []

        # Padding
        graph = "<div>"
        if len(historicaldata) < config["history"]:
            for i in range(0, config["history"] - len(historicaldata)):
                graph += '<abbr title="(No data)"><span class="square"></span></abbr>'

        newdata = []

        percent_ok = 0
        for i in historicaldata:
            i = int(i)
            newdata.append(i)
            if i > 1:
                graph += '<abbr title="('
                graph += str(i) + \
                    ' outages detected)"><span class="square dot-fail"></span></abbr>'
            elif i == 1:
                graph += '<abbr title="(1 outage detected)"><span class="square dot-warn"></span></abbr>'
            else:
                percent_ok += 1
                graph += '<abbr title="(No outages)"><span class="square dot-ok"></span></abbr>'

        graph += "</div>"

        newdata.append(g_errors)

        if len(historicaldata) > 5:
            percent = round(percent_ok / (len(historicaldata) / 100.0), 2)
            graph += "<small><strong>" + \
                str(percent) + "% Uptime</strong></small>"
        else:
            graph += "<small><strong>Not enough data yet for the uptime metric.</strong></small>"

        if len(newdata) > config["history"]:
            newdata = newdata[-config["history"]:]

        a = open("old.db", "w")
        a.write(str(newdata))

        return graph


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

page = HtmlPage("templates/main.html")
page.add_data("title", config["title"])
page.add_data("desc", config["desc"])
page.add_data("refresh", str(config["refresh"]))
page.add_data("now", "<small>Last Update: " + dt_string + "</small>")


g_errors = 0
html = ""
for section in config["sections"]:
    sectionhtml = ""
    if section["type"] == "tests":
        sectionhtml = HtmlRender.tests(section)
    if section["type"] == "text":
        sectionhtml = HtmlRender.text(section)
    html += sectionhtml

page.add_data("graph", HtmlRender.graph())

if g_errors > 0:
    page.add_data("popup", config["popup"])
else:
    page.add_data("popup", '')

page.add_data("content", html)
with open(config["outputpath"] + config["outputname"], "w") as status_out:
    status_out.write(page.get_html())

copyfile("templates/vanilla.css", config["outputpath"] + "vanilla.css")
copyfile("templates/style.css", config["outputpath"] + "style.css")
