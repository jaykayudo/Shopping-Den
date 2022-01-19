// Drag and Drop file
var dragArea = document.getElementById("drag-area");
var dragText = document.getElementById("drag-text");
var AltFileInput = document.getElementById("alt-file");
var fileInput = document.getElementById("file");
var file;
var imgBox = document.getElementById("image-box");

function showImageFile(){
    var validExtension = ["image/jpeg","image/jpg","image/png"]
    if(file.length > 3){
        Swal.fire({
            title:"Please select at most 3 images",
            icon:"error"
        })
        dragArea.classList.remove("drag-active")
        dragText.textContent = "Drag and Drop Product Images"
        fileInput.value = ""
        fileInput.files = []
        imgBox.innerHTML = `No Image`
        return
    }
    var error = false
    imgBox.innerHTML = ""
    for(var x = 0; x < file.length; x++){
        if(validExtension.includes(file[x].type)){
        
            // var filereader = new FileReader()
            // filereader.onload = ()=>{
            //     var fileURL = filereader.result;
            //     if(fileURL == "data:"){
            //         dragArea.classList.remove("drag-active");
            //         alert("Error parsing file")
            //         error = True
            //         return
            //     }
            //     else{
            //         var imgTag = `<div class="col-4 product-img-box"><img class="product-img" src="${fileURL}"></div>`
            //         imgBox.innerHTML += imgTag;
            //     }
            // }
            // filereader.readAsDataURL(file[x])
        }else{
            dragArea.classList.remove("drag-active")
            dragText.textContent = "Drag and Drop Product Images"
        
                Swal.fire({
                    title:"File should be of .jpg or .jpeg or .png type",
                    icon:"error"
                })
            error = True
            break
        }
    }
    if(!error){
        fileInput.files = file;
        dragArea.classList.add("drag-active");
        dragText.textContent = `${file.length} images selected`
    }
    else{
        dragArea.classList.remove("drag-active");
        dragText.textContent = `Drag and Drop Product Images`
    }
    
}

AltFileInput.addEventListener('click',function(e){
    e.preventDefault();
    fileInput.click();
})
fileInput.addEventListener('change',function(){
    file = this.files;
    if(file.length > 3){
        Swal.fire({
            title:"Please select at most 3 images",
            icon:"error"
        })
        fileInput.value = ""
        dragArea.classList.remove("drag-active")
        dragText.textContent = "Drag and Drop Product Images"
        this.value = ""
        this.files = []
        imgBox.innerHTML = ``
        return
    }
    if(file.length != 0){
        showImageFile();
    }
    else{
        dragText.textContent = "Drag and Drop Product Images"
        dragArea.classList.remove("drag-active");
    } 
    
})
dragArea.addEventListener("dragover",function(event){
    event.preventDefault();
    dragText.textContent = "Release to Upload Images"
    dragArea.classList.add("drag-active");
})
dragArea.addEventListener("dragleave",function(event){
    event.preventDefault();
    if(!file){
    dragText.textContent = "Drag and Drop Product Images"
    dragArea.classList.remove("drag-active");
    }
    else{
        dragArea.classList.add("drag-active");
        dragText.textContent = `${file.length} images selected`
    }
})
dragArea.addEventListener("drop",function(event){
    event.preventDefault();
    file = event.dataTransfer.files;
    if(file){
        showImageFile()
    }else{
        dragText.textContent = "Drag and Drop Product Images"
        dragArea.classList.remove("drag-active");
    }
})