from fastapi import APIRouter

from database import users, products, orders, database
from models import User, UserIn, Product, ProductIn, Order, OrderIn
from bcrypt import gensalt, hashpw

router = APIRouter()


@router.get("/users", response_model=list[User], tags=["Users"])
async def get_users():
    query = users.select()
    result = await database.fetch_all(query)
    users_with_orders = []
    for row in result:
        user = User.model_validate(dict(row))
        orders_items = await database.fetch_all(orders.select().where(orders.c.user_id == user.id))
        user.orders = [Order.model_validate(dict(ord)) for ord in orders_items]
        users_with_orders.append(user)

    return users_with_orders


@router.post("/users", response_model=User, tags=["Users"])
async def create_user(user: UserIn):
    salt = gensalt()
    password_hash = hashpw(user.password.encode('utf-8'), salt=salt)
    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=password_hash.decode('utf-8')
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


@router.get("/users/{user_id}", response_model=User, tags=["Users"])
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    user = User.model_validate(dict(result))
    orders_items = await database.fetch_all(orders.select().where(orders.c.user_id == user.id))
    user.orders = [Order.model_validate(dict(ord)) for ord in orders_items]
    return user


@router.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id ==
                                 user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@router.get("/products", response_model=list[Product], tags=["Products"])
async def get_product():
    query = products.select()
    result = await database.fetch_all(query)
    products_with_orders = []
    for row in result:
        product = Product.model_validate(dict(row))
        orders_items = await database.fetch_all(orders.select().where(orders.c.product_id == product.id))
        product.orders = [Order.model_validate(dict(ord)) for ord in orders_items]
        products_with_orders.append(product)

    return products_with_orders


@router.post("/products", response_model=Product, tags=["Products"])
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@router.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    product = Product.model_validate(dict(result))
    orders_items = await database.fetch_all(orders.select().where(orders.c.product_id == product.id))
    product.orders = [Order.model_validate(dict(ord)) for ord in orders_items]
    return product


@router.put("/products/{product_id}", response_model=Product, tags=["Products"])
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id ==
                                    product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}


@router.get("/orders", response_model=list[Order], tags=["Orders"])
async def get_order():
    query = orders.select()
    return await database.fetch_all(query)


@router.post("/orders", response_model=Order, tags=["Orders"])
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@router.get("/orders/{order_id}", response_model=Order, tags=["Orders"])
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@router.put("/orders/{order_id}", response_model=Order, tags=["Orders"])
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id ==
                                  order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'order deleted'}
