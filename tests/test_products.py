"""
Pruebas de Caja Negra:
test_get_all_products: Verifica que el endpoint para obtener todos los
productos devuelva una lista y un estado 200.
test_create_product: Prueba la creación de un nuevo producto y verifica que el
ID se devuelva correctamente y que los datos coincidan.
test_update_product: Verifica que la actualización de un producto devuelva el
nuevo nombre y un estado 200.
test_delete_product: Prueba la eliminación de un producto y asegura que el
estado sea 204.
test_get_product_not_found: Prueba la respuesta del endpoint para un producto
que no existe y asegura que devuelva un estado 404.

Pruebas de Caja Blanca:
test_product_model_validation: Verifica que la lógica de validación de modelos
no permita crear productos con datos inválidos.
test_calculate_discount: Comprueba la lógica de cálculo de descuentos para
asegurar que se calcule correctamente.
test_product_creation_logic: Prueba la lógica interna al crear un producto
para asegurarse de que se asignen correctamente los valores.

"""

import pytest
from httpx import AsyncClient
from pydantic import ValidationError

from app.api.v1.endpoints.products import create_product
from app.main import app
from app.schemas.product import ProductCreate


BASE_URL = "http://127.0.0.1:8000/api/v1"


# Pruebas de Caja Negra
@pytest.mark.asyncio
async def test_get_all_products():
    """Prueba de caja negra para obtener todos los productos."""
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/products/")
        assert response.status_code == 200
        assert isinstance(
            response.json(), list
        )  # Verifica que la respuesta sea una lista
        # Aquí podrías verificar la cantidad de productos si es necesario
        # assert len(response.json()) == expected_number_of_products


@pytest.mark.asyncio
async def test_create_product():
    """Prueba de caja negra para crear un nuevo producto."""
    new_product = {
        "name": "Naproxeno",
        "description": "Se vende por par",
        "price": 1500,
        "stock": 40,
    }
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/products/", json=new_product)
        assert response.status_code == 200
        assert (
            "id" in response.json()
        )  # Verifica que se haya devuelto un ID del producto
        assert (
            response.json()["name"] == new_product["name"]
        )  # Verifica que el nombre sea el mismo


@pytest.mark.asyncio
async def test_update_product():
    """Prueba de caja negra para actualizar un producto existente."""
    updated_product = {
        "name": "Naproxeno ACTUALIZADO",
        "description": "Nueva descripción",
        "price": 1800,
        "stock": 30,
    }
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.put("/products/10", json=updated_product)
        assert response.status_code == 200
        assert (
            response.json()["name"] == updated_product["name"]
        )  # Verifica que el nombre se haya actualizado


# @pytest.mark.asyncio
# async def test_delete_product():
#     """Prueba de caja negra para eliminar un producto."""
#     async with AsyncClient(app=app, base_url=BASE_URL) as client:
#         response = await client.delete("/products/19")
#         assert response.status_code == 200  # Verifica que la eliminación fue exitosa


@pytest.mark.asyncio
async def test_get_product_not_found():
    """Prueba de caja negra para obtener un producto que no existe."""
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get(
            "/products/999"
        )  # Suponiendo que el ID 999 no existe
        assert response.status_code == 404  # Verifica que se devuelva un error 404


# Pruebas de Caja Blanca
@pytest.mark.asyncio
async def test_product_created_without_name():
    """Prueba de caja blanca para validar la creación de un producto."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(name="", description="Nueva descripción", price=1800, stock=30)

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "String should have at least 1 character" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_created_without_price():
    """Prueba de caja blanca para validar la creación de un producto."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x", description="Nueva descripción", price=None, stock=30
        )

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "Decimal input should be an integer, float, string or Decimal object" in str(
        exc_info.value
    )


@pytest.mark.asyncio
async def test_product_created_with_string_in_price():
    """Prueba de caja blanca para validar la creación de un producto."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x",
            description="Nueva descripción",
            price="Incorrect",
            stock=30,
        )

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "Input should be a valid decimal" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_created_with_negative_price():
    """Prueba de caja blanca para validar la creación de un producto sin stock."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x", description="Nueva descripción", price=-1800, stock=30
        )

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "Input should be greater than 0" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_created_without_stock():
    """Prueba de caja blanca para validar la creación de un producto sin stock."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x", description="Nueva descripción", price=1800, stock=None
        )

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "Input should be a valid integer" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_created_with_string_in_stock():
    """Prueba de caja blanca para validar la creación de un producto."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x",
            description="Nueva descripción",
            price=1800,
            stock="Incorrect",
        )

    # Validar que el mensaje de error esperado está dentro de la excepción
    assert "Input should be a valid integer" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_created_with_negative_stock():
    """Prueba de caja blanca para validar la creación de un producto sin stock."""
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            name="Producto x", description="Nueva descripción", price=1800, stock=-1
        )

    assert "Input should be greater than or equal to 0" in str(exc_info.value)


@pytest.mark.asyncio
async def test_product_creation_logic(mocker):
    """Prueba de caja blanca para la lógica interna al crear un producto."""

    new_product = {
        "name": "Producto B",
        "description": "Nueva descripción",
        "price": 15.0,
        "stock": 30,
    }

    # Mock de la base de datos
    mock_db = mocker.MagicMock()
    mock_db.add = mocker.MagicMock()
    mock_db.commit = mocker.MagicMock()
    mock_db.refresh = mocker.MagicMock()  # Mock para refresh

    # Crear una instancia de ProductCreate con el diccionario
    product_create_instance = ProductCreate(**new_product)

    # Simular el comportamiento del refresh para asignar un ID
    mock_db.refresh.side_effect = lambda x: setattr(
        x, "id", 1
    )  # Simula que se asigna un ID

    product = create_product(product_create_instance, db=mock_db)

    # Asegúrate de que se llamó a add y commit
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    # Verifica que el producto devuelto tiene un ID
    assert product.id is not None
    assert product.name == new_product["name"]
