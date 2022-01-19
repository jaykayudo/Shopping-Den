function checksaved(){
    var savebtn = document.getElementsByClassName('saved-product-btn')
    for(var x = 0; x< savebtn.length; x++){
        id = savebtn[x].dataset['id']
        $.ajax({
            url:'/posts/check-saved-item/',
            type:"get",
            data:{id:id},
            success:function(response){
                if(response.max){
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
    
}