# Generated by Django 2.1.8 on 2020-11-28 16:18

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Bodegas',
            },
        ),
        migrations.CreateModel(
            name='Cierre_Diario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('total_operaciones_entrada', models.IntegerField(verbose_name='Total de operaciones de entrada')),
                ('total_operaciones_salida', models.IntegerField(verbose_name='Total de operaciones de salida')),
                ('dinero_depositar', models.FloatField(verbose_name='Dinero Total a depositar')),
                ('fecha', models.DateTimeField(verbose_name='Fecha de cierre')),
            ],
            options={
                'verbose_name_plural': 'Estado del cierre',
            },
        ),
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Clasificaciones',
            },
        ),
        migrations.CreateModel(
            name='ConsejoPopular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Consejos Populares',
            },
        ),
        migrations.CreateModel(
            name='Estado_Cierre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Estado')),
            ],
            options={
                'verbose_name_plural': 'Estado del cierre',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Municipios',
            },
        ),
        migrations.CreateModel(
            name='Notificacion_general',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('titulo', models.CharField(max_length=100, verbose_name='Título')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
                ('mensaje', models.TextField(max_length=250, verbose_name='Mensaje')),
            ],
            options={
                'verbose_name_plural': 'Notificaciones',
            },
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('factura', models.CharField(blank=True, help_text='En caso de operación por Facturación', max_length=100, verbose_name='Número de Factura')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
                ('cantidad', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad')),
                ('imp_pv', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Imp/PV')),
                ('imp_pc', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Imp/PC')),
                ('bodega', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Bodega', verbose_name='Bodega')),
            ],
        ),
        migrations.CreateModel(
            name='ProdPrecioCosto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha')),
                ('valor', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Valor')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('codigo', models.CharField(max_length=100, null=True, unique=True, verbose_name='Código')),
                ('precio_venta', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio de Venta')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('clasificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Clasificacion', verbose_name='Clasificación')),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.CreateModel(
            name='Saldo_Inicial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('fecha', models.DateTimeField(verbose_name='Fecha')),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BodegaApp.Bodega', verbose_name='Bodega de Origen')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BodegaApp.Producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name_plural': 'Saldo Inicial',
            },
        ),
        migrations.CreateModel(
            name='SeccionOperacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Sección de operaciones',
            },
        ),
        migrations.CreateModel(
            name='TipoOperacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Operaciones',
            },
        ),
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('fecha_traslado', models.DateTimeField(verbose_name='Fecha de traslado')),
                ('bodega_origen_confirmacion', models.BooleanField(verbose_name='Confirmacion Bodega Origen')),
                ('bodega_destino_confirmacion', models.BooleanField(verbose_name='Confirmacion Bodega Destino')),
                ('bodega_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BodegaApp.Bodega', verbose_name='Bodega de Destino')),
                ('bodega_origen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='BodegaOrigen', to='BodegaApp.Bodega', verbose_name='Bodega de Origen')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BodegaApp.Producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name_plural': 'Traslados',
            },
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Unidad de Medida')),
            ],
            options={
                'verbose_name_plural': 'Unidades de Medidas',
            },
        ),
        migrations.CreateModel(
            name='UserApp',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False, null=True)),
                ('image', models.ImageField(default='static/users/userDefault1.png', null=True, upload_to='static/users', verbose_name='Avatar')),
                ('referUser', models.UUIDField(null=True)),
                ('fa2', models.BooleanField(default=False, verbose_name='2FA')),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uui', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre')),
                ('consejo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.ConsejoPopular', verbose_name='Consejo Popular')),
            ],
            options={
                'verbose_name_plural': 'Zonas',
            },
        ),
        migrations.AddField(
            model_name='seccionoperacion',
            name='tipo_operacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.TipoOperacion', verbose_name='Tipo de Operación'),
        ),
        migrations.AddField(
            model_name='producto',
            name='unidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.UnidadMedida', verbose_name='Unidad de Medidas'),
        ),
        migrations.AddField(
            model_name='prodpreciocosto',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Producto', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='operacion',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Producto', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='operacion',
            name='seccion_operacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.SeccionOperacion', verbose_name='Sección de Operación'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Provincia', verbose_name='Provincia'),
        ),
        migrations.AddField(
            model_name='consejopopular',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Municipio', verbose_name='Municipio'),
        ),
        migrations.AddField(
            model_name='cierre_diario',
            name='estado_de_cierre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BodegaApp.Estado_Cierre'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Administrador'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='productos',
            field=models.ManyToManyField(to='BodegaApp.Producto', verbose_name='Productos'),
        ),
        migrations.AddField(
            model_name='bodega',
            name='zona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BodegaApp.Zona', verbose_name='Zona'),
        ),
    ]
