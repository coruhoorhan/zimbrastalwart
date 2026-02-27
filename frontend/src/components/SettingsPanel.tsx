import React, { useEffect, useState } from "react";

export default function SettingsPanel() {
    const [host, setHost] = useState("");
    const [status, setStatus] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/config/")
            .then(r => r.json())
            .then(d => setHost(d.zimbra_host))
            .catch(() => { });
    }, []);

    const handleSave = async () => {
        setStatus("Saving...");
        try {
            await fetch("http://localhost:8000/config/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ zimbra_host: host })
            });
            setStatus("Config Saved!");
            setTimeout(() => setStatus(""), 2000);
        } catch {
            setStatus("Error saving");
        }
    }

    return (
        <div className="bg-white p-6 rounded-lg shadow mb-6 border border-gray-100">
            <h2 className="text-xl font-bold mb-4 text-gray-800">1. Migration Settings</h2>
            <div className="flex gap-4 items-center flex-wrap">
                <label className="font-semibold text-gray-700">Zimbra Server IP / Host:</label>
                <input
                    className="border border-gray-300 p-2 rounded w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g. mail.domain.com"
                    value={host}
                    onChange={e => setHost(e.target.value)}
                />
                <button onClick={handleSave} className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded shadow focus:outline-none transition-colors">
                    Save Config
                </button>
                {status && <span className="text-sm font-medium text-green-600">{status}</span>}
            </div>
        </div>
    )
}
