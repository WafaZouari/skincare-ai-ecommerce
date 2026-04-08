#backend architecture overview
backend/
├── app/
│   ├── main.py          ✅ App entry point, CORS, router wiring
│   ├── core/
│   │   └── config.py    ✅ Settings with pydantic-settings + .env
│   ├── db/
│   │   └── database.py  ✅ SQLAlchemy engine + MongoDB connection
│   ├── models/
│   │   └── user.py      ✅ User ORM model (PostgreSQL)
│   ├── schemas/
│   │   ├── user.py      ✅ UserCreate / UserUpdate / UserResponse
│   │   └── ai_session.py ✅ MongoDB AI session schema
│   ├── services/
│   │   ├── user_service.py  ✅ User CRUD logic
│   │   └── ai_service.py    ✅ AI session logic (MongoDB)
│   └── api/v1/
│       └── endpoints/
│           ├── users.py       ✅ User routes
│           └── ai_sessions.py ✅ AI session routes
├── .env                 ⚠️  Minimal (missing SECRET_KEY, etc.)
└── requirements.txt     ✅ All core deps installed
