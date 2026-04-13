const notesList = document.getElementById("notes-list");
const noteForm = document.getElementById("note-form");
const refreshButton = document.getElementById("refresh-button");
const statusMessage = document.getElementById("status-message");

function formatDate(value) {
    if (!value) {
        return "Brak daty";
    }

    const date = new Date(value);
    return date.toLocaleString("pl-PL");
}

function showStatus(message, isError = false) {
    statusMessage.textContent = message;
    statusMessage.classList.toggle("error-message", isError);
}

async function loadNotes() {
    notesList.innerHTML = "<p>Ładowanie notatek...</p>";

    try {
        const response = await fetch("/api/notes");

        if (!response.ok) {
            throw new Error("Nie udało się pobrać notatek.");
        }

        const notes = await response.json();

        if (notes.length === 0) {
            notesList.innerHTML = "<p>Brak notatek.</p>";
            return;
        }

        notesList.innerHTML = "";

        for (const note of notes) {
            const noteElement = document.createElement("article");
            noteElement.className = "note-item";

            noteElement.innerHTML = `
                <h3>${escapeHtml(note.title)}</h3>
                <div class="note-meta">
                    Utworzono: ${formatDate(note.created_at)}
                </div>
                <div class="note-content">${escapeHtml(note.content)}</div>
                <div class="note-actions">
                    <button class="delete-button" data-id="${note.id}">Usuń</button>
                </div>
            `;

            notesList.appendChild(noteElement);
        }

        const deleteButtons = document.querySelectorAll(".delete-button");
        deleteButtons.forEach((button) => {
            button.addEventListener("click", async () => {
                const noteId = button.dataset.id;
                await deleteNote(noteId);
            });
        });
    } catch (error) {
        notesList.innerHTML = "<p>Nie udało się załadować notatek.</p>";
        showStatus(error.message, true);
    }
}

async function createNote(event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!title || !content) {
        showStatus("Tytuł i treść są wymagane.", true);
        return;
    }

    try {
        const response = await fetch("/api/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title, content })
        });

        if (!response.ok) {
            throw new Error("Nie udało się dodać notatki.");
        }

        noteForm.reset();
        showStatus("Notatka została dodana.");
        await loadNotes();
    } catch (error) {
        showStatus(error.message, true);
    }
}

async function deleteNote(noteId) {
    try {
        const response = await fetch(`/api/notes/${noteId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Nie udało się usunąć notatki.");
        }

        showStatus("Notatka została usunięta.");
        await loadNotes();
    } catch (error) {
        showStatus(error.message, true);
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

noteForm.addEventListener("submit", createNote);
refreshButton.addEventListener("click", loadNotes);

loadNotes();