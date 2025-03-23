from .user import router as user_router
from .master import router as master_router
from .menu import router as menu_router
from .module import router as module_router

routers = [user_router, master_router, menu_router, module_router]
