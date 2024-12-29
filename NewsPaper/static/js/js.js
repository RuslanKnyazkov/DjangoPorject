window.YaAuthSuggest.init(
    {
      client_id: "a8a421cbc51a4886904975d758cdee76",
      response_type: "token",
      redirect_uri: "https://oauth.yandex.ru/verification_code"
    },
    "https://oauth.yandex.ru",
    { view: "default" }
  )
  .then(({handler}) => handler())
  .then(data => console.log('Сообщение с токеном', data))
  .catch(error => console.log('Обработка ошибки', error))