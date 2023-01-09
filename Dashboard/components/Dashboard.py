from django_unicorn.components import UnicornView
from CustomUser.models import UserProfile
from General.models import Review
import psutil

from Order.models import Order, OrderStatus
from datetime import datetime, timedelta, time

class DashboardView(UnicornView):
    newOrdersCount = 0
    newUsersCount = 0
    newReviewsCount = 0
    todaysSales = 0
    ramUsage = [0, "green"]
    cpuUsage = [0, "green"]
    diskUsage = [0, "green"]

    def get_new_orders_count(self):
        today = datetime.now().date()
        yesterday = today - timedelta(1)
        self.newOrdersCount = Order.objects.filter(createdAt__gte=yesterday).count()

    def get_new_users_count(self):
        today = datetime.now().date()
        yesterday = today - timedelta(1)
        self.newUsersCount = UserProfile.objects.filter(date_joined__gte=yesterday).count()

    def get_new_reviews_count(self):
        today = datetime.now().date()
        yesterday = today - timedelta(1)
        self.newReviewsCount = Review.objects.filter(created_at__gte=yesterday).count()

    def get_today_sales(self):
        today = datetime.now().date()
        yesterday = today - timedelta(1)
        orders = Order.objects.filter(createdAt__gte=yesterday, status=OrderStatus.delivered.value)
        for order in orders:
            self.todaysSales += order.grandAmount

    def get_ram_usage(self):
        percentage = psutil.virtual_memory()[2]
        self.ramUsage[0] = percentage
        if (percentage > 80):
            self.ramUsage[1] = "red"
        elif (percentage > 40):
            self.ramUsage[1] = "orange"
        else:
            self.ramUsage[1] = "green"

    def get_cpu_usage(self):
        percentage = psutil.cpu_percent()
        print(psutil.disk_usage("/").percent)
        self.cpuUsage[0] = percentage
        if (percentage > 80):
            self.cpuUsage[1] = "red"
        elif (percentage > 40):
            self.cpuUsage[1] = "orange"
        else:
            self.cpuUsage[1] = "green"

    def get_disk_usage(self):
        percentage = psutil.disk_usage("/").percent
        self.diskUsage[0] = percentage
        if (percentage > 80):
            self.diskUsage[1] = "red"
        elif (percentage > 40):
            self.diskUsage[1] = "orange"
        else:
            self.diskUsage[1] = "green"

    def mount(self):
        self.get_server_updates()

    def get_server_updates(self):
        self.get_new_orders_count()
        self.get_new_users_count()
        self.get_new_reviews_count()
        self.get_today_sales()
        self.get_ram_usage()
        self.get_cpu_usage()
        self.get_disk_usage()