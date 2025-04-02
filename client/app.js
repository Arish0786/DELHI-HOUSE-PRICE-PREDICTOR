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
    $.get("/api/get_location_names", function (data) {
        console.log("Received data:", data); // Debugging step
        if (!data || !data.locations) {
            console.error("Invalid response from server:", data);
            return;
        }
        const locations = data.locations;
        $("#uiLocations").empty();
        locations.forEach(loc => $("#uiLocations").append(new Option(loc)));
    }).fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Error loading locations:", textStatus, errorThrown);
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

     const dataToSend = {
        area: parseFloat(sqft),  // Ensure it's a number
        bhk: parseInt(bhk),      // Ensure it's a number
        bath: parseInt(bath),    // Ensure it's a number
        location: location.trim() // Ensure no extra spaces
    };

    console.log("Sending data:", dataToSend);

    $.ajax({
        url: "/api/predict_home_price", // Removed `/api/`
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            area: parseFloat(sqft),
            bhk: bhk,
            bath: bath,
            location: location
        }),
        success: function (data) {
            estPrice.html(`<h2>${data.estimated_price} Rupees</h2>`);
        },
        error: function (err) {
            console.error("Error:", err);
            alert("Something went wrong. Try again.");
        }
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
