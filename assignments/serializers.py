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
            "model_answer",
            "submitted",
            "grade",
            "created_at",
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    student_name = serializers.CharField(source='student.username', read_only=True)
    assignment_question = serializers.CharField(source='assignment.question', read_only=True)
    submitted_at = serializers.ReadOnlyField()

    class Meta:
        model = Submission
        fields = ["id", "assignment", "assignment_question", "student", "student_name", "file", "link", "text", "submitted_at", "grade", "feedback"]
        read_only_fields = ["grade", "feedback"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not (attrs.get("file") or attrs.get("link") or attrs.get("text")):
            raise serializers.ValidationError(
                "You must provide a file, link, or text for the submission."
            )
        return attrs
class SubmissionGradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
        
    def validate_grade(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("The grade must be between 0 and 100.")
        return value
