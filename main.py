        #используемые функции
def upload_cloud(file,account):
    with open(file,'w') as fout:
        fout.write(account['fio'] + '\n')
        fout.write(str(account['year']) + '\n')
        fout.write(account['password'] + '\n')
        fout.write(str(account['money']) + '\n')
        fout.write(str(account['limit']) + '\n')
        fout.write(str(len(account['transactions'])) + '\n')
        for transaction in account['transactions']:
            fout.write(transaction['comment'] + '\n')
            fout.write(str(transaction['amount']) + '\n')


def download_cloud(file,account):
    with open(file) as fin:
        account['fio'] = fin.readline().strip()
        account['year'] = int(fin.readline().strip())
        account['password'] = fin.readline().strip()
        account['money'] = int(fin.readline().strip())
        account['limit'] = int(fin.readline().strip())
        account['transactions'] = []
        len_transactions = int(fin.readline().strip())
        for i in range(len_transactions):
            comment = fin.readline().strip()
            amount = int(fin.readline().strip())
            transaction = {'comment':comment,'amount':amount}
            account['transactions'].append(transaction)


def create_account():
    account['fio'] = str(input('Введите ФИО: '))
    birthday_year = int(input('Введите год рождения: '))
    account['year'] = 2024 - birthday_year
    print('Создан аккаунт: ' + account['fio'] + ' (' + str(account['year']) + ' лет' + ')')
    while True:
        account['password'] = str(input('Введите пароль: '))
        password_confirm = str(input('Повторите пароль: '))
        if account['password'] == password_confirm:
            print('Аккаунт успешно зарегистрирован!')
            account['money'] = 0
            print('Текущий баланс: ' + str(account['money']))
            break
        else:
            print('Пароли не совпадают')
    account['limit'] = int(input('Выставление лимита на счет: '))
    upload_cloud('data.txt', account)


def cash_in_money(account, cash_in):
    if (cash_in + account['money']) >= account['limit']:
        print('Введенная сумма превысит лимит!')
        print('Ваш лимит: ' + str(account['limit']))
    else:
        account['money'] += cash_in
        print('Счет успешно пополнен!')
        print('Ваш баланс: ' + str(account['money']))
        upload_cloud('data.txt', account)


def cash_out_money(account, password_test):
    if password_test == account['password']:
        print('Ваш баланс: ' + str(account['money']))
        cash_out = int(input('Введите сумму снятия: '))
        if cash_out > account['money']:
            print('Недостаточно средств!')
        else:
            account['money'] -= cash_out
            print('Снятие успешно завершено, ваш баланс: ' + str(account['money']))
            upload_cloud('data.txt', account)
    else:
        print('Неверный пароль!')


def limit_add_new():
    password_test = str(input('Для изменения лимита введите пароль: '))
    if password_test == account['password']:
        print('Нынешний лимит: ' + str(account['limit']))
        limit_new = int(input('Выставление нового лимита на счет: '))
        if limit_new >= account['money']:
            print('Лимит успешно изменен!')
            print('Ваш лимит: ' + str(account['limit']))
            account['limit'] = limit_new
            upload_cloud('data.txt', account)
        else:
            print('Лимит меньше нынешнего счета!')
    else:
        print('Неверный пароль!')


def balance_vision():
    password_test = str(input('Для выведения баланса введите пароль: '))
    if password_test == account['password']:
        print('Ваш лимит: ' + str(account['limit']))
        print('Ваш баланс: ' + str(account['money']))
    else:
        print('Неверный пароль!')


def new_transaction(account):
    comment = input('Введите назначение транзакции: ')
    amount = int(input('Введите сумму будущего пополнения: '))
    transaction = {'comment': comment, 'amount': amount}
    account['transactions'].append(transaction)
    print('Активные транзакции: ' + str(len(account['transactions'])))
    upload_cloud('data.txt', account)


def del_transaction(account):
    comment = input('Введите назначение транзакции: ')
    amount = int(input('Введите сумму будущего пополнения: '))
    transaction = {'comment': comment, 'amount': amount}
    account['transactions'].remove(transaction)
    print('Транзакция: (' + transaction['comment'] + ') успешно удалена!')
    upload_cloud('data.txt', account)


def transactions_apply(account):
    rejected_transactions = []
    for transaction in account['transactions']:
        if transaction['amount'] + account['money'] <= account['limit']:
            account['money'] += transaction['amount']
            print('Применена транзакция: ' + transaction['comment'])
        else:
            rejected_transactions.append(transaction)
            print('Не применена транзакция из-за превышения установленного лимта: ' + transaction['comment'] + '!!!')
    account['transactions'] = rejected_transactions
    upload_cloud('data.txt', account)


def transactions_stat(account):
    statistic_transactions = {}
    for transaction in account['transactions']:
        statistic_transactions[transaction['amount']] = statistic_transactions.get(transaction['amount'],0) + 1
    for amount, count in statistic_transactions.items():
        print(str(amount) + ': ' + str(count) + ' платеж(а)')


def transactions_sum(account):
    for transaction in account['transactions']:
        yield transaction


def filtration_transactions(account, threshold):
    for transaction in transactions_sum(account):
        if sum(transaction['amount'] for transaction in account['transactions']) >= threshold:
            print(f"{transaction['amount']}: "f"{transaction['comment']}")
        else:
            print('Сумма транзакций меньше введенного порога!!!')


def main_code():
    print('Загрузить данные из облака?')
    print('Если желаете загрузить: введите да')
    op_cloud = str(input())
    if op_cloud == 'да':
        try:
            download_cloud('data.txt', account)
        except FileNotFoundError:
            print('Файл отсуствует!!!\nБудет произведено закрытие программы!')
            exit()
        print('Данные успешно загружены!')
    else:
        print('Данные загружены не будут!')
    print('Добро пожаловать!')
    while True:
        try:
            print('1.Создать аккаунт')
            print('2.Положить деньги на счет')
            print('3.Снять деньги')
            print('4.Вывести баланс на экран')
            print('5.Выставление лимита на счет')
            print('6.Транзакции')
            print('7.Выйти из программы')
            command = int(input('Введите номер команды: '))
            if command == 1:
                create_account()
            elif command == 2:
                cash_in = int(input('Введите сумму пополнения: '))
                cash_in_money(account, cash_in)
            elif command == 3:
                password_test = str(input('Для снятия денег введите пароль: '))
                cash_out_money(account, password_test)
            elif command == 4:
                balance_vision()
            elif command == 5:
                limit_add_new()
            elif command == 6:
                while True:
                    print('Транзакции:')
                    print('1.Выставление ожидаемого пополнения')
                    print('2.Удалить транзакцию')
                    print('3.Применить транзакции')
                    print('4.Статистика по ожидаемым пополнениям')
                    print('5.Фильтрация отложенных пополнений')
                    print('6.Выход')
                    op = int(input('Введите номер команды: '))
                    if op == 1:
                        new_transaction(account)
                    elif op == 2:
                        del_transaction(account)
                    elif op == 3:
                        transactions_apply(account)
                    elif op == 4:
                        transactions_stat(account)
                    elif op == 5:
                        threshold = int(input('Введите сумму порога: '))
                        filtration_transactions(account, threshold)
                    elif op == 6:
                        print('Выход из операций ТРАЗАКЦИИ!')
                        break
                    else:
                        print('Нет такой операции')
            elif command == 7:
                print('Всего доброго, до встречи!!!')
                break
            else:
                print('Нет такой операции')
        except ValueError:
            print('Данные введены не корректно!!!\nВведите числа вместо текста!')
            continue
        #основной код программы
if __name__ == '__main__':
    account = {'fio': '', 'year': -1, 'password': '', 'money': 0, 'limit': -1, 'transactions': []}
    transactions = []
    main_code()
