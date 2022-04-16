const deleteNote = noteId => {
    if (confirm('Are you sure to delete that note?')) {
        fetch('/delete-note', {
            method: 'POST',
            body: JSON.stringify({noteID: noteId})
        }).then((_res) => {
            window.location.href = '/';
        });
    }
}