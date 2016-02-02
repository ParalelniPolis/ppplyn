#!/usr/bin/python2
# -*- coding: utf-8 -*-

import requests

from lxml.html import document_fromstring


class CHMUWeather(object):

    # °C
    temperature_air = None

    # hPa
    air_pressure = None

    # km/h
    air_wind = None

    website_url = "http://www.in-pocasi.cz/archiv/stanice.php?stanice=praha_ruzyne"

    def __init__(self):

        self.download_page()

        self.parse_content()

    def download_page(self):

        self.website_content = requests.get(self.website_url).content

    def parse_content(self):

        website = document_fromstring(self.website_content)

        columns = website.cssselect("table.oblastits tbody tr.hlavast td")

        self.temperature_air = float(columns[1].text_content().split(" ")[0])

        self.air_pressure = float(columns[3].text_content().split(" ")[0])

        self.air_wind = float(columns[2].text_content().split(" ")[0])
