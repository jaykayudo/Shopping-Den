function changeimg(e){
    $("#big-img").fadeOut(1000, function(){
        var bigScreen = document.getElementById("big-img")
        var img = e.querySelector("img")
        bigScreen.src = img.src
        $("#big-img").fadeIn(1000)
    })
}
function available_switch(e,num){
    $.ajax({
        url:'/cart/change-quantity/',
        type:'post',
        data:{
            quantity_id: num,
            quantity: document.getElementById(num).value,
            csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        success: function(response){
            
        },
        error: function(response){
            console.log(response)
        }
    });
}
var navBtn = document.getElementById("nav-button");
var navbar = document.getElementById("style-navbar");
function responsiveNav(){
    navbar.classList.toggle("responsive")
    navBtn.classList.toggle("rotate")
}
navBtn.addEventListener("click",responsiveNav)

function locationFilter(e){
    e.parentNode.submit()
    
}
function sortFilter(e){
    if(e.value != "")
        filterForm = document.getElementById('form-filter').submit()
}
function deletePost(id,name){
    Swal.fire({
        title:"Delete "+name+ " Post?",
        text:"these action cannot be reverted",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085db",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it"
    }).then(result=>{
        if(result.isConfirmed){
            window.location.href ='/posts/'+id+'/delete';
        }
    })
}
function saveItem(e,id){
    $.ajax({
        url:'/posts/save-item/',
        type:"get",
        data:{id:id},
        success:function(response){
            if(response.max){
                Swal.fire("you have reached your save limit. remove post from saved post(s) to save this post")
                return
            }
            if(!response.auth){
                Swal.fire({
                    text:"U need to login in order to save post",
                    icon:"warning"
                })
                return
            }
            if(response.saved){
                Swal.fire({
                    text:"item saved",
                    icon:"success"
                })
                e.innerHTML = '<i class="fa fa-bookmark"></i>'
            }
            else{
                Swal.fire({
                    text:"item removed",
                    icon:"success"
                })
                e.innerHTML = '<i class="fa fa-bookmark-o"></i>'
            }
        },
        error:function(){
            Swal.fire({
                text:"Item could not be saved",
                icon:"error"
            })
        }
    })
}
function removeSavedItem(id){
    window.location.href ='/posts/'+id+'/save-item/delete';
}