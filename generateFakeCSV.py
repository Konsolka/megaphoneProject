import random
import csv
from datetime import date
from faker import Faker
from faker.providers import date_time


class User:
    def __init__(self, uid, curr_balance, date_added, age, city_of_residence, time_stamp, active_tariff):
        self.uid = uid
        self.curr_balance = curr_balance
        self.date_added = date_added
        self.age = age
        self.city_of_res = city_of_residence
        self.time_stamp = time_stamp
        self.active_tariff = active_tariff

    def __repr__(self):
        return 'ID: {ids}|curr balance: {curr_balance}| date add: {date_add}| age: {age}| city: {city}| time_stamp: {time_stamp}| active tariff {active_tariff}'.format(
            ids=self.uid, curr_balance=self.curr_balance, date_add=self.date_added, age=self.age, city=self.city_of_res,
            time_stamp=self.time_stamp,
            active_tariff=self.active_tariff
        )

    def retTup(self):
        tup = (
            self.uid, self.curr_balance, self.date_added, self.age, self.city_of_res, self.time_stamp,
            self.active_tariff)
        return tup


class UserGenerator:
    def __init__(self):
        self.uid = 0

    def generateUser(self):
        self.uid += 1
        curr_balance = round(random.uniform(0, 500), 1)
        date_added = fake.date_between('-5y')
        age = random.randint(date.today().year - date_added.year + 14, 100)
        city_of_res = fake.city_name()
        time_stamp = fake.date_time_between('-5y')
        active_tariff = random.randint(1, 6)
        return User(self.uid, curr_balance, date_added, age, city_of_res, time_stamp, active_tariff)


class Activity:
    def __init__(self, activity_id, time_stamp, service_type, spend, uid):
        self.activity_id = activity_id
        self.time_stamp = time_stamp
        self.service_type = service_type
        self.spend_amount = spend
        self.uid = uid

    def __repr__(self):
        return 'activity id {activity_id}| time stamp {time_stamp}| service type {service_type}| spend amount {spend}| UId {uid}'.format(
            activity_id=self.activity_id, time_stamp=self.time_stamp, service_type=self.service_type,
            spend=self.spend_amount, uid=self.uid
        )

    def retTup(self):
        tup = (self.activity_id, self.time_stamp, self.uid, self.service_type, self.spend_amount)
        return tup


class GenerateUserActivity:
    def __init__(self):
        self.activity_id = 0

    def generateActivity(self, generate_to_user: User):
        self.activity_id += 1
        time_stamp = fake.date_time_between(generate_to_user.date_added)
        service_type = random.choice(['смс', 'Звонок', 'Траффик'])
        spend_amount = random.randint(0, 10) if service_type != 'смс' else 1
        return Activity(self.activity_id, time_stamp, service_type, spend_amount, generate_to_user.uid)


def createFakeCSV():
    users = []
    activities = []
    activity = GenerateUserActivity()
    user = UserGenerator()

    fake.add_provider(date_time)
    for i in range(25):
        new_user = user.generateUser()
        users.append(new_user)
        perform_activities = random.randint(100, 200) * (new_user.date_added.year - new_user.time_stamp.year)
        for j in range(perform_activities):
            activities.append(activity.generateActivity(new_user))
    with open('users.csv', mode='w', encoding="utf-8") as user_file:
        user_writer = csv.writer(user_file)
        tup1 = ("id", "Текущий баланс", "Дата добавления", "Возраст", "Город проживания",
                "Временная метка последней активности", "Активный тариф")
        user_writer.writerow(tup1)
        for u in users:
            user_writer.writerow(u.retTup())
    with open('actions.csv', mode='w', encoding="utf-8") as tariff_file:
        tariff_writer = csv.writer(tariff_file)
        tup1 = ("id", "Метка времени", "id абонента", "Тип услуги", "Объем затраченных единиц")
        tariff_writer.writerow(tup1)
        for a in activities:
            tariff_writer.writerow(a.retTup())


if __name__ == '__main__':
    fake = Faker('ru-RU')
    createFakeCSV()
