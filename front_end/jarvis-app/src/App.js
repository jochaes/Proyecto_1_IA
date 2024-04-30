import './App.css';
import VoiceChat from './components/VoiceChat';
import FaceRecognition from './components/FaceRecognition';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Our App</h1>
      </header>

      <div className='Components'>
        <FaceRecognition />
        <VoiceChat />
        
      </div>
      
      
    </div>
  );
}

export default App;
