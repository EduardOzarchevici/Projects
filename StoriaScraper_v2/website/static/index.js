async function saveFavorite(announcementId) {
    try {
        const response = await fetch('/save-favorite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: announcementId })
        });

        const data = await response.json();
        if (response.ok) {
            //alert('Anunț salvat ca favorit!');
        } else {
            alert('Eroare: ' + data.error);
        }
    } catch (error) {
        console.error('Eroare la salvarea favoritului:', error);
        //alert('A apărut o problemă!');
    }
}

function deleteFavorite(favId) {
    fetch('/delete-favorite', {
        method: 'POST',
        body: JSON.stringify({ favId: favId })
    }).then((_res) => {
        window.location.href = "/favorites";
    })
}
