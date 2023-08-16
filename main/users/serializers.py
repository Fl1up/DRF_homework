import datetime

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей  - владельца"""

    pay = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_pay(self, instance):
        """Добавление истории платежей"""
        payments_list = []
        if instance.pay_set.all():
            for i in instance.pay_set.all().values_list():
                pay_list = []
                # дата
                pay_list.append(i[2])
                # сумма платежа
                pay_list.append(i[5])
                # тип оплаты
                pay_list.append(i[6])
                payments_list.append(pay_list)

            return payments_list
        return None


class UserSerializerForOthers(serializers.ModelSerializer):
    """Сериализатор для пользователей - общий"""

    class Meta:
        model = User
        fields = (
            "email",
            "avatar",
            "country",
            "first_name",
            "last_name",
        )
