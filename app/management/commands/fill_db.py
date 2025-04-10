import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike, QuestionDislike, AnswerDislike
from django.db import connection, transaction

RATIO = 100
MAX_TAGS_PER_QUESTION = 3

class Command(BaseCommand):
    help = 'Fills the database with randomized data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', type=int, default=RATIO,
                            help='Coefficient for scaling the amount of data')

    def handle(self, *args, **options):
        ratio = options['ratio']

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_ratings = ratio * 100  # for each type of rating

        with transaction.atomic():  

            # Users (Bulk Create)
            users = [User(username=get_random_string(10) + str(i),
                          email=f'{get_random_string(10) + str(i)}@example.com',  
                          password='password123')
                     for i in range(num_users)]
            User.objects.bulk_create(users)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users'))

            # Users -> Profiles (Bulk Create)
            profiles = [Profile(user=user) for user in users]
            Profile.objects.bulk_create(profiles)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(profiles)} profiles'))

            # Tags (Bulk Create)
            tags = [Tag(name=get_random_string(8) + str(i)) for i in range(num_tags)]
            Tag.objects.bulk_create(tags)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(tags)} tags'))

            # Create questions
            questions = []
            for i in range(num_questions):
                title = f'Random Question {i} ' + get_random_string(20)
                content = f'Random content for question {i} ' + get_random_string(50)
                author = random.choice(profiles)
                questions.append(Question(title=title, content=content, author=author))

            Question.objects.bulk_create(questions)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(questions)} questions'))

            # Tag Assignment
            self.stdout.write('Assigning tags to questions...')

            
            tags = list(Tag.objects.all())
            questions = list(Question.objects.all())

            question_tags = []  

            for question in questions:
                num_tags_to_add = random.randint(0, min(MAX_TAGS_PER_QUESTION, len(tags)))
                random_tags = random.sample(tags, num_tags_to_add)

                for tag in random_tags:
                    question_tags.append((question.id, tag.id)) 

           
            with connection.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO app_question_tags (question_id, tag_id) VALUES (%s, %s)",
                    question_tags,
                )

            self.stdout.write(self.style.SUCCESS('Finished assigning tags to questions!'))

            # Answers 
            self.stdout.write('Creating answers...')
            questions = list(Question.objects.all())  
            answers = []
            for i in range(num_answers):
                question = random.choice(questions)
                content = f'Random answer content {i} ' + get_random_string(50)
                author = random.choice(profiles)
                answers.append(Answer(question=question, content=content, author=author))
            Answer.objects.bulk_create(answers)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(answers)} answers'))

            # Create unique pairs for likes and dislikes
            self.stdout.write('Creating likes/dislikes...')
            num_total_ratings = num_ratings * 2  # Total likes and dislikes for both Question and Answer

            
            question_likes = []
            question_dislikes = []
            question_pairs = set()

            
            answer_likes = []
            answer_dislikes = []
            answer_pairs = set()

            question_model_count = Question.objects.count()
            answer_model_count = Answer.objects.count()
            users_count = User.objects.count()

            for _ in range(num_total_ratings): 
                user = users[random.randint(0,users_count - 1)]
                if random.random() < 0.5: # QuestionLike , QuestionDislike

                    question = questions[random.randint(0, question_model_count - 1)]
                    if (question.id, user.id) not in question_pairs:
                        if random.random() < 0.5:
                            question_likes.append(QuestionLike(question=question, user=user))
                        else:
                            question_dislikes.append(QuestionDislike(question=question, user=user))
                        question_pairs.add((question.id, user.id))

                else: # AnswerLike, AnswerDislike
                    answer = answers[random.randint(0, answer_model_count - 1)]
                    if (answer.id, user.id) not in answer_pairs:
                        if random.random() < 0.5:
                            answer_likes.append(AnswerLike(answer=answer, user=user))
                        else:
                            answer_dislikes.append(AnswerDislike(answer=answer, user=user))
                        answer_pairs.add((answer.id, user.id))

            QuestionLike.objects.bulk_create(question_likes)
            QuestionDislike.objects.bulk_create(question_dislikes)

            AnswerLike.objects.bulk_create(answer_likes)
            AnswerDislike.objects.bulk_create(answer_dislikes)

            self.stdout.write(self.style.SUCCESS('Likes and dislikes created. Exiting'))
        self.stdout.write(self.style.SUCCESS('Finished filling the database!'))
        