$(document).ready(function () {
    const $loadingElement = $('.loading');
    const $emptyFiles = $('.empty-files');
    const $cards = $('.content-cards');

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
                            <div class="header">${item.name}</div>
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

    getFiles(false);
});