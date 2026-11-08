// Controller for /skills/manage/: wires the API client, the row builders and the page.
import { createSkillsApi } from './api.js';
import { buildSkillRow, createElement, displayPageSection } from './dom.js';

const SEARCH_DEBOUNCE_DELAY = 300;
const SECTION_IDS = ['loading', 'error', 'empty', 'skills-table'];

const config = document.getElementById('skills-app').dataset;
const permissions = {
    isAuthenticated: config.authenticated === 'true',
    canEdit: config.canEdit === 'true',
    canDelete: config.canDelete === 'true',
    loginUrl: config.loginUrl,
};

const api = createSkillsApi({
    listUrl: config.listUrl,
    detailUrlTemplate: config.detailUrl,
    starUrlTemplate: config.starUrl,
});

const searchForm = document.getElementById('skills-search-form');
const searchInput = document.getElementById('skills-search-input');
const categorySelect = document.getElementById('skills-category-select');
const sortSelect = document.getElementById('skills-sort-select');
const emptyMessage = document.getElementById('empty-message');
const skillsBody = document.getElementById('skills-body');
const skillForm = document.getElementById('skill-form');
const editForm = document.getElementById('edit-skill-form');

let searchDebounceTimer = null;
let currentController = null;
let editingSkillId = null;
// Skills whose star request is still in flight; a second click would race the first.
const pendingStars = new Set();

function showSection(sectionId) {
    displayPageSection(SECTION_IDS, sectionId);
}

function reportError(error) {
    // fetch() rejects with a TypeError when the server is unreachable.
    const message = error instanceof TypeError
        ? 'Tidak dapat terhubung ke server. Silakan coba lagi.'
        : error.message;

    showToast('Gagal', message, 'error');
}

function formPayload(form) {
    const payload = {};

    new FormData(form).forEach(function (value, key) {
        if (key !== 'csrfmiddlewaretoken') {
            payload[key] = value;
        }
    });

    return payload;
}

// Keep the category dropdown in sync with the categories the API has returned.
function syncCategoryOptions(skills) {
    const known = new Set(Array.from(categorySelect.options).map(option => option.value));

    skills.forEach(function (skill) {
        if (skill.category && !known.has(skill.category)) {
            known.add(skill.category);
            const option = createElement('option', '', skill.category);
            option.value = skill.category;
            categorySelect.appendChild(option);
        }
    });
}

async function loadSkills() {
    // Cancel the previous request so a slow, older response
    // cannot overwrite the results of a newer one.
    if (currentController) {
        currentController.abort();
    }

    const controller = new AbortController();
    currentController = controller;

    showSection('loading');

    const name = searchInput.value.trim();

    try {
        const skills = await api.list({
            name: name,
            category: categorySelect.value,
            ordering: sortSelect.value,
        }, controller.signal);

        if (skills.length === 0) {
            emptyMessage.textContent = name || categorySelect.value
                ? 'Tidak ada skill yang cocok dengan pencarian.'
                : 'Belum ada skill yang ditambahkan.';
            skillsBody.replaceChildren();
            showSection('empty');
            return;
        }

        syncCategoryOptions(skills);
        skillsBody.replaceChildren(...skills.map(skill => buildSkillRow(skill, permissions)));
        showSection('skills-table');
    } catch (error) {
        if (error.name === 'AbortError') {
            return;
        }

        showSection('error');
    } finally {
        if (currentController === controller) {
            currentController = null;
        }
    }
}

function replaceRow(skill) {
    const row = document.getElementById('skill-' + skill.id);

    // The table may have been reloaded (a new search) while a request was in flight.
    if (row) {
        row.replaceWith(buildSkillRow(skill, permissions));
    }
}

// What the row should look like once the server accepts the toggle.
function withToggledStar(skill) {
    const starred = !skill.is_starred;
    const names = skill.starred_by_names ? skill.starred_by_names.split(', ') : [];
    const nextNames = starred
        ? names.concat(config.username)
        : names.filter(name => name !== config.username);

    return {
        ...skill,
        is_starred: starred,
        star_count: skill.star_count + (starred ? 1 : -1),
        starred_by_names: nextNames.join(', '),
    };
}

// Optimistic update: the row changes instantly, then the server's answer replaces it,
// or the previous state is restored when the request fails.
async function toggleStar(button) {
    const id = button.dataset.id;

    if (pendingStars.has(id)) {
        return;
    }

    const previous = JSON.parse(button.closest('tr').dataset.skill);
    pendingStars.add(id);
    replaceRow(withToggledStar(previous));

    try {
        replaceRow(await api.toggleStar(id));
    } catch (error) {
        replaceRow(previous);
        reportError(error);
    } finally {
        pendingStars.delete(id);
    }
}

async function deleteSkill(button) {
    button.disabled = true;

    try {
        await api.remove(button.dataset.id);
        showToast('Berhasil', 'Skill berhasil dihapus!', 'success');
        loadSkills();
    } catch (error) {
        button.disabled = false;
        reportError(error);
    }
}

async function addSkill(event) {
    event.preventDefault();

    const submitButton = skillForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        await api.create(formPayload(skillForm));
        skillForm.reset();
        document.getElementById('add-skill-modal').hidePopover();
        showToast('Berhasil', 'Skill baru berhasil ditambahkan!', 'success');
        loadSkills();
    } catch (error) {
        reportError(error);
    } finally {
        submitButton.disabled = false;
    }
}

function openEditModal(skill) {
    editingSkillId = skill.id;
    editForm.elements.name.value = skill.name;
    editForm.elements.icon_url.value = skill.icon_url;
    editForm.elements.category.value = skill.category;
    document.getElementById('edit-skill-modal').showPopover();
}

async function saveSkill(event) {
    event.preventDefault();

    const submitButton = editForm.querySelector('button[type="submit"]');
    submitButton.disabled = true;

    try {
        // PATCH sends the edited fields; star data stays server-side.
        await api.update(editingSkillId, formPayload(editForm));
        document.getElementById('edit-skill-modal').hidePopover();
        showToast('Berhasil', 'Skill berhasil diperbarui!', 'success');
        loadSkills();
    } catch (error) {
        reportError(error);
    } finally {
        submitButton.disabled = false;
    }
}

// One listener on the table body keeps working after rows are re-rendered.
skillsBody.addEventListener('click', function (event) {
    const button = event.target.closest('button[data-action]');

    if (!button) {
        return;
    }

    if (button.dataset.action === 'star') {
        toggleStar(button);
    } else if (button.dataset.action === 'delete') {
        deleteSkill(button);
    } else if (button.dataset.action === 'edit') {
        openEditModal(JSON.parse(button.closest('tr').dataset.skill));
    }
});

if (skillForm) {
    skillForm.addEventListener('submit', addSkill);
}

if (editForm) {
    editForm.addEventListener('submit', saveSkill);
}

// Changing a dropdown applies immediately; there is nothing to debounce.
categorySelect.addEventListener('change', loadSkills);
sortSelect.addEventListener('change', loadSkills);

// Wait until the user stops typing before sending a request.
searchInput.addEventListener('input', function () {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(loadSkills, SEARCH_DEBOUNCE_DELAY);
});

searchForm.addEventListener('submit', function (event) {
    event.preventDefault();
    // Search right away and drop the pending debounced search.
    clearTimeout(searchDebounceTimer);
    loadSkills();
});

loadSkills();
