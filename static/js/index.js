(function ($) {
    const $loadingElement = $('.loading');
    const $emptyFiles = $('.empty-files');
    const $cards = $('.content-cards');
    const $uploadPhotos = $('.upload-photos');

    // fix menu when passed
    $('.masthead')
        .visibility({
            once: false,
            onBottomPassed: function () {
                $('.fixed.menu').transition('fade in');
            },
            onBottomPassedReverse: function () {
                $('.fixed.menu').transition('fade out');
            }
        })
    ;

    // create sidebar and attach to menu open
    $('.ui.sidebar')
        .sidebar('attach events', '.toc.item');

    function fileListEmpty() {
        $emptyFiles.show();
        $cards.hide();

        $loadingElement.hide();
    }

    function drawCards(data, refresh) {
        if (refresh) {
            removeCards();
        }

        data.forEach(function (item) {
            const newElement = `
                <div class="column">
                    <div class="ui fluid card">
                        <div class="content">
                            <a class="delete-image" 
                                href="javascript:void(0);">
                                <i data-path="${item.path_display}" class="right floated remove icon red"></i>
                            </a>
                            <div class="header" style="word-wrap: break-word;">${item.name}</div>
                            <div class="meta">
                                <span class="date">Created at ${moment(item.client_modified).format('LL')}</span>
                            </div>
                        </div>
                        <div class="blurring dimmable image" style="height: 250px;">
                            <img src="${item.thumbnail}" style="position: absolute; max-height: 100%; max-width: 100%; width: auto;height: auto; top: 0; bottom: 0; left: 0; right: 0; margin: auto;">
                        </div>
                    </div>
                </div>
                
            `;

            $cards.append(newElement);
        });

        $cards.show();
        $emptyFiles.hide();
        $loadingElement.hide();
    }

    function removeCards() {
        $cards.empty();
    }

    $cards.on('click', '.delete-image', function (e) {
        e.preventDefault();

        const $el = $(e.target);

        const path = $el.data('path');

        swal({
            title: "Are you sure?",
            text: "Once deleted, you will not be able to recover this file!",
            icon: "warning",
            buttons: {
                cancel: {
                    text: "Cancel",
                    visible: true,
                    closeModal: true,
                },
                confirm: {
                    text: "Delete",
                    value: true,
                    visible: true,
                    closeModal: false
                }
            },
            dangerMode: true
        }).then((willDelete) => {
            if (willDelete) {
                $.ajax({
                    type: 'POST',
                    url: urls.removeFile,
                    data: {
                        path
                    },
                    success: function (resp) {
                        swal(resp.message, {icon: "success"});
                        getFiles(true);
                    },
                    error: function () {
                        swal("Oh noes!", "The AJAX request failed!", "error");
                        $loadingElement.hide();
                    }
                });
            }
        });
    });

    function getFiles(refresh) {
        if (refresh) {
            $loadingElement.show();
        }

        $.getJSON(urls.fileList).then(function (response) {
            const data = response.data;

            if (data.length === 0) {
                fileListEmpty();
            } else {
                drawCards(data, refresh);
            }
        });
    }

    $('.upload-photos-btn').on('click', function (e) {
        e.preventDefault();

        $('.ui.modal.upload-modal')
            .modal({
                keyboardShortcuts: false,
                onApprove: function () {
                    return false;
                }
            }).modal('show')
        ;
    });

    Dropzone.options.myDropzone = {
        addRemoveLinks: true,
        acceptedFiles: ".png,.jpg,.jpeg",
        autoProcessQueue: false,
        maxFiles: 5,
        uploadMultiple: true,
        init: function () {
            let myDropzone = this;

            this.on("maxfilesexceeded", function (file) {
                swal("Max files exceeded", "You only can upload 5 files at the time", "error");
                this.removeFile(file);
            });

            this.on("addedfile", function () {
                if (this.files.length > 0) {
                    $uploadPhotos.removeClass('disabled');
                } else {
                    $uploadPhotos.addClass('disabled');
                }
            });

            this.on("removedfile", function () {
                if (this.files.length > 0) {
                    $uploadPhotos.removeClass('disabled');
                } else {
                    $uploadPhotos.addClass('disabled');
                }
            });

            this.on("completemultiple", function (resp) {
                $uploadPhotos.removeClass('loading');
                $uploadPhotos.removeClass('disabled');

                $('.ui.modal.upload-modal').modal('hide');

                swal("Files uploaded successfully", {icon: "success"});

                getFiles(true);
            });

            $uploadPhotos.on('click', function (e) {
                e.preventDefault();
                $uploadPhotos.addClass('loading');
                $uploadPhotos.addClass('disabled');
                myDropzone.processQueue();
            });
        }
    };

    getFiles(false);
})(jQuery);