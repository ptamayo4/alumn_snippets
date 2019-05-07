$(function () {
    var $modal = $('#cropModal');
    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_profile_pic").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $modal.foundation('open');
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#cropModal").on("open.zf.reveal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            cropBoxResizable: false,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("closed.zf.reveal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        console.log(`X: ${$("#id_x").val()}\nY:${$("#id_y").val()}\nH:${$("#id_height").val()}\nW:${$("#id_width").val()}\n`)
    });
});
