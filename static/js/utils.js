function getCookie(name) {
    const prefix = name + '=';
    const match = document.cookie
        .split(';')
        .map(function (part) { return part.trim(); })
        .find(function (part) { return part.startsWith(prefix); });

    return match ? decodeURIComponent(match.slice(prefix.length)) : null;
}
