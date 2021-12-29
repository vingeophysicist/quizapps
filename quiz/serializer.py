from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizTaker, UsersAnswer

class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'image', 'slug', 'questions_count']
        read_only_fields = ['questions_count']

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "label"]

class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = "__all__"
        
        
class MyQuizListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "image", "slug", "question_count", "completed", "score", "progress"]
        read_only_fields = ["question_count", "completed", "progress"]
        
    def get_completed(self,obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            return quiztaker.completed
        except QuizTaker.DoesNotExist:
            return None
    
    def get_progress(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == False:
                question_answered = UsersAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
                total_question = obj.question_set.all().count()
                return int(question_answered / total_question)
            return None
        except QuizTaker.DoesNotExist:
            return None
    
    
    def get_question_count(self, obj):
        return obj.question_set.all().count()
    
    def get_score(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == True:
                return quiztaker.score
            return None
        except QuizTaker.DoesNotExist:
            return None
        
                
        
        
class QuizTakerSerializer(serializers.ModelSerializer):
    usersanswer_set = UsersAnswerSerializer(many=True)

    class Meta:
        model = QuizTaker
        fields = "__all__"  


class QuizDetailSerializer(serializers.ModelSerializer):
	quiztakers_set = serializers.SerializerMethodField()
	question_set = QuestionSerializer(many=True)

	class Meta:
		model = Quiz
		fields = "__all__"

	def get_quiztakers_set(self, obj):
		try:
			quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
			serializer = QuizTakerSerializer(quiz_taker)
			return serializer.data
		except QuizTaker.DoesNotExist:
			return None



