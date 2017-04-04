from .Field import *

class ModolMetaclass(type):
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)

		if attrs.get('__table__', None) == None:
			raise RuntimeError('未指定表名称')

		mappings = dict()
		fields = []
		primaryKey = None

		for k, v in attrs.items():
			if isinstance(v, Field):
				mappings[k] = v
				if v.isPrimaryKey:
					if primaryKey:
						raise RuntimeError('已经指定了主键！')
					primaryKey = k
				else:
					fields.append(k)
		for k in fields:
			attrs.pop(k)
		if not primaryKey:
			raise RuntimeError(attrs.__table__ + '表没有主键')

		attrs['__mappings__'] = mappings
		attrs['__fields__'] = fields
		attrs['__primaryKey__'] = primaryKey

		return type.__new__(cls, name, bases, attrs)



class Model(dict, metaclass=ModolMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise RuntimeError("'Model' object has no attribute '%s'" %key)

	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):		
		if key in self:
			value = getattr(self, key)
		else:
			field = self.__mappings__[key]
			value = field.default() if callable(field.default) else field.default
			setattr(self, key, value)
		return value

	def getComment(self, key):
		field = self.__mappings__[key]
		comment = field.comment
		if comment == None:
			return key
		return comment

	def getSaveSQL(self):
		keyList = ', '.join(list( map( lambda f: '`%s`' %f, self.__fields__) ) )
		valueList = []
		for k in self.__fields__:
			v = self.getValue(k)
			v = "'%s'" %v.replace("'", "\\'") if isinstance(self.__mappings__[k], StringField) else v
			valueList.append(v)
		valueList = ', '.join(list( map( lambda f: '%s' %f, valueList) ) )
		sql = 'INSERT INTO %s(%s) VALUES (%s)' %(self.__table__, keyList, valueList)
		return sql

	def __str__(self):
		s = ''
		for k, v in self.__mappings__.items():
			s += '%s : %s\n' %(self.getComment(k), self.getValue(k))
		return s

class Movie(Model):
	__table__ = 'movie'

	id  = IntegerField(isPrimaryKey=True, comment='ID')							# ID
	title = StringField(columnType='varchar', comment='电影')					# 电影
	directors = StringField(columnType='varchar', comment='导演')				# 导演
	writers	= StringField(columnType='varchar', comment='编剧')					# 编剧
	casts = StringField(columnType='varchar', comment='主演')					# 主演
	genres = StringField(columnType='varchar', comment='类型')					# 类型
	countries = StringField(columnType='varchar', comment='制片国家/地区')			# 制片国家/地区
	languages = StringField(columnType='varchar', comment='语言')				# 语言
	pubdates = StringField(columnType='varchar', comment='上映日期')				# 上映日期
	durations = StringField(columnType='varchar', comment='片长')				# 片长
	aka = StringField(columnType='varchar', comment='又名')						# 又名
	summary = StringField(columnType='varchar', comment='简介')					# 简介
	rating = FloatField(comment='评分')											# 评分
	rating_count = IntegerField(comment='评分人数')								# 评分人数
	image_url = StringField(columnType='varchar', comment='海报链接')				# 海报链接

if __name__ == '__main__':
	movie1 = Movie(title='La La Land')
	movie1.save()
	print(movie1)