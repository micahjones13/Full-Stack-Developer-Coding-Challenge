import React, { useState, useEffect } from "react";
import { AgGridColumn, AgGridReact } from "ag-grid-react";
import "ag-grid-enterprise";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine-dark.css";
import axios from "axios";
const Alerts = (props) => {
  const [gridApi, setGridApi] = useState(null);
  const [gridColumnApi, setGridColumnApi] = useState(null);
  // const [alerts, setAlerts] = useState(null);
  console.log(props, "PROPS");
  let alert_columns = ["errorMessage", "errorCategory", "errorTime"];
  // let alert_columns = [];
  // props.alerts.map(el => {

  // })
  return (
    <div
      className="ag-theme-alpine-dark"
      style={{ height: "50vh", width: "100%" }}
    >
      <AgGridReact rowData={props.alerts}>
        {alert_columns.map((el) => {
          return <AgGridColumn field={el} key={el} sortable={true} />;
        })}
      </AgGridReact>
    </div>
  );
};

export default Alerts;