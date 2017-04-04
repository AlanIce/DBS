class Field(object):
	def __init__(self, columnType, isPrimaryKey=False, default=None, comment=None):
		self.columnType = columnType
		self.isPrimaryKey = isPrimaryKey
		self.default = default
		self.comment = comment

class StringField(Field):
	def __init__(self, columnType, isPrimaryKey=False, default='', comment=None):
		super().__init__(columnType, isPrimaryKey, default, comment)

class IntegerField(Field):
	def __init__(self, isPrimaryKey=False, default=0, comment=None):
		super().__init__('int', isPrimaryKey, default, comment)

class FloatField(Field):
	def __init__(self, isPrimaryKey=False, default=0, comment=None):
		super().__init__('real', isPrimaryKey, default, comment)