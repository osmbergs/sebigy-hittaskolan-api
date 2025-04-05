import sqlalchemy as sa


from sqlalchemy.ext.declarative import declarative_base


metadata = sa.MetaData()
Base = declarative_base(metadata=metadata)
