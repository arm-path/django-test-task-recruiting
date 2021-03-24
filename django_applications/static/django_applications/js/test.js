const questions = document.querySelectorAll('.js-questions')
const send = document.getElementById('js-send')
const test = document.getElementById('js-test-id').textContent
const url = document.getElementsByTagName('form')[0].action
const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value

send.addEventListener('click', (event) => {
    let questions_json = []
    event.preventDefault()
    questions.forEach(function (entry) {
        let id = entry.querySelector('.js-question-id').textContent
        let question = entry.querySelector('.js-question').textContent
        let answer = entry.querySelector('.js-answer').checked
        questions_json.push({"pk": id, "question": question, "answer": answer})
    })
    $.ajax({
        method: "POST",
        url: url,
        data: {
            "csrfmiddlewaretoken": csrf_token,
            "orden_code": test,
            "questions": JSON.stringify(questions_json)
        },
        dataType: 'json',
        success: function (data) {
            if (data.success) {
                if (data.success === 'true') document.location.href = '/?action=success'
                else document.location.href = '/?action=error'
            }
        },
        error: function (data) {
            document.location.href = '/?action=error'
        }
    })
})
