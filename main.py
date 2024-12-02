import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fasthtml.common import *

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app, rt = fast_app()

def get_autos():
    response = supabase.table('auto').select('*').execute()
    return response.data

def create_form():
    return Form(id="create-form", hx_post="/", hx_target="#auto-list", hx_swap="beforeend")

def create_row():
    return Tr(
        Th("Agregar"),
        Th(Input(name="placa", type="text", placeholder="Placa", form="create-form")),
        Th(Input(name="modelo", type="text", placeholder="Modelo", form="create-form")),
        Th(Input(name="marca", type="text", placeholder="Marca", form="create-form")),
        Th(Input(name="año", type="number", placeholder="Año", form="create-form")),
        Th(Input(name="disponibilidad", type="text", placeholder="Disponibilidad", form="create-form")),
        Th(Input(type="submit", value="Agregar", form="create-form")),
        id="create-row", hx_swap_oob="true"
    )

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
                            hx_post=f"/update/{auto_id}/{column_name}",
                            target_id=cell_id,
                            hx_swap="outerHTML",
                            hx_trigger="keyup[key=='Enter'] changed",
                        )
        attributes["hx_trigger"] = "keyup[key=='Escape']"
        attributes["hx_post"] = f"/reset/{auto_id}/{column_name}"
    else:
        inner_html = column_value
        attributes["hx_trigger"] = "click"
        attributes["hx_post"] = f"/swap/{auto_id}/{column_name}"
    return Td(inner_html, **attributes)

def auto_row(auto: dict):
    return Tr(
        Td(auto.get("idauto")),  # Usa auto.get() para evitar errores si la clave no existe
        auto_cell(auto.get("idauto"), "placa", auto.get("placa")),
        auto_cell(auto.get("idauto"), "modelo", auto.get("modelo")),
        auto_cell(auto.get("idauto"), "marca", auto.get("marca")),
        auto_cell(auto.get("idauto"), "año", str(auto.get("año"))),
        auto_cell(auto.get("idauto"), "disponibilidad", auto.get("disponibilidad")),
        Td(
            Button("Eliminar",
                    hx_delete=f"/{auto.get('idauto')}",
                    hx_confirm="¿Estás seguro?",
                    hx_swap="outerHTML",
                    target_id=f"auto-{auto.get('idauto')}"
                    ),
        ),
        id=f"auto-{auto.get('idauto')}"
    )

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
            create_row()
        ),
        Tbody(
            map(auto_row, autos_data), id="auto-list"
        )
    )

@rt("/")
def get():
    return Titled("Autos", create_form(), auto_table())

@rt("/")
def post(auto: dict):
    response = supabase.table('auto').insert(auto).execute()
    new_auto = response.data[0]
    return auto_row(new_auto), create_row()

@rt("/swap/{auto_id:int}/{column_name:str}")
def post(auto_id: int, column_name: str, pre_value: str):
    return auto_cell(auto_id, column_name, pre_value, edit=True)

@rt("/update/{auto_id:int}/{column_name:str}")
def post(auto_id: int, column_name: str, auto: dict):
    auto["idauto"] = auto_id
    response = supabase.table('auto').update({column_name: auto[column_name]}).eq('idauto', auto_id).execute()
    updated_auto = response.data[0]
    return auto_cell(auto_id, column_name, updated_auto[column_name])

@rt("/reset/{auto_id:int}/{column_name:str}")
def post(auto_id: int, column_name: str, pre_value: str):
    return auto_cell(auto_id, column_name, pre_value)

@rt("/{auto_id:int}")
def delete(auto_id: int):
    supabase.table('auto').delete().eq('idauto', auto_id).execute()
    return

serve()