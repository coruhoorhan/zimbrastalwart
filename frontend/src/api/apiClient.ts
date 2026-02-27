const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const request = async (path: string, options?: RequestInit) => {
    const res = await fetch(`${API_BASE_URL}${path}`, options);
    if (!res.ok) {
        const body = await res.text();
        throw new Error(body || `HTTP ${res.status}`);
    }
    return res;
};

export const fetchUsers = async () => {
    const res = await request("/users/");
    return res.json();
};

export const startFullSync = async () => {
    await request("/sync/full", { method: "POST" });
};

export const startDeltaSync = async () => {
    await request("/sync/delta", { method: "POST" });
};

export const runMXCheck = async () => {
    await request("/cutover/mx_check", { method: "POST" });
};

export const startImport = async () => {
    const res = await request("/users/import", { method: "POST" });
    return res.json();
};

export const addUser = async (email: string, source_password: string) => {
    const res = await request("/users/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source_password })
    });
    return res.json();
};

export const getConfig = async () => {
    const res = await request("/config/");
    return res.json();
};

export const saveConfig = async (zimbra_host: string) => {
    const res = await request("/config/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zimbra_host }),
    });
    return res.json();
};

export const testSync = async (zimbra_host: string, email: string, source_password: string) => {
    const res = await request("/sync/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zimbra_host, email, source_password }),
    });
    return res.json();
};
