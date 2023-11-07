var currentlyLoading = false;
var legalCurrentlyLoading = false;

$(document).ready(function () {
    console.log("All finished loading!")

    // Generate a little example text
    $('body').on('click', '.example-btn', function () {
        if ($('.lang-dropdown').val() == 'de-DE') {
            $('.text-textarea').val('Die Basisprognose geht davon aus, dass sich das globale Wachstum von 3,5 Prozent im Jahr 2022 auf 3,0 Prozent im Jahr 2023 und 2,9 Prozent im Jahr 2024 verlangsamen wird, was deutlich unter dem historischen (2000-19) Durchschnitt von 3,8 Prozent liegt. In den fortgeschrittenen Volkswirtschaften wird mit einer Abschwächung von 2,6 Prozent im Jahr 2022 auf 1,5 Prozent im Jahr 2023 und 1,4 Prozent im Jahr 2024 gerechnet, da die Straffung der Politik zu greifen beginnt. Für die Schwellen- und Entwicklungsländer wird ein leichter Rückgang des Wachstums von 4,1 % im Jahr 2022 auf 4,0 % in den Jahren 2023 und 2024 erwartet. Die globale Inflation wird den Prognosen zufolge stetig zurückgehen, und zwar von 8,7 Prozent im Jahr 2022 auf 6,9 Prozent im Jahr 2023 und 5,8 Prozent im Jahr 2024, was auf eine straffere Geldpolitik zurückzuführen ist, die durch niedrigere internationale Rohstoffpreise unterstützt wird. Die Kerninflation wird den Projektionen zufolge im Allgemeinen allmählicher zurückgehen, und in den meisten Fällen wird erwartet, dass die Inflation erst 2025 zum Zielwert zurückkehrt.')
        } else {
            $('.text-textarea').val('The baseline forecast is for global growth to slow from 3.5 percent in 2022 to 3.0 percent in 2023 and 2.9 percent in 2024, well below the historical (2000–19) average of 3.8 percent. Advanced economies are expected to slow from 2.6 percent in 2022 to 1.5 percent in 2023 and 1.4 percent in 2024 as policy tightening starts to bite. Emerging market and developing economies are projected to have a modest decline in growth from 4.1 percent in 2022 to 4.0 percent in both 2023 and 2024. Global inflation is forecast to decline steadily, from 8.7 percent in 2022 to 6.9 percent in 2023 and 5.8 percent in 2024, due to tighter monetary policy aided by lower international commodity prices. Core inflation is generally projected to decline more gradually, and inflation is not expected to return to target until 2025 in most cases.');
        }
    })

    // Generate a little example text for legal as well
    $('body').on('click', '.legal-example-btn', function () {
        $('.legal-text-textarea').val('Kaution bei rauchenden Mietern.')
    })

    // Handle the extracting of legal references here
    $('body').on('click', '.extract-references-btn', function () {
        if (legalCurrentlyLoading) return;

        $('.legal-result-div').hide(100);
        var confidence = parseInt($('.legal-confidence-range').val());
        var text = $('.legal-text-textarea').val();
        var $btn = $(this);
        var oldHtml = $btn.html();
        $btn.html('Extracting...');
        legalCurrentlyLoading = true;

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/legal/extract',
            data: JSON.stringify({ text: text, confidence: confidence }),
            success: function (data) {
                console.log(data);
                if (data.status == 200) {
                    // Show the references
                    var totalHtml = '<div>';
                    data.result.references.forEach(item => {
                        var ref = item[0];
                        var res = item[1];
                        var context = item[2];
                        var tocs = item[3];

                        var html = '<hr class="mb-2 mt-2"/><div class="legal-result-wrapper">';
                        var header = '<div class="legal-result-header text-left flex-wrap flexed align-items-center justify-content-start">';
                        header += '<i class="mr-3 fas fa-book-open text-dark"></i>'
                        tocs.forEach(toc => {
                            if (toc == '') return;
                            header += `<span>${toc}<i class="ml-1 mr-1 fas fa-chevron-right text-dark"></i></span>`;
                        })
                        header += ` <span class="ref">${ref}</span>`;
                        header += '</div>'
                        html += header;

                        var context = `<i class="text-dark mt-2 mb-2 fas fa-gavel"></i><p class="context">"${context}"</p>`;

                        html += context + '</div>';
                        totalHtml += html;
                    });
                    totalHtml += '</div>'
                    $('.legal-result-div').show(100);
                    $('.references-result-container').html(totalHtml);
                }
                $btn.html(oldHtml);
                legalCurrentlyLoading = false;
            },
            error: function (error) {
                $btn.html(oldHtml);
                $('.legal-result-div').show(100);
                legalCurrentlyLoading = false;
                console.log(error);
            }
        });
    })

    // Handle the extracting of topics here
    $('body').on('click', '.extract-topics-btn', function () {
        if (currentlyLoading) return;

        $('.result-div').hide(100);
        var lang = $('.lang-dropdown').val();
        var corpus = $('.corpus-dropdown').val();
        var confidence = parseInt($('.confidence-range').val());
        var text = $('.text-textarea').val();
        var $btn = $(this);
        var oldHtml = $btn.html();
        $btn.html('Extracting...');
        $('.topics-result-container').html('');
        $('.sources-list').html('');
        currentlyLoading = true;

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/api/extract',
            data: JSON.stringify({ lang: lang, text: text, corpus: corpus, confidence: confidence }),
            success: function (data) {
                console.log(data);
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
                            `<a class="mt-1 btn btn-light mr-1" href="${source}" target="_blank">Source ${count}</a>`)
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