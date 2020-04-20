"""
Module Introduction.

Any module level documentation comes here.
"""
import re
import logging
import urllib.request

from lxml import html
from tf_workers import (  # pylint: disable=E0611
    Worker, WorkerResponse, ResponseCodes as RC
)
from tf_workers.config import ApplicationConfig  # pylint: disable=E

config = ApplicationConfig.get_config()

log = logging.getLogger(__name__)


class PasteBinSpider(Worker):
    """
    MyWorker.

    Description and list of parameters. For example:

    :param domain_or_ip:
        Required - The domain or IP Address to perform whois and IPWhois on
    """

    name = 'pastebin'
    resource_requirements = 'LOW'
    domain = "https://pastebin.com"
    base_url = "https://pastebin.com/archive"
    counter = 0

    def _init_settings(self):
        """Initialize worker settings."""
        super()._init_settings()

    def __init__(self, matches, **kwargs):
        """Create worker object."""
        self.matches = matches
        super().__init__(kwargs)

    def start_process(self, matches):
        result = []
        page_source = self.get_raw_html(self.base_url)
        doc = html.fromstring(page_source)
        pastes = doc.xpath('.//*[@id="content_left"]/div[4]/table[@class="maintable"]/tr')
        for i in pastes:
            self.counter += 1

            for j in i.xpath('//td[1]/a'):
                print(j.attrib['href'])

                detail_page_source = self.get_raw_html(self.domain + j.attrib['href'])
                paste_snippets = self.get_html_elements(detail_page_source)
                for snippet in paste_snippets:

                    snippet_str = html.tostring(snippet).decode("utf8")
                    matched_regex = []

                    for match in matches:
                        raw_match = self.get_raw_string(match)
                        match_string = self.match_string_regex(snippet_str, raw_match)

                        if match_string:
                            matched_regex.append(match)
                        else:
                            continue

                    if len(matched_regex) > 0:
                        snippet_link = self.domain + j.attrib['href']
                        result_dict = dict()
                        result_dict['url'] = snippet_link
                        result_dict['matches'] = matched_regex
                        result.append(result_dict)
            if self.counter == 1:
                break

        print("reached limit...................")
        return result

    def match_string_regex(self, snippet, match):
        # import pdb; pdb.set_trace()
        match_object = re.findall(match, snippet)
        if match_object:
            return True
        return False

    def get_raw_string(self, match):
        raw_string = r"{}".format(match)
        return raw_string

    def get_html_elements(self, source):
        doc = html.fromstring(source)

        paste_snippets = doc.xpath('//*[@id="content_left"]')
        return paste_snippets

    def get_raw_html(self, url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        htmlBytes = response.read()
        htmlStr = htmlBytes.decode("utf8")
        return htmlStr

    def run(self):
        """Call this method to run the WHOIS worker."""
        super().run()
        result = self.start_process(self.matches)
        self.response = WorkerResponse()
        self.response.response_code = RC.SUCCESS
        self.response.data = result

        # TODO: Actual worker code comes here for performing worker task and
        # populating self.response.data with the result.
        # If you have defined any input settings in _init_settings() those
        # are accessible here using self.settings.setting_name.value

        return self.response

