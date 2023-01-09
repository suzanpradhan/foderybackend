from this import s
from django_unicorn.components import UnicornView


class SidebarView(UnicornView):
    user = None
    username = ""

    def mount(self):
        self.user = self.request.user
        if self.user.profile_exists():
            self.username =  self.user.profile_full_name()
        else:
            self.username =  self.user.email

