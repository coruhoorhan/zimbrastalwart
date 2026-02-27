import UserTable from "./components/UserTable";
import SettingsPanel from "./components/SettingsPanel";

function App() {
    return (
        <div className="container mx-auto p-4 md:p-8 max-w-6xl">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">Enterprise Mail Migration Panel</h1>
                <p className="text-gray-500 mt-2">Manage your Zimbra to Stalwart migration test dynamically.</p>
            </header>
            <SettingsPanel />
            <UserTable />
        </div>
    );
}

export default App;
