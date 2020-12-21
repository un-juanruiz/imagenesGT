
function eliminar(){
    swal({
        title: "¿Estás seguro de querer eliminar la imagen?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          swal("La imagen ha sido eliminada", {
            icon: "success",
          });
        }
      });
    }
    
