from rolepermissions.roles import AbstractUserRole

class Trainee(AbstractUserRole):
    available_permissions = {'view_workout': True}

class Trainer(AbstractUserRole):
    available_permissions = {
        'view_workout': True, 'create_workout': True, 'edit_workout': True, 'delete_workout': True, 'create_trainee': True
    }

class Admin(AbstractUserRole):
    available_permissions = {
        'view_workout': True, 'create_workout': True, 'edit_workout': True, 'delete_workout': True, 'create_trainee': True, 'create_trainer': True
    }