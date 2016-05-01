from django.db import models
from apps.autenticacion.models import User
from apps.autenticacion.models import Role
from guardian.shortcuts import assign_perm, get_perms

# Create your models here.


class ProductBacklog(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return "%d" % self.id


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

    El model se encarga de guardar informacion de todos los proyectos del sistema.

    :param id: Id unico
    :param name: Nombre del proyecto
    :param date_start: Fecha de inicio del proyecto
    :param date_end: Fecha de finalizacion del proyecto
    :param scrum_master: Scrum Master del proyecto
    :param product_owner: Product Owner del proyecto
    :param development_team: Todos los Development Teams del proyecto
    :param product_backlog: Todos los User Stories del proyecto
    """
    # Public fields mapped to DB columns
    id = models.AutoField(primary_key=True)
    name = models.TextField('Project name', unique=True)
    date_start = models.DateField()
    date_end = models.DateField()
    scrum_master = models.ForeignKey(User, null=True, related_name='fk_project_scrum_master')
    product_owner = models.ForeignKey(User, null=True, related_name='fk_project_product_owner')
    development_team = models.ManyToManyField(User, related_name='mm_project_development_team')
    product_backlog = models.OneToOneField(ProductBacklog)

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
        Asigna el permiso ``perm`` sobre la instancia al usuario ``user``.
        En caso de que no exista el permiso se alza DoesNotExists.

        :param perm: Cadena que identifica el permiso. Ver clase interna Meta de Project.
        :param user: Instancia de User del usuario a quien asignamos el permiso.
        """
        assign_perm(perm, user.user, self)

    def get_perms(self, user):
        """
        Obtiene una lista de todos los permisos de usuario ``user`` sobre la instancia.

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


class Sprint(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, null=True)

    def __str__(self):
        return "%d" % self.id


