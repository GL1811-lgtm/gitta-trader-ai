import React from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const Grid = () => {
    const columnDefs = [
        { headerName: "Symbol", field: "symbol" },
        { headerName: "Signal", field: "signal" },
        { headerName: "Confidence", field: "confidence" },
        { headerName: "Reason", field: "reason" }
    ];

    const rowData = [
        { symbol: "NIFTY", signal: "BUY", confidence: 0.88, reason: "Simulated response for frontend testing." }
    ];

    return (
        <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
            <AgGridReact
                columnDefs={columnDefs}
                rowData={rowData}>
            </AgGridReact>
        </div>
    );
};

export default Grid;