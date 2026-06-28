

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активна'),
        ),

        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),

        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1,
                                                         verbose_name='Количество')),
                ('cart', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items', to='store.cart',
                    verbose_name='Корзина')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Позиция корзины',
                'verbose_name_plural': 'Позиции корзины',
            },
        ),

        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(
                blank=True, related_name='carts',
                through='store.CartItem', to='store.product',
                verbose_name='Товары'),
        ),
    ]
