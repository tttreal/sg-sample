"""
URL configuration for sogl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include

from game.views import announce
from game.views import chara
from game.views import event
from game.views import gacha
from game.views import home
from game.views import mission
from game.views import party
from game.views import present
from game.views import quest

urlpatterns = [
    path("home", home.index),
    path("chara/list", chara.list_),
    path("chara/enhancement", chara.enhancement),
    path("chara/enhancement_exec", chara.enhancement_exec),
    path("chara/sell_exec", chara.sell_exec),
    path("party/list", party.list_),
    path("party/edit", party.edit),
    path("party/set_use_party", party.set_use_party),
    path("party/edit_exec", party.edit_exec),
    path("quest/list", quest.list_),
    path("quest/exec", quest.exec),
    path("present/box", present.box),
    path("present/receive", present.receive),
    path("present/debug_send", present.debug_send),
    path("present/debug_send_exec", present.debug_send_exec),
    path("gacha/list", gacha.list_),
    path("gacha/exec", gacha.exec),
    path("announce/detail", announce.detail),
    path("mission/list", mission.list_),
    path("mission/achieve", mission.achieve),
    path("event/top", event.top),
    path("event/exec_quest", event.exec_quest),
]
