from guardian.shortcuts import assign_perm
from rest_framework.viewsets import ModelViewSet

from onadata.apps.api import serializers
from onadata.apps.api import permissions
from onadata.apps.api import mixins
from onadata.apps.api.tools import get_xform
from onadata.apps.odk_logger.models import Note


class NoteViewSet(mixins.ViewPermissionMixin, ModelViewSet):
    """## Add Notes to a submission

A `POST` payload of parameters:

    `note` - the note string to add to a data point
    `instance` - the data point id

 <pre class="prettyprint">
  <b>POST</b> /api/v1/notes</pre>

Payload

    {"instance": 1, "note": "This is a note."}

  > Response
  >
  >     {
  >          "id": 1,
  >          "instance": 1,
  >          "note": "This is a note."
  >          ...
  >     }
  >
  >     HTTP 201 OK

# Get List of notes for a data point

A `GET` request will return the list of notes applied to a data point.

 <pre class="prettyprint">
  <b>GET</b> /api/v1/notes</pre>


  > Response
  >
  >     [{
  >          "id": 1,
  >          "instance": 1,
  >          "note": "This is a note."
  >          ...
  >     }, ...]
  >
  >
  >        HTTP 200 OK
"""
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = [permissions.ViewDjangoObjectPermissions,
                          permissions.IsAuthenticated, ]

    def pre_save(self, obj):
        # throws PermissionDenied if request.user has no permission to xform
        get_xform(obj.instance.xform.pk, self.request)

    def post_save(self, obj, created=False):
        if created:
            assign_perm('add_note', self.request.user, obj)
            assign_perm('change_note', self.request.user, obj)
            assign_perm('delete_note', self.request.user, obj)
            assign_perm('view_note', self.request.user, obj)

    def create(self, request, *args, **kwargs):
        return super(self.__class__, self).create(request, *args, **kwargs)
