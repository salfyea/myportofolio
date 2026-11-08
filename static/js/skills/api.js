// Thin client for /api/v1/skills/. It knows URLs and error shapes, not the DOM.

const ID_PLACEHOLDER = '00000000-0000-0000-0000-000000000000';

// DRF answers 400 with {field: [messages]} and 403 with {detail: message}.
export function apiErrorMessage(data, status) {
    const messages = Object.values(data)
        .flat()
        .filter(value => typeof value === 'string');

    return messages.join(' ') || 'Terjadi kesalahan (status ' + status + ').';
}

export function createSkillsApi({ listUrl, detailUrlTemplate, starUrlTemplate }) {
    const urlFor = (template, id) => template.replace(ID_PLACEHOLDER, id);

    // Single entry point for every request that changes data.
    async function write(url, method, payload) {
        const response = await fetch(url, {
            method: method,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                // getCookie comes from utils.js, loaded before this deferred module.
                'X-CSRFToken': window.getCookie('csrftoken'),
            },
            body: payload === undefined ? undefined : JSON.stringify(payload),
        });

        // 204 has no body, so calling .json() would throw.
        if (response.status === 204) {
            return null;
        }

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(apiErrorMessage(data, response.status));
        }

        return data;
    }

    return {
        async list(params, signal) {
            const url = new URL(listUrl, window.location.origin);

            Object.entries(params).forEach(function ([key, value]) {
                if (value) {
                    url.searchParams.set(key, value);
                }
            });

            const response = await fetch(url, {
                headers: { Accept: 'application/json' },
                signal: signal,
            });

            if (!response.ok) {
                throw new Error('Request failed with status ' + response.status);
            }

            return response.json();
        },
        create: payload => write(listUrl, 'POST', payload),
        update: (id, payload) => write(urlFor(detailUrlTemplate, id), 'PATCH', payload),
        remove: id => write(urlFor(detailUrlTemplate, id), 'DELETE'),
        toggleStar: id => write(urlFor(starUrlTemplate, id), 'POST'),
    };
}
