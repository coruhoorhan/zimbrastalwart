import React from "react";

interface ProgressBarProps {
    status: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ status }) => {
    let width = "0%";
    let color = "bg-gray-400";

    switch (status) {
        case "PENDING":
        case "NEW":
            width = "10%";
            color = "bg-gray-400";
            break;
        case "ACCOUNT_CREATED":
            width = "30%";
            color = "bg-blue-500";
            break;
        case "FULL_SYNC_RUNNING":
            width = "60%";
            color = "bg-yellow-500";
            break;
        case "FULL_SYNC_DONE":
        case "DONE":
            width = "100%";
            color = "bg-green-500";
            break;
        case "ERROR":
            width = "100%";
            color = "bg-red-500";
            break;
        default:
            width = "0%";
            color = "bg-gray-400";
    }

    return (
        <div className="w-full bg-gray-200 rounded h-4">
            <div className={`${color} h-4 rounded`} style={{ width }}></div>
        </div>
    );
};

export default ProgressBar;
