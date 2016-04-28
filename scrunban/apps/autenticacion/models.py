from django.core.exceptions import FieldError
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User as djUser
from django.contrib.auth.models import Group as djGroup
from guardian.shortcuts import assign_perm, get_perms

class UserManager(models.Manager):
    """
    Clase administradora de operaciones a nivel de tabla del modelo ``User''.
    """
    #TODO Check in ERS for optional fields...
    def create(self, **kwargs):
        """
        Crea un usuario.
        :param kwargs: User details.
        :returns: En caso de haberse creado, el nuevo usuario. Sino ``None''
        """
        # Checking for required fields
        required_fields = ['username', 'password']
        for required_field in required_fields:
            if required_field not in kwargs.keys():
                raise KeyError('{} is required.'.format(required_field))

        # Checking if username has already been taken
        if djUser.objects.filter(username=kwargs['username']).count() == 0:
            dj_user = djUser.objects.create(username=kwargs['username'])
            dj_user.set_password(kwargs['password'])
            dj_user.email = kwargs.get('email', '')
            dj_user.first_name = kwargs.get('first_name', '')
            dj_user.last_name = kwargs.get('last_name', '')
            dj_user.save()

            new_user = User.objects.create(
                user=dj_user,
                telefono=kwargs.get('telefono', ''),
                direccion=kwargs.get('direccion', '')
            )
            new_user.save()

            return new_user
        else:
            return None

    def filter(self, **kwargs):
        """
        Returns the results of a query.
        :param kwargs: Query details.
        :returns: An instance of QuerySet containing the results of the query.
        """
        django_user_fields = ['username', 'email', 'first_name', 'last_name']
        custom_user_fields = ['direccion', 'telefono']

        # Check arguments
        accepted_fields = django_user_fields + custom_user_fields
        for key in kwargs.keys():
            if key not in accepted_fields:
                raise FieldError('Cannot resolve {} into field.'.format(key))

        # Construct params
        params = {}
        for key, value in kwargs.items():
            if key not in custom_user_fields:
                new_key = 'user__' + key
                params[new_key] = value
            else:
                params[key] = value

        # Make query and return
        return User.objects.filter(**params)


    #TODO Deprecated, find something like filter
    def get(self, username):
        results = [user for user in User.objects.all() if user.user.username == username]
        if len(results) == 0:
            return None
        else:
            return results[0]

class User(models.Model):
    """

    Este modelo *extiende* (no hereda) el model por defecto de Django:
    ``django.contrib.auth.models.User``, agregando algunos campos.

    El model se encarga de guardar informacion de todos los usuarios del sistema

    :param id: Id unico
    :param user: Model por defecto de Django. Usado con la funcion de autenticacion del framework.
    :param telefono: Nro. de Telefono
    :param direccion: Direccion

    """
    # Public fields mapped to DB columns
    user = models.OneToOneField(djUser, verbose_name="Usuario para Autenticacion")
    telefono = models.TextField("Telefono")
    direccion = models.TextField("Direccion")

    # Public fields for simplicity
    objects = models.Manager()
    users = UserManager()

    def get_username(self):
        """
        Returns the user username
        """
        return self.user.get_username()

    def get_email(self):
        """
        Returns the user email
        """
        return self.user.email

    def set_email(self, new_email):
        """
        Sets the user email
        """
        self.user.email = new_email
        self.user.save()

    def get_first_name(self):
        """
        Returns the user first name
        """
        return self.user.first_name

    def set_first_name(self, new_first_name):
        """
        Sets the user first name
        """
        self.user.first_name = new_first_name
        self.user.save()

    def get_last_name(self):
        """
        Returns the user last name
        """
        return self.user.last_name

    def set_last_name(self, new_last_name):
        """
        Sets the user last name
        """
        self.user.last_name = new_last_name
        self.user.save()

    def get_telefono(self):
        """
        Returns the user telephone
        """
        return self.telefono

    def set_telefono(self, new_telefono):
        """
        Sets the user telephone
        """
        self.telefono = new_telefono
        self.save()

    def get_direccion(self):
        """
        Returns the user address
        """
        return self.direccion

    def set_direccion(self, new_direccion):
        """
        Sets the user address
        """
        self.direccion = new_direccion
        self.save()


    def __str__(self):
        username = self.user.get_username()
        return "{}".format(username)

@receiver(models.signals.post_delete, sender=User, dispatch_uid='user_delete_signal')
def user_delete(sender, instance, *args, **kwargs):
    """
    Escucha al evento de eliminación de User para eliminar el User de Django asociado.
    """
    instance.user.delete()

class RoleManager(models.Manager):
    def create(self, **kwargs):
        """
        Wrapper of the creation function for Role
        :param kwargs: Role data.
        :returns: None if the role has not been created or
        the instance of the new role.
        """
        # Checking for required fields
        required_fields = ['name']
        for required_field in required_fields:
            if required_field not in kwargs.keys():
                raise KeyError('{} is required.'.format(required_field))

        # Checking if name has already been taken
        if djGroup.objects.filter(name=kwargs['name']).count() == 0:
            dj_group = djGroup.objects.create(name=kwargs['name'])

            new_role = Role.objects.create(
                group=dj_group,
                desc_larga=kwargs.get('desc_larga', 'Sin descripcion.')
            )

            return new_role

        else:
            return None

    def filter(self, **kwargs):
        """
        Returns the results of a query.
        :param kwargs: Query details.
        :returns: An instance of QuerySet containing the results of the query.
        """
        django_group_fields = ['name'] # We does not use the permission field
        custom_group_fields = ['desc_larga']

        # Check arguments
        accepted_fields = django_group_fields + custom_group_fields
        for key in kwargs.keys():
            if key not in accepted_fields:
                raise FieldError('Cannot resolve {} into field.'.format(key))

        # Construct params
        params = {}
        for key, value in kwargs.items():
            if key not in custom_group_fields:
                new_key = 'group__' + key
                params[new_key] = value
            else:
                params[key] = value

        # Make query and return
        return Role.objects.filter(**params)

class Role(models.Model):
    """
    Este modelo *extiende* (no hereda) el model por defecto de Django:
    ``django.contrib.auth.models.Group``, agregando un campo.

    El model es usado para manejar los roles en el sistema.

    :param id: Id unico
    :param group: Modelo por defecto de Django. Usado con el framework
    :param desc_larga: Descripcion larga de un rol (nombre legible para usuario)

    """
    # Public fields mapped to DB columns
    group = models.OneToOneField(djGroup, on_delete=models.CASCADE, verbose_name="Grupo")
    desc_larga = models.TextField("Descripcion larga")

    # Public fields for simplicity
    objects = models.Manager()
    roles = RoleManager()

    def add_user(self, user):
        """
        Adds the user to this role
        :param user: Instance of autenticacion.models.User
        """
        user.user.groups.add(self.group)

    def remove_user(self, user):
        """
        Removes user from this role
        :param user: Instance of autenticacion.models.User
        """
        user.user.groups.remove(self.group)

    def add_perm(self, permission):
        """

        Agrega un permiso al rol

        :param permission: Instancia de contrib.auth.models.Permission
        """
        self.group.permissions.add(permission)

    def remove_perm(self, permission):
        """

        Quita un permiso del rol

        :param permission: Instancia de contrib.auth.models.Permission
        """
        self.group.permissions.remove(permission)

    def get_perms(self):
        """

        Obtiene una lista de todos los permisos asociados al rol
        :return: Lista de instancias de contrib.auth.models.Permission
        """

        return self.group.permissions.all()


    def get_name(self):
        """
        Returns role name
        """
        return self.group.name

    def get_desc(self):
        """
        Returns role description
        """
        return self.desc_larga

    def set_desc(self, new_desc):
        """
        Sets role description
        """
        self.desc_larga = new_desc
        self.save()

    def get_users(self):
        """
        Retorna usuarios asociados al rol

        :return: Lista de usuarios
        """

        users = list(user.user for user in self.group.user_set.all())


        return users


    def __str__(self):
        return "{g.name}, desc_larga: {d}".format(g=self.group, d=self.desc_larga)


@receiver(models.signals.post_delete, sender=Role, dispatch_uid='role_delete_signal')
def role_delete(sender, instance, *args, **kwargs):
    """
    Escucha al evento de eliminación de Role para eliminar el Group de Django asociado.
    """
    instance.group.delete()

class ProjectManager(models.Manager):
    def create(self, **kwargs):
        """
        Wrapper of the creation function for Project.
        :param kwargs: Project data.
        :returns: None if the project has not been created or
        the instance of the new project.
        """
        # Checking for required fields
        required_fields = ['name']
        for required_field in required_fields:
            if required_field not in kwargs.keys():
                raise KeyError('{} is required.'.format(required_field))

        # Checking if name has already been taken
        if Project.projects.filter(name=kwargs['name']).count() == 0:
            return Project.objects.create(name=kwargs['name'])

        else:
            return None

    def filter(self, **kwargs):
        """
        Returns the results of a query.
        :param kwargs: Query details.
        :returns: An instance of QuerySet containing the results of the query.
        """
        return Project.objects.filter(**kwargs)

class Project(models.Model):
    """
    Dummy project class!!
    """
    # Public fields mapped to DB columns
    name = models.TextField('Project name')

    # Public fields for simplicity
    objects = models.Manager()
    projects = ProjectManager()

    class Meta:
        default_permissions = () # To explicitly list permissions
        permissions = (
            ('add_project', 'Crea un projecto y asigna el "Scrum Master".'),
            ('delete_project', 'Elimina un projecto.'),
            ('view_project_details', 'Ver detalles del projecto.'),
            ('view_kanbam', 'Ver Kanbam.'),
        )

    def assign_perm(self, perm, user):
        """
        Asigna el permiso ``perm'' sobre la instancia al usuario ``user''.
        En caso de que no exista el permiso se alza DoesNotExists.

        :param perm: Cadena que identifica el permiso. Ver clase interna Meta de Project.
        :param user: Instancia de User del usuario a quien asignamos el permiso.
        """
        assign_perm(perm, user.user, self)

    def get_perms(self, user):
        """
        Obtiene una lista de todos los permisos de usuario ``user'' sobre la instancia.

        :param user: Instancia de User de quien obtenemos la lista de permisos.
        :returns: La lista de permisos asignados a user sobre la actual instancia.
        """
        return get_perms(user.user, self)


    def get_name(self):
        """
        Returns the project name
        """
        return self.name

    def add_rol(self, **kwargs):
        """

        Crea un rol de proyecto con un nombre de la forma ``idProyecto_name`` si es que ``name`` es especificado,
         de lo contrario el nombre queda de la forma ``idProyecto_r_num`` donde ``num`` va aumentando secuencialmente.


        :param desc_larga:  Descripcion larga del Rol
        :param name:  Nombre en codigo del Rol
        :returns: Instancia del nuevo rol creado
        """

        required_fields = ['desc_larga']
        for required_field in required_fields:
            if required_field not in kwargs.keys():
                raise KeyError('{} is required.'.format(required_field))

        p_id = self.id
        r_name = ''

        if ('name' not in kwargs.keys()):
            r_tot = Role.objects.filter(group__name__startswith=str(p_id) + '_r_')
            if (len(r_tot) == 0):
                r_name = str(p_id) + '_r_0'
            else:
                r_last = r_tot.last().get_name()
                r_last = int(r_last[len(r_last) - 1]) + 1
                r_name = str(p_id) + '_r_' + str(r_last)
        else:
            r_name = str(p_id) + '_' + kwargs['name']

        data = {
            'name' : r_name,
            'desc_larga' : kwargs['desc_larga'],

        }
        new_rol = Role.roles.create(**data)
        return new_rol

    def remove_rol(self, short_name):
        """

        Remueve un rol de un proyecto

        :param short_name: Nombre en codigo del Rol
        """

        p_id = self.id
        Role.objects.filter(group__name=short_name)[0].delete()

    def get_roles(self):

        """

        Obtiene una lista de todos los roles asociados con el proyecto

        :returns: Una lista de roles
        """

        p_id = self.id
        roles = Role.objects.filter(group__name__startswith=str(p_id) + '_')

        return roles

    def get_user_perms(self, user):
        """

        Obtiene una lista de todos los permisos de un Usuario asociados al proyecto a traves de algun rol

        :param user: Instancia de usuario
        :returns: Lista de permisos
        """
        p_id = self.id
        roles = user.user.groups.filter(name__startswith=str(p_id) + '_')

        perms = []

        for rol in roles:
            perms += rol.permissions.all()

        return perms

    def has_perm(self, user, perm):
        """

        Verifica si un usuario tiene un permiso dado dentro de un proyecto

        :param user: Instancia de usuario que se va a verificar que tenga el permiso
        :param perm: Permiso que se desea verificar en su nombre en codigo
        :return:
        """

        for p in self.get_user_perms(user):
            if (p.codename == perm):
                return True

        return False

    def __str__(self):
        return "{}".format(self.name)
