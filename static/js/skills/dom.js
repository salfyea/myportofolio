// Builds table rows. Text always goes through textContent, so API values
// are never interpreted as HTML.

export function createElement(tagName, className, text) {
    const element = document.createElement(tagName);

    if (className) {
        element.className = className;
    }

    if (text !== undefined) {
        element.textContent = text;
    }

    return element;
}

// Show exactly one of the loading / error / empty / table containers.
export function displayPageSection(sectionIds, activeId) {
    sectionIds.forEach(function (id) {
        document.getElementById(id).classList.toggle('hide', id !== activeId);
    });
}

function buildStarControl(skill, { isAuthenticated, loginUrl }) {
    const label = (skill.is_starred ? '★ ' : '☆ ') + skill.star_count;
    const className = skill.is_starred ? 'star-button star-button--active' : 'star-button';

    if (!isAuthenticated) {
        const loginLink = createElement('a', 'star-button', label);
        loginLink.href = loginUrl;
        loginLink.setAttribute('aria-label', 'Login untuk memberi star ' + skill.name);
        return loginLink;
    }

    const button = createElement('button', className, label);
    button.type = 'button';
    button.dataset.action = 'star';
    button.dataset.id = skill.id;
    button.setAttribute('aria-pressed', String(skill.is_starred));
    button.setAttribute('aria-label', (skill.is_starred ? 'Batalkan star ' : 'Beri star ') + skill.name);

    if (skill.starred_by_names) {
        button.title = 'Diberi star oleh: ' + skill.starred_by_names;
    }

    return button;
}

function buildDeleteControls(skill) {
    const modalId = 'delete-skill-' + skill.id;
    const fragment = document.createDocumentFragment();

    const openButton = createElement('button', 'button button-danger', 'Hapus');
    openButton.type = 'button';
    openButton.setAttribute('popovertarget', modalId);
    fragment.appendChild(openButton);

    const modal = createElement('div', 'delete-modal');
    modal.id = modalId;
    modal.setAttribute('popover', 'auto');

    const backdrop = createElement('button', 'delete-modal__backdrop');
    backdrop.type = 'button';
    backdrop.setAttribute('popovertarget', modalId);
    backdrop.setAttribute('popovertargetaction', 'hide');
    backdrop.setAttribute('aria-label', 'Tutup');
    modal.appendChild(backdrop);

    const content = createElement('div', 'delete-modal__content');
    content.appendChild(createElement('h2', '', 'Hapus Skill?'));

    const question = createElement('p', '', 'Apakah kamu yakin ingin menghapus ');
    question.appendChild(createElement('strong', '', skill.name));
    question.appendChild(document.createTextNode('?'));
    content.appendChild(question);

    const actions = createElement('div', 'delete-modal__actions');

    const cancelButton = createElement('button', 'button button-secondary', 'Batal');
    cancelButton.type = 'button';
    cancelButton.setAttribute('popovertarget', modalId);
    cancelButton.setAttribute('popovertargetaction', 'hide');
    actions.appendChild(cancelButton);

    const confirmButton = createElement('button', 'button button-danger', 'Ya, Hapus');
    confirmButton.type = 'button';
    confirmButton.dataset.action = 'delete';
    confirmButton.dataset.id = skill.id;
    actions.appendChild(confirmButton);

    content.appendChild(actions);
    modal.appendChild(content);
    fragment.appendChild(modal);

    return fragment;
}

// permissions: { isAuthenticated, canEdit, canDelete, loginUrl }
export function buildSkillRow(skill, permissions) {
    const row = document.createElement('tr');
    row.id = 'skill-' + skill.id;
    row.dataset.skill = JSON.stringify(skill);

    row.appendChild(createElement('td', '', skill.name));
    row.appendChild(createElement('td', '', skill.category));

    const starCell = document.createElement('td');
    starCell.appendChild(buildStarControl(skill, permissions));
    row.appendChild(starCell);

    const actionsCell = createElement('td', 'skills-table__actions');

    if (permissions.canEdit) {
        const editButton = createElement('button', 'button button-secondary', 'Edit');
        editButton.type = 'button';
        editButton.dataset.action = 'edit';
        editButton.dataset.id = skill.id;
        actionsCell.appendChild(editButton);
    }

    if (permissions.canDelete) {
        actionsCell.appendChild(buildDeleteControls(skill));
    }

    row.appendChild(actionsCell);
    return row;
}
