"""Regular expressions for Python Readability.

This module contains compiled regular expressions that are used throughout the project.
"""

import re

# Regular expressions from parser.go
RX_VIDEOS = re.compile(r'(?i)//(www\.)?((dailymotion|youtube|youtube-nocookie|player\.vimeo|v\.qq)\.com|(archive|upload\.wikimedia)\.org|player\.twitch\.tv)')
RX_TOKENIZE = re.compile(r'(?i)\W+')
RX_WHITESPACE = re.compile(r'(?i)^\s*$')
RX_HAS_CONTENT = re.compile(r'(?i)\S$')
RX_HASH_URL = re.compile(r'(?i)^#.+')
RX_PROPERTY_PATTERN = re.compile(r'(?i)\s*(dc|dcterm|og|article|twitter)\s*:\s*(author|creator|description|title|site_name|published_time|modified_time|image\S*)\s*')
RX_NAME_PATTERN = re.compile(r'(?i)^\s*(?:(dc|dcterm|article|og|twitter|weibo:(article|webpage))\s*[\.:]\s*)?(author|creator|description|title|site_name|published_time|modified_time|image)\s*$')
RX_TITLE_SEPARATOR = re.compile(r'(?i) [\|\-\\/>»] ')
RX_TITLE_HIERARCHY_SEP = re.compile(r'(?i) [\\/>»] ')
RX_TITLE_REMOVE_FINAL_PART = re.compile(r'(?i)(.*)[\|\-\\/>»] .*')
RX_TITLE_REMOVE_1ST_PART = re.compile(r'(?i)[^\|\-\\/>»]*[\|\-\\/>»](.*)')
RX_TITLE_ANY_SEPARATOR = re.compile(r'(?i)[\|\-\\/>»]+')
RX_DISPLAY_NONE = re.compile(r'(?i)display\s*:\s*none')
RX_VISIBILITY_HIDDEN = re.compile(r'(?i)visibility\s*:\s*hidden')
RX_SENTENCE_PERIOD = re.compile(r'(?i)\.( |$)')
RX_SHARE_ELEMENTS = re.compile(r'(?i)(\b|_)(share|sharedaddy)(\b|_)')
RX_FAVICON_SIZE = re.compile(r'(?i)(\d+)x(\d+)')
RX_LAZY_IMAGE_SRCSET = re.compile(r'(?i)\.(jpg|jpeg|png|webp)\s+\d')
RX_LAZY_IMAGE_SRC = re.compile(r'(?i)^\s*\S+\.(jpg|jpeg|png|webp)\S*\s*$')
RX_IMG_EXTENSIONS = re.compile(r'(?i)\.(jpg|jpeg|png|webp)')
RX_SRCSET_URL = re.compile(r'(?i)(\S+)(\s+[\d.]+[xw])?(\s*(?:,|$))')
RX_B64_DATA_URL = re.compile(r'(?i)^data:\s*([^\s;,]+)\s*;\s*base64\s*,')
RX_JSON_LD_ARTICLE_TYPES = re.compile(r'(?i)^Article|AdvertiserContentArticle|NewsArticle|AnalysisNewsArticle|AskPublicNewsArticle|BackgroundNewsArticle|OpinionNewsArticle|ReportageNewsArticle|ReviewNewsArticle|Report|SatiricalArticle|ScholarlyArticle|MedicalScholarlyArticle|SocialMediaPosting|BlogPosting|LiveBlogPosting|DiscussionForumPosting|TechArticle|APIReference$')
RX_CDATA = re.compile(r'^\s*<!\[CDATA\[|\]\]>\s*$')
RX_SCHEMA_ORG = re.compile(r'(?i)^https?\:\/\/schema\.org\/?$')

# Regular expressions from internal/re2go/class-weight.go
RX_POSITIVE_CLASS = re.compile(r'(?i)article|body|content|entry|hentry|h-entry|main|page|pagination|post|text|blog|story')
RX_NEGATIVE_CLASS = re.compile(r'(?i)-ad-|hidden|^hid$| hid$| hid |^hid |banner|combx|comment|com-|contact|foot|footer|footnote|gdpr|masthead|media|meta|outbrain|promo|related|scroll|share|shoutbox|sidebar|skyscraper|sponsor|shopping|tags|tool|widget')

# Regular expressions from internal/re2go/check-byline.go
RX_BYLINE = re.compile(r'(?i)byline|author|dateline|writtenby|p-author')

# Regular expressions from internal/re2go/grab-article.go
RX_UNLIKELY_CANDIDATES = re.compile(r'(?i)-ad-|ai2html|banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|footer|gdpr|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote')
RX_MAYBE_CANDIDATE = re.compile(r'(?i)and|article|body|column|content|main|shadow')

# Regular expressions from internal/re2go/normalize.go
RX_NORMALIZE_SPACES = re.compile(r'(?i)\s{2,}')

# Constants from parser.go
UNLIKELY_ROLES = {
    'menu': True,
    'menubar': True,
    'complementary': True,
    'navigation': True,
    'alert': True,
    'alertdialog': True,
    'dialog': True,
}

DIV_TO_P_ELEMS = {
    'blockquote': True,
    'dl': True,
    'div': True,
    'img': True,
    'ol': True,
    'p': True,
    'pre': True,
    'table': True,
    'ul': True,
    'select': True,
}

ALTER_TO_DIV_EXCEPTIONS = ['div', 'article', 'section', 'p']

PRESENTATIONAL_ATTRIBUTES = [
    'align', 'background', 'bgcolor', 'border', 'cellpadding',
    'cellspacing', 'frame', 'hspace', 'rules', 'style',
    'valign', 'vspace',
]

DEPRECATED_SIZE_ATTRIBUTE_ELEMS = ['table', 'th', 'td', 'hr', 'pre']

PHRASING_ELEMS = [
    'abbr', 'audio', 'b', 'bdo', 'br', 'button', 'cite', 'code', 'data',
    'datalist', 'dfn', 'em', 'embed', 'i', 'img', 'input', 'kbd', 'label',
    'mark', 'math', 'meter', 'noscript', 'object', 'output', 'progress', 'q',
    'ruby', 'samp', 'script', 'select', 'small', 'span', 'strong', 'sub',
    'sup', 'textarea', 'time', 'var', 'wbr',
]

# Helper functions for regular expressions
def is_positive_class(class_name: str) -> bool:
    """Check if a class name is positive.
    
    Args:
        class_name: The class name to check
        
    Returns:
        True if the class name is positive, False otherwise
    """
    return bool(RX_POSITIVE_CLASS.search(class_name))


def is_negative_class(class_name: str) -> bool:
    """Check if a class name is negative.
    
    Args:
        class_name: The class name to check
        
    Returns:
        True if the class name is negative, False otherwise
    """
    return bool(RX_NEGATIVE_CLASS.search(class_name))


def is_byline(text: str) -> bool:
    """Check if a text is a byline.
    
    Args:
        text: The text to check
        
    Returns:
        True if the text is a byline, False otherwise
    """
    return bool(RX_BYLINE.search(text))


def is_unlikely_candidate(match_string: str) -> bool:
    """Check if a match string is an unlikely candidate.
    
    Args:
        match_string: The match string to check
        
    Returns:
        True if the match string is an unlikely candidate, False otherwise
    """
    return bool(RX_UNLIKELY_CANDIDATES.search(match_string))


def maybe_its_a_candidate(match_string: str) -> bool:
    """Check if a match string might be a candidate.
    
    Args:
        match_string: The match string to check
        
    Returns:
        True if the match string might be a candidate, False otherwise
    """
    return bool(RX_MAYBE_CANDIDATE.search(match_string))


def count_commas(text: str) -> int:
    """Count the number of commas in a text.
    
    Args:
        text: The text to count commas in
        
    Returns:
        The number of commas in the text
    """
    return text.count(',')


def normalize_spaces(text: str) -> str:
    """Normalize spaces in a text.
    
    Args:
        text: The text to normalize spaces in
        
    Returns:
        The text with normalized spaces
    """
    return RX_NORMALIZE_SPACES.sub(' ', text)
