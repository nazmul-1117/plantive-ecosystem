from enum import StrEnum

class Permission(StrEnum):

    # User
    CREATE_POST: str = "create_post"
    DELETE_POST: str = "delete_post"

    # Plant
    CREATE_PLANT: str = "create_plant"
    UPDATE_PLANT: str = "update_plant"
    DELETE_PLANT: str = "delete_plant"

    # Garden
    CREATE_GARDEN: str = "create_garden"
    UPDATE_GARDEN: str = "update_garden"

    # Marketplace
    CREATE_PRODUCT: str = "create_product"
    UPDATE_PRODUCT: str = "update_product"
    DELETE_PRODUCT: str = "delete_product"

    # Admin
    MANAGE_USERS: str = "create_users"
    MANAGE_ROLES: str = "create_roles"