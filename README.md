PMAH (Password Manager And Hash Utility) es una aplicación de gestión de contraseñas desarrollada en Python utilizando Tkinter para la interfaz gráfica y 
MongoDB para el almacenamiento seguro de credenciales. La aplicación permite almacenar, verificar, actualizar y eliminar contraseñas de manera sencilla y segura.

Características

Almacenar Contraseñas: Guarda contraseñas de forma segura con hash bcrypt.
Verificar Contraseñas: Comprueba si una contraseña proporcionada coincide con la almacenada.
Actualizar Contraseñas: Permite actualizar una contraseña existente.
Eliminar Contraseñas: Borra una contraseña almacenada para un usuario y plataforma específicos.
Ver Información Almacenada: Muestra todas las contraseñas almacenadas en una vista tabular.

Requisitos
Para ejecutar esta aplicación, necesitas:

Python 3.x
MongoDB
Paquetes Python: tkinter, pymongo, bcrypt


Configuración
Instala MongoDB: Asegúrate de tener MongoDB instalado y en ejecución en tu máquina local. La aplicación se conecta a MongoDB en mongodb://localhost:27017/.

Uso
Almacenar Contraseña: Introduce el nombre de usuario, la plataforma y la contraseña para almacenarla.
Verificar Contraseña: Ingresa el nombre de usuario, la plataforma y la contraseña para verificar su validez.
Actualizar Contraseña: Proporciona el nombre de usuario, la plataforma, la contraseña antigua y la nueva para actualizarla.
Eliminar Contraseña: Ingresa el nombre de usuario y la plataforma para eliminar la contraseña correspondiente.
Ver Información Almacenada: Consulta todas las contraseñas almacenadas en una vista tabular.
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para proponer cambios o mejoras.


