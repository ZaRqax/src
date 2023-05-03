ENTITIES_ORDERING_FIELDS = (
    'title',
    'parent__title',
    'type__title',
)
ENTITY_CHILDREN_ORDERING_FIELDS = ('created_at',)
XLSX_FILE_NAME = 'Перечень объектов ({date}).xlsx'
