from rest_framework import serializers
from .models import Assignment, Submission
from typing import Any, Dict

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id",
            "lesson",
            "kid",
            "question",
            "answer",
            "submitted",
            "grade",
            "created_at",
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    submitted_at = serializers.ReadOnlyField()

    class Meta:
        model = Submission
        fields = ["id", "assignment", "student", "file", "link", "text", "submitted_at", "grade", "feedback"]
        read_only_fields = ["grade", "feedback"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not (attrs.get("file") or attrs.get("link") or attrs.get("text")):
            raise serializers.ValidationError(
                "You must provide a file, link, or text for the submission."
            )
        return attrs
