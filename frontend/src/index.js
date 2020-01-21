import ReactDom from "react-dom";
import React from 'react';
import App from "./components/App";

const wrapper = document.getElementById('app');

wrapper ? ReactDom.render(<App />, wrapper) : null;
