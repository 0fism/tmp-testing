document.addEventListener('DOMContentLoaded', function () {

    //Heart onclick triggered likeToggle
    document.querySelectorAll('.fa-heart').forEach(div => {
        div.onclick = function () {
            likeToggle(this);
            //"Toggle async await promise, element"
            function likeToggle(element) {
                //console.log('testing'); 
                
                fetch(`/like/${element.dataset.id}`)
                    // .then(response => response.json())  <=can be write as
                    .then(response => {return response.json();})
                    .then(data => {
                        element.querySelector('trigger').innerHTML = data.totalLikes;
                        element.className = data.likeIcon;
                    });
            }
           
        };
    });


    //Edit form toggle effect
    document.querySelectorAll("[id^='edit_post_']").forEach(a => {
    a.onclick = function () {

        //console.log('first null: open form');
        var selectDataset = document.querySelector('#post_text_' + this.dataset.id);
        selectDataset.style.display = 'none';  //none
        document.querySelector('#form_' + this.dataset.id).querySelector('#id_form_edit').value = selectDataset.innerHTML;
        document.querySelector('#form_' + this.dataset.id).style.display = '';  //null
    };
});

    document.querySelectorAll("[id^='close_form_']").forEach(a => {
        a.onclick = function () {
            //console.log('second: close form');
            closeFormToggle(this);

            function closeFormToggle(element) {
                var selectDataset = document.querySelector('#post_text_' + element.dataset.id);
                selectDataset.style.display = '';  //null
                document.querySelector('#form_' + element.dataset.id).style.display = 'none';  //none
            }
        };

    });

    //Click follow button
    if (document.getElementById("followButton")){
        d = document.querySelector('#followButton');
        d.addEventListener("mouseover", function (event) {
            if (this.className == "btn btn-outline-primary"){
                this.style.backgroundColor = "#007bff";
                this.innerHTML = "Following"
            }else{
                this.style.backgroundColor = "red";
                this.innerHTML = "Unfollow";
                
            }
        });
    
        d.addEventListener("mouseout", function (event) {
            if (this.className == "btn btn-outline-primary"){
                this.style.backgroundColor = "white";
                this.innerHTML = "Follow"
            }else{
                this.style.backgroundColor = "#007bff";
                this.innerHTML = "Following";
                
            }
        });
    
        d.addEventListener("click", function (event) {
            fetch(`/follow/${this.dataset.id}`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('#followToggleButton').innerHTML = data.total_followers;
                    if (data.status == "following") {
                        this.innerHTML = "Following";
                        this.className = "btn btn-primary";
                    } else {
                        this.style.backgroundColor = "#007bff";
                        this.innerHTML = "Follow";
                        this.className = "btn btn-outline-primary";
                    }
                });
    
        });

    };


    function alertMessage(data, alert, id) {
        let d = document.createElement('div');
        d.setAttribute('id', 'alertMessage');
        d.setAttribute('role', 'alert');
        alert.appendChild(d);
        var alertMessage = document.getElementById('alertMessage');

        document.querySelector('#post_text_' + id).innerHTML = data.text;
        d.innerHTML = "Post successfully!!!!";
        d.className = 'alert alert-success';

        setTimeout(function () {
            if (alertMessage) {
                $(alertMessage).fadeOut(10);
                alertMessage.remove();
                document.querySelector('#form_' + id).style.display = 'none';
                document.querySelector('#post_text_' + id).style.display = '';
            }
        }, 500);
    }

    document.querySelectorAll("[id^='form_']").forEach(form => {
        form.onsubmit = function () {
            this.querySelector('#close_button').style.display = "none";
            if (this.querySelector('#alertMessage') != null) {
                this.querySelector('#alertMessage').remove();
            }

            fetch(`/edit_post/${this.dataset.id}`, {
                    method: 'POST',
                    headers: {
                        'user-agent': 'Mozilla/4.0 MDN Example',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: $(this).serialize()
                })
                .then(response => response.json())
                .then(data => {
                    alertMessage(data, this.querySelector('#post_text_alert_' + this.dataset.id), this.dataset.id);
                    this.querySelector('#close_button').style.display = "";
                })
                ;
        }

    });
});