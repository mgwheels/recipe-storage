import { APITester } from "./components/APITester";
import "./styles/index.css";

import logo from "./assets/logo.svg";
import reactLogo from "./assets/react.svg";

export function App() {
  return (
    <div className="app">
      <h1>Recipe Storage</h1>
      <p>
        A UI interface for recipe-storage Python API, built with <code>bun</code>!
      </p>
      <APITester />
    </div>
  );
}

export default App;
