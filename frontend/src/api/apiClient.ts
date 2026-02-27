export const fetchUsers = async () => {
    const res = await fetch("http://localhost:8000/users/");
    return res.json();
};

export const startFullSync = async () => {
    await fetch("http://localhost:8000/sync/full", { method: "POST" });
};

export const startDeltaSync = async () => {
    await fetch("http://localhost:8000/sync/delta", { method: "POST" });
};

export const runMXCheck = async () => {
    await fetch("http://localhost:8000/cutover/mx_check", { method: "POST" });
};

export const startImport = async () => {
    const res = await fetch("http://localhost:8000/users/import", { method: "POST" });
    return res.json();
};

export const addUser = async (email: string, source_password: string) => {
    const res = await fetch("http://localhost:8000/users/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, source_password })
    });
    return res.json();
};
