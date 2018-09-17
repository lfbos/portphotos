from rest_framework import serializers


class PhotoSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    client_modified = serializers.DateTimeField()
    parent_shared_folder_id = serializers.CharField(max_length=200)
    media_info = serializers.CharField(max_length=200)
    content_hash = serializers.CharField(max_length=200)
    path_display = serializers.CharField(max_length=200)
    size = serializers.IntegerField()
    thumbnail = serializers.CharField(max_length=1024, required=False)

