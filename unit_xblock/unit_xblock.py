"""
An XBlock which groups related XBlocks together.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from web_fragments.fragment import Fragment
from xblock.completable import XBlockCompletionMode
from xblock.core import XBlock
from xblock.fields import Scope, String


# Make '_' a no-op so we can scrape strings.
_ = lambda text: text


class UnitXBlock(XBlock):
    """
    Unit XBlock: An XBlock which groups related XBlocks together.

    This is meant to replace most usages of the "vertical" XBlock.

    This version is explicitly designed to not contain LMS-related
    logic, like vertical does. The application which renders XBlocks
    and/or the runtime should manage things like bookmarks, completion
    tracking, etc.

    This version also avoids any and all XModule mixins.
    """
    has_children = True
    completion_mode = XBlockCompletionMode.AGGREGATOR

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.content,
        default=_("Unit"),
    )

    def student_view(self, context=None):
        """Provide default student view."""
        result = Fragment()
        child_frags = self.runtime.render_children(self, context=context)
        result.add_resources(child_frags)
        result.add_content('<div class="unit-xblock vertical">')
        for frag in child_frags:
            result.add_content(frag.content)
        result.add_content('</div>')
        return result

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("UnitXBlock",
             """
                <unit>
                    <html_demo>
                        This is an <strong>HTML</strong> XBlock inside the unit.
                        Below is a separate "thumbs" block:
                    </html_demo>
                    <thumbs/>
                </unit>
             """),
        ]

    def get_icon_class(self):
        """
        Returns the highest priority icon class.
        """
        child_classes = set(child.get_icon_class() for child in self.get_children())
        new_class = 'other'
        CLASS_PRIORITY = ['video', 'problem']  # Copied from vertical_block.py. Make this configurable?
        for higher_class in CLASS_PRIORITY:
            if higher_class in child_classes:
                new_class = higher_class
        return new_class

    def index_dictionary(self):
        """
        Return dictionary prepared with module content and type for indexing.
        """
        # return key/value fields in a Python dict object
        # values may be numeric / string or dict
        # default implementation is an empty dict
        xblock_body = super(UnitXBlock, self).index_dictionary()
        index_body = {
            "display_name": self.display_name,
        }
        if "content" in xblock_body:
            xblock_body["content"].update(index_body)
        else:
            xblock_body["content"] = index_body
        # We use "Sequence" for sequentials and units/verticals
        xblock_body["content_type"] = "Sequence"

        return xblock_body
