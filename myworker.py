"""
Module Introduction.

Any module level documentation comes here.
"""
import re
import logging
import urllib.request
from lxml import html

from tf_workers import (  # pylint: disable=E0611
    Worker, SettingProperty, WorkerResponse, ResponseCodes as RC
)
from tf_workers.config import ApplicationConfig  # pylint: disable=E

config = ApplicationConfig.get_config()

log = logging.getLogger(__name__)

print("!!testing!!!")
class MyWorker(Worker):
    """
    MyWorker.

    Description and list of parameters. For example:

    :param domain_or_ip:
        Required - The domain or IP Address to perform whois and IPWhois on
    """

    name = 'myworker'
    resource_requirements = 'LOW'
    base_url = "https://gist.github.com/discover?page={page_num}"
    counter = 0
    requires = [
        # any additional python modules come here
    ]
    os_requires = [
        # Any additional OS (Linux-Ubuntu) packages come here
    ]

    def _init_settings(self):
        """Initialize worker settings."""
        print('!!!running!!!')
        super()._init_settings()
        # Add any arguments/properties required by the worker here.
        # self.settings.add(SettingProperty(
        #     name='property_name', data_type=str,
        #     description='property description'))

        # Note: These are inputs to the worker. If you wafrom myworker import MyWorkert any information
        # passed to the worker it must be added to self.sMyWorker(['test', 'tester'], 100).run()ttings

    def __init__(self, matches, limit, **kwargs):
        """Create worker object."""
        self.matches = matches
        self.limit = limit
        super().__init__(kwargs)
    
    def start_process(self, matches, limit):
        result = list()
        completed_snippet = list()
        for item in range(1, limit):
            if self.counter < limit:
                url = self.base_url.format(page_num=str(item))
                page_source = self.get_raw_html(url)
                gist_snippets = self.get_html_elements(page_source)
                for snippet in gist_snippets:
                    if snippet not in completed_snippet:
                        self.counter += 1
                        snippet_str = html.tostring(snippet).decode("utf8")
                        matched_regex = list()
                        completed_snippet.append(snippet)
                        for match in matches:
                            raw_match = self.get_raw_string(match)
                            match_string = self.match_string_regex(snippet_str, raw_match)
                            if match_string:
                                matched_regex.append(match)
                                snippet_link = self.get_snippet_link(snippet)
                                result_dict = dict()
                                result_dict['url'] = snippet_link
                                result_dict['matches'] = matched_regex
                                result.append(result_dict)
                            else:
                                continue
                    else:
                        continue
                    
            else:
                print("reached limit...................")
        return result 

    def get_snippet_link(self, snippet):
        link = snippet.cssselect('div.js-gist-file-update-container')[0].cssselect('a.link-overlay')[0].get('href')
        if snippet:
            return link
        return ''


    def match_string_regex(self, snippet, match):
        match_object = re.findall(match, snippet)
        if match_object:
            return True
        return False

    def get_raw_string(self, match):
        raw_string = r"{}".format(match)
        return raw_string

    def get_html_elements(self, source):
        doc = html.fromstring(source)
        gist_snippets = doc.xpath("//div[@class='gist-snippet']")
        return gist_snippets

    def get_raw_html(self, url):
        request = urllib.request.Request('https://gist.github.com/discover?page=3')
        response = urllib.request.urlopen(request)
        htmlBytes = response.read()
        htmlStr = htmlBytes.decode("utf8")
        return htmlStr

    def run(self):
        """Call this method to run the WHOIS worker."""
        super().run()
        print('matches ', self.matches)
        print('limit ', self.limit)
        print('name', self.name)
        result = self.start_process(self.matches, self.limit)
        self.response = WorkerResponse(RC.SUCCESS, '', result)
        # self.response.response_code = RC.SUCCESS
        # self.response.data = {}
        # TODO: Actual worker code comes here for performing worker task and
        # populating self.response.data with the result.
        # If you have defined any input settings in _init_settings() those
        # are accessible here using self.settings.setting_name.value

        return self.response


