def pytest_collection_modifyitems(items):
    """Добавлять маркеры автоматически к каждому тесту."""

    for item in items:
        item.add_marker('django_db')
