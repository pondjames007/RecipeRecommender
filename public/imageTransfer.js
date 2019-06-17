let socket = io();

socket.on('connect', ()=>{
    console.log('connected');
})


let getRecipe = document.getElementById('getRecipe')
getRecipe.addEventListener('click', ()=>{
    let imgs = document.querySelectorAll('.dz-preview img')
    let filename = ""
    for(let img of imgs){
        filename += img.alt + ","
    }
    console.log(filename)
    socket.emit('recipeName', {filename: filename});
    
})

socket.on('message', (message)=>{
    console.log('here!!');
    let div_imgResult = document.getElementById('image-transfer')
    console.log(div_imgResult)
    

    for(let i = 0; i < message.inputImages.length-1; i++){
        let img = document.createElement('img');
        img.src = '/images/result_' + i + '.jpg';
        div_imgResult.appendChild(img);
    }
    

})


socket.on('keywords', (keywords)=>{
    let div_keyword = document.querySelector('.recipe-texts');
    let kw = document.createElement('p');
    kw.innerText = keywords;
    div_keyword.appendChild(kw);

    let div_recipeImg = document.querySelector('.recipe-image')
    let img = document.createElement('img');
    img.src = '/images/output.jpg';
    div_recipeImg.appendChild(img);

})
