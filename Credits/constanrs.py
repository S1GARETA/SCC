# Словарь соответствия строкового типа буста к хранимому в базе данных числу
BOOST_TYPE_NAME_TO_NUMBER = {
    'casual': 0, # Классический буст
    'auto': 1, # Автоматический буст
}
# Соответствие числового значения к строковому. Нужно для представления данных в панели администратора Django.
BOOST_TYPE_CHOICES = {
    (BOOST_TYPE_NAME_TO_NUMBER['casual'], 'casual'),
    (BOOST_TYPE_NAME_TO_NUMBER['auto'], 'auto'),
}
# Конфигурация различных типов бустов. Параметры будут влиять на изменение значений различных бустов в модели (например, при покупке буста).
# Здесь можно описать какие угодно параметры.
# У нас все скейлы будут умножаться на соответствующие поля, определяя величину, на которую будут изменяться значения.
BOOST_TYPE_VALUES = {
    BOOST_TYPE_NAME_TO_NUMBER['casual']: {
        'click_power_scale': 1, # В классическом бусте сила клика будет оставаться такой, какая она есть.
        'auto_click_power_scale': 0, # В классическом бусте сила автоклика будет уничтожена.
        'price_scale': 2, # Немного вырастет в цене.
    },
    BOOST_TYPE_NAME_TO_NUMBER['auto']: {
        'click_power_scale': 0, # В автоматическом бусте сила клика будет самовыпиливаться.
        'auto_click_power_scale': 1, # В автоматическом бусте сила автоклика останется прежней.
        'price_scale': 3, # Невероятно вырастет в цене.
    }
}