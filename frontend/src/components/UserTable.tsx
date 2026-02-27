import React, { useEffect, useState } from "react";
import { fetchUsers, startFullSync, startDeltaSync, startImport, addUser } from "../api/apiClient";
import ProgressBar from "./ProgressBar";

interface User {
    email: string;
    status: string;
    mails: number;
    size: string;
    error: string | null;
}

const UserTable: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [newEmail, setNewEmail] = useState("");
    const [newPass, setNewPass] = useState("");
    const [testResult, setTestResult] = useState<{ status: string, msg: string } | null>(null);

    const loadUsers = async () => {
        try {
            const data = await fetchUsers();
            setUsers(data);
        } catch (e) { console.error(e); }
    };

    useEffect(() => {
        loadUsers();
        const interval = setInterval(loadUsers, 5000); // 5s realtime update
        return () => clearInterval(interval);
    }, []);

    const handleImport = async () => {
        await startImport();
        loadUsers();
    };

    const handleFullSync = async () => {
        await startFullSync();
        loadUsers();
    };

    const handleDeltaSync = async () => {
        await startDeltaSync();
        loadUsers();
    };

    const handleAddUser = async () => {
        if (!newEmail) return;
        await addUser(newEmail, newPass);
        setNewEmail("");
        setNewPass("");
        loadUsers();
    };

    const handleTestUser = async () => {
        if (!newEmail || !newPass) {
            setTestResult({ status: "error", msg: "Email and password are required for a dry-run test." });
            return;
        }
        setTestResult({ status: "info", msg: "Testing connection... Please wait." });
        try {
            const hostRes = await fetch("http://localhost:8000/config/");
            const hostData = await hostRes.json();

            const res = await fetch("http://localhost:8000/sync/test", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ zimbra_host: hostData.zimbra_host, email: newEmail, source_password: newPass })
            });
            const data = await res.json();
            setTestResult({
                status: data.status === 'success' ? 'success' : 'error',
                msg: data.message
            });
        } catch (e) {
            setTestResult({ status: "error", msg: "Network error testing connection." });
        }
    };


    return (
        <div className="bg-white p-6 rounded-lg shadow border border-gray-100">

            <div className="mb-8 border-b pb-6">
                <h2 className="text-xl font-bold mb-4 text-gray-800">2. Test & Add Single User</h2>
                <div className="flex gap-3 flex-wrap items-end">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Source Email</label>
                        <input className="border border-gray-300 p-2 rounded w-64 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="user@belediye.bel.tr" value={newEmail} onChange={e => setNewEmail(e.target.value)} />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Source Password</label>
                        <input className="border border-gray-300 p-2 rounded w-52 focus:outline-none focus:ring-2 focus:ring-blue-500" type="password" placeholder="Zimbra Password" value={newPass} onChange={e => setNewPass(e.target.value)} />
                    </div>
                    <button onClick={handleTestUser} className="bg-purple-100 text-purple-700 hover:bg-purple-200 font-bold px-4 py-2 rounded shadow-sm focus:outline-none transition-colors border border-purple-200">
                        Dry-run Test
                    </button>
                    <button onClick={handleAddUser} className="bg-gray-800 text-white hover:bg-gray-900 font-medium px-4 py-2 rounded shadow focus:outline-none transition-colors">
                        Add to Migration List
                    </button>
                </div>
                {testResult && (
                    <div className={`mt-4 p-3 rounded text-sm whitespace-pre-wrap ${testResult.status === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : testResult.status === 'info' ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-red-50 text-red-700 border border-red-200'}`}>
                        {testResult.msg}
                    </div>
                )}
            </div>

            <div className="flex gap-2 mb-4 justify-between items-center">
                <h2 className="text-xl font-bold text-gray-800">3. Migration Queue</h2>
                <div className="flex gap-2">
                    <button onClick={handleImport} className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1.5 rounded text-sm transition-colors border border-gray-300">Mock LDAP Import</button>
                    <button onClick={handleFullSync} className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded text-sm shadow transition-colors">Start Full Sync</button>
                    <button onClick={handleDeltaSync} className="bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded text-sm shadow transition-colors">Start Delta Sync</button>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 border rounded-lg overflow-hidden">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">User Account</th>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Sync Status</th>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Mails Processed</th>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Storage</th>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider w-1/4">Progress</th>
                            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Logs</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {users.length === 0 ? (
                            <tr>
                                <td colSpan={6} className="px-4 py-8 text-center text-gray-500">No users in queue. Add directly above or use mock import.</td>
                            </tr>
                        ) : users.map(user => (
                            <tr key={user.email} className="hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium text-gray-900 truncate max-w-xs" title={user.email}>{user.email}</td>
                                <td className="px-4 py-3 text-sm text-gray-500">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-bold rounded-full ${user.status.includes('ERROR') ? 'bg-red-100 text-red-800' : user.status.includes('DONE') ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                        {user.status}
                                    </span>
                                </td>
                                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{user.mails}</td>
                                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{user.size}</td>
                                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500"><ProgressBar status={user.status} /></td>
                                <td className="px-4 py-3 text-sm text-red-500 max-w-xs truncate" title={user.error || ""}>{user.error || "-"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default UserTable;
