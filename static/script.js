document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('visualizeBtn').addEventListener('click', function() {
        var file = document.getElementById('fileInput').files[0];
        var visualizationType = document.getElementById('visualizationType').value;
        if (file) {
            var formData = new FormData();
            formData.append('file', file);
            formData.append('visualizationType', visualizationType);
            document.getElementById('loadingIndicator').style.display = 'block';

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loadingIndicator').style.display = 'none';
                if (data.success) {
                    var plot = data.plot;
                    var chartContainer = document.getElementById('chartContainer');
                    chartContainer.innerHTML = `<img src="data:image/png;base64,${plot}" alt="Plot">`;
                } else {
                    document.getElementById('errorMessage').innerText = 'Error: ' + data.error;
                    document.getElementById('errorMessage').style.display = 'block';
                }
            })
            .catch(error => {
                document.getElementById('loadingIndicator').style.display = 'none';
                document.getElementById('errorMessage').innerText = 'Error: ' + error;
                document.getElementById('errorMessage').style.display = 'block';
            });
        } else {
            alert('Please upload a file.');
        }
    });

    // Show file input on label click
    var uploadBtn = document.querySelector('.upload-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function() {
            document.getElementById('fileInput').click();
        });
    } else {
        console.error('Upload button not found.');
    }
});
