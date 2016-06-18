from datetime import datetime
import logging
import urllib2

from google.appengine.api import memcache
from lxml import html

MEMCACHE_TIMEOUT = 20 * 60  # 20 minutes

def get_rom_filename(rom):
    if rom == "cm-13-0":
        return "cm-13.0"
    else:
        raise Exception("Unknown version")


def get_folder_info(device):
    if device != "i9105p":
        raise Exception("Unknown device")

    return get_and_parse_folder_info('https://basketbuild.com/devs/GHsR/CM-13/i9105p/')


def get_and_parse_folder_info(url):
    cache_key = "folder:%s" % url
    data = memcache.get(cache_key)
    if data:
        return data

    logging.info("Fetching:" + url)
    data = urllib2.urlopen(url).read()

    tree = html.fromstring(data)
    info = []
    for f in tree.cssselect('[itemtype="http://schema.org/SoftwareApplication"]'):
        # Note: URL for basketbuild doesn't actually work. We assume that localstore will always return a value.
        info.append({
            'filename': f.cssselect("[itemprop=name]")[0].text_content().strip(),
            'md5sum': get_md5sum("https://basketbuild.com" + f.cssselect("[itemprop=downloadUrl]")[0].get('href')),
            'url': f.cssselect("[itemprop=downloadUrl]")[0].attrib['href']
        })

    memcache.add(key=cache_key, value=info, time=MEMCACHE_TIMEOUT)
    return info


def get_md5sum(url):
    cache_key = "md5:%s" % url
    data = memcache.get(cache_key)
    if data:
        return data

    logging.info("Fetching:" + url)
    data = urllib2.urlopen(url).read()

    tree = html.fromstring(data)
    md5 = tree.xpath("normalize-space((//*[text() = 'File MD5:']/following-sibling::text())[1])")

    memcache.add(key=cache_key, value=md5)
    return md5


def get_thread(device, rom):
    if device != "i9105p":
        raise Exception("Unknown device")

    if rom == "cm-13-0":
        return _fetch_memcache('http://forum.xda-developers.com/galaxy-s2-plus/orig-development/rom-cyanogenmod-13-t3265341/')
    else:
        raise Exception("Unknown version")


def _fetch_memcache(url):
    cache_key = "url:%s" % url
    data = memcache.get(cache_key)
    if data:
        return data

    data = urllib2.urlopen(url).read()
    logging.info("Fetching:" + url)
    memcache.add(key=cache_key, value=data, time=MEMCACHE_TIMEOUT)
    return data


def timestamp_from_build_date(build_date):
    return datetime.strptime(build_date, "%Y%m%d").strftime("%s")
