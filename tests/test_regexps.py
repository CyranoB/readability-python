"""Tests for regular expressions."""

import unittest
import re

from readability.regexps import (
    RX_VIDEOS,
    RX_TOKENIZE,
    RX_WHITESPACE,
    RX_HAS_CONTENT,
    RX_HASH_URL,
    RX_PROPERTY_PATTERN,
    RX_NAME_PATTERN,
    RX_TITLE_SEPARATOR,
    RX_TITLE_HIERARCHY_SEP,
    RX_TITLE_REMOVE_FINAL_PART,
    RX_TITLE_REMOVE_1ST_PART,
    RX_TITLE_ANY_SEPARATOR,
    RX_DISPLAY_NONE,
    RX_VISIBILITY_HIDDEN,
    RX_SENTENCE_PERIOD,
    RX_SHARE_ELEMENTS,
    RX_FAVICON_SIZE,
    RX_LAZY_IMAGE_SRCSET,
    RX_LAZY_IMAGE_SRC,
    RX_IMG_EXTENSIONS,
    RX_SRCSET_URL,
    RX_B64_DATA_URL,
    RX_JSON_LD_ARTICLE_TYPES,
    RX_CDATA,
    RX_SCHEMA_ORG,
    RX_POSITIVE_CLASS,
    RX_NEGATIVE_CLASS,
    RX_BYLINE,
    RX_UNLIKELY_CANDIDATES,
    RX_MAYBE_CANDIDATE,
    RX_NORMALIZE_SPACES,
    UNLIKELY_ROLES,
    DIV_TO_P_ELEMS,
    ALTER_TO_DIV_EXCEPTIONS,
    PRESENTATIONAL_ATTRIBUTES,
    DEPRECATED_SIZE_ATTRIBUTE_ELEMS,
    PHRASING_ELEMS,
    is_positive_class,
    is_negative_class,
    is_byline,
    is_unlikely_candidate,
    maybe_its_a_candidate,
    count_commas,
    normalize_spaces,
    evaluate_class_weight
)


class TestRegexps(unittest.TestCase):
    """Test the regular expressions."""

    def test_rx_videos(self):
        """Test RX_VIDEOS regex."""
        # Test matching URLs
        self.assertTrue(RX_VIDEOS.search("https://www.youtube.com/watch?v=12345"))
        self.assertTrue(RX_VIDEOS.search("https://youtube.com/watch?v=12345"))
        self.assertTrue(RX_VIDEOS.search("https://player.vimeo.com/video/12345"))
        self.assertTrue(RX_VIDEOS.search("https://www.dailymotion.com/video/x12345"))
        self.assertTrue(RX_VIDEOS.search("https://v.qq.com/x/page/12345.html"))
        self.assertTrue(RX_VIDEOS.search("https://archive.org/details/12345"))
        self.assertTrue(RX_VIDEOS.search("https://upload.wikimedia.org/wikipedia/commons/12345"))
        self.assertTrue(RX_VIDEOS.search("https://player.twitch.tv/12345"))
        self.assertTrue(RX_VIDEOS.search("https://youtube-nocookie.com/embed/12345"))
        
        # Test non-matching URLs
        self.assertFalse(RX_VIDEOS.search("https://example.com/video"))
        self.assertFalse(RX_VIDEOS.search("https://vimeo.org/12345"))  # Wrong domain
        self.assertFalse(RX_VIDEOS.search("https://youtu.be/12345"))  # Short URL not matched

    def test_rx_tokenize(self):
        """Test RX_TOKENIZE regex."""
        # Test tokenization
        self.assertEqual(RX_TOKENIZE.split("hello world"), ["hello", "world"])
        self.assertEqual(RX_TOKENIZE.split("hello, world!"), ["hello", "world", ""])
        self.assertEqual(RX_TOKENIZE.split("hello-world"), ["hello", "world"])
        self.assertEqual(RX_TOKENIZE.split("hello_world"), ["hello_world"])  # Underscore is not split

    def test_rx_whitespace(self):
        """Test RX_WHITESPACE regex."""
        # Test whitespace matching
        self.assertTrue(RX_WHITESPACE.match("   "))
        self.assertTrue(RX_WHITESPACE.match("\t\n\r"))
        self.assertTrue(RX_WHITESPACE.match(""))
        
        # Test non-whitespace
        self.assertFalse(RX_WHITESPACE.match("hello"))
        self.assertFalse(RX_WHITESPACE.match(" hello "))

    def test_rx_has_content(self):
        """Test RX_HAS_CONTENT regex."""
        # Test content detection
        self.assertTrue(RX_HAS_CONTENT.search("hello"))
        self.assertTrue(RX_HAS_CONTENT.search(" hello"))
        
        # Test no content
        self.assertFalse(RX_HAS_CONTENT.search(""))
        self.assertFalse(RX_HAS_CONTENT.search(" "))
        self.assertFalse(RX_HAS_CONTENT.search("\t\n\r"))

    def test_rx_hash_url(self):
        """Test RX_HASH_URL regex."""
        # Test hash URLs
        self.assertTrue(RX_HASH_URL.match("#section1"))
        self.assertTrue(RX_HASH_URL.match("#top"))
        
        # Test non-hash URLs
        self.assertFalse(RX_HASH_URL.match("https://example.com"))
        self.assertFalse(RX_HASH_URL.match("section1"))
        self.assertFalse(RX_HASH_URL.match(""))

    def test_rx_property_pattern(self):
        """Test RX_PROPERTY_PATTERN regex."""
        # Test property patterns
        match = RX_PROPERTY_PATTERN.search("og:title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "og")
        self.assertEqual(match.group(2), "title")
        
        match = RX_PROPERTY_PATTERN.search("dc:creator")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "dc")
        self.assertEqual(match.group(2), "creator")
        
        match = RX_PROPERTY_PATTERN.search("article:published_time")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "article")
        self.assertEqual(match.group(2), "published_time")
        
        match = RX_PROPERTY_PATTERN.search("twitter:image")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "twitter")
        self.assertEqual(match.group(2), "image")
        
        # Test with spaces
        match = RX_PROPERTY_PATTERN.search("  og : title  ")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "og")
        self.assertEqual(match.group(2), "title")
        
        # Test non-matching patterns
        self.assertFalse(RX_PROPERTY_PATTERN.search("title"))
        self.assertFalse(RX_PROPERTY_PATTERN.search("og-title"))
        self.assertFalse(RX_PROPERTY_PATTERN.search("fb:title"))  # fb not in pattern

    def test_rx_name_pattern(self):
        """Test RX_NAME_PATTERN regex."""
        # Test name patterns
        match = RX_NAME_PATTERN.search("author")
        self.assertTrue(match)
        self.assertIsNone(match.group(1))
        self.assertEqual(match.group(3), "author")
        
        match = RX_NAME_PATTERN.search("dc.title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "dc")
        self.assertEqual(match.group(3), "title")
        
        match = RX_NAME_PATTERN.search("og:description")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "og")
        self.assertEqual(match.group(3), "description")
        
        match = RX_NAME_PATTERN.search("weibo:article:image")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "weibo:article")
        self.assertEqual(match.group(3), "image")
        
        # Test with spaces
        match = RX_NAME_PATTERN.search("  dc : title  ")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "dc")
        self.assertEqual(match.group(3), "title")
        
        # Test non-matching patterns
        self.assertFalse(RX_NAME_PATTERN.search("keywords"))
        self.assertFalse(RX_NAME_PATTERN.search("fb:title"))  # fb not in pattern

    def test_rx_title_separator(self):
        """Test RX_TITLE_SEPARATOR regex."""
        # Test title separators
        self.assertTrue(RX_TITLE_SEPARATOR.search("Title | Site Name"))
        self.assertTrue(RX_TITLE_SEPARATOR.search("Title - Site Name"))
        self.assertTrue(RX_TITLE_SEPARATOR.search("Title > Site Name"))
        self.assertTrue(RX_TITLE_SEPARATOR.search("Title / Site Name"))
        self.assertTrue(RX_TITLE_SEPARATOR.search("Title » Site Name"))
        
        # Test non-matching patterns
        self.assertFalse(RX_TITLE_SEPARATOR.search("Title: Site Name"))
        self.assertFalse(RX_TITLE_SEPARATOR.search("Title + Site Name"))
        self.assertFalse(RX_TITLE_SEPARATOR.search("Title and Site Name"))

    def test_rx_title_hierarchy_sep(self):
        """Test RX_TITLE_HIERARCHY_SEP regex."""
        # Test title hierarchy separators
        self.assertTrue(RX_TITLE_HIERARCHY_SEP.search("Title > Site Name"))
        self.assertTrue(RX_TITLE_HIERARCHY_SEP.search("Title / Site Name"))
        self.assertTrue(RX_TITLE_HIERARCHY_SEP.search("Title » Site Name"))
        
        # Test non-matching patterns
        self.assertFalse(RX_TITLE_HIERARCHY_SEP.search("Title | Site Name"))
        self.assertFalse(RX_TITLE_HIERARCHY_SEP.search("Title - Site Name"))
        self.assertFalse(RX_TITLE_HIERARCHY_SEP.search("Title: Site Name"))

    def test_rx_title_remove_final_part(self):
        """Test RX_TITLE_REMOVE_FINAL_PART regex."""
        # Test title final part removal
        match = RX_TITLE_REMOVE_FINAL_PART.search("Title | Site Name")
        self.assertTrue(match)
        self.assertEqual(match.group(1).strip(), "Title")
        
        match = RX_TITLE_REMOVE_FINAL_PART.search("Title - Site Name")
        self.assertTrue(match)
        self.assertEqual(match.group(1).strip(), "Title")
        
        match = RX_TITLE_REMOVE_FINAL_PART.search("Title > Site Name")
        self.assertTrue(match)
        self.assertEqual(match.group(1).strip(), "Title")
        
        # Test with multiple separators
        match = RX_TITLE_REMOVE_FINAL_PART.search("Section > Title | Site Name")
        self.assertTrue(match)
        self.assertEqual(match.group(1).strip(), "Section > Title")
        
        # Test non-matching patterns
        self.assertFalse(RX_TITLE_REMOVE_FINAL_PART.search("Title"))
        self.assertFalse(RX_TITLE_REMOVE_FINAL_PART.search("Title: Site Name"))

    def test_rx_title_remove_1st_part(self):
        """Test RX_TITLE_REMOVE_1ST_PART regex."""
        # Test title first part removal
        match = RX_TITLE_REMOVE_1ST_PART.search("Site Name | Title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), " Title")
        
        match = RX_TITLE_REMOVE_1ST_PART.search("Site Name - Title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), " Title")
        
        match = RX_TITLE_REMOVE_1ST_PART.search("Site Name > Title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), " Title")
        
        # Test with multiple separators
        match = RX_TITLE_REMOVE_1ST_PART.search("Site Name | Section > Title")
        self.assertTrue(match)
        self.assertEqual(match.group(1), " Section > Title")
        
        # Test non-matching patterns
        self.assertFalse(RX_TITLE_REMOVE_1ST_PART.search("Title"))
        self.assertFalse(RX_TITLE_REMOVE_1ST_PART.search("Title: Site Name"))

    def test_rx_title_any_separator(self):
        """Test RX_TITLE_ANY_SEPARATOR regex."""
        # Test title any separator
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title | Site Name"), "Title  Site Name")
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title - Site Name"), "Title  Site Name")
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title > Site Name"), "Title  Site Name")
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title / Site Name"), "Title  Site Name")
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title » Site Name"), "Title  Site Name")
        
        # Test with multiple separators
        self.assertEqual(RX_TITLE_ANY_SEPARATOR.sub("", "Title | Section > Site Name"), "Title  Section  Site Name")

    def test_rx_display_none(self):
        """Test RX_DISPLAY_NONE regex."""
        # Test display:none detection
        self.assertTrue(RX_DISPLAY_NONE.search("display:none"))
        self.assertTrue(RX_DISPLAY_NONE.search("display: none"))
        self.assertTrue(RX_DISPLAY_NONE.search("display : none"))
        self.assertTrue(RX_DISPLAY_NONE.search("display:none !important"))
        self.assertTrue(RX_DISPLAY_NONE.search("style=\"color: red; display: none;\""))
        
        # Test non-matching patterns
        self.assertFalse(RX_DISPLAY_NONE.search("display:block"))
        self.assertFalse(RX_DISPLAY_NONE.search("display:inline"))
        self.assertFalse(RX_DISPLAY_NONE.search("displaynone"))  # Missing colon

    def test_rx_visibility_hidden(self):
        """Test RX_VISIBILITY_HIDDEN regex."""
        # Test visibility:hidden detection
        self.assertTrue(RX_VISIBILITY_HIDDEN.search("visibility:hidden"))
        self.assertTrue(RX_VISIBILITY_HIDDEN.search("visibility: hidden"))
        self.assertTrue(RX_VISIBILITY_HIDDEN.search("visibility : hidden"))
        self.assertTrue(RX_VISIBILITY_HIDDEN.search("visibility:hidden !important"))
        self.assertTrue(RX_VISIBILITY_HIDDEN.search("style=\"color: red; visibility: hidden;\""))
        
        # Test non-matching patterns
        self.assertFalse(RX_VISIBILITY_HIDDEN.search("visibility:visible"))
        self.assertFalse(RX_VISIBILITY_HIDDEN.search("visibility:inherit"))
        self.assertFalse(RX_VISIBILITY_HIDDEN.search("visibilityhidden"))  # Missing colon

    def test_rx_sentence_period(self):
        """Test RX_SENTENCE_PERIOD regex."""
        # Test sentence period detection
        self.assertTrue(RX_SENTENCE_PERIOD.search("This is a sentence."))
        self.assertTrue(RX_SENTENCE_PERIOD.search("This is a sentence. "))
        
        # Test non-matching patterns
        self.assertFalse(RX_SENTENCE_PERIOD.search("This is a sentence"))
        self.assertFalse(RX_SENTENCE_PERIOD.search("This is a sentence.but no space"))
        self.assertFalse(RX_SENTENCE_PERIOD.search("This is a sentence.2"))

    def test_rx_share_elements(self):
        """Test RX_SHARE_ELEMENTS regex."""
        # Test share elements detection
        self.assertTrue(RX_SHARE_ELEMENTS.search("share-buttons"))
        self.assertTrue(RX_SHARE_ELEMENTS.search("social-share"))
        self.assertTrue(RX_SHARE_ELEMENTS.search("twitter-share"))
        self.assertTrue(RX_SHARE_ELEMENTS.search("facebook_share"))
        self.assertTrue(RX_SHARE_ELEMENTS.search("sharedaddy"))
        self.assertTrue(RX_SHARE_ELEMENTS.search("jp-sharedaddy"))
        
        # Test non-matching patterns
        self.assertFalse(RX_SHARE_ELEMENTS.search("shared-responsibility"))
        self.assertFalse(RX_SHARE_ELEMENTS.search("shareholders"))
        self.assertFalse(RX_SHARE_ELEMENTS.search("ashare"))  # No word boundary

    def test_rx_favicon_size(self):
        """Test RX_FAVICON_SIZE regex."""
        # Test favicon size detection
        match = RX_FAVICON_SIZE.search("32x32")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "32")
        self.assertEqual(match.group(2), "32")
        
        match = RX_FAVICON_SIZE.search("16x16")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "16")
        self.assertEqual(match.group(2), "16")
        
        match = RX_FAVICON_SIZE.search("favicon-192x192.png")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "192")
        self.assertEqual(match.group(2), "192")
        
        # Test non-matching patterns
        self.assertFalse(RX_FAVICON_SIZE.search("32x"))
        self.assertFalse(RX_FAVICON_SIZE.search("x32"))
        self.assertFalse(RX_FAVICON_SIZE.search("32X32"))  # Case sensitive

    def test_rx_lazy_image_srcset(self):
        """Test RX_LAZY_IMAGE_SRCSET regex."""
        # Test lazy image srcset detection
        self.assertTrue(RX_LAZY_IMAGE_SRCSET.search("image.jpg 1x"))
        self.assertTrue(RX_LAZY_IMAGE_SRCSET.search("image.jpeg 2x"))
        self.assertTrue(RX_LAZY_IMAGE_SRCSET.search("image.png 800w"))
        self.assertTrue(RX_LAZY_IMAGE_SRCSET.search("image.webp 1200w"))
        
        # Test non-matching patterns
        self.assertFalse(RX_LAZY_IMAGE_SRCSET.search("image.jpg"))
        self.assertFalse(RX_LAZY_IMAGE_SRCSET.search("image.gif 1x"))
        self.assertFalse(RX_LAZY_IMAGE_SRCSET.search("image.svg 2x"))

    def test_rx_lazy_image_src(self):
        """Test RX_LAZY_IMAGE_SRC regex."""
        # Test lazy image src detection
        self.assertTrue(RX_LAZY_IMAGE_SRC.match("image.jpg"))
        self.assertTrue(RX_LAZY_IMAGE_SRC.match("  image.jpeg  "))
        self.assertTrue(RX_LAZY_IMAGE_SRC.match("image.png"))
        self.assertTrue(RX_LAZY_IMAGE_SRC.match("image.webp"))
        self.assertTrue(RX_LAZY_IMAGE_SRC.match("https://example.com/image.jpg"))
        
        # Test non-matching patterns
        self.assertFalse(RX_LAZY_IMAGE_SRC.match("image.jpg 1x"))
        self.assertFalse(RX_LAZY_IMAGE_SRC.match("image.gif"))
        self.assertFalse(RX_LAZY_IMAGE_SRC.match("image.svg"))

    def test_rx_img_extensions(self):
        """Test RX_IMG_EXTENSIONS regex."""
        # Test image extensions detection
        self.assertTrue(RX_IMG_EXTENSIONS.search("image.jpg"))
        self.assertTrue(RX_IMG_EXTENSIONS.search("image.jpeg"))
        self.assertTrue(RX_IMG_EXTENSIONS.search("image.png"))
        self.assertTrue(RX_IMG_EXTENSIONS.search("image.webp"))
        self.assertTrue(RX_IMG_EXTENSIONS.search("https://example.com/image.jpg?size=large"))
        
        # Test non-matching patterns
        self.assertFalse(RX_IMG_EXTENSIONS.search("image.gif"))
        self.assertFalse(RX_IMG_EXTENSIONS.search("image.svg"))
        self.assertFalse(RX_IMG_EXTENSIONS.search("imagejpg"))  # No dot

    def test_rx_srcset_url(self):
        """Test RX_SRCSET_URL regex."""
        # Test srcset URL detection
        match = RX_SRCSET_URL.search("image.jpg 1x")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image.jpg")
        self.assertEqual(match.group(2), " 1x")
        
        match = RX_SRCSET_URL.search("image.jpg 800w")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image.jpg")
        self.assertEqual(match.group(2), " 800w")
        
        match = RX_SRCSET_URL.search("image.jpg")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image.jpg")
        self.assertIsNone(match.group(2))
        
        match = RX_SRCSET_URL.search("image.jpg, ")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image.jpg,")
        self.assertIsNone(match.group(2))
        
        # Test with multiple URLs
        srcset = "image.jpg 1x, image2.jpg 2x"
        matches = list(RX_SRCSET_URL.finditer(srcset))
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].group(1), "image.jpg")
        self.assertEqual(matches[0].group(2), " 1x")
        self.assertEqual(matches[1].group(1), "image2.jpg")
        self.assertEqual(matches[1].group(2), " 2x")

    def test_rx_b64_data_url(self):
        """Test RX_B64_DATA_URL regex."""
        # Test base64 data URL detection
        match = RX_B64_DATA_URL.search("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFeAJ5gJ2CfQAAAABJRU5ErkJggg==")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image/png")
        
        match = RX_B64_DATA_URL.search("data:text/plain;base64,SGVsbG8gV29ybGQh")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "text/plain")
        
        # Test with spaces
        match = RX_B64_DATA_URL.search("data: image/jpeg ; base64 , /9j/4AAQSkZJRgABAQEAYABgAAD")
        self.assertTrue(match)
        self.assertEqual(match.group(1), "image/jpeg")
        
        # Test non-matching patterns
        self.assertFalse(RX_B64_DATA_URL.search("data:image/png,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFeAJ5gJ2CfQAAAABJRU5ErkJggg=="))  # Missing base64
        self.assertFalse(RX_B64_DATA_URL.search("https://example.com/image.png"))

    def test_rx_json_ld_article_types(self):
        """Test RX_JSON_LD_ARTICLE_TYPES regex."""
        # Test JSON-LD article types detection
        self.assertTrue(RX_JSON_LD_ARTICLE_TYPES.search("Article"))
        self.assertTrue(RX_JSON_LD_ARTICLE_TYPES.search("NewsArticle"))
        self.assertTrue(RX_JSON_LD_ARTICLE_TYPES.search("BlogPosting"))
        self.assertTrue(RX_JSON_LD_ARTICLE_TYPES.search("TechArticle"))
        self.assertTrue(RX_JSON_LD_ARTICLE_TYPES.search("ScholarlyArticle"))
        
        # Test non-matching patterns
        self.assertFalse(RX_JSON_LD_ARTICLE_TYPES.search("WebPage"))
        self.assertFalse(RX_JSON_LD_ARTICLE_TYPES.search("Product"))
        self.assertFalse(RX_JSON_LD_ARTICLE_TYPES.search("Organization"))
        self.assertFalse(RX_JSON_LD_ARTICLE_TYPES.search("xArticle"))  # 'x' prefix prevents match

    def test_rx_cdata(self):
        """Test RX_CDATA regex."""
        # Test CDATA detection
        self.assertTrue(RX_CDATA.search("<![CDATA["))
        self.assertTrue(RX_CDATA.search("]]>"))
        self.assertTrue(RX_CDATA.search("  <![CDATA[  "))
        self.assertTrue(RX_CDATA.search("  ]]>  "))
        
        # Test non-matching patterns
        self.assertFalse(RX_CDATA.search("<![CDATA"))
        self.assertFalse(RX_CDATA.search("]]"))
        self.assertFalse(RX_CDATA.search("CDATA"))

    def test_rx_schema_org(self):
        """Test RX_SCHEMA_ORG regex."""
        # Test schema.org detection
        self.assertTrue(RX_SCHEMA_ORG.search("https://schema.org"))
        self.assertTrue(RX_SCHEMA_ORG.search("http://schema.org"))
        self.assertTrue(RX_SCHEMA_ORG.search("https://schema.org/"))
        
        # Test non-matching patterns
        self.assertFalse(RX_SCHEMA_ORG.search("https://schema.org/Article"))
        self.assertFalse(RX_SCHEMA_ORG.search("https://schemas.org"))
        self.assertFalse(RX_SCHEMA_ORG.search("https://example.com/schema.org"))

    def test_rx_positive_class(self):
        """Test RX_POSITIVE_CLASS regex."""
        # Test positive class detection
        self.assertTrue(RX_POSITIVE_CLASS.search("article"))
        self.assertTrue(RX_POSITIVE_CLASS.search("content"))
        self.assertTrue(RX_POSITIVE_CLASS.search("main"))
        self.assertTrue(RX_POSITIVE_CLASS.search("blog-post"))
        self.assertTrue(RX_POSITIVE_CLASS.search("article-content"))
        
        # Test non-matching patterns
        self.assertFalse(RX_POSITIVE_CLASS.search("sidebar"))
        self.assertFalse(RX_POSITIVE_CLASS.search("footer"))
        self.assertFalse(RX_POSITIVE_CLASS.search("comment"))

    def test_rx_negative_class(self):
        """Test RX_NEGATIVE_CLASS regex."""
        # Test negative class detection
        self.assertTrue(RX_NEGATIVE_CLASS.search("sidebar"))
        self.assertTrue(RX_NEGATIVE_CLASS.search("comment"))
        self.assertTrue(RX_NEGATIVE_CLASS.search("footer"))
        self.assertTrue(RX_NEGATIVE_CLASS.search("hidden"))
        self.assertTrue(RX_NEGATIVE_CLASS.search("social-share"))
        
        # Test non-matching patterns
        self.assertFalse(RX_NEGATIVE_CLASS.search("article"))
        self.assertFalse(RX_NEGATIVE_CLASS.search("content"))
        self.assertFalse(RX_NEGATIVE_CLASS.search("main"))

    def test_rx_byline(self):
        """Test RX_BYLINE regex."""
        # Test byline detection
        self.assertTrue(RX_BYLINE.search("byline"))
        self.assertTrue(RX_BYLINE.search("author"))
        self.assertTrue(RX_BYLINE.search("dateline"))
        self.assertTrue(RX_BYLINE.search("writtenby"))
        self.assertTrue(RX_BYLINE.search("p-author"))
        
        # Test non-matching patterns
        self.assertFalse(RX_BYLINE.search("content"))
        self.assertFalse(RX_BYLINE.search("article"))
        self.assertFalse(RX_BYLINE.search("publication"))

    def test_rx_unlikely_candidates(self):
        """Test RX_UNLIKELY_CANDIDATES regex."""
        # Test unlikely candidates detection
        self.assertTrue(RX_UNLIKELY_CANDIDATES.search("sidebar"))
        self.assertTrue(RX_UNLIKELY_CANDIDATES.search("comment"))
        self.assertTrue(RX_UNLIKELY_CANDIDATES.search("footer"))
        self.assertTrue(RX_UNLIKELY_CANDIDATES.search("header"))
        self.assertTrue(RX_UNLIKELY_CANDIDATES.search("social"))
        
        # Test non-matching patterns
        self.assertFalse(RX_UNLIKELY_CANDIDATES.search("article"))
        self.assertFalse(RX_UNLIKELY_CANDIDATES.search("content"))
        self.assertFalse(RX_UNLIKELY_CANDIDATES.search("main"))

    def test_rx_maybe_candidate(self):
        """Test RX_MAYBE_CANDIDATE regex."""
        # Test maybe candidate detection
        self.assertTrue(RX_MAYBE_CANDIDATE.search("article"))
        self.assertTrue(RX_MAYBE_CANDIDATE.search("body"))
        self.assertTrue(RX_MAYBE_CANDIDATE.search("content"))
        self.assertTrue(RX_MAYBE_CANDIDATE.search("main"))
        self.assertTrue(RX_MAYBE_CANDIDATE.search("column"))
        self.assertTrue(RX_MAYBE_CANDIDATE.search("shadow"))
        
        # Test non-matching patterns
        self.assertFalse(RX_MAYBE_CANDIDATE.search("sidebar"))
        self.assertFalse(RX_MAYBE_CANDIDATE.search("footer"))
        self.assertFalse(RX_MAYBE_CANDIDATE.search("comment"))

    def test_rx_normalize_spaces(self):
        """Test RX_NORMALIZE_SPACES regex."""
        # Test normalize spaces
        self.assertEqual(RX_NORMALIZE_SPACES.sub(" ", "  hello  world  "), " hello world ")
        self.assertEqual(RX_NORMALIZE_SPACES.sub(" ", "hello\n\n\nworld"), "hello world")
        self.assertEqual(RX_NORMALIZE_SPACES.sub(" ", "hello\t\t\tworld"), "hello world")
        self.assertEqual(RX_NORMALIZE_SPACES.sub(" ", "hello   world"), "hello world")

    def test_constants(self):
        """Test constants."""
        # Test UNLIKELY_ROLES
        self.assertTrue("menu" in UNLIKELY_ROLES)
        self.assertTrue("navigation" in UNLIKELY_ROLES)
        self.assertTrue("complementary" in UNLIKELY_ROLES)
        self.assertTrue(UNLIKELY_ROLES["menu"])
        
        # Test DIV_TO_P_ELEMS
        self.assertTrue("div" in DIV_TO_P_ELEMS)
        self.assertTrue("blockquote" in DIV_TO_P_ELEMS)
        self.assertTrue("p" in DIV_TO_P_ELEMS)
        self.assertTrue(DIV_TO_P_ELEMS["div"])
        
        # Test ALTER_TO_DIV_EXCEPTIONS
        self.assertTrue("div" in ALTER_TO_DIV_EXCEPTIONS)
        self.assertTrue("article" in ALTER_TO_DIV_EXCEPTIONS)
        self.assertTrue("section" in ALTER_TO_DIV_EXCEPTIONS)
        self.assertTrue("p" in ALTER_TO_DIV_EXCEPTIONS)
        
        # Test PRESENTATIONAL_ATTRIBUTES
        self.assertTrue("align" in PRESENTATIONAL_ATTRIBUTES)
        self.assertTrue("style" in PRESENTATIONAL_ATTRIBUTES)
        self.assertTrue("border" in PRESENTATIONAL_ATTRIBUTES)
        
        # Test DEPRECATED_SIZE_ATTRIBUTE_ELEMS
        self.assertTrue("table" in DEPRECATED_SIZE_ATTRIBUTE_ELEMS)
        self.assertTrue("th" in DEPRECATED_SIZE_ATTRIBUTE_ELEMS)
        self.assertTrue("td" in DEPRECATED_SIZE_ATTRIBUTE_ELEMS)
        
        # Test PHRASING_ELEMS
        self.assertTrue("span" in PHRASING_ELEMS)
        self.assertTrue("img" in PHRASING_ELEMS)
        self.assertTrue("a" not in PHRASING_ELEMS)  # 'a' is not in the list


class TestHelperFunctions(unittest.TestCase):
    """Test the helper functions."""
    
    def test_is_positive_class(self):
        """Test is_positive_class function."""
        # Test positive classes
        self.assertTrue(is_positive_class("article"))
        self.assertTrue(is_positive_class("content"))
        self.assertTrue(is_positive_class("main"))
        self.assertTrue(is_positive_class("blog-post"))
        self.assertTrue(is_positive_class("article-content"))
        
        # Test negative classes
        self.assertFalse(is_positive_class("sidebar"))
        self.assertFalse(is_positive_class("footer"))
        self.assertFalse(is_positive_class("comment"))
        self.assertFalse(is_positive_class(""))
        self.assertFalse(is_positive_class(None))
    
    def test_is_negative_class(self):
        """Test is_negative_class function."""
        # Test negative classes
        self.assertTrue(is_negative_class("sidebar"))
        self.assertTrue(is_negative_class("comment"))
        self.assertTrue(is_negative_class("footer"))
        self.assertTrue(is_negative_class("hidden"))
        self.assertTrue(is_negative_class("social-share"))
        
        # Test positive classes
        self.assertFalse(is_negative_class("article"))
        self.assertFalse(is_negative_class("content"))
        self.assertFalse(is_negative_class("main"))
        self.assertFalse(is_negative_class(""))
        self.assertFalse(is_negative_class(None))
    
    def test_is_byline(self):
        """Test is_byline function."""
        # Test bylines
        self.assertTrue(is_byline("byline"))
        self.assertTrue(is_byline("author"))
        self.assertTrue(is_byline("dateline"))
        self.assertTrue(is_byline("writtenby"))
        self.assertTrue(is_byline("p-author"))
        
        # Test non-bylines
        self.assertFalse(is_byline("content"))
        self.assertFalse(is_byline("article"))
        self.assertFalse(is_byline("publication"))
        self.assertFalse(is_byline(""))
        self.assertFalse(is_byline(None))
    
    def test_is_unlikely_candidate(self):
        """Test is_unlikely_candidate function."""
        # Test unlikely candidates
        self.assertTrue(is_unlikely_candidate("sidebar"))
        self.assertTrue(is_unlikely_candidate("comment"))
        self.assertTrue(is_unlikely_candidate("footer"))
        self.assertTrue(is_unlikely_candidate("header"))
        self.assertTrue(is_unlikely_candidate("social"))
        
        # Test likely candidates
        self.assertFalse(is_unlikely_candidate("article"))
        self.assertFalse(is_unlikely_candidate("content"))
        self.assertFalse(is_unlikely_candidate("main"))
        self.assertFalse(is_unlikely_candidate(""))
        self.assertFalse(is_unlikely_candidate(None))
    
    def test_maybe_its_a_candidate(self):
        """Test maybe_its_a_candidate function."""
        # Test maybe candidates
        self.assertTrue(maybe_its_a_candidate("article"))
        self.assertTrue(maybe_its_a_candidate("body"))
        self.assertTrue(maybe_its_a_candidate("content"))
        self.assertTrue(maybe_its_a_candidate("main"))
        self.assertTrue(maybe_its_a_candidate("column"))
        
        # Test non-maybe candidates
        self.assertFalse(maybe_its_a_candidate("sidebar"))
        self.assertFalse(maybe_its_a_candidate("footer"))
        self.assertFalse(maybe_its_a_candidate("comment"))
        self.assertFalse(maybe_its_a_candidate(""))
        self.assertFalse(maybe_its_a_candidate(None))
    
    def test_count_commas(self):
        """Test count_commas function."""
        # Test comma counting
        self.assertEqual(count_commas("hello, world"), 1)
        self.assertEqual(count_commas("one, two, three, four"), 3)
        self.assertEqual(count_commas("no commas here"), 0)
        self.assertEqual(count_commas(""), 0)
    
    def test_normalize_spaces(self):
        """Test normalize_spaces function."""
        # Test space normalization
        self.assertEqual(normalize_spaces("  hello  world  "), " hello world ")
        self.assertEqual(normalize_spaces("hello\n\n\nworld"), "hello world")
        self.assertEqual(normalize_spaces("hello\t\t\tworld"), "hello world")
        self.assertEqual(normalize_spaces("hello   world"), "hello world")
        self.assertEqual(normalize_spaces(""), "")
    
    def test_evaluate_class_weight(self):
        """Test evaluate_class_weight function."""
        # Test with positive class
        self.assertEqual(evaluate_class_weight("article"), 25)
        self.assertEqual(evaluate_class_weight("content"), 25)
        self.assertEqual(evaluate_class_weight("main"), 25)
        
        # Test with negative class
        self.assertEqual(evaluate_class_weight("sidebar"), -25)
        self.assertEqual(evaluate_class_weight("comment"), -25)
        self.assertEqual(evaluate_class_weight("footer"), -25)
        
        # Test with both positive and negative
        self.assertEqual(evaluate_class_weight("article sidebar"), 0)  # +25 -25 = 0
        
        # Test with ID
        self.assertEqual(evaluate_class_weight("", "content"), 25)
        self.assertEqual(evaluate_class_weight("", "sidebar"), -25)
        self.assertEqual(evaluate_class_weight("article", "sidebar"), 0)  # +25 -25 = 0
        
        # Test with empty values
        self.assertEqual(evaluate_class_weight(""), 0)
        self.assertEqual(evaluate_class_weight("", ""), 0)
        self.assertEqual(evaluate_class_weight(None, None), 0)
