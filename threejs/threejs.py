"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.template import Template, Context
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment
from xblock.reference.plugins import Filesystem
from xblockutils.studio_editable import StudioEditableXBlockMixin


@XBlock.needs('fs')
class ThreeJSXBlock(StudioEditableXBlockMixin, XBlock):
    """
    XBlock for show 3D model
    """

    count = Integer(
            default=0, scope=Scope.user_state,
            help="A simple counter, to show something happening",
    )

    three_model = String(
        default='',
        scope=Scope.settings,
        resettable_editor=False,
        help="3D model in JSON presition"
    )
    texture = String(
        default='',
        scope=Scope.settings,
        resettable_editor=False,
        help="Model Texture "
    )

    editable_fields = ('texture', 'three_model')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ThreeJSXBlock, shown to students
        when viewing courses.
        """

        context = {
            'self': self
        }
        template = self.render_template("static/html/threejs.html", context)
        frag = Fragment(template)
        frag.add_css(self.resource_string("static/css/threejs.css"))
        frag.add_javascript(self.resource_string("static/js/src/three.min.js"))
        frag.add_javascript(self.resource_string("static/js/src/car.js"))
        frag.add_javascript(self.resource_string("static/js/src/threejs.js"))
        frag.add_javascript(self.resource_string("static/js/src/main.js"))

        frag.initialize_js('ThreeJSXBlock')
        return frag

    def studio_view(self, context):
        """
        Render a form for editing this XBlock
        """
        fragment = Fragment()
        context = {'fields': []}
        # Build a list of all the fields that can be edited:
        for field_name in self.editable_fields:
            field = self.fields[field_name]
            assert field.scope in (Scope.content, Scope.settings), (
                "Only Scope.content or Scope.settings fields can be used with "
                "StudioEditableXBlockMixin. Other scopes are for user-specific data and are "
                "not generally created/configured by content authors in Studio."
            )
            field_info = self._make_field_info(field_name, field)
            if field_info is not None:
                context["fields"].append(field_info)
        fragment.content = self.render_template('static/html/studio_edit.html', context)
        fragment.add_css(self.resource_string("static/css/threejs.css"))
        fragment.add_javascript(self.resource_string("static/js/src/studio_edit.js"))
        fragment.initialize_js('ThreeJSStudioEditableXBlock')
        return fragment


    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def file_upload(self, data, suffix=''):
        pass

    def get_current_url_resource(self):
        return 'http://127.0.0.1:8880/user/name/tree'

    def render_template(self, template_path, context):
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    def _make_field_info(self, field_name, field):
        info = super(ThreeJSXBlock, self)._make_field_info(field_name, field)
        if field_name == 'file_noteBook':
            info['type'] = 'file_uploader'
        return info

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ThreeJSXBlock",
             """<threejs/>
             """),
            ("Multiple ThreeJSXBlock",
             """<vertical_demo>
                <threejs/>
                <threejs/>
                <threejs/>
                </vertical_demo>
             """),
        ]
