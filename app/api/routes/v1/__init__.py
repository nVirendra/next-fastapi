from .user import router as user_router
from .new_user import router as new_user_router
from .master import router as master_router
from .menu import router as menu_router
from .module import router as module_router
from .role import router as role_router

routers = [user_router, master_router, menu_router, module_router, role_router, new_user_router]
