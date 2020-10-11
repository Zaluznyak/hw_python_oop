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
        sum = 0
        now = dt.datetime.now()
        for record in self.records:
            if record.date == now.date():
                sum += record.amount
        return sum

    def get_week_stats(self):
        """Getting the sum of last week."""
        sum = 0
        now = dt.datetime.now()
        week_ago = now - dt.timedelta(days=6)
        print(week_ago)
        for record in self.records:
            date = record.date
            if week_ago.date() <= date <= now.date():
                sum += record.amount
        return sum


class Record:
    def __init__(self, amount,
                 comment, date=None):
        date_format = '%d.%m.%Y'
        if date:
            date_event = dt.datetime.strptime(date, date_format)
        else:
            date_event = dt.datetime.now()
        self.amount = amount
        self.comment = comment
        self.date = date_event.date()


class CashCalculator(Calculator):
    EURO_RATE = 90.82
    USD_RATE = 76.77

    def get_today_cash_remained(self, currency):
        """Write rest cash of today."""
        balance = self.limit - self.get_today_stats()
        if currency.lower() == 'rub':
            translate_crnc = 'руб'
        elif currency.lower() == 'usd':
            balance /= self.USD_RATE
            balance = round(balance, 2)
            translate_crnc = 'USD'
        elif currency.lower() == 'eur':
            balance /= self.EURO_RATE
            balance = round(balance, 2)
            translate_crnc = 'Euro'
        else:
            return('Неизвестная валюта!')
        if balance > 0:
            return(f'На сегодня осталось {balance} {translate_crnc}')
        elif balance < 0:
            balance = abs(balance)
            return(f'Денег нет, держись: '
                   f'твой долг - {balance} {translate_crnc}')
        else:
            return('Денег нет, держись')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """Write rest calories of today."""
        remains = self.limit - self.get_today_stats()
        if remains > 0:
            return(f'Сегодня можно съесть что-нибудь ещё,'
                   f' но с общей калорийностью не более {remains} кКал')
        else:
            return('Хватит есть!')


if __name__ == 'main':
    cash_cal = CashCalculator(1000)
    cash_cal.add_record(Record(amount=145, comment="кофе"))
    cash_cal.add_record(Record(amount=300, comment="Серёге за обед"))
    print(cash_cal.get_today_cash_remained("rub"))
