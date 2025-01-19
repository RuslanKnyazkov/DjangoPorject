document.addEventListener('DOMContentLoaded', () => {

const button = document.getElementById('btn_sub');

button.addEventListener('click', () => {
        $.post( '/post/subscribe/' ,
        {'cat_id': button.value},
        function(data) {
            const toastLiveExample = document.getElementById('liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
            if (data.status === true) {
                button.innerHTML = 'Вы подписаны'
                button.className = "btn btn-success"
                toastBootstrap.show()}
            else {
                button.innerHTML = 'Подписаться'
                button.className = "btn btn-primary"
                hidePopup()
                }
            })
        })
    })


$.ajax({method: "GET",
        url: "/post/subscribe/",
        success: (response) => {
        console.log(response)
        const button = document.getElementById('btn_sub')
        const userSubscribeStatus = document.getElementById('sub_id')
        .classList.replace('hidden-sub-div','show-sub-div')
        console.log(userSubscribeStatus)

        for (i = 0; i< response.all_subscribe_category.length; ++i){

        if (parseInt(button.value) === response.all_subscribe_category[i].category_id){
                button.innerHTML = 'Вы подписаны'
                button.className = "btn btn-success"
                return;
            }
        else {
                button.innerHTML = 'Подписаться'
                button.className = "btn btn-primary"
            }
        }
        }
    })