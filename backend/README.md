# Python Backend

```
backend/
│
├── app/
│   ├── routers/
│   │     auth_router.py
│   │     user_router.py
│   │     plant_router.py
│   │     garden_router.py
│   │     community_router.py
│   │     ai_router.py
│
│   ├── controllers/
│   │     auth_controller.py
│   │     user_controller.py
│   │     plant_controller.py
│   │     garden_controller.py
│   │     community_controller.py
│   │     ai_controller.py
│
│   ├── services/
│   │     auth_service.py
│   │     user_service.py
│   │     plant_service.py
│   │     garden_service.py
│   │     community_service.py
│   │     ai_service.py
│
│   ├── models/
│   │     user.py
│   │     plant.py
│   │     garden.py
│   │     post.py
│   │     comment.py
│   │     like.py
│
│   ├── schemas/
│   │     auth_schema.py
│   │     user_schema.py
│   │     plant_schema.py
│   │     garden_schema.py
│   │     community_schema.py
│
│   ├── middleware/
│   │     auth_middleware.py
│   │     exception_handler.py
│
│   ├── config/
│   │     database.py
│   │     settings.py
│   │     jwt.py
│
├── main.py
├── requirements.txt
└── alembic/

```

# Backend in JS
```md
backend/api-server
│
├── controllers
│   ├── authController.js
│   ├── plantController.js
│
├── routes
│   ├── authRoutes.js
│   ├── plantRoutes.js
│
├── models
│   ├── User.js
│   ├── Plant.js
│
├── middleware
│   ├── authMiddleware.js
│
├── services
│   ├── aiService.js
│
├── config
│   ├── database.js
│
└── server.js

```