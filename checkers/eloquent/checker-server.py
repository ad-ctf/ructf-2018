#!/usr/bin/python3
import re
import traceback
from hashlib import sha256
from base64 import b64encode

import sys

import markdown
from markdown.extensions.toc import TocExtension

from generators import gen_login, gen_password, gen_article_title, gen_article_content
from service_api import signin, signup, post_article, get_article_content, suggest_article, \
    get_article_id_by_cookies, get_suggestions_by_cookies, ApiException

OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110

ARTICLE_PATTERN = re.compile(r'<div\sclass=\"col-md-3\">(.+)', re.DOTALL)
TABLE_OF_CONTENTS_PATTERN = re.compile(r'<a\shref=\"#(.+)\">.{1,5}\)')
PREGENERATED_TABLE_OF_CONTENTS_PATTERN = re.compile(r'<h[3-6]\sid=\"(.+)\"')
FLAG_LINE_TEMPLATE = re.compile(r"<div\sclass=\"card-header\">(.+)</div>")
ARTICLE_ID_TEMPLATE = re.compile(r"/article/(\d+)")


def print_to_stderr(*args):
    print(*args, file=sys.stderr)


def info():
    print("vulns: 1")
    exit(OK)


def not_found(*args):
    print_to_stderr("Unsupported command %s" % sys.argv[1])
    return CHECKER_ERROR


def get_base_of_hash_of_string(s):
    return b64encode(sha256(s.encode()).digest()).decode()


def get_article_hash(table_of_contents):
    return get_base_of_hash_of_string(','.join(table_of_contents))


def get_article_table_of_contents(article_content, pregen=False):
    pattern = PREGENERATED_TABLE_OF_CONTENTS_PATTERN if pregen else TABLE_OF_CONTENTS_PATTERN
    return re.findall(pattern, article_content)


def check_article_navigation(host, cookies, article_id, table_of_contents):
    article_page = get_article_content(host, cookies, article_id)
    if 'id="mid-text"' not in article_page:
        print_to_stderr("Article page misses navbar subtitle field")
        exit(MUMBLE)
    for header in table_of_contents:
        if 'href="#{}"'.format(header) not in article_page:
            print_to_stderr('No table-of-contents link for "{}"'.format(header))
            exit(MUMBLE)
        if 'id="{}"'.format(header) not in article_page:
            print_to_stderr('No section id for "{}"'.format(header))
            exit(MUMBLE)


def emulate_articles_view(host, cookies):
    suggestions_page = get_suggestions_by_cookies(host, cookies)
    for article_id in re.findall(ARTICLE_ID_TEMPLATE, suggestions_page):
        article_page = get_article_content(host, cookies, article_id)
        for header in get_article_table_of_contents(article_page):
            if 'href="#{}"'.format(header) not in article_page:
                print_to_stderr('Suggestion article {} misses toc link {}'.format(article_id, header))
                exit(MUMBLE)


def check(host):
    username = gen_login()
    password = gen_password()
    cookies = signup(host, username, password)
    post_article(host, cookies, gen_article_title(), gen_article_content())
    article_id = get_article_id_by_cookies(host, cookies, from_suggestions=False)
    article_content = get_article_content(host, cookies, article_id)
    table_of_contents = get_article_table_of_contents(article_content)
    check_article_navigation(host, cookies, article_id, table_of_contents)
    exit(OK)


def get_flag_by_cookies(host, cookies):
    suggestions_content = get_suggestions_by_cookies(host, cookies)
    matching = re.search(FLAG_LINE_TEMPLATE, suggestions_content)
    if matching is None:
        print_to_stderr("No matching with flag pattern, hostname: {}".format(host))
        exit(CORRUPT)
    if len(matching.groups()) == 0:
        print_to_stderr("Empty matching with flag pattern, hostname: {}".format(host))
        exit(CORRUPT)
    return matching.group(1)


def put(host, flag_id, flag, vuln):
    username = gen_login()
    password = gen_password()
    cookies = signup(host, username, password)
    article_title = flag
    article_content = gen_article_content()
    html_content = markdown.markdown(article_content, safe_mode='escape', extensions=[TocExtension(baselevel=3)])
    suggest_article(host, cookies, article_title, article_content, username)
    article_id = get_article_id_by_cookies(host, cookies)
    table_of_contents = get_article_table_of_contents(html_content, pregen=True)
    print(','.join([username, password, article_id, get_article_hash(table_of_contents)]))
    print_to_stderr(','.join([username, password, article_id, get_article_hash(table_of_contents)]))
    exit(OK)


def get(host, flag_id, flag, vuln):
    username, password, article_id, article_hash = flag_id.split(',')
    cookies = signin(host, username, password)
    table_of_contents = get_article_table_of_contents(get_article_content(host, cookies, article_id))
    real_article_hash = get_article_hash(table_of_contents)
    if article_hash != real_article_hash:
        print_to_stderr('expected article_hash="{}"\nreal article_hash="{}"'.format(article_hash, real_article_hash))
        exit(MUMBLE)
    real_flag = get_flag_by_cookies(host, cookies)
    if real_flag != flag:
        print_to_stderr('expected flag={}\nreal flag={}'.format(flag, real_flag))
        exit(CORRUPT)
    emulate_articles_view(host, cookies)
    exit(OK)


COMMANDS = {'check': check, 'put': put, 'get': get, 'info': info}


def main():
    try:
        COMMANDS.get(sys.argv[1], not_found)(*sys.argv[2:])
    except ApiException as e:
        print_to_stderr(e.exc_message)
        exit(int(e.exc_type.value))
    except Exception:
        traceback.print_exc()
        exit(CHECKER_ERROR)

if __name__ == '__main__':
    main()
