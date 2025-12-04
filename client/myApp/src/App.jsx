// import './App.css';
import { AskAiComp } from './AskAiComp.jsx';
// import baseImg from 'C:/Users/nnoam/Desktop/FullStackStudy/BookingAgency/client/myApp/src/assets/shore.png';
import baseImg from 'C:/Users/nnoam/Desktop/FullStackStudy/BookingAgency/client/myApp/src/assets/pexels-asadphoto-2549017.jpg';


function App() {
  const myStyle = {
    backgroundImage: `url(${baseImg})`,
    // Or, if using a URL directly:
    // backgroundImage: 'url("https://example.com/your-image.jpg")',
    backgroundSize: 'cover', // Adjust as needed (e.g., 'contain', 'auto')
    backgroundRepeat: 'no-repeat', // Adjust as needed
    backgroundPosition: 'center', // Adjust as needed
    height: '100vh', // Example: Make the div fill the viewport height
    width: '100wv'
  };

  return (
    <div style={myStyle}>
      <AskAiComp />
    </div>
  )
}

export default App
