import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fasthtml.common import *

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app, rt = fast_app(
    hdrs=(Link(rel="icon", type="assets/x-icon", href="/assets/logo.png"),),
)

# Function to get data for auto table
def get_autos():
    response = supabase.table('auto').select('*').execute()
    return response.data

# Function to get data for usuario table
def get_usuarios():
    response = supabase.table('usuario').select('*').execute()
    return response.data

# Function to get data for empleado table
def get_empleados():
    response = supabase.table('empleado').select('*').execute()
    return response.data

# Function to create a form for autos
def create_form_auto():
    return Form(id="create-form-auto", hx_post="/auto", hx_target="#auto-list", hx_swap="beforeend")

# Function to create a form for usuarios
def create_form_usuario():
    return Form(id="create-form-usuario", hx_post="/usuario", hx_target="#usuario-list", hx_swap="beforeend")

# Function to create a form for empleados
def create_form_empleado():
    return Form(id="create-form-empleado", hx_post="/empleado", hx_target="#empleado-list", hx_swap="beforeend")

# Function to create a row for autos
def create_row_auto():
    return Tr(
        Th("Agregar"),
        Th(Input(name="placa", type="text", placeholder="Placa", form="create-form-auto")),
        Th(Input(name="modelo", type="text", placeholder="Modelo", form="create-form-auto")),
        Th(Input(name="marca", type="text", placeholder="Marca", form="create-form-auto")),
        Th(Input(name="año", type="number", placeholder="Año", form="create-form-auto")),
        Th(Input(name="disponibilidad", type="text", placeholder="Disponibilidad", form="create-form-auto")),
        Th(Input(type="submit", value="Agregar", form="create-form-auto")),
        id="create-row-auto", hx_swap_oob="true"
    )

# Function to create a row for usuarios
def create_row_usuario():
    return Tr(
        Th("Agregar"),
        Th(Input(name="nombre", type="text", placeholder="Nombre", form="create-form-usuario")),
        Th(Input(name="apellido", type="text", placeholder="Apellido", form="create-form-usuario")),
        Th(Input(name="dni", type="text", placeholder="DNI", form="create-form-usuario")),
        Th(Input(name="email", type="email", placeholder="Email", form="create-form-usuario")),
        Th(Input(name="contrasena", type="password", placeholder="Contraseña", form="create-form-usuario")),
        Th(Input(name="telefono", type="tel", placeholder="Teléfono", form="create-form-usuario")),
        Th(Input(name="fechanac", type="date", placeholder="Fecha de Nacimiento", form="create-form-usuario")),
        Th(Input(name="direccion", type="text", placeholder="Dirección", form="create-form-usuario")),
        Th(Input(name="nrolicencia", type="text", placeholder="Número de Licencia", form="create-form-usuario")),
        Th(Input(name="fechaexplicen", type="date", placeholder="Fecha de Expiración de Licencia", form="create-form-usuario")),
        Th(Input(type="submit", value="Agregar", form="create-form-usuario")),
        id="create-row-usuario", hx_swap_oob="true"
    )

# Function to create a row for empleados
def create_row_empleado():
    return Tr(
        Th("Agregar"),
        Th(Input(name="nombreempleado", type="text", placeholder="Nombre Empleado", form="create-form-empleado")),
        Th(Input(name="cargo", type="text", placeholder="Cargo", form="create-form-empleado")),
        Th(Input(name="email", type="email", placeholder="Email", form="create-form-empleado")),
        Th(Input(name="contrasena", type="password", placeholder="Contraseña", form="create-form-empleado")),
        Th(Input(name="telefono", type="tel", placeholder="Teléfono", form="create-form-empleado")),
        Th(Input(name="idauto", type="number", placeholder="ID Auto", form="create-form-empleado")),
        Th(Input(type="submit", value="Agregar", form="create-form-empleado")),
        id="create-row-empleado", hx_swap_oob="true"
    )

# Function to create a table cell for auto
def auto_cell(auto_id: int, column_name: str, column_value: str, edit: bool = False):
    cell_id = f"auto-{auto_id}-{column_name}"
    attributes = {
        "id": cell_id,
        "hx_swap": "outerHTML",
        "hx_vals": {'pre_value': column_value},
    }
    if edit:
        inner_html = Input(name=column_name,
                            value=column_value,
                            type="text" if column_name != "año" else "number",
                            hx_post=f"/update/auto/{auto_id}/{column_name}",
                            target_id=cell_id,
                            hx_swap="outerHTML",
                            hx_trigger="keyup[key=='Enter'] changed",
                        )
        attributes["hx_trigger"] = "keyup[key=='Escape']"
        attributes["hx_post"] = f"/reset/auto/{auto_id}/{column_name}"
    else:
        inner_html = column_value
        attributes["hx_trigger"] = "click"
        attributes["hx_post"] = f"/swap/auto/{auto_id}/{column_name}"
    return Td(inner_html, **attributes)

# Function to create a table cell for usuario
def usuario_cell(usuario_id: int, column_name: str, column_value: str, edit: bool = False):
    cell_id = f"usuario-{usuario_id}-{column_name}"
    attributes = {
        "id": cell_id,
        "hx_swap": "outerHTML",
        "hx_vals": {'pre_value': column_value},
    }
    if edit:
        inner_html = Input(name=column_name,
                            value=column_value,
                            type="text" if column_name != "contrasena" else "password",
                            hx_post=f"/update/usuario/{usuario_id}/{column_name}",
                            target_id=cell_id,
                            hx_swap="outerHTML",
                            hx_trigger="keyup[key=='Enter'] changed",
                        )
        attributes["hx_trigger"] = "keyup[key=='Escape']"
        attributes["hx_post"] = f"/reset/usuario/{usuario_id}/{column_name}"
    else:
        inner_html = column_value
        attributes["hx_trigger"] = "click"
        attributes["hx_post"] = f"/swap/usuario/{usuario_id}/{column_name}"
    return Td(inner_html, **attributes)

# Function to create a table cell for empleado
def empleado_cell(empleado_id: int, column_name: str, column_value: str, edit: bool = False):
    cell_id = f"empleado-{empleado_id}-{column_name}"
    attributes = {
        "id": cell_id,
        "hx_swap": "outerHTML",
        "hx_vals": {'pre_value': column_value},
    }
    if edit:
        inner_html = Input(name=column_name,
                            value=column_value,
                            type="text" if column_name not in ["contrasena", "email", "telefono", "idauto"] else "password" if column_name == "contrasena" else "email" if column_name == "email" else "tel" if column_name == "telefono" else "number",
                            hx_post=f"/update/empleado/{empleado_id}/{column_name}",
                            target_id=cell_id,
                            hx_swap="outerHTML",
                            hx_trigger="keyup[key=='Enter'] changed",
                        )
        attributes["hx_trigger"] = "keyup[key=='Escape']"
        attributes["hx_post"] = f"/reset/empleado/{empleado_id}/{column_name}"
    else:
        inner_html = column_value
        attributes["hx_trigger"] = "click"
        attributes["hx_post"] = f"/swap/empleado/{empleado_id}/{column_name}"
    return Td(inner_html, **attributes)

# Function to create a table row for auto
def auto_row(auto: dict):
    return Tr(
        Td(auto.get("idauto")),
        auto_cell(auto.get("idauto"), "placa", auto.get("placa")),
        auto_cell(auto.get("idauto"), "modelo", auto.get("modelo")),
        auto_cell(auto.get("idauto"), "marca", auto.get("marca")),
        auto_cell(auto.get("idauto"), "año", str(auto.get("año"))),
        auto_cell(auto.get("idauto"), "disponibilidad", auto.get("disponibilidad")),
        Td(
            Button("Eliminar", hx_delete=f"/auto/{auto.get('idauto')}", hx_confirm="¿Estás seguro?", hx_swap="outerHTML", target_id=f"auto-{auto.get('idauto')}"),
        ),
        id=f"auto-{auto.get('idauto')}"
    )

# Function to create a table row for usuario
def usuario_row(usuario: dict):
    return Tr(
        Td(usuario.get("idusuario")),
        usuario_cell(usuario.get("idusuario"), "nombre", usuario.get("nombre")),
        usuario_cell(usuario.get("idusuario"), "apellido", usuario.get("apellido")),
        usuario_cell(usuario.get("idusuario"), "dni", usuario.get("dni")),
        usuario_cell(usuario.get("idusuario"), "email", usuario.get("email")),
        usuario_cell(usuario.get("idusuario"), "contrasena", "******"),
        usuario_cell(usuario.get("idusuario"), "telefono", usuario.get("telefono")),
        usuario_cell(usuario.get("idusuario"), "fechanac", usuario.get("fechanac")),
        usuario_cell(usuario.get("idusuario"), "direccion", usuario.get("direccion")),
        usuario_cell(usuario.get("idusuario"), "nrolicencia", usuario.get("nrolicencia")),
        usuario_cell(usuario.get("idusuario"), "fechaexplicen", usuario.get("fechaexplicen")),
        Td(
            Button("Eliminar", hx_delete=f"/usuario/{usuario.get('idusuario')}", hx_confirm="¿Estás seguro?", hx_swap="outerHTML", target_id=f"usuario-{usuario.get('idusuario')}"),
        ),
        id=f"usuario-{usuario.get('idusuario')}"
    )

# Function to create a table row for empleado
def empleado_row(empleado: dict):
    return Tr(
        Td(empleado.get("idempleado")),
        empleado_cell(empleado.get("idempleado"), "nombreempleado", empleado.get("nombreempleado")),
        empleado_cell(empleado.get("idempleado"), "cargo", empleado.get("cargo")),
        empleado_cell(empleado.get("idempleado"), "email", empleado.get("email")),
        empleado_cell(empleado.get("idempleado"), "contrasena", "******"),
        empleado_cell(empleado.get("idempleado"), "telefono", empleado.get("telefono")),
        empleado_cell(empleado.get("idempleado"), "idauto", str(empleado.get("idauto"))),
        Td(
            Button("Eliminar", hx_delete=f"/empleado/{empleado.get('idempleado')}", hx_confirm="¿Estás seguro?", hx_swap="outerHTML", target_id=f"empleado-{empleado.get('idempleado')}"),
        ),
        id=f"empleado-{empleado.get('idempleado')}"
    )

# Function to create the auto table
def auto_table():
    autos_data = get_autos()
    return Table(
        Thead(
            Tr(
                Th("ID", scope="col"),
                Th("Placa", scope="col"),
                Th("Modelo", scope="col"),
                Th("Marca", scope="col"),
                Th("Año", scope="col"),
                Th("Disponibilidad", scope="col"),
                Th("Acción", scope="col")
            ),
            create_row_auto()
        ),
        Tbody(map(auto_row, autos_data), id="auto-list")
    )

# Function to create the usuario table
def usuario_table():
    usuarios_data = get_usuarios()
    return Table(
        Thead(
            Tr(
                Th("ID", scope="col"),
                Th("Nombre", scope="col"),
                Th("Apellido", scope="col"),
                Th("DNI", scope="col"),
                Th("Email", scope="col"),
                Th("Contraseña", scope="col"),
                Th("Teléfono", scope="col"),
                Th("Fecha de Nacimiento", scope="col"),
                Th("Dirección", scope="col"),
                Th("Número de Licencia", scope="col"),
                Th("Fecha de Expiración de Licencia", scope="col"),
                Th("Acción", scope="col")
            ),
            create_row_usuario()
        ),
        Tbody(map(usuario_row, usuarios_data), id="usuario-list")
    )

# Function to create the empleado table
def empleado_table():
    empleados_data = get_empleados()
    return Table(
        Thead(
            Tr(
                Th("ID", scope="col"),
                Th("Nombre Empleado", scope="col"),
                Th("Cargo", scope="col"),
                Th("Email", scope="col"),
                Th("Contraseña", scope="col"),
                Th("Teléfono", scope="col"),
                Th("ID Auto", scope="col"),
                Th("Acción", scope="col")
            ),
            create_row_empleado()
        ),
        Tbody(map(empleado_row, empleados_data), id="empleado-list")
    )


@rt("/")
def home():
    return Titled(
        "Página Principal",
        Div(
            H1("Bienvenido a la Gestión de Datos"),
            P("Selecciona una opción para continuar:"),
            Ul(
                Li(A("Gestión de Autos", href="/autos")),
                Li(A("Gestión de Usuarios", href="/usuarios")),
                Li(A("Gestión de Empleados", href="/empleados")),
            )
        )
    )



# Routes for Auto
@rt("/autos")
def get_autos_page():
    return Titled(
        "Gestión de Autos",
        Div(
            A("Ir a Usuarios", href="/usuarios"),
            " | ",
            A("Ir a Empleados", href="/empleados"),
            Hr(),
            create_form_auto(),
            auto_table()
        )
    )

@rt("/auto", methods=["POST"])
def post_auto(auto: dict):
    response = supabase.table('auto').insert(auto).execute()
    new_auto = response.data[0]
    return auto_row(new_auto), create_row_auto()

@rt("/auto/{auto_id:int}", methods=["DELETE"])
def delete_auto(auto_id: int):
    supabase.table('auto').delete().eq('idauto', auto_id).execute()
    return

@rt("/swap/auto/{auto_id:int}/{column_name:str}", methods=["POST"])
def swap_auto(auto_id: int, column_name: str, pre_value: str):
    return auto_cell(auto_id, column_name, pre_value, edit=True)

@rt("/update/auto/{auto_id:int}/{column_name:str}", methods=["POST"])
def update_auto(auto_id: int, column_name: str, auto: dict):
    auto["idauto"] = auto_id
    response = supabase.table('auto').update({column_name: auto[column_name]}).eq('idauto', auto_id).execute()
    updated_auto = response.data[0]
    return auto_cell(auto_id, column_name, updated_auto[column_name])

@rt("/reset/auto/{auto_id:int}/{column_name:str}", methods=["POST"])
def reset_auto(auto_id: int, column_name: str, pre_value: str):
    return auto_cell(auto_id, column_name, pre_value)



# Routes for Usuario
@rt("/usuarios")
def get_usuarios_page():
    return Titled(
        "Gestión de Usuarios",
        Div(
            A("Ir a Autos", href="/autos"),
            " | ",
            A("Ir a Empleados", href="/empleados"),
            Hr(),
            create_form_usuario(),
            usuario_table()
        )
    )

@rt("/usuario", methods=["POST"])
def post_usuario(usuario: dict):
    response = supabase.table('usuario').insert(usuario).execute()
    new_usuario = response.data[0]
    return usuario_row(new_usuario), create_row_usuario()

@rt("/usuario/{usuario_id:int}", methods=["DELETE"])
def delete_usuario(usuario_id: int):
    supabase.table('usuario').delete().eq('idusuario', usuario_id).execute()
    return

@rt("/swap/usuario/{usuario_id:int}/{column_name:str}", methods=["POST"])
def swap_usuario(usuario_id: int, column_name: str, pre_value: str):
    return usuario_cell(usuario_id, column_name, pre_value, edit=True)

@rt("/update/usuario/{usuario_id:int}/{column_name:str}", methods=["POST"])
def update_usuario(usuario_id: int, column_name: str, usuario: dict):
    usuario["idusuario"] = usuario_id
    response = supabase.table('usuario').update({column_name: usuario[column_name]}).eq('idusuario', usuario_id).execute()
    updated_usuario = response.data[0]
    return usuario_cell(usuario_id, column_name, updated_usuario[column_name])

@rt("/reset/usuario/{usuario_id:int}/{column_name:str}", methods=["POST"])
def reset_usuario(usuario_id: int, column_name: str, pre_value: str):
    return usuario_cell(usuario_id, column_name, pre_value)



# Routes for Empleado
@rt("/empleados")
def get_empleados_page():
    return Titled(
        "Gestión de Empleados",
        Div(
            A("Ir a Autos", href="/autos"),
            " | ",
            A("Ir a Usuarios", href="/usuarios"),
            Hr(),
            create_form_empleado(),
            empleado_table()
        )
    )

@rt("/empleado", methods=["POST"])
def post_empleado(empleado: dict):
    response = supabase.table('empleado').insert(empleado).execute()
    new_empleado = response.data[0]
    return empleado_row(new_empleado), create_row_empleado()

@rt("/empleado/{empleado_id:int}", methods=["DELETE"])
def delete_empleado(empleado_id: int):
    supabase.table('empleado').delete().eq('idempleado', empleado_id).execute()
    return

@rt("/swap/empleado/{empleado_id:int}/{column_name:str}", methods=["POST"])
def swap_empleado(empleado_id: int, column_name: str, pre_value: str):
    return empleado_cell(empleado_id, column_name, pre_value, edit=True)

@rt("/update/empleado/{empleado_id:int}/{column_name:str}", methods=["POST"])
def update_empleado(empleado_id: int, column_name: str, empleado: dict):
    empleado["idempleado"] = empleado_id
    response = supabase.table('empleado').update({column_name: empleado[column_name]}).eq('idempleado', empleado_id).execute()
    updated_empleado = response.data[0]
    return empleado_cell(empleado_id, column_name, updated_empleado[column_name])

@rt("/reset/empleado/{empleado_id:int}/{column_name:str}", methods=["POST"])
def reset_empleado(empleado_id: int, column_name: str, pre_value: str):
    return empleado_cell(empleado_id, column_name, pre_value)


serve()
