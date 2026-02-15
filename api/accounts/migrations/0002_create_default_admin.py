from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Account = apps.get_model('accounts', 'Account')

    if User.objects.filter(is_superuser=True).exists():
        print("⚠️  Superuser already exists. Skipping default admin creation.")
        return

    admin_user = User.objects.create(
        username='admin',
        password=make_password('admin123'),
        is_superuser=True,
        is_staff=True,
        is_active=True,
        first_name='System',
        last_name='Administrator',
        email='admin@localhost'
    )

    Account.objects.create(
        user=admin_user,
        license_number=None
    )

def reverse_migration(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, reverse_migration),
    ]