from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True,
                                          verbose_name='Название жанра')),
                ('slug', models.SlugField(max_length=100, unique=True,
                                          verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100,
                                                verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100,
                                               verbose_name='Фамилия')),
                ('birth_year', models.PositiveSmallIntegerField(
                    blank=True, null=True, verbose_name='Год рождения')),
                ('bio', models.TextField(blank=True, verbose_name='Биография')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255,
                                           verbose_name='Название')),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='books',
                    to='catalog.author',
                    verbose_name='Автор',
                )),
                ('genres', models.ManyToManyField(
                    blank=True,
                    related_name='books',
                    to='catalog.genre',
                    verbose_name='Жанры',
                )),
                ('description', models.TextField(verbose_name='Описание')),
                ('published_year', models.PositiveSmallIntegerField(
                    verbose_name='Год издания')),
                ('pages', models.PositiveSmallIntegerField(
                    verbose_name='Количество страниц')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8,
                                              verbose_name='Цена (руб.)')),
                ('rating', models.FloatField(
                    default=0.0,
                    validators=[
                        django.core.validators.MinValueValidator(0.0),
                        django.core.validators.MaxValueValidator(5.0),
                    ],
                    verbose_name='Рейтинг',
                )),
                ('status', models.CharField(
                    choices=[
                        ('available', 'В наличии'),
                        ('out_of_stock', 'Нет в наличии'),
                        ('coming_soon', 'Скоро в продаже'),
                    ],
                    default='available',
                    max_length=20,
                    verbose_name='Статус',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Добавлена')),
                ('cover_color', models.CharField(
                    default='#4A90D9',
                    help_text='Например: #4A90D9',
                    max_length=7,
                    verbose_name='Цвет обложки (HEX)',
                )),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['-created_at'],
            },
        ),

        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reviews',
                    to='catalog.book',
                    verbose_name='Книга',
                )),
                ('reviewer_name', models.CharField(max_length=100,
                                                   verbose_name='Имя читателя')),
                ('score', models.PositiveSmallIntegerField(
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(5),
                    ],
                    verbose_name='Оценка (1-5)',
                )),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Дата отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
    ]
