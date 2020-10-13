import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        """Add record in list records."""
        self.records.append(record)

    def get_today_stats(self):
        """Getting the rest of the limit."""
        now = dt.date.today()
        rest = sum([record.amount for record in self.records
                   if record.date == now])
        return rest

    def get_week_stats(self):
        """Getting the sum of last week."""
        now = dt.date.today()
        week_ago = now - dt.timedelta(days=6)
        sum_week = sum([record.amount for record in self.records
                       if week_ago <= record.date <= now])
        return sum_week

    def remains(self):
        """Getting the remained of today."""
        remain = self.limit - self.get_today_stats()
        return remain


class Record:
    def __init__(self, amount,
                 comment, date=None):
        DATE_FORMAT = '%d.%m.%Y'
        if date is None:
            date_event = dt.date.today()
        else:
            date_event = dt.datetime.strptime(date, DATE_FORMAT).date()

        self.amount = amount
        self.comment = comment
        self.date = date_event


class CashCalculator(Calculator):
    EURO_RATE = 91.02
    USD_RATE = 77.08

    def get_today_cash_remained(self, currency):
        """Write rest cash of today."""
        remain = self.remains()
        if remain == 0:
            return 'Денег нет, держись'
        conversion = {
            'rub': [1, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
            }
        if currency.lower() not in conversion:
            return 'Неизвестная валюта'
        value = conversion[currency.lower()]
        balance = round(remain / value[0], 2)
        translate_crnc = value[1]
        if balance > 0:
            return f'На сегодня осталось {balance} {translate_crnc}'
        balance = abs(balance)
        return ('Денег нет, держись:'
                f' твой долг - {balance} {translate_crnc}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Write rest calories of today."""
        remain = self.remains()
        if remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {remain} кКал')
        return 'Хватит есть!'


if __name__ == 'main':
    cash_cal = CashCalculator(1000)
    cash_cal.add_record(Record(amount=145, comment="кофе"))
    cash_cal.add_record(Record(amount=300, comment="Серёге за обед"))
    print(cash_cal.get_today_cash_remained("rub"))
