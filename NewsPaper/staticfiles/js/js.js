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
    /**
     * Handles the success response from the subscription request.
     * @param {object} response - The response data from the server.
     * @returns {undefined}
     */
    success: (response) => {
        console.log(response);

        // Get the subscription button and user subscription status element
        const button = document.getElementById('btn_sub');
        const userSubscribeStatus = document.getElementById('sub_id')
            .classList.replace('hidden-sub-div', 'show-sub-div');
        console.log(userSubscribeStatus);

        // Iterate over all subscribed categories
        for (let i = 0; i < response.all_subscribe_category.length; ++i) {
            // Check if the current category matches the button's value
            if (parseInt(button.value) === response.all_subscribe_category[i].category_id) {
                button.innerHTML = 'Вы подписаны'; // Update button text to "You are subscribed"
                button.className = "btn btn-success"; // Change button style to success
                return;
            } else {
                button.innerHTML = 'Подписаться'; // Update button text to "Subscribe"
                button.className = "btn btn-primary"; // Change button style to primary
            }
        }
    }
})