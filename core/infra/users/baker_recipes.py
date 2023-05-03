from itertools import cycle

from model_bakery.recipe import (
    Recipe,
    seq,
)

from .models import User


first_name_choices = ['Алексей', 'Александр', 'Денис', 'Владимир', 'Олег', 'Владислав']
last_name_choices = ['Сидоров', 'Иванов', 'Петров', 'Сердюков', 'Кузнецов', 'Попов', 'Васильев']
middle_name_choices = ['Алексеевич', 'Александрович', 'Денисович', 'Владимирович', 'Олегович', 'Владиславович']


user = Recipe(
    User,
    email=seq('user', suffix='@example.com'),
    first_name=cycle(first_name_choices),
    last_name=cycle(last_name_choices),
    middle_name=cycle(middle_name_choices),
    is_active=True,
)
