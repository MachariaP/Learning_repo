import './App.css';

function App(props) {
  return (
    <div className='todoapp stack-large'>
      <h1>TodoMatic</h1>
      <form>
        <h2 className='label-wrapper'>
          <label htmlFor='new-todo-input' className='label__lg'>
            What needs to be done?
          </label>
        </h2>
        <input
          type='text'
          id='new-todo-input'
          className='input input__lg'
          name='text'
          autocomplete='off'
        />
        <button type='submit' className='btn btn__primary btn__lg'>
          Add
        </button>
      </form>
    </div>
  );
}

export default App;
