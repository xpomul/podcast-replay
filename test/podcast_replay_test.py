"""Tests for the service() function"""

import datetime
from main  import podcast_replay
import xml.etree.ElementTree as ET

TESTFEED = feed = '''
<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Tue, 27 Feb 2023 17:05:19 +0200</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 01
</title>
<link>
https://www.google.com/foobar/1
</link>
<pubDate>Tue, 20 Feb 2023 10:15:14 +0200</pubDate>
<guid isPermaLink="false">e5483b63-473e-4a06-9ed6-2d84e64cae9e</guid>
<description>
Episode Desc 01
</description>
<enclosure length="7258368" type="audio/mpeg" url="https://www.google.com/foobar/1.mp3" />
<itunes:duration>00:07:33</itunes:duration>
</item>
<item>
<title>
Episode Title 02
</title>
<link>
https://www.google.com/foobar/2
</link>
<pubDate>Tue, 27 Feb 2023 12:22:11 +0200</pubDate>
<guid isPermaLink="false">10e4bd4e-a467-4223-895f-b0fbedb58f7d</guid>
<description>
Episode Desc 02
</description>
<enclosure length="72548" type="audio/mpeg" url="https://www.google.com/foobar/2.mp3" />
<itunes:duration>00:05:51</itunes:duration>
</item>
</channel>
</rss>
'''

def test_transform_podcast_default():
    config = {
        'skip': 0,
        'rate' : 1,
        'date' : '2023-04-01'}

    result_xml = podcast_replay.transform_podcast(TESTFEED, config)

    # convert xml to string
    result_string = ET.tostring(result_xml, encoding="unicode", method="xml")

    # compare
    assert result_string == '''<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Sun, 02 Apr 2023 00:00:00 GMT</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 01
</title>
<link>
https://www.google.com/foobar/1
</link>
<pubDate>Sat, 01 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">e5483b63-473e-4a06-9ed6-2d84e64cae9e</guid>
<description>
Episode Desc 01
</description>
<enclosure length="7258368" type="audio/mpeg" url="https://www.google.com/foobar/1.mp3" />
<itunes:duration>00:07:33</itunes:duration>
</item>
<item>
<title>
Episode Title 02
</title>
<link>
https://www.google.com/foobar/2
</link>
<pubDate>Sun, 02 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">10e4bd4e-a467-4223-895f-b0fbedb58f7d</guid>
<description>
Episode Desc 02
</description>
<enclosure length="72548" type="audio/mpeg" url="https://www.google.com/foobar/2.mp3" />
<itunes:duration>00:05:51</itunes:duration>
</item>
</channel>
</rss>'''

def test_transform_podcast_skip():
    config = {
        'skip': 1,
        'rate' : 1,
        'date' : '2023-04-01'}

    result_xml = podcast_replay.transform_podcast(TESTFEED, config)

    # convert xml to string
    result_string = ET.tostring(result_xml, encoding="unicode", method="xml")

    # compare
    assert result_string == '''<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Sat, 01 Apr 2023 00:00:00 GMT</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 02
</title>
<link>
https://www.google.com/foobar/2
</link>
<pubDate>Sat, 01 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">10e4bd4e-a467-4223-895f-b0fbedb58f7d</guid>
<description>
Episode Desc 02
</description>
<enclosure length="72548" type="audio/mpeg" url="https://www.google.com/foobar/2.mp3" />
<itunes:duration>00:05:51</itunes:duration>
</item>
</channel>
</rss>'''

def test_transform_podcast_rate():
    config = {
        'skip': 0,
        'rate' : 3,
        'date' : '2023-04-01'}

    result_xml = podcast_replay.transform_podcast(TESTFEED, config)

    # convert xml to string
    result_string = ET.tostring(result_xml, encoding="unicode", method="xml")

    # compare
    assert result_string == '''<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Tue, 04 Apr 2023 00:00:00 GMT</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 01
</title>
<link>
https://www.google.com/foobar/1
</link>
<pubDate>Sat, 01 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">e5483b63-473e-4a06-9ed6-2d84e64cae9e</guid>
<description>
Episode Desc 01
</description>
<enclosure length="7258368" type="audio/mpeg" url="https://www.google.com/foobar/1.mp3" />
<itunes:duration>00:07:33</itunes:duration>
</item>
<item>
<title>
Episode Title 02
</title>
<link>
https://www.google.com/foobar/2
</link>
<pubDate>Tue, 04 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">10e4bd4e-a467-4223-895f-b0fbedb58f7d</guid>
<description>
Episode Desc 02
</description>
<enclosure length="72548" type="audio/mpeg" url="https://www.google.com/foobar/2.mp3" />
<itunes:duration>00:05:51</itunes:duration>
</item>
</channel>
</rss>'''

def test_transform_podcast_skipfuture():
    config = {
        'skip': 0,
        'rate' : 2,
        'date' : '2023-04-01'}

    fake_now = datetime.datetime(2023, 4, 2)
    result_xml = podcast_replay.transform_podcast(TESTFEED, config, fake_now)

    # convert xml to string
    result_string = ET.tostring(result_xml, encoding="unicode", method="xml")

    # compare
    assert result_string == '''<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Sat, 01 Apr 2023 00:00:00 GMT</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 01
</title>
<link>
https://www.google.com/foobar/1
</link>
<pubDate>Sat, 01 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">e5483b63-473e-4a06-9ed6-2d84e64cae9e</guid>
<description>
Episode Desc 01
</description>
<enclosure length="7258368" type="audio/mpeg" url="https://www.google.com/foobar/1.mp3" />
<itunes:duration>00:07:33</itunes:duration>
</item>
</channel>
</rss>'''

def test_transform_podcast_respect_date_order():
    config = {
        'skip': 1,
        'rate' : 2,
        'date' : '2023-04-01'}

    # replace date string to fake different order
    modified_testfeed = TESTFEED.replace('<pubDate>Tue, 27 Feb 2023 12:22:11 +0200</pubDate>', '<pubDate>Sun, 01 Jan 2023 00:00:00 +0200</pubDate>')

    fake_now = datetime.datetime(2023, 4, 2)
    result_xml = podcast_replay.transform_podcast(modified_testfeed, config, fake_now)

    # convert xml to string
    result_string = ET.tostring(result_xml, encoding="unicode", method="xml")

    # compare
    assert result_string == '''<rss xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>My Podcast</title>
<link>
https://www.google.com/foobar
</link>
<description>
My Description
</description>
<lastBuildDate>Sat, 01 Apr 2023 00:00:00 GMT</lastBuildDate>
<image>
<url>
https://www.google.com/fooimg
</url>
<title>Podcast Title</title>
<link>
https://www.google.com/fooimg
</link>
</image>
<category>Music</category>
<language>de-DE</language>
<generator>FooBarMachine</generator>
<copyright>© 2023 Me, Myself, and I</copyright>
<itunes:author>Me, Myself, and I</itunes:author>
<atom:link href="https://www.google.com/foobar" rel="self" title="Podcast Title" type="application/rss+xml" />
<item>
<title>
Episode Title 01
</title>
<link>
https://www.google.com/foobar/1
</link>
<pubDate>Sat, 01 Apr 2023 00:00:00 GMT</pubDate>
<guid isPermaLink="false">e5483b63-473e-4a06-9ed6-2d84e64cae9e</guid>
<description>
Episode Desc 01
</description>
<enclosure length="7258368" type="audio/mpeg" url="https://www.google.com/foobar/1.mp3" />
<itunes:duration>00:07:33</itunes:duration>
</item>
</channel>
</rss>'''

