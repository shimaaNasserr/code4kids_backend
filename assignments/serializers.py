from rest_framework import serializers
from .models import Assignment, Submission
from lessons.models import Lesson
from typing import Any, Dict

class AssignmentSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.course.title', read_only=True)
    submissions_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            "id",
            "lesson",
            "lesson_title",
            "course_title",
            "question",
            "model_answer",
            "grade",
            "created_at",
            "submissions_count"
        ]
        read_only_fields = ['created_at', 'submissions_count']

    def get_submissions_count(self, obj):
        return obj.submissions.count()

    def validate_lesson(self, value):
        if not Lesson.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Lesson does not exist.")
        return value

class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    student_name = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    assignment_question = serializers.CharField(source='assignment.question', read_only=True)
    lesson_title = serializers.CharField(source='assignment.lesson.title', read_only=True)
    course_title = serializers.CharField(source='assignment.lesson.course.title', read_only=True)
    submitted_at = serializers.ReadOnlyField()
    is_graded = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = [
            "id", "assignment", "assignment_question", "lesson_title", "course_title",
            "student", "student_name", "student_email", "file", "link", "text",
            "submitted_at", "grade", "feedback", "is_graded"
        ]
        read_only_fields = ["grade", "feedback", "submitted_at", "is_graded"]

    def get_is_graded(self, obj):
        return obj.grade is not None

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not (attrs.get("file") or attrs.get("link") or attrs.get("text")):
            raise serializers.ValidationError(
                "You must provide at least one of: file, link, or text for the submission."
            )
        
        assignment = attrs.get('assignment')
        student = self.context['request'].user
        
        if self.instance is None: 
            if Submission.objects.filter(assignment=assignment, student=student).exists():
                raise serializers.ValidationError(
                    "You have already submitted for this assignment."
                )
        
        return attrs

class SubmissionGradingSerializer(serializers.ModelSerializer):
    graded_by = serializers.CharField(source='graded_by.username', read_only=True)
    graded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'grade', 'feedback', 'graded_by', 'graded_at']
        
    def validate_grade(self, value):
        """التحقق من صحة الدرجة"""
        if value is not None:
            if not (0 <= value <= 100):
                raise serializers.ValidationError("Grade must be between 0 and 100.")
        return value

class AssignmentDetailSerializer(AssignmentSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)
    
    class Meta(AssignmentSerializer.Meta):
        fields = AssignmentSerializer.Meta.fields + ['submissions']