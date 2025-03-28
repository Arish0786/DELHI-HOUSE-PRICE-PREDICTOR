$(document).ready(function () {
    loadLocations();

    $("#searchLocation").on("input", function () {
        filterLocations($(this).val());
    });

    $("#uiLocations").on("change", function () {
        $("#searchLocation").val($(this).val());
    });
});

function loadLocations() {
    $.get("http://127.0.0.1:5000/get_location_names", function (data) {
        const locations = data.locations;
        $("#uiLocations").empty();
        locations.forEach(loc => $("#uiLocations").append(new Option(loc)));
    });
}

function filterLocations(search) {
    $("#uiLocations option").each(function () {
        $(this).toggle($(this).text().toLowerCase().includes(search.toLowerCase()));
    });
}

function onClickedEstimatePrice() {
    const sqft = $("#uiSqft").val();
    const bhk = $(".bhk-btn.active").text();
    const bath = $(".bath-btn.active").text();
    const location = $("#searchLocation").val();
    const estPrice = $("#uiEstimatedPrice");

    if (!sqft || !bhk || !bath || !location) {
        alert("Please fill all fields correctly.");
        return;
    }

    $.post("http://127.0.0.1:5000/predict_home_price", {
        total_sqft: parseFloat(sqft),
        bhk: bhk,
        bath: bath,
        location: location
    }, function (data) {
        estPrice.html(`<h2>${data.estimated_price} Rupees</h2>`);
    });
}

function selectBHK(value) {
    $(".bhk-btn").removeClass("active");
    $(`.bhk-btn:nth-child(${value})`).addClass("active");
}

function selectBath(value) {
    $(".bath-btn").removeClass("active");
    $(`.bath-btn:nth-child(${value})`).addClass("active");
}
