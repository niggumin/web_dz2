from django.db import models
from django.contrib.auth.models import User
# from django.db.models import Q


# Managers

class QuestionManager(models.Manager):
    def best(self):
        return self.order_by('-likes')  

    def new(self):
        return self.order_by('-created_at')

    def with_tag(self, tag_name):
        return self.filter(tag__name = tag_name)
    
    

class AnswerManager(models.Manager):

    def under_question(self, question):
        return self.filter(question=question)

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username  


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    tags = models.ManyToManyField(Tag, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()  

    
    def likes_count(self):
        return self.likes.count()

    
    def dislikes_count(self):
        return self.dislikes.count()
    
    def answers_count(self):  
        return self.answer_set.count()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def likes_count(self):
        return self.likes.count()

    
    def dislikes_count(self):
        return self.dislikes.count()
    
    def __str__(self):
        return f'Ответ на вопрос "{self.question.title}" от {self.author.user.username}'


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')  # Added related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')

class QuestionDislike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='dislikes')  # Added related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')  # Added related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

class AnswerDislike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='dislikes')  # Added related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('answer', 'user')