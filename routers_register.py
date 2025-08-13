from aiogram import Dispatcher
from handlers.complete_habit_handler import router as complete_router
from middlewares.antispam import AntiSpamMiddleware
from handlers import honor_handler
from handlers import motivation
from handlers import subscription_sync

from handlers.about_me.about_options import router as about_options_router
from handlers.about_me.referral_handler import router as referral_router
from handlers.about_me.statistics import router as statistics_router
from handlers.about_me.profile_view import router as profile_view_router
from handlers.about_me.profile_fsm import router as profile_fsm_router
from handlers.about_me.members import router as members_router


from handlers.dreams import dreams_views
from handlers.dreams import halls_views
from handlers.dreams import plans_views
from handlers.dreams import goals_views
from handlers.dreams import goals_fsm
from handlers.dreams import dream_photos_fsm
from handlers.dreams import goals_menu




from handlers import (
    start,
    habit_add,
    challenge_select,
    habit_confirm,
    habit_auto_confirm,
    delete_habit,
)
from keyboards import menu

async def register_all_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(honor_handler.router)
    dp.include_router(menu.router)
    dp.include_router(motivation.router)

    # ⬆️ СРАЗУ ПОСЛЕ menu
    dp.include_router(goals_menu.router)
    dp.include_router(goals_fsm.router)
    dp.include_router(goals_views.router)
    dp.include_router(dream_photos_fsm.router)
    dp.include_router(dreams_views.router)
    dp.include_router(halls_views.router)
    dp.include_router(plans_views.router)

    dp.include_router(habit_add.router)
    dp.include_router(challenge_select.router)
    dp.include_router(habit_confirm.router)
    dp.include_router(habit_auto_confirm.router)
    dp.include_router(delete_habit.router)
    dp.include_router(complete_router)
    dp.include_router(referral_router) 
    dp.update.middleware(AntiSpamMiddleware(delay=1))
    dp.include_router(profile_view_router)
    dp.include_router(profile_fsm_router)
    dp.include_router(statistics_router)
    dp.include_router(members_router)
    dp.include_router(subscription_sync.router)
    dp.include_router(about_options_router)




