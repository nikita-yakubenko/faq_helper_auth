from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    objects = UserManager() # IMPORTANT! don't forget to include it

    username = None # to force django to login using email instead of username
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Organization(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    name = models.CharField(verbose_name='Название', max_length=255)


class Knowledgedb(models.Model):

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    name = models.CharField(verbose_name='Название', max_length=255)
    is_active = models.BooleanField(default=False)


class QnARelation(models.Model):

    knowledgedb = models.ForeignKey(Knowledgedb, on_delete=models.CASCADE, verbose_name='База знаний')


class Answer(models.Model):

    text = models.TextField(verbose_name='Текст ответа')
    qna_relation = models.OneToOneField(QnARelation, on_delete=models.CASCADE, verbose_name='Связка')


class Question(models.Model):

    text = models.TextField(verbose_name='Текст вопроса')
    qna_relation = models.ForeignKey(QnARelation, on_delete=models.CASCADE, verbose_name='Связка')
