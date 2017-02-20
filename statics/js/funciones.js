var iPastie=0;
var menuVisible=1;
var menuPerfilVisible=0;

function desplegarMenu() {
 var ancho, value;
 ancho=$(window).width();
    if(menuVisible==1){
        if(ancho>=1024){
                $(".menu").css("display","none");
                $(".cont-invisible-menu").css("display","none");
                $(".contenido").css("width","83%");
        }
        if(ancho>=768 && ancho <1024){
                $(".menu").css("display","none");
                $(".cont-invisible-menu").css("display","none");
                $(".contenido").css("width","80%");
        }
        if(ancho>=500 && ancho <768){
                $(".menu").css("display","none");
                $(".cont-invisible-menu").css("display","none");
                $(".contenido").css("width","100%");
        }
        if(ancho<500){
                $(".menu").css("display","none");
                $(".cont-invisible-menu").css("display","none");
        }
       menuVisible=0;
    }
    else{
        if(ancho>=1024){
                $(".menu").css("display","block");
                $(".cont-invisible-menu").css("display","block");
                $(".contenido").css("width","66%");
        }
        if(ancho>=768 && ancho <1024){
                $(".menu").css("display","block");
                $(".cont-invisible-menu").css("display","block");
                $(".contenido").css("width","60%");
        }
        if(ancho>=500 && ancho <768){
                $(".menu").css("display","block");
                $(".cont-invisible-menu").css("display","block");
                $(".contenido").css("width","73%");
        }
        if(ancho<500){
                $(".menu").css("display","block");
                $(".cont-invisible-menu").css("display","block");
        }
        menuVisible=1;
    }
}

function desplegarMenuPerfil() {
    var ancho;
    ancho=$(window).width();
    if (menuPerfilVisible==0) {
        if(ancho>767){
            $(".menu-perfil-der").css("display","block");
            $(".vista-perfil").css("background-color","#777777");           
            menuPerfilVisible=1; 
        }
        if(ancho<=767 && menuVisible==1){
            $(".menu-perfil-izq").css("display","block");
            $(".vista-perfil").css("background-color","#777777");
            menuPerfilVisible=1; 
        }   
    }
    else{
        if(ancho>767){
            $(".menu-perfil-der").css("display","none");
            $(".vista-perfil").css("background-color","#555555");
            menuPerfilVisible=0;
        }
        if(ancho<=767 && menuVisible==1){
            $(".menu-perfil-izq").css("display","none");
            $(".vista-perfil").css("background-color","#555555");
            menuPerfilVisible=0;
        }   
    }
}

function cargarPastiesInicio() {
    var i, mostrado=0, clon, nodo, Ultnodo;

    $.getJSON("statics/json/pasties.json", function(cont) {
            i=cont.length-1;
            while(mostrado<5){
                if(i>=0 && cont[i]!=null){
                    if (cont[i].private==false) {
                        nodo = $(".content").first();
                        clon=nodo.clone()
                        clon.find(".data_owner").append(cont[i].owner);
                        clon.find(".data_date").append(cont[i].date);
                        clon.find(".data_title").append(cont[i].title );                     
                        clon.find(".data_content").append(cont[i].content);
                        clon.find(".data_hashtag").append("<b>"+cont[i].hashtag+"</b>");
                        Ultnodo=$(".content").last();
                        clon.insertAfter(Ultnodo);
                        mostrado++;
                        iPastie=i;
                    }
                    i--;
                }
            }
            $(".content").first().remove();              
        });

}


function lee_json() {
	var i, mostrado=0, clon, nodo;
    $.getJSON("statics/json/pasties.json", function(cont) {
            i=iPastie-1;
            while(mostrado<5 && i>=0){
                if(i>=0 && cont[i]!=null){
                    if (cont[i].private==false) {
                        nodo = $(".content").last();
                        clon=nodo.clone()
                        clon.find(".data_owner").html(cont[i].owner);
                        clon.find(".data_date").html(cont[i].date);
                        clon.find(".data_title").html(cont[i].title );                     
                        clon.find(".data_content").html(cont[i].content);
                        clon.find(".data_hashtag").html("<b>"+cont[i].hashtag+"</b>" );
                        clon.insertAfter(nodo);
                        mostrado++;
                        iPastie=i;
                    }
                    i--;
                    if(i<0) $(".botUpdate").hide();
                }
            }              
        }); 
}

function cargarPerfilOtro(){
    document.location.href="/user";
}
function cargarPastiesHashtag(){
    alert("Pasties filtrados por categoria selecionada");
    document.location.href="index.html";   
}
function crear(){
    alert('Su pastie ha sido creado exitosamente');
}

function recuperar(){
    alert('Se ha enviado una contrasena provisional al correo electronico asociado a tu cuenta');
}

function eliminar(){
    confirm("Desea Eliminar el pastie seleccionado?");
}

function editar(){
    alert('Su pastie ha sido modificado exitosamente');
}

function no_reg(){
    alert('Este usuario no se encuentra registrado');
}