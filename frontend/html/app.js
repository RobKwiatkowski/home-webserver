const notesList = document.getElementById("notes-list");
const noteForm = document.getElementById("note-form");
const refreshButton = document.getElementById("refresh-button");
const statusMessage = document.getElementById("status-message");
const submitButton = document.getElementById("submit-button");
const cancelEditButton = document.getElementById("cancel-edit-button");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");

let editingNoteId = null;

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

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function resetFormState() {
    editingNoteId = null;
    noteForm.reset();
    submitButton.textContent = "Dodaj notatkę";
    cancelEditButton.hidden = true;
}

function startEdit(note) {
    editingNoteId = note.id;
    titleInput.value = note.title;
    contentInput.value = note.content;
    submitButton.textContent = "Zapisz zmiany";
    cancelEditButton.hidden = false;
    showStatus(`Edytujesz notatkę: ${note.title}`);
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
                    Utworzono: ${formatDate(note.created_at)}<br>
                    Zaktualizowano: ${formatDate(note.updated_at)}
                </div>
                <div class="note-content">${escapeHtml(note.content)}</div>
                <div class="note-actions">
                    <button class="edit-button" data-id="${note.id}">Edytuj</button>
                    <button class="delete-button" data-id="${note.id}">Usuń</button>
                </div>
            `;

            notesList.appendChild(noteElement);

            const editButton = noteElement.querySelector(".edit-button");
            editButton.addEventListener("click", () => startEdit(note));

            const deleteButton = noteElement.querySelector(".delete-button");
            deleteButton.addEventListener("click", async () => {
                await deleteNote(note.id);
            });
        }
    } catch (error) {
        notesList.innerHTML = "<p>Nie udało się załadować notatek.</p>";
        showStatus(error.message, true);
    }
}

async function createOrUpdateNote(event) {
    event.preventDefault();

    const title = titleInput.value.trim();
    const content = contentInput.value.trim();

    if (!title || !content) {
        showStatus("Tytuł i treść są wymagane.", true);
        return;
    }

    const isEditing = editingNoteId !== null;
    const url = isEditing ? `/api/notes/${editingNoteId}` : "/api/notes";
    const method = isEditing ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title, content })
        });

        if (!response.ok) {
            throw new Error(
                isEditing
                    ? "Nie udało się zaktualizować notatki."
                    : "Nie udało się dodać notatki."
            );
        }

        showStatus(
            isEditing
                ? "Notatka została zaktualizowana."
                : "Notatka została dodana."
        );

        resetFormState();
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

        if (editingNoteId === noteId) {
            resetFormState();
        }

        showStatus("Notatka została usunięta.");
        await loadNotes();
    } catch (error) {
        showStatus(error.message, true);
    }
}

noteForm.addEventListener("submit", createOrUpdateNote);
refreshButton.addEventListener("click", loadNotes);
cancelEditButton.addEventListener("click", () => {
    resetFormState();
    showStatus("Edycja anulowana.");
});

loadNotes();