let params = (new URL(document.location)).searchParams;
const message = document.getElementById('message')

if (params.get("action") === 'success') {
    message.classList.remove('hide')
    message.classList.add('show')
    message.classList.add('alert-success')
    message.textContent = 'Рекрут создан, тестовое задание пройдено, ' +
        'пожалуйста ожидайте приглашения в орден, \n' +
        'в случае успеха на ваш электронный адрес будет отправлено письмо!'
} else {
    message.classList.remove('show')
    message.classList.remove('alert-success')
    message.classList.add('hide')
}