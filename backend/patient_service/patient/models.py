import mongoengine as me

class Patient(me.Document):
    _id = me.ObjectIdField()
    user = me.StringField(required=True, unique=True)
    medical_record_id = me.StringField(default="")

    meta = {
        'collection': 'patient'
    }

    def __str__(self):
        return self.user