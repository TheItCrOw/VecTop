var currentlyLoading = false;

$(document).ready(function () {
    console.log("All finished loading!")

    // Handle the extracting of topics here
    $('body').on('click', '.extract-topics-btn', function () {
        if (currentlyLoading) return;

        $('.result-div').hide(100);
        lang = $('.lang-dropdown').val();
        text = $('.text-textarea').val();
        $btn = $(this);
        var oldHtml = $btn.html();
        $btn.html('Extracting...');
        $('.topics-result-container').html('');
        $('.sources-list').html('');
        currentlyLoading = true;

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/extract',
            data: JSON.stringify({ lang: lang, text: text }),
            success: function (data) {
                if (data.status == 200) {
                    console.log(data.result);
                    // Show the topics
                    data.result.topics.forEach(topics => {
                        var maintopic = topics[0];
                        var html = `<ul class='col-3 m-0 p-0 main'>${maintopic}<ul>`;
                        var subtopics = topics[1];
                        subtopics.forEach(subtopic => {
                            html += `<li class="sub"> ${subtopic}</li>`;
                        })
                        html += '</ul></ul>';
                        console.log(html);
                        $('.result-div').show(100);
                        $('.topics-result-container').html(html);
                    });
                    // Show the sources
                    var count = 1;
                    data.result.sources.forEach(source => {
                        $('.sources-list').append(
                            `<a class="btn btn-light mr-1" href="${source}" target="_blank">Source ${count}</a>`)
                        count += 1;
                    });
                }
                $btn.html(oldHtml);
                currentlyLoading = false;
            },
            error: function (error) {
                $btn.html(oldHtml);
                $('.result-div').show(100);
                $('.topics-result-container').html('Something went wrong, sorry... try again later.');
                currentlyLoading = false;
                console.log(error);
            }
        });
    })
});