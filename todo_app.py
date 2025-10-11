import typer # type: ignore
import sqlite3
from datetime import datetime

# Mi app de tareas
app = typer.Typer()
DB_FILE = "mis_tareas.db"

# -----------------------------
# Funciones de la base de datos
# -----------------------------

def crear_tabla():
    """Crea la tabla de tareas si no existe"""
    with sqlite3.connect(DB_FILE) as conexion:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                estado TEXT DEFAULT 'pendiente',
                fecha_creacion TEXT
            )
        """)
        conexion.commit()

def agregar_tarea(nombre: str, descripcion: str):
    """Agrega una tarea nueva"""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    with sqlite3.connect(DB_FILE) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO tareas (nombre, descripcion, fecha_creacion) VALUES (?, ?, ?)",
            (nombre, descripcion, fecha)
        )
        conexion.commit()
    typer.echo(f"✅ La tarea '{nombre}' se agregó correctamente!")

def mostrar_tareas(ver_todas: bool = False):
    """Muestra las tareas guardadas"""
    with sqlite3.connect(DB_FILE) as conexion:
        cursor = conexion.cursor()
        if ver_todas:
            cursor.execute("SELECT * FROM tareas")
        else:
            cursor.execute("SELECT * FROM tareas WHERE estado = 'pendiente'")
        tareas = cursor.fetchall()

    if not tareas:
        typer.echo("📭 No hay tareas que mostrar.")
        return

    for tid, nombre, descripcion, estado, fecha in tareas:
        icono = "✅" if estado == "completada" else "🕓"
        typer.echo(f"[{tid}] {nombre} → {descripcion} | {icono} | {fecha}")

def actualizar_tarea(id: int, nombre: str = None, descripcion: str = None, estado: str = None):
    """Actualiza una tarea existente"""
    with sqlite3.connect(DB_FILE) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
        tarea = cursor.fetchone()

        if not tarea:
            typer.echo("⚠️ No se encontró una tarea con ese ID.")
            return

        nuevo_nombre = nombre if nombre else tarea[1]
        nueva_descripcion = descripcion if descripcion else tarea[2]
        nuevo_estado = estado if estado else tarea[3]

        cursor.execute("""
            UPDATE tareas
            SET nombre = ?, descripcion = ?, estado = ?
            WHERE id = ?
        """, (nuevo_nombre, nueva_descripcion, nuevo_estado, id))
        conexion.commit()
    typer.echo(f"🔁 Tarea '{nuevo_nombre}' actualizada correctamente!")

def borrar_tarea(id: int):
    """Elimina una tarea"""
    with sqlite3.connect(DB_FILE) as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
        tarea = cursor.fetchone()

        if not tarea:
            typer.echo("⚠️ No existe una tarea con ese ID.")
            return

        if typer.confirm(f"¿Deseas borrar la tarea '{tarea[1]}'?"):
            cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
            conexion.commit()
            typer.echo(f"🗑️ Tarea '{tarea[1]}' eliminada!")

# -----------------------------
# Comandos de la app
# -----------------------------

@app.command("nueva")
def cmd_nueva(nombre: str, descripcion: str = typer.Option("", help="Opcional: descripción de la tarea")):
    """Crea una tarea nueva"""
    crear_tabla()
    agregar_tarea(nombre, descripcion)

@app.command("ver")
def cmd_ver(todas: bool = typer.Option(False, help="Mostrar todas las tareas")):
    """Muestra las tareas"""
    mostrar_tareas(todas)

@app.command("editar")
def cmd_editar(
    id: int,
    nombre: str = typer.Option(None, help="Nuevo nombre"),
    descripcion: str = typer.Option(None, help="Nueva descripción"),
    estado: str = typer.Option(None, help="Estado: pendiente o completada")
):
    """Edita una tarea existente"""
    actualizar_tarea(id, nombre, descripcion, estado)

@app.command("borrar")
def cmd_borrar(id: int):
    """Borra una tarea"""
    borrar_tarea(id)

# -----------------------------
# Inicio de la app
# -----------------------------

if __name__ == "__main__":
    crear_tabla()
    app()

