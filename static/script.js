$(document).ready(function() {

    // Fetch location data and display it
    $.getJSON('/location', function(data) {
        if (data.length > 0) {
            var item = data[0];
            var locationInfo = `Latitude ${item.latitude}, Longitude ${item.longitude}`;
            $('#locationInfo').text(locationInfo);
        } else {
            $('#locationInfo').text('Location data unavailable.');
        }
    });

    // Fetch current swell data
    $.getJSON('/current_swell', function(data) {
        var currentSwellTableBody = $('#currentSwellTable tbody');
        currentSwellTableBody.empty();  // Clear previous data
        data.forEach(function(item) {
            currentSwellTableBody.append(
                `<tr>
                    <td>${new Date(item.time).toLocaleString()}</td>
                    <td>${item.swell_wave_height}</td>
                    <td>${item.swell_wave_direction}</td>
                    <td>${item.swell_wave_period}</td>
                </tr>`
            );
        });
    });

    // Fetch hourly swell data and render the charts
    $.getJSON('/hourly_swell', function(data) {
        var labels = [];
        var swellWaveHeights = [];
        var swellWaveDirections = [];
        var swellWavePeriods = [];

        data.forEach(function(item) {
            labels.push(new Date(item.time).toLocaleString());
            swellWaveHeights.push(item.swell_wave_height);
            swellWaveDirections.push(item.swell_wave_direction);
            swellWavePeriods.push(item.swell_wave_period);
        });

        // Create the chart for Wave Height
        var ctxHeight = document.getElementById('hourlyWaveHeightChart').getContext('2d');
        var hourlyWaveHeightChart = new Chart(ctxHeight, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Wave Height (m)',
                    data: swellWaveHeights,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Wave Height (m)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        // Create the chart for Wave Direction
        var ctxDirection = document.getElementById('hourlyWaveDirectionChart').getContext('2d');
        var hourlyWaveDirectionChart = new Chart(ctxDirection, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Wave Direction (°)',
                    data: swellWaveDirections,
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Wave Direction (°)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });

        // Create the chart for Wave Period
        var ctxPeriod = document.getElementById('hourlyWavePeriodChart').getContext('2d');
        var hourlyWavePeriodChart = new Chart(ctxPeriod, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Wave Period (s)',
                    data: swellWavePeriods,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Wave Period (s)'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    });
});