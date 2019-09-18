import uuid

class Item:
    
    def __init__(self, public, required, type):
        self.public = public #True or False
        self.required = required #True or False
        self.type = type #{str, int, object, 'etc...'}
        self.value = None
    
    def __set_name__(self, inst,  name):
        print(f'initializing "{name}" descriptor')
        self.name = name

    def __repr__(self):
        return f'{self.__dict__}'

    def __set__(cls, inst, value):
        if value.__class__ == cls.type:
            cls.value = value
            inst.__dict__[cls.name] = value
        else:
            raise ValueError(f"Wrong Data Type used instead of '{cls.type}'")

    def __get__(cls, inst, classname):
        return inst.__dict__[cls.name]
    

class DBItem:
    partkey = Item(public=False, required=True, type=str)
    sortkey = Item(public=False, required=True, type=str)
    id_ = Item(public=False, required=True, type=str)
    record_type = Item(public=False, required=False, type=str)
    
    def __init__(self, partkey, sortkey, id_, record_type):
        self.partkey = partkey
        self.sortkey = sortkey
        self.id_ = id_
        self.record_type = record_type

    def __repr__(self):
        return f'{self.__dict__}'

    def __str__(self):
        return f'{self.__dict__}'

    def to_dict(self):
        return self.__dict__

    def get_public_fields(self):
        return {k for k,v in self.get_descriptor_fields() 
                if hasattr(v, 'public') and v.public}
     
    def get_hidden_fields(self):
        return {k for k,v in self.get_descriptor_fields() 
                if hasattr(v, 'public') and not v.public}
     
    def get_required_fields(self):
        return {k for k,v in self.get_descriptor_fields() 
                if hasattr(v, 'required') and v.required}

    def get_descriptor_fields(self):
        return (
            *type(self).__dict__.items(),
            *DBItem.__dict__.items()
        )


class Owner(DBItem):
    name = Item(public=True, required=True, type=str)
    surname = Item(public=True, required=True, type=str)
    telephone = Item(public=False, required=False, type=str)

    def __init__(self, name, surname, user_id, telephone):
        id_ = uuid.uuid4().__str__()
        self.name = name
        self.surname = surname
        self.telephone = telephone
        super().__init__('owner_',f"{user_id}_{id_}", id_ , 'owner' )


owner = Owner(
    'owners name', 'owners surname', 
    uuid.uuid4().__str__(), 
    '18001231314324'
)
owner2 =  Owner(
    'owners name2', 
    'owners surname2', 
    uuid.uuid4().__str__(), 
    '18001231314325'
)

print(f'owner={owner}\n, owner2={owner2}')
print(f'owner public fields={owner.get_public_fields()}\n')
print(f'owner2 public fields={owner2.get_public_fields()}\n')
print(f'owner private fields={owner.get_hidden_fields()}\n')
print(f'owner2 private fields={owner2.get_hidden_fields()}\n')
print(f'owner required fields={owner.get_required_fields()}\n')
print(f'owner2 required fields={owner2.get_required_fields()}\n')
owner.name = 'New Name'
print(f"owner's new name is {owner.name}")
print(f'owner={owner}\n, owner2={owner2}')
owner.partkey = 'property'
print(f"owner's new partkey is '{owner.partkey}'")
print(f'object as a dict {owner.to_dict()}')
owner.name = 1 # this will cause error as int type is not allowed for name field
