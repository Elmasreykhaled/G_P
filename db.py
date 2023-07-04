from peewee import *
db = SqliteDatabase('patients.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 100})


class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = db


class Patients(BaseModel):
    patient_id = AutoField(unique=True, null=False)
    patient_name = CharField(null=False)
    patient_national_id = DecimalField(max_digits=14, unique=True)
    patient_ray_path = CharField(null=False)
    patient_state = CharField(null=False)


def connect():
    db.connect()
    db.create_tables([Patients])
    db.close()
