import { useState } from 'react';
import './App.css';

function App(props) {
  const [count, setCount] = useState(0);

  return (
    <>
      <header>
        <h1>Hello, {props.subject}!</h1>
        <button type="button" className="primary" onClick={() => setCount(count + 1)}>
          Clicked {count} times
        </button>
      </header>
    </>
  );
}

export default App;