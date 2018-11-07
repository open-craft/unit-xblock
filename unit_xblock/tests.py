from __future__ import absolute_import, division, print_function, unicode_literals
import re
import unittest
from xml.dom import minidom

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.completable import XBlockCompletionMode
from xblock.test.test_parsing import XmlTest

from unit_xblock import UnitXBlock


class FakeHTMLBlock(XBlock):
    """ An HTML block for use in tests """
    def student_view(self, context=None):
        """Provide simple HTML student view."""
        return Fragment("This is some HTML.")


class FakeVideoBlock(XBlock):
    """ A video block for use in tests """
    def student_view(self, context=None):
        """Provide simple Video student view."""
        return Fragment(
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/B-EFayAA5_0"'
            ' frameborder="0" allow="autoplay; encrypted-media"></iframe>'
        )


class UnitXBlockTests(XmlTest, unittest.TestCase):
    """
    Tests of the Unit XBlock.

    There's not much to this block, so we keep it simple.
    """
    maxDiff = None

    @XBlock.register_temp_plugin(FakeHTMLBlock, identifier='html')
    @XBlock.register_temp_plugin(FakeVideoBlock, identifier='video')
    def test_unit_html(self):
        block = self.parse_xml_to_block("""\
            <unit>
                <html/>
                <video/>
            </unit>
        """)

        html = block.runtime.render(block, 'student_view').content

        self.assertXmlEqual(html, (
            '<div class="xblock-v1 xblock-v1-student_view" data-usage="u_1" data-block-type="unit">'
                '<div class="unit-xblock vertical">'
                    '<div class="xblock-v1 xblock-v1-student_view" data-usage="u_3" data-block-type="html">'
                        'This is some HTML.'
                    '</div>'
                    '<div class="xblock-v1 xblock-v1-student_view" data-usage="u_5" data-block-type="video">'
                        '<iframe width="560" height="315" src="https://www.youtube.com/embed/B-EFayAA5_0"'
                        ' frameborder="0" allow="autoplay; encrypted-media"></iframe>'
                    '</div>'
                '</div>'
            '</div>'
        ))

    def test_is_aggregator(self):
        self.assertEqual(XBlockCompletionMode.get_mode(UnitXBlock), XBlockCompletionMode.AGGREGATOR)

    def assertXmlEqual(self, xml_str_a, xml_str_b):
        """
        Assert that the given XML strings are equal,
        ignoring attribute order and some whitespace variations.
        """
        def clean(xml_str):
            # Collapse repeated whitespace:
            xml_str = re.sub(r'(\s)\s+', r'\1', xml_str)
            xml_bytes = xml_str.encode('utf8')
            return minidom.parseString(xml_bytes).toprettyxml()
        self.assertEqual(clean(xml_str_a), clean(xml_str_b))
